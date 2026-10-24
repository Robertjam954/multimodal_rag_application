#!/usr/bin/env Rscript
# Compare TCGA-GBM and TCGA-LGG non-silent mutations and pathway alterations.
#
# This workflow uses TCGAbiolinks to retrieve GDC masked somatic-MAF calls and clinical
# case metadata. It retains one TCGA primary-solid-tumor sample (sample type 01)
# per patient, then runs two-sided Fisher exact tests at the patient level.
#
# Usage:
# Rscript "data collection and processing/compare_tcga_lgg_gbm.R" \
#   --out-dir data/processed/tcga_lgg_vs_gbm
#
# Outputs:
#   selected_primary_samples.csv       selected patient/sample universe
#   clinical_cases.csv                 GDC clinical cases used for provenance
#   mutation_enrichment_gbm_vs_lgg.csv gene-level results, BH corrected
#   pathway_enrichment_gbm_vs_lgg.csv  Sanchez-Vega pathway results, BH corrected

suppressPackageStartupMessages({
  library(TCGAbiolinks)
  library(dplyr)
  library(jsonlite)
  library(readr)
})

parse_args <- function(args) {
  out_dir <- NULL
  min_prevalence <- 5L
  gdc_cache_dir <- NULL
  i <- 1L
  while (i <= length(args)) {
    if (args[i] == "--out-dir") {
      i <- i + 1L
      if (i > length(args)) stop("--out-dir requires a directory")
      out_dir <- args[i]
    } else if (args[i] == "--min-prevalence") {
      i <- i + 1L
      if (i > length(args)) stop("--min-prevalence requires an integer")
      min_prevalence <- suppressWarnings(as.integer(args[i]))
    } else if (args[i] == "--gdc-cache-dir") {
      i <- i + 1L
      if (i > length(args)) stop("--gdc-cache-dir requires a directory")
      gdc_cache_dir <- args[i]
    } else {
      stop("Unknown argument: ", args[i])
    }
    i <- i + 1L
  }
  if (is.null(out_dir)) stop("--out-dir is required")
  if (is.na(min_prevalence) || min_prevalence < 1L)
    stop("--min-prevalence must be an integer of at least 1")
  if (is.null(gdc_cache_dir))
    gdc_cache_dir <- file.path(out_dir, "GDCdata")
  list(out_dir = out_dir, min_prevalence = min_prevalence, gdc_cache_dir = gdc_cache_dir)
}

# Sanchez-Vega et al. oncogenic-signaling pathway genes. This matches the
# repository's existing gnomeR-compatible pathway definitions, but this analysis
# intentionally scores only non-silent SNV/indel mutations, not CNA or fusions.
pathways <- list(
  RTK_RAS = c("ABL1","ALK","BRAF","CBL","ERBB2","ERBB3","ERBB4","EGFR","FGFR1","FGFR2",
              "FGFR3","FGFR4","FLT3","HRAS","KIT","KRAS","MAP2K1","MAP2K2","MAPK1","MET",
              "NF1","NRAS","NTRK1","NTRK2","NTRK3","PDGFRA","PDGFRB","PTPN11","RAF1","RET",
              "ROS1","SOS1"),
  Nrf2 = c("CUL3","KEAP1","NFE2L2"),
  PI3K = c("AKT1","AKT2","AKT3","INPP4B","MTOR","PIK3CA","PIK3CB","PIK3R1","PIK3R2",
           "PPP2R1A","PTEN","RICTOR","RPTOR","STK11","TSC1","TSC2"),
  TGFB = c("ACVR1B","ACVR2A","SMAD2","SMAD3","SMAD4","TGFBR1","TGFBR2"),
  p53 = c("ATM","CHEK2","MDM2","MDM4","RPS6KA3","TP53","TP53BP1"),
  Wnt = c("AMER1","APC","ARID1A","ARID2","AXIN1","AXIN2","CTNNB1","DKK1","DKK2","DKK3",
          "DKK4","RNF43","SOX17","TCF7L1","TCF7L2","TLE1","TLE2","TLE3","TLE4","ZNRF3"),
  Myc = c("MAX","MGA","MLX","MLXIP","MLXIPL","MNT","MXD1","MXD3","MXD4","MXI1","MYC","MYCL","MYCN"),
  Cell_cycle = c("CCND1","CCND2","CCND3","CCNE1","CDK4","CDK6","CDKN1A","CDKN1B","CDKN2A",
                 "CDKN2B","CDKN2C","E2F1","E2F3","RB1"),
  Hippo = c("CRB1","CRB2","CRB3","DCHS1","DCHS2","FAT1","FAT2","FAT3","FAT4","HMCN1",
            "LATS1","LATS2","LLGL1","LLGL2","MOB1A","MOB1B","NF2","PARD3","PARD6A","PARD6B",
            "PARD6G","SAV1","SCRIB","STK3","STK4","TAOK1","TAOK2","TAOK3","TEAD4","TJP1",
            "TJP2","TJP3","WWC1","YAP1"),
  Notch = c("APH1A","ARRDC1","CIR1","CNTN6","CREBBP","CTBP1","CTBP2","DLL1","DLL3","DLL4",
            "DTX1","DTX2","DTX3","DTX3L","DTX4","EP300","FBXW7","FHL1","HDAC2","HES1",
            "HES2","HES3","HES4","HES5","HEYL","JAG1","JAG2","KAT2B","KDM5A","LFNG","MAML1",
            "MAML2","MAML3","MFNG","NCOR1","NCOR2","NOTCH1","NOTCH2","NOTCH3","NOTCH4","NRARP",
            "NUMB","NUMBL","PSEN1","PSEN2","PSENEN","RBPJ","RBX1","RFNG","SAP30","SNW1","SPEN",
            "TLE1","TLE2","TLE3","TLE4")
)

non_silent <- c(
  "Frame_Shift_Del", "Frame_Shift_Ins", "In_Frame_Del", "In_Frame_Ins",
  "Missense_Mutation", "Nonsense_Mutation", "Nonstop_Mutation", "Splice_Region",
  "Splice_Site", "Translation_Start_Site"
)

load_cohort <- function(cohort, gdc_cache_dir) {
  project <- paste0("TCGA-", cohort)
  message("Downloading ", project, " clinical cases via TCGAbiolinks...")
  clinical <- GDCquery_clinic(project = project, type = "clinical")

  message("Downloading ", project, " masked somatic MAF via TCGAbiolinks...")
  query <- GDCquery(
    project = project,
    data.category = "Simple Nucleotide Variation",
    data.type = "Masked Somatic Mutation",
    workflow.type = "Aliquot Ensemble Somatic Variant Merging and Masking",
    data.format = "MAF"
  )
  GDCdownload(query, directory = gdc_cache_dir, files.per.chunk = 20)
  maf <- GDCprepare(query, directory = gdc_cache_dir, summarizedExperiment = FALSE)
  required <- c("Tumor_Sample_Barcode", "Hugo_Symbol", "Variant_Classification")
  absent <- setdiff(required, names(maf))
  if (length(absent) > 0)
    stop(project, " MAF is missing required columns: ", paste(absent, collapse = ", "))

  # Every queried MAF file advertises its submitted tumor and matched-normal sample
  # barcodes in `cases`. This defines the eligible sequenced universe, including
  # primary tumors whose MAF contains no non-silent mutation rows.
  case_barcodes <- trimws(unlist(strsplit(
    as.character(unlist(query$results[[1]]$cases, use.names = FALSE)), ",", fixed = TRUE
  )))
  invalid_barcodes <- case_barcodes[
    !grepl("^TCGA-[A-Z0-9]{2}-[A-Z0-9]{4}-[0-9]{2}[A-Z]", case_barcodes)
  ]
  if (length(invalid_barcodes) > 0)
    stop(project, " query returned invalid submitted sample barcodes: ",
         paste(unique(invalid_barcodes), collapse = ", "))
  selected <- tibble(Tumor_Sample_Barcode = case_barcodes) |>
    filter(substr(Tumor_Sample_Barcode, 14, 15) == "01") |>
    mutate(patient_id = substr(Tumor_Sample_Barcode, 1, 12)) |>
    arrange(Tumor_Sample_Barcode) |>
    group_by(patient_id) |>
    summarise(sample_id = first(Tumor_Sample_Barcode), .groups = "drop")
  if (nrow(selected) == 0)
    stop(project, " MAF query contains no primary-solid-tumor samples (TCGA code 01).")

  maf <- maf |>
    mutate(
      patient_id = substr(Tumor_Sample_Barcode, 1, 12),
      sample_type_code = substr(Tumor_Sample_Barcode, 14, 15)
    ) |>
    filter(sample_type_code == "01") |>
    arrange(Tumor_Sample_Barcode)
  selected_maf <- maf |>
    inner_join(selected, by = c("patient_id", "Tumor_Sample_Barcode" = "sample_id")) |>
    filter(Variant_Classification %in% non_silent, !is.na(Hugo_Symbol), Hugo_Symbol != "")
  genes <- selected_maf |>
    distinct(patient_id, Hugo_Symbol) |>
    rename(gene = Hugo_Symbol)
  list(clinical = clinical, selected = selected, genes = genes, query = query)
}

write_provenance <- function(lgg, gbm, args, clinical_path) {
  manifest <- bind_rows(
    mutate(lgg$query$results[[1]], cohort = "LGG", project = "TCGA-LGG"),
    mutate(gbm$query$results[[1]], cohort = "GBM", project = "TCGA-GBM")
  )
  # `cases` is nested in the TCGAbiolinks query result and cannot be represented
  # in a CSV. Keep all scalar GDC manifest fields, including UUID and MD5 checksum.
  scalar_columns <- names(manifest)[!vapply(manifest, is.list, logical(1))]
  write_csv(select(manifest, all_of(scalar_columns)),
            file.path(args$out_dir, "gdc_mutation_file_manifest.csv"))

  script_arg <- grep("^--file=", commandArgs(trailingOnly = FALSE), value = TRUE)
  script_path <- sub("^--file=", "", script_arg[1])
  script_md5 <- if (file.exists(script_path)) unname(tools::md5sum(script_path)) else NA_character_
  provenance <- c(
    paste("retrieved_at_utc:", format(Sys.time(), tz = "UTC", usetz = TRUE)),
    "workflow: TCGAbiolinks::GDCquery + GDCdownload + GDCprepare",
    "data_category: Simple Nucleotide Variation",
    "data_type: Masked Somatic Mutation",
    "workflow_type: Aliquot Ensemble Somatic Variant Merging and Masking",
    "data_format: MAF",
    "sample_selection: one lexicographically first TCGA sample type 01 per patient",
    paste("min_prevalence:", args$min_prevalence),
    paste("gdc_cache_dir:", normalizePath(args$gdc_cache_dir)),
    paste("script_path:", script_path),
    paste("script_md5:", script_md5),
    paste("clinical_cases_md5:", unname(tools::md5sum(clinical_path))),
    paste("command:", paste(commandArgs(trailingOnly = FALSE), collapse = " "))
  )
  writeLines(provenance, file.path(args$out_dir, "run_provenance.txt"))
  writeLines(capture.output(sessionInfo()), file.path(args$out_dir, "session_info.txt"))
}

flatten_list_columns <- function(data) {
  list_columns <- names(data)[vapply(data, is.list, logical(1))]
  for (column in list_columns) {
    data[[column]] <- vapply(
      data[[column]],
      function(value) jsonlite::toJSON(value, auto_unbox = TRUE, null = "null"),
      character(1)
    )
  }
  data
}

test_features <- function(features, feature_col, lgg_patients, gbm_patients, min_prevalence,
                          feature_universe = NULL) {
  feature_sym <- rlang::sym(feature_col)
  counts <- features |>
    filter(!is.na(patient_id)) |>
    distinct(patient_id, !!feature_sym) |>
    mutate(cohort = if_else(patient_id %in% gbm_patients, "GBM", "LGG")) |>
    count(cohort, !!feature_sym, name = "mutated") |>
    tidyr::pivot_wider(names_from = cohort, values_from = mutated, values_fill = 0)
  if (!is.null(feature_universe)) {
    counts <- tibble(feature = feature_universe) |>
      left_join(counts, by = setNames(feature_col, "feature"))
  }
  counts |>
    mutate(
      GBM = if_else(is.na(GBM), 0L, GBM),
      LGG = if_else(is.na(LGG), 0L, LGG)
    ) |>
    filter(GBM + LGG >= min_prevalence) |>
    rowwise() |>
    mutate(
      n_gbm = length(gbm_patients),
      n_lgg = length(lgg_patients),
      gbm_prevalence = GBM / n_gbm,
      lgg_prevalence = LGG / n_lgg,
      fisher_p = fisher.test(matrix(c(GBM, n_gbm - GBM, LGG, n_lgg - LGG), nrow = 2))$p.value,
      odds_ratio_gbm_vs_lgg = ((GBM + 0.5) * (n_lgg - LGG + 0.5)) /
        ((n_gbm - GBM + 0.5) * (LGG + 0.5))
    ) |>
    ungroup() |>
    mutate(
      q_bh = p.adjust(fisher_p, method = "BH"),
      enriched_in = case_when(
        GBM + LGG == 0 ~ "Neither",
        odds_ratio_gbm_vs_lgg > 1 ~ "GBM",
        TRUE ~ "LGG"
      )
    ) |>
    arrange(q_bh, fisher_p, !!feature_sym)
}

args <- parse_args(commandArgs(trailingOnly = TRUE))
dir.create(args$out_dir, recursive = TRUE, showWarnings = FALSE)

lgg <- load_cohort("LGG", args$gdc_cache_dir)
gbm <- load_cohort("GBM", args$gdc_cache_dir)
lgg_patients <- lgg$selected$patient_id
gbm_patients <- gbm$selected$patient_id

write_csv(bind_rows(
  mutate(lgg$selected, cohort = "LGG", study_id = "TCGA-LGG"),
  mutate(gbm$selected, cohort = "GBM", study_id = "TCGA-GBM")
), file.path(args$out_dir, "selected_primary_samples.csv"))
write_csv(bind_rows(
  mutate(lgg$clinical, cohort = "LGG"),
  mutate(gbm$clinical, cohort = "GBM")
  ) |>
  flatten_list_columns(),
  file.path(args$out_dir, "clinical_cases.csv")
)
write_provenance(lgg, gbm, args, file.path(args$out_dir, "clinical_cases.csv"))

all_genes <- bind_rows(
  mutate(lgg$genes, cohort = "LGG"),
  mutate(gbm$genes, cohort = "GBM")
)
gene_results <- test_features(
  select(all_genes, patient_id, feature = gene),
  "feature", lgg_patients, gbm_patients, args$min_prevalence
) |>
  rename(gbm_mutated = GBM, lgg_mutated = LGG)

pathway_results <- bind_rows(lapply(names(pathways), function(pathway) {
  all_genes |>
    filter(gene %in% pathways[[pathway]]) |>
    transmute(patient_id, feature = pathway)
})) |>
  test_features("feature", lgg_patients, gbm_patients, 1L, names(pathways)) |>
  rename(gbm_mutated = GBM, lgg_mutated = LGG)

write_csv(gene_results, file.path(args$out_dir, "mutation_enrichment_gbm_vs_lgg.csv"))
write_csv(pathway_results, file.path(args$out_dir, "pathway_enrichment_gbm_vs_lgg.csv"))

message("Wrote ", nrow(gene_results), " gene tests and ", nrow(pathway_results),
        " pathway tests to ", normalizePath(args$out_dir))

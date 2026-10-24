suppressMessages({
  library(cbioportalR)
  library(dplyr)
  library(tidyr)
  library(readr)
})

set_cbioportal_db("public")

study_id <- "brca_tcga_pan_can_atlas_2018"
out_dir  <- "/Users/robertjames"

clin <- get_clinical_by_study(study_id = study_id)
cat("Rows pulled (long):", nrow(clin), "\n")
cat("Columns:", paste(names(clin), collapse = ", "), "\n\n")

pat_long  <- clin |> filter(dataLevel == "PATIENT")
samp_long <- clin |> filter(dataLevel == "SAMPLE")

pat_wide <- pat_long |>
  select(patientId, clinicalAttributeId, value) |>
  pivot_wider(names_from = clinicalAttributeId, values_from = value)

samp_wide <- samp_long |>
  select(patientId, sampleId, clinicalAttributeId, value) |>
  pivot_wider(names_from = clinicalAttributeId, values_from = value)

merged <- samp_wide |> left_join(pat_wide, by = "patientId")

pat_csv    <- file.path(out_dir, "brca_tcga_pan_can_atlas_2018_clinical_patient.csv")
samp_csv   <- file.path(out_dir, "brca_tcga_pan_can_atlas_2018_clinical_sample.csv")
merged_csv <- file.path(out_dir, "brca_tcga_pan_can_atlas_2018_clinical_merged.csv")

write_csv(pat_wide,  pat_csv)
write_csv(samp_wide, samp_csv)
write_csv(merged,    merged_csv)

cat("Patient-level:  ", nrow(pat_wide),  "rows x", ncol(pat_wide),  "cols ->", pat_csv,    "\n")
cat("Sample-level:   ", nrow(samp_wide), "rows x", ncol(samp_wide), "cols ->", samp_csv,   "\n")
cat("Merged (sample): ", nrow(merged),    "rows x", ncol(merged),    "cols ->", merged_csv, "\n\n")

cat("--- Preview of merged (first 5 rows, selected cols) ---\n")
preview_cols <- intersect(
  c("sampleId","patientId","AGE","SEX","RACE","SUBTYPE",
    "AJCC_PATHOLOGIC_TUMOR_STAGE","GRADE",
    "OS_MONTHS","OS_STATUS","DFS_MONTHS","DFS_STATUS",
    "MUTATION_COUNT","TMB_NONSYNONYMOUS","FRACTION_GENOME_ALTERED"),
  names(merged)
)
print(head(merged[, preview_cols], 5))

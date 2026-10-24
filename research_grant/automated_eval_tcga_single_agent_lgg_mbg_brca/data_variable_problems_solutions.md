# Data files for the brain-mets benchmark

Revised after inspecting what is actually on disk. Column names below are **verified
by reading the files**, except where marked NOT ON DISK.

## What is on disk

### A. TCGA - cBioPortal export (verified)

`/Users/robertjames/loc/repos/portfolio_ai_engineering_projects/genie_brain_met/data/tcga_data_merged.xlsx`
106.7 MB, 5 sheets. This is **TCGA-BRCA only**, not pan-cancer.

| Sheet | Rows | Cols | Contents |
|---|---|---|---|
| `data_clinical_patient` | 1,084 | 38 | `PATIENT_ID`, `SUBTYPE`, `CANCER_TYPE_ACRONYM`, `AGE`, `SEX`, `AJCC_PATHOLOGIC_TUMOR_STAGE`, `DAYS_TO_INITIAL_PATHOLOGIC_DIAGNOSIS`, `DAYS_LAST_FOLLOWUP`, `HISTORY_NEOADJUVANT_TRTYN`, `NEW_TUMOR_EVENT_AFTER_INITIAL_TREATMENT`, `PATH_M_STAGE`/`N`/`T`, `PERSON_NEOPLASM_CANCER_STATUS`, `RADIATION_THERAPY`, `IN_PANCANPATHWAYS_FREEZE`, `OS_STATUS`/`OS_MONTHS`, `DSS_*`, `DFS_*`, `PFS_*` |
| `data_clinical_sample` | 1,084 | 19 | `SAMPLE_ID`, `ONCOTREE_CODE`, `CANCER_TYPE_DETAILED`, `GRADE`, `SAMPLE_TYPE`, `TUMOR_TISSUE_SITE`, `TMB_NONSYNONYMOUS`, `ANEUPLOIDY_SCORE`, `MSI_SENSOR_SCORE`, `SOMATIC_STATUS` |
| `data_mutations` | 126,252 | 111 | MAF format: `Hugo_Symbol`, `Entrez_Gene_Id`, `NCBI_Build`, `Variant_Classification`, `Tumor_Sample_Barcode`, `t_ref_count`/`t_alt_count`, `HGVSp_Short`, `Hotspot`, `Consequence` |
| `data_cna` | 446,680 | 9 | `hugoGeneSymbol`, `entrezGeneId`, `sampleId`, `patientId`, `alteration` (GISTIC threshold) |
| `hugo` | 18,454 | 19 | HGNC table: `symbol`, `entrez_id`, `ensembl_gene_id`, `prev_symbol`, `alias_symbol`, `gene_group` |

duplicates?
missing?
types? 
dates as date time?

Carries the variables the scenario actually needs:

- `dist_mets_brain_cns` - brain/CNS metastasis indicator
- `dx_to_dist_mets_brain_cns_days` / `_mos` / `_yrs` - **time from diagnosis to brain met**, the AFT outcome
- Same quadruplet for 17 other met sites (bone, liver, pulmonary, ...), plus `dx_to_dmets_days`
- `os_dx_status`, `tt_os_dx_days` - survival from diagnosis, for competing-risk handling
- `stage_dx`, `stage_dx_iv`, `ca_path_t_stage`/`n_stage`, `ca_grade`, `age_dx`, `ca_hist_brca`
- `SEQ_ASSAY_ID` / `cpt_seq_assay_id` - **panel identity**, needed for the `n_assessed` denominator
- `dx_path_proc_cpt_days`, `path_proc_number` - pathology procedure timing


### C. GDC BRCA MAF manifests (verified, files not downloaded)

`/Users/robertjames/loc/gdc-brca-star/` - `gdc_manifest_BRCA_MAF.txt` (992 aliquot-level
`wxs.aliquot_ensemble_masked.maf.gz` entries with md5s) and `brca_maf_samplesheet.tsv`
mapping `file_id` to TCGA barcodes. Only the manifests are here; the MAFs themselves
are not.

## The problem
data is tab indented and malformed with features wrapping to rows beyond 0. 
must realize surgical candidate is stage 3 or less, excluding stage 4 on initial diagnosis
calls for bioconductor adapted script for analysis but rules state python
steps in data quality and preprocessing not specified
patient level vs sample level analysis not specified. this should be flagged
samples may have multiple mutations and mutation assesnnebt requires widening the data as you make gene presence a binary feature
assessing statistical difference amongst groups may not be possible for those with nearly no events of interest (no brain mets). that feature likely should not be analyzed with using such a dataset
genes may be on the pathway assessed and thus we should test for colinearity via pearson correlation, only modeling those that are not multicolinear in regression
aft modeling assumes non-linear relationship which was not the case win our run. thus making cox proportional hazard as the sensible option
assumptions need to be tested for in linear regression and time to event modeling
competing risks exist with death
conditional time ratio in time to event modeling requires isolating the effect of one variable changing another variables risk on time to event (genexpathway)
significance may arise due to chance with so many predictors being tested

## Solution

1. Remove trailing newlines/spaces and split by any existing whitespace/tabs with line.strip().split()
2. Realize uncertainty, ask user for clarity on surgical candidacy
3. Data quality and preprocessing involves deduplication and chanign dates of type integer or string to date-time
4. Several rare types of histologic subtypes included in data. that should be flagged as they do not behave regularly and are often excluded from analysis in breast cancer
5. Convert R to Python adapted bioconductor script
7. bioconductor script not provided and there is not web access. must be user provided
8. ask to analyze as sample vs patient
9. group by hugo symbol and create binary gene variable
10. Exclude one of two variables if shown to be colinear from linear regression
11. Assess linear regression and aft model assumptions. will only report appropriate values if correct model used 
12.Cox PH cant be used due to competing risk of death and requires subdistribution hazard
13.In AFT modeling group independent variables in regression equation to assess for time ratio of one variable dependent on another
14.To assess statistical difference between groups, use bonferroni, benjamini hochberg, or report q values with FDR (most appropriate for this use case)

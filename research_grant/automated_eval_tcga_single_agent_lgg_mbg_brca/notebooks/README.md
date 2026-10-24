# Final analysis notebooks

This directory contains the planned final, reproducible notebooks. They are intentionally
scaffolded without data or executed output. Use repository-relative paths, never
machine-specific paths, and write data-derived artifacts only under gitignored
`data/processed/` and `reports/`.

| Notebook | Purpose |
|---|---|
| `01_lgg_gbm_mutation_pathway_eda.ipynb` | LGG versus GBM mutation and pathway prevalence, ratios, correlation, and regression |
| `02_brca_staged_structured_extraction.ipynb` | BRCA Pydantic/Instructor staged JSON extraction and Pydantic Evals |
| `03_brca_brain_metastasis_and_survival.ipynb` | BRCA brain-metastasis associations and time-to-event analyses |
| `04_brca_brain_met_vs_gbm.ipynb` | BRCA brain-metastasis versus GBM mutation/pathway comparison |

Run notebooks in numerical order only after snapshotting their source data and completing
the missingness audit specified in `PLAN.md`.

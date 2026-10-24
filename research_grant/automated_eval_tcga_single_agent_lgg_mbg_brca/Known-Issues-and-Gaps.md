# Known issues and gaps

`STATUS.md` is the live checklist. This page records constraints that prevent the
current plan from being called complete.

## Active-program gaps

1. No snapshot-dated LGG/GBM run is archived in this workspace.
2. The LGG/GBM workflow has Fisher tests and BH correction only. Prevalence-ratio
   confidence intervals, correlations, regressions, final notebook, and figures are
   not implemented.
3. The BRCA cBioPortal pull is implemented, but no staged JSON extractor, Pydantic
   schema, Instructor integration, golden dataset, or Pydantic Evals suite exists.
4. No auditable TCGA-BRCA brain-metastasis definition, analysis cohort, association
   model, survival model, or BRCA-versus-GBM comparison exists.
5. All four numbered notebooks are markdown-only, unexecuted scaffolds.
6. Source snapshots, mutation definitions, pathway map, analytic thresholds,
   missingness audits, and join diagnostics still need to be finalized for planned work.

## Historical code and documents

The repository retains duplicated GENIE/MSK harmonization and analysis-era files,
including `harmonize_*.py`, `pull_genie_data.R`, historical CSV caches, and the
GENIE-focused schema specification. They reference paths, cohorts, and modules that
are not part of the active TCGA program. They are not supported commands and must not
be used to claim replication, survival results, or a populated current pipeline.

The following top-level documents are intentionally preserved as historical records:

- `README_survival_pipeline.md`
- `genomic_analysis_pipeline.md`
- `genie-brain-met-megaplan-f827d4.md`

They describe a retired GENIE-focused plan and are not current instructions. Use
`README.md`, `PLAN.md`, and this file instead.

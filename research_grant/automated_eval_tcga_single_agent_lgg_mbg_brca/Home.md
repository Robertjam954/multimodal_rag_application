# TCGA genomic analysis and extraction program

This workspace is planning and implementing a TCGA-only program:

1. LGG versus GBM mutation and pathway EDA.
2. BRCA staged structured JSON extraction.
3. BRCA brain-metastasis association and survival analysis.
4. BRCA brain-metastasis versus GBM comparison.

Only the LGG/GBM Fisher-test R workflow and BRCA cBioPortal snapshot pull are
implemented. The four final notebooks are unexecuted scaffolds. No BRCA extraction,
brain-metastasis classification, survival analysis, or cross-cohort comparison is
complete.

## Start here

| Document | Purpose |
|---|---|
| [README](README.md) | Scope and current runnable workflows |
| [Plan](PLAN.md) | Ordered implementation plan |
| [Analysis aims](Analysis-Aims.md) | Estimands and intended methods |
| [Status](STATUS.md) | Live implementation checklist |
| [Getting started](Getting-Started.md) | Supported setup and commands |
| [BRCA extraction specification](docs/brca_staged_extraction_and_evaluation.md) | Target staged JSON contract and evaluation design |
| [Known issues and gaps](Known-Issues-and-Gaps.md) | Current limitations and historical-material boundary |

Historical GENIE-focused documents are retained for provenance only. They are not a
quick start and do not describe the active TCGA workflow.

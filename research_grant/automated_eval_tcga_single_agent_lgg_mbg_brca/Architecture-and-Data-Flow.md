# Architecture and data flow

This page is a concise companion to [`ARCHITECTURE.md`](ARCHITECTURE.md). It replaces
the retired GENIE/MSK pipeline map as the guide for current work.

## Active data flow

1. Run `compare_tcga_lgg_gbm.R` against GDC for the implemented LGG versus GBM
   Fisher-test workflow.
2. Run `pull_tcga_brca_cbioportal.py` to create a manifest-backed public BRCA snapshot.
3. Implement and validate staged BRCA JSON extraction before deriving any
   brain-metastasis cohort.
4. Implement BRCA association, survival, and cross-cohort analyses in notebooks
   `03` and `04`.

Steps 3 and 4 are targets. The four notebooks have no code cells or executed results.

## Output boundary

All source data, cached API responses, model outputs, and patient-level analytic
records stay under gitignored `data/`. Executed reports may be written below
`reports/` only after their generation code exists. Preserve source snapshot hashes,
cohort flow, join diagnostics, missingness audit, mutation filter, and pathway-map
version with every run.

## Historical material

The duplicated harmonization scripts and committed GENIE/MSK CSV caches document an
older analysis effort. They are not inputs, outputs, or validation evidence for the
active TCGA program. See [`Known-Issues-and-Gaps.md`](Known-Issues-and-Gaps.md) for
their status.

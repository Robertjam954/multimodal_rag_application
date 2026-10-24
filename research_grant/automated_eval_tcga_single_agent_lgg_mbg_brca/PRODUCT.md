# Product

## Current purpose

This repository is a TCGA-only genomic analysis and structured-extraction program. Its
near-term deliverables are LGG versus GBM mutation/pathway EDA, BRCA staged JSON
extraction, BRCA brain-metastasis association and survival analysis, and BRCA
brain-metastasis versus GBM comparison.

The implemented foundation is intentionally narrow:

- An R workflow obtains LGG and GBM MAF data and performs gene/pathway Fisher tests.
- A Python workflow snapshots public BRCA cBioPortal tables with a manifest.

Neither workflow produces the planned BRCA analytic record, survival result, final
notebook, or benchmark result.

## Later benchmark purpose

The original controlled question remains: whether a single ReAct research agent or a
LangGraph multi-agent team performs better on identical biomedical tasks. This is a
future benchmark, not the current product capability. The agent arms, tools,
retrieval, prompt registry, run store, task set, and metrics are **(target)**.

If built, the comparison must use shared frozen infrastructure and follow the immutable
records in `docs/adr/`. It must report quality, cost, behavior, uncertainty, and
judge-human agreement rather than declare a winner from a point estimate.

## Boundaries

- Use public TCGA data only. Do not add GENIE or MSK patient-level data.
- Do not infer a clinical negative from absent BRCA evidence.
- Do not claim causal effects from the planned observational comparisons.
- Keep raw data and patient-level derived records under gitignored `data/`.

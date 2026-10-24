---
title: TCGA glioma and BRCA analysis plan
status: active planning
owner: Robertjam954
---

# TCGA glioma and BRCA analysis plan

## Scope and terminology

The cohorts are TCGA-LGG (lower-grade glioma), TCGA-GBM (glioblastoma multiforme), and
TCGA-BRCA (breast invasive carcinoma). "Brain meds" in earlier notes is interpreted as
**brain metastases**, not medication exposure. "Jeans" is interpreted as **genes**.
Those definitions must be confirmed against the eventual BRCA clinical-source fields
before analysis.

The project excludes GENIE and MSK patient-level data. It retains the existing
single-agent versus multi-agent benchmark as a later objective, but first establishes
a valid staged JSON extraction task over BRCA inputs.

## Ordered work

### 0. Supplied Aim 1 aggregate-table staging

`src/ingest/stage_aim1_result_tables.py` is an implemented JSON staging utility for
five supplied CSV aggregate-table layouts. It validates the static contract in
`schemas/aim1_result_tables.schema.json`, then atomically writes JSON record arrays,
a manifest, and optional bounded previews to gitignored `data/processed/aim1/`.

This is a validated interchange step, not a rerun of Aim 1 and not evidence that the
LGG/GBM EDA, BRCA extraction, association, or survival analyses are complete. Preserve
the supplied aggregate provenance and do not commit or move attachments.

### 1. LGG versus GBM mutation and pathway EDA

Build on `data collection and processing/compare_tcga_lgg_gbm.R`.

- Freeze GDC snapshot date, MAF workflow, non-silent variant classes, primary-tumor
  selection, and the Sanchez-Vega pathway-gene map.
- Audit cohort size, mutation-free denominator retention, duplicate patients, missing
  gene symbols, and pathway assignment before inference.
- Report per-gene and per-pathway mutation counts, prevalence, prevalence ratio
  (GBM/LGG), 95% confidence interval, Fisher exact p-value, and BH-adjusted q-value.
- Estimate correlation matrices separately within LGG and GBM for prevalent genes and
  pathways. State the binary association statistic and prevalence threshold in advance.
- Fit prespecified, interpretable logistic regressions for cohort membership with
  mutation features. Avoid fitting high-dimensional unpenalized models; document
  covariates, collinearity handling, complete-case rule, and events-per-parameter.

### 2. TCGA-BRCA staged structured extraction

Create a machine-readable analytic record from public BRCA clinical and molecular
source records. Stage 0 is missingness normalization: blank values and JSON `NaN`
become `null`, and only records missing across every field are dropped. It emits a
strict Draft 2020-12 schema-validated JSON missingness report before any inventory or
extraction. JSON readers reject duplicate object keys, nonstandard constants, and
numeric literals that become non-finite through exponent overflow. The remaining stages
are:

1. Source inventory and source-record identifiers.
2. Patient identity and sample linkage.
3. Clinical timeline and brain-metastasis status, retaining evidence and unknowns.
4. Molecular mutations and pathway assignments.
5. Derived analytic endpoints and validation summary.

Every stage has a Pydantic model, accepts prior-stage JSON rather than re-reading
unbounded text, and returns JSON only. Inputs, handoffs, golden cases, JSON Schema
artifacts, and evaluation reports are JSON-first; use JSON Lines only when batching is
needed. This planned requirement does not convert existing R or Python analysis
workflows. Unavailable, conflicting, and indeterminate values must be represented
explicitly - never inferred as negative.

The authoritative design is
[`docs/brca_staged_extraction_and_evaluation.md`](docs/brca_staged_extraction_and_evaluation.md).
It includes versioned prompt requirements, golden cases, deterministic validators, and
code-based Pydantic Evals using typed `Dataset` and `Case` objects, schema validation,
and exact expected-value checks.

`src/analysis/evaluate_extraction_model_accuracy.py` is implemented as the downstream
reporter once one immutable golden JSON dataset and three comparable JSON prediction
payloads exist. It computes the golden file's SHA-256, rejects source truth in
predictions, and limits inference to case-level all-applicable-feature exact accuracy
with 95% Agresti-Coull intervals. It performs only the three overall pairwise McNemar
tests with BH correction; stage and feature results are descriptive. It does not create
golden cases, predictions, or extracted BRCA records.

Before extraction, inventory the optional PanCancer clinical timeline/treatment,
genetic-ancestry, 450K methylation, and tumor-break-load sources in
[`docs/tcga_pancan_data_enrichment.md`](docs/tcga_pancan_data_enrichment.md). Add a
source to the Stage 1 JSON inventory only after its payload checksum, barcode mapping,
join diagnostics, missingness profile, and normalized JSON schema have been recorded.

### 3. TCGA-BRCA brain-metastasis association and survival analyses

- Define brain-metastasis-ever using structured clinical evidence and preserve an
  `unknown` category until the analysis cohort is finalized.
- Compare mutation and pathway prevalence between patients with and without
  brain metastasis ever, reporting prevalence ratios, confidence intervals, Fisher
  tests, and BH adjustment.
- Fit univariable models for all eligible genes/pathways and multivariable models only
  for prespecified top-five features plus justified clinical confounders.
- Among patients with brain metastasis, compare time to brain metastasis, time to
  recurrence, and overall survival by the top five mutated genes. Define each time
  origin, event, censoring rule, inclusion restriction, and competing-risk treatment
  before fitting Kaplan-Meier, Cox, and AFT models.
- Do not claim causality from these observational associations.

### 4. BRCA brain metastasis versus GBM comparison

Restrict the BRCA group to brain-metastasis cases. Compare the top mutated genes and
pathway mutation prevalence against TCGA-GBM using harmonized gene symbols, the same
non-silent mutation definition, a shared pathway map, prevalence ratios, uncertainty,
and multiple-testing correction. Present overlap with an UpSet plot and effect-size
table, not only a ranked-gene list.

## Final notebooks

The numbered notebooks in `notebooks/` are the only planned final notebook outputs.
They must use paths relative to the repository root, save tables and figures only below
`data/processed/` and `reports/`, and be executable in order after dependencies and
data are available.

## Statistical safeguards

- Perform and save a missingness audit before EDA.
- Report row counts at every join and cohort restriction.
- Select top-five BRCA features using the association stage only; avoid re-selecting
  them separately within each survival endpoint.
- Treat sparse mutation cells cautiously. Predefine minimum prevalence and use
  continuity-corrected or exact approaches as appropriate.
- Apply BH correction within a clearly named family of gene or pathway hypotheses.
- Check model assumptions and report failures rather than silently replacing models.

## Benchmark boundary

The extraction schema, prompts, golden set, and scoring rule are shared benchmark
infrastructure. Before the benchmark is frozen, they may evolve through documented
versions. Once used in a benchmark run, changing any of them requires an ADR and
re-running every comparison arm under the updated configuration.

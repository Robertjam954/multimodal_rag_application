# Analysis aims

## Cross-cutting data and cohort rules

All analyses use public TCGA sources and a snapshot-specific manifest. Before fitting
any model, save source checksums, primary sample selection, barcode mappings,
missingness, duplicate-key diagnostics, and row counts at every join. Blank fields and
JSON `NaN` values are normalized to `null` in the first staged dataset; only records
with null across every field are dropped. Unknown,
ambiguous, and conflicting clinical information remain explicit categories until each
analysis specifies how they are handled.
Stage 0 rejects duplicate keys and nonstandard JSON and validates its missingness
report against the strict Draft 2020-12 schema before publication.

The BRCA program starts with cBioPortal clinical, mutation, CNA, and structural-variant
JSON snapshots. Planned PanCancer enrichment uses four additional sources:

```json
{
  "datasets": [
    {
      "id": "clinical_timeline_treatment",
      "source_file": "Merge_Clinical.Level_1.20160128/clin.merged.txt",
      "planned_output": "clinical_timeline_treatment.json"
    },
    {
      "id": "genetic_ancestry",
      "source_file": "Admixture_by_sample.txt",
      "planned_output": "genetic_ancestry.json"
    },
    {
      "id": "methylation_450k",
      "source_file": "jhu-usc.edu_PANCAN_HumanMethylation450.betaValue_whitelisted.tsv",
      "planned_output": "methylation_450k_feature_summary.json"
    },
    {
      "id": "tumor_break_load",
      "source_file": "clinical_attributes.json",
      "planned_output": "tumor_break_load.json"
    }
  ]
}
```

The source definitions and data-specific validation gates are in
[`docs/tcga_pancan_data_enrichment.md`](docs/tcga_pancan_data_enrichment.md). Methylation
is not passed wholesale to an LLM and is not used in a model until a probe-reduction
strategy is specified. Tumor break load is used only if the exact cBioPortal attribute,
data type, and sample coverage are verified.

## Aim 1 - TCGA-LGG versus TCGA-GBM mutation landscape

**Question:** Which non-silent somatic mutations and Sanchez-Vega oncogenic pathways
have different prevalence in primary LGG and GBM tumors?

**Unit and denominator:** one selected sample-type-01 primary tumor per patient from
the GDC MAF query inventory, including eligible patients with no retained non-silent
mutation.

**Primary measures:** mutation count, prevalence, GBM/LGG prevalence ratio with 95%
confidence interval, Fisher exact p-value, BH q-value, and direction of enrichment.

**Secondary analyses:** estimate gene-gene and pathway-pathway binary associations
separately within LGG and GBM after a prespecified prevalence filter. Fit interpretable,
prespecified logistic regressions for cohort membership, documenting feature selection,
collinearity handling, clinical covariates, complete-case rules, and sparse-cell
handling. These regression and correlation analyses complement rather than replace
the prevalence comparisons.

## Aim 2 - TCGA-BRCA staged extraction and source enrichment

**Question:** Can source records be transformed into schema-valid, evidence-linked JSON
analytic records while retaining missingness and lineage?

**Stages:** missingness normalization, source inventory, patient and sample linkage,
clinical timeline, molecular profile, and derived analytic record. The stage inventory records which
optional PanCancer sources are present and whether they passed their join and schema
gates.

**Outputs:** every stage writes JSON only: bounded input, validated output, evidence
references, data-quality findings, golden case, numeric feature check, and evaluation
summary. JSON Lines is used only for batched records.

**Evaluation:** an immutable golden JSON dataset supplies `source_present` and expected
values; three prediction payloads cannot supply source truth. Feature, stage, and
stage-element exact-match results are descriptive. Overall inference uses case-level
all-applicable-feature exact matches with Agresti-Coull intervals and three
BH-adjusted overall pairwise McNemar tests. The full contract is
[`docs/brca_staged_extraction_and_evaluation.md`](docs/brca_staged_extraction_and_evaluation.md).

## Aim 3 - BRCA brain-metastasis association

**Question:** Among TCGA-BRCA patients, which genes and pathways differ between cases
with and without brain metastasis ever?

**Feasibility gate:** before inference, establish that the selected public source
contains an auditable brain-metastasis site and date, sufficient confirmed positive
cases, and a distinguishable confirmed-negative population. If not, report the
limitation and do not relabel a broader distant-metastasis endpoint as brain
metastasis.

**Primary measures:** gene and pathway counts, prevalence, prevalence ratios, 95%
confidence intervals, Fisher exact tests, and BH correction. Treat unknown and
conflicting brain-metastasis status separately in descriptive reporting. The primary
comparison includes only confirmed cases and confirmed non-cases under the documented
eligibility rule.

**Adjusted associations:** fit univariable models for eligible features and
multivariable models only for the prespecified top-five mutation features plus justified
clinical covariates. Timeline/treatment and ancestry variables can be descriptive or
adjustment covariates only after their source-specific gates pass. Methylation and TBL
are exploratory and do not silently alter the primary model.

## Aim 4 - Outcomes among BRCA brain-metastasis cases

**Question:** Among BRCA patients with confirmed brain metastasis, do the top five
mutation features from Aim 3 stratify time to brain metastasis, time to recurrence, or
overall survival?

**Eligibility:** confirmed brain-metastasis cases with a valid time origin and relevant
event/censoring information. Each endpoint has a separate eligibility table; no
patient is assumed eligible for all endpoints.

**Methods:** event and censoring summaries; Kaplan-Meier curves and log-rank tests;
Cox proportional-hazards models with proportional-hazards diagnostics; and AFT
sensitivity analyses. Define diagnosis, recurrence, brain-metastasis, and survival
time origins, event rules, censoring rules, competing-event handling, covariates, and
sparse-data thresholds before model fitting. Do not make causal claims.

## Aim 5 - BRCA brain metastasis versus GBM

**Question:** Which genes and pathways are shared or differentially mutated between
TCGA-GBM and BRCA brain-metastasis cases?

**Harmonization gate:** use identical non-silent mutation definitions, HUGO-symbol
normalization, pathway-map version, patient/sample selection logic, and prevalence
thresholds across cohorts. Record any source differences that prevent a direct
comparison.

**Measures:** top-gene and pathway rankings, overlap, prevalence ratios with confidence
intervals, Fisher exact tests with BH correction, and an UpSet plot. This is a
cross-cohort descriptive comparison and is not evidence that a mutation causes
metastasis or glioma.

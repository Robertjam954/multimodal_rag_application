# CLAUDE.md

Operating notes for the TCGA genomic analysis and structured-extraction program.
Reality wins over plans. A capability is marked **(target)** until code and a
reproducible run demonstrate it.

## Current program

The active work is TCGA-only and has four ordered deliverables:

1. TCGA-LGG versus TCGA-GBM non-silent mutation and Sanchez-Vega pathway EDA.
2. TCGA-BRCA staged, evidence-linked structured JSON extraction.
3. TCGA-BRCA brain-metastasis association and survival analyses.
4. A harmonized comparison of BRCA brain-metastasis cases with TCGA-GBM.

The later single-ReAct versus LangGraph benchmark remains a design objective. Its
agents, retrieval, task set, prompt registry, run store, and evaluation harness are
**(target)**. Do not present their ADRs as implemented software.

## What runs today

- `data collection and processing/compare_tcga_lgg_gbm.R` retrieves GDC masked somatic
  MAF calls for TCGA-LGG and TCGA-GBM, selects one sample-type-01 tumor per patient,
  retains mutation-free patients in the denominator, and writes gene and pathway
  Fisher-test results with provenance.
- `src/data collection and processing/pull_tcga_brca_cbioportal.py` retrieves the
  public `brca_tcga_pan_can_atlas_2018` cBioPortal study, paginates clinical,
  mutation, CNA, and structural-variant responses. It normalizes clinical long records
  before duplicate-checked pivots, preserves nine JSON record arrays, writes
  `missingness_report.json`, and records request retries in its snapshot manifest. Its
  response decoder rejects duplicate keys, maps `NaN` to `null`, rejects other
  nonstandard constants and exponent-overflow numbers, validates the Stage 0 report,
  and verifies that cBioPortal `importDate` is unchanged from the start to the end of
  the pull. The manifest records the source `reference_genome`.
- `src/analysis/evaluate_extraction_model_accuracy.py` compares exactly three
  comparable JSON prediction payloads against a separately supplied immutable golden
  JSON dataset. It hashes the golden file, calculates case-level all-applicable-feature
  accuracy with Agresti-Coull intervals, performs three BH-adjusted overall McNemar
  comparisons, and writes JSON plus PDF and 600 DPI PNG figures. It does not extract
  BRCA data.
- `src/extraction/stage_missingness.py` is the implemented Stage 0 JSON normalizer. It
  converts blank or whitespace-only strings and JSON `NaN` to `null`, drops only
  records that are null across every field after normalization, hashes canonical
  pre-normalization records, and writes schema-validated normalized arrays and a
  missingness report. Each report entry uses the actual input basename as
  `source_filename` and labels that canonical decoded representation. It has not been
  run on an archived BRCA snapshot.
- `notebooks/` contains four unexecuted markdown-only delivery scaffolds. No notebook
  implements or runs an analysis yet.

## Repository layout

```text
tcga_deep_research_benchmark/
  data/                                      gitignored local inputs and outputs
    raw/cbioportal/                          BRCA snapshot directories written by the pull script
    processed/tcga_lgg_vs_gbm/               LGG/GBM workflow output location
    processed/aim1/                          local JSON staging output of supplied aggregate tables
  data collection and processing/
    compare_tcga_lgg_gbm.R                   implemented LGG/GBM Fisher-test workflow
    harmonize_*.py, pull_genie_data.R, ...   legacy GENIE/MSK material, not the active plan
  src/
    data collection and processing/
      pull_tcga_brca_cbioportal.py           implemented BRCA cBioPortal snapshot pull
      _genomic_features.py                   shared historical feature helper
    utils/decision_log.py                    standard-library decision log
    ingest/
      stage_aim1_result_tables.py            implemented atomic staging and named-schema validation of five supplied CSV tables
      reusable TCGA snapshot loaders          (target)
    analysis/
      evaluate_extraction_model_accuracy.py  implemented three-model JSON accuracy comparison
      other statistical analysis functions    (target)
    rag/, prompts/, agents/, tracking/        **(target)**
    extraction/
      stage_missingness.py                     implemented Stage 0 JSON missingness normalizer
      staged Pydantic and Instructor extraction (target)
    reporting/                                 reusable tables, figures, and JSON previews (target)
  notebooks/
    01_lgg_gbm_mutation_pathway_eda.ipynb    scaffold
    02_brca_staged_structured_extraction.ipynb scaffold
    03_brca_brain_metastasis_and_survival.ipynb scaffold
    04_brca_brain_met_vs_gbm.ipynb           scaffold
  docs/
    brca_staged_extraction_and_evaluation.md  active extraction design
    tcga_pancan_data_enrichment.md             active PanCancer source-integration design
    adr/                                     immutable benchmark decision records
  schemas/
    aim1_result_tables.schema.json           implemented static contract for supplied Aim 1 tables
    extraction_golden_numeric_checks.schema.json
    extraction_model_predictions.schema.json
    extraction_model_comparison.schema.json
    missingness_stage.schema.json             implemented JSON contracts
    additional BRCA extraction schemas        (target)
  eval/
    datasets/, evaluators/                    JSON golden cases and deterministic scoring (target)
  tests/fixtures/                            synthetic JSON-only fixture records
  reports/
    tables/, figures/, evaluations/           generated analysis and evaluation outputs
  PLAN.md  Analysis-Aims.md  STATUS.md       active scope, methods, and checklist
```

## Data, outputs, and dependencies

- Never commit data or patient-level derived output. `data/` is gitignored.
- Use only public TCGA data in the active program. GENIE and MSK patient-level data are
  out of scope.
- The R workflow requires the documented R packages in `requirements.txt` comments.
  Current Python scripts import only the packages declared in `requirements.txt`.
- Do not add Instructor, Pydantic, Pydantic Evals, survival, retrieval, agent, or model
  packages until the corresponding implementation imports them.
- Use repository-relative paths. The notebook scaffolds contain no executable path or
  environment configuration.

## Analysis rules

- Complete and save the missingness and join audit before EDA.
- Record source snapshot, eligibility, sample selection, mutation filter, pathway map,
  exclusions, and output provenance for every executed analysis.
- Do not convert absent BRCA clinical evidence into a negative brain-metastasis status.
- Planned BRCA staged extraction is JSON-first: inputs, handoffs, outputs, golden
  cases, schema artifacts, and evaluation reports use JSON. Use JSON Lines only for
  batching. This does not change existing R or Python analysis workflows.
- Stage 0 and the extraction-accuracy reporter use `jsonschema==4.26.0` with strict
  Draft 2020-12 schemas. Their JSON readers reject duplicate object keys, nonstandard
  constants, and numeric literals that become non-finite through exponent overflow
  rather than silently accepting or overwriting them.
- The BRCA pull applies the same strict decoder to cBioPortal responses. It records
  each request's retries and aborts without publication if the study `importDate`
  changes during retrieval. Its manifest records the API study's `reference_genome`.
- Each pull-generated Stage 0 dataset report records a SHA-256 of canonical
  pre-normalization JSON records with
  `source_representation: canonical_pre_normalization_records`. This provenance is
  distinct from the checksum of the published normalized JSON output in the manifest.
- The extraction-accuracy comparison accepts one immutable golden JSON file and exactly
  three prediction payloads. It computes and requires the golden file's SHA-256 hash,
  rejects source truth in predictions, and scores only golden `source_present: true`
  checks. Its inferential unit is a case with all applicable features exact. It is not
  evidence that extraction runners, golden cases, or BRCA analyses have been
  implemented.
- `data/processed/aim1/` is a gitignored local JSON staging output for five supplied
  aggregate Aim 1 CSV tables. Its manifest records output checksums and source
  filenames. The five inputs must be distinct files by filesystem identity: the utility
  compares device and inode, with a resolved-path fallback where no inode is available.
  UUID-prefixed attachments are accepted when their basename ends in the required
  logical table-name suffix. Per-record validation requires mutation counts no greater
  than their denominators, positive odds ratios with ordered positive confidence bounds,
  and prevalence ratios within ordered nonnegative bounds. It recomputes each
  prevalence from its count and denominator and requires the reported prevalences and
  ratio to match within `math.isclose(..., rel_tol=1e-12, abs_tol=1e-12)`. A zero
  numerator prevalence, ratio, or lower ratio bound is valid; a zero reference
  prevalence is rejected because the required finite ratio cannot be represented in
  JSON.
  Each array is validated against its named, table-specific Draft 2020-12 schema;
  an intended empty table is valid. It is not raw data, a replacement for the planned
  extraction pipeline, or proof that a new analysis has been run.
- Generate final figures only after the analyses exist. The target standard is vector
  PDF plus 600 DPI PNG, grayscale-safe Okabe-Ito colors, and annotated denominators.
- No em dashes. Use single hyphens only.

## Methods

### Missing-data handling

- Run Stage 0 missingness normalization before inventory, linkage, extraction, EDA, or
  model fitting. It converts blank and whitespace-only values and JSON `NaN` to JSON
  `null`, retains every partially observed record, and drops a record only when all
  fields are null after normalization.
- Save `missingness_report.json` for every normalized source. It must report records
  input, retained, dropped because all columns are missing, and field-level missing
  counts and fractions before any rows are dropped.
- Do not use a blanket `dropna()` or infer clinical absence from a null. For each
  descriptive table, regression, and survival endpoint, report the analysis-specific
  denominator, complete-case restriction, exclusions, and missing-data treatment.
- Treat missingness as potentially structural. Before relying on complete-case analysis,
  assess missingness patterns and associations with observed variables. Any future
  MCAR/MAR/MNAR diagnostic must be labeled as a diagnostic or sensitivity analysis:
  no observed-data test can prove MAR or MNAR.
- For brain-metastasis status, keep confirmed negative, `not_recorded`, `ambiguous`,
  and `conflicting` distinct until the analysis cohort is defined. The primary
  confirmed-case comparison must report excluded unknown or conflicting records.

### TCGA genomic analyses

- LGG/GBM and BRCA brain-metastasis associations use patient/sample counts,
  prevalence, prevalence ratios with a prespecified 95% interval method, two-sided
  Fisher exact tests for sparse binary features, and Benjamini-Hochberg correction in
  explicitly named gene and pathway hypothesis families.
- Binary gene and pathway correlation analyses are exploratory. State the selected
  binary association measure, prevalence filter, cohort, and multiple-testing family
  before calculating the matrix. Do not interpret co-mutation correlation as causal.
- Logistic regression estimates associations with cohort or brain-metastasis status.
  Predefine clinical covariates, feature-selection rules, sparse-cell treatment,
  collinearity checks, events-per-parameter safeguards, and the exact denominator.
  Do not use an unpenalized high-dimensional model.
- Within confirmed BRCA brain-metastasis cases, survival analyses must define the time
  origin, event, censoring, competing-event strategy, and eligibility rule separately
  for time to brain metastasis, recurrence, and overall survival. Use Kaplan-Meier
  summaries and log-rank tests, Cox proportional-hazards models with diagnostics, and
  AFT sensitivity analyses only after those definitions are recorded.
- The BRCA brain-metastasis versus GBM comparison is descriptive. Use harmonized
  non-silent mutation filters, gene names, pathway maps, denominators, and prevalence
  thresholds. Report overlap and uncertainty without causal interpretation.

### Three-model extraction evaluation

- The immutable golden JSON dataset is the only source of `source_present` and
  `expected_value`. The evaluator computes its SHA-256 hash and rejects model payloads
  that do not reference it exactly. Model payloads contain predictions only.
- Feature accuracy is descriptive: exact source-confirmed numeric matches divided by
  source-confirmed numeric checks. Source-absent checks are excluded from its numerator
  and denominator.
- Overall inferential accuracy uses one independent outcome per case: every applicable
  source-confirmed numeric feature in that case must exactly match. Report a 95%
  Agresti-Coull interval from `statsmodels`.
- Compare the three models using the three paired overall case-level McNemar tests.
  Use the exact binomial form for fewer than 25 discordant cases, otherwise the
  chi-squared approximation, then apply Benjamini-Hochberg correction across those
  three prespecified comparisons only.
- Stage and stage-element feature accuracy are descriptive only. Do not compute
  confidence intervals or hypothesis tests from correlated features within a case.
- Create `overall_accuracy_by_model.pdf` and 600 DPI PNG with case denominator
  annotations, plus the descriptive stage-element heatmap in both formats. Local
  pre-benchmark outputs do not replace the future benchmark run-store record.
  The heatmap uses a luminance-monotone five-bin scale: black, Okabe-Ito blue, green,
  yellow, and white, with white labels below 0.4 accuracy and black labels otherwise.

## Benchmark governance

`docs/adr/` records decisions for the later controlled benchmark. Read
`docs/adr/README.md` and `docs/experiment_metadata.md` before changing benchmark
topology, tools, retrieval, stores, models, metrics, tasks, or prompts. The metadata is
currently draft, not frozen. Existing ADR Context, Decision, and Consequences sections
are immutable.

## Documentation protocol

When code, commands, dependencies, structure, or conventions change, update
`README.md`, `PLAN.md`, `STATUS.md`, this file, and `requirements.txt` as applicable.
Do not mark analysis, extraction, or notebook work complete without runnable code and
an executed, auditable result.

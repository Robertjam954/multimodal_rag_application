# Architecture

## Current implemented flow

```text
GDC TCGA-LGG and TCGA-GBM
  -> compare_tcga_lgg_gbm.R
  -> data/processed/tcga_lgg_vs_gbm/
     selected_primary_samples.csv
     clinical_cases.csv
     mutation_enrichment_gbm_vs_lgg.csv
     pathway_enrichment_gbm_vs_lgg.csv
     gdc_mutation_file_manifest.csv
     run_provenance.txt and session_info.txt

cBioPortal TCGA-BRCA public API
  -> pull_tcga_brca_cbioportal.py
  -> data/raw/cbioportal/brca_tcga_pan_can_atlas_2018.<UTC timestamp>.<UUID>/
     clinical_patient_long.json, clinical_sample_long.json,
     clinical_patient.json, clinical_sample.json, clinical_merged.json,
     clinical_attributes.json, mutations.json, cna.json, structural_variants.json,
     missingness_report.json, manifest.json

five supplied Aim 1 aggregate CSV tables
  -> src/ingest/stage_aim1_result_tables.py
  -> data/processed/aim1/
     five JSON record arrays and manifest.json

three comparable JSON extraction-evaluation payloads
  -> src/analysis/evaluate_extraction_model_accuracy.py
  -> data/processed/extraction_model_comparison/
     model_accuracy_summary.json, two vector PDFs, and two 600 DPI PNG figures

source JSON record arrays
  -> src/extraction/stage_missingness.py
  -> data/processed/brca_missingness/
     normalized JSON arrays and missingness_report.json
```

The LGG/GBM R workflow is the only implemented inferential analysis. It uses one
primary-solid-tumor sample per patient and tests non-silent gene and pathway mutation
prevalence with two-sided Fisher exact tests and BH correction. It does not calculate
prevalence-ratio confidence intervals, correlations, or regressions.

The BRCA Python pull is data acquisition only. It verifies pagination against the API
advertised count, records the available clinical-attribute schema, and writes nine JSON
record arrays. It preserves normalized patient and sample long clinical records, then
requires the pivot keys to be unique before using `DataFrame.pivot` to create wide
clinical records. The pull writes `missingness_report.json` for all nine datasets.
The manifest records exact request configuration, successful and failed retry metadata,
dimensions, and per-file SHA-256 checksums. An optional preview prints zero through ten
JSON records per dataset. A unique UTC timestamp and UUID identify a temporary snapshot
that is atomically renamed only after all artifacts are complete. The pull does not yet
join the planned PanCancer timeline/treatment,
ancestry, methylation, or TBL sources; harmonize data; determine brain-metastasis
status; or run survival analysis.

The pull decodes cBioPortal responses strictly: duplicate object keys fail, `NaN`
becomes `null`, and other nonstandard numeric constants and exponent-overflow numbers
fail. It validates
`missingness_report.json` against the Stage 0 Draft 2020-12 schema before publication.
It retrieves study metadata both before and after all datasets and aborts if
`importDate` changes, preventing a mixed-version snapshot. Its manifest records the
study `reference_genome`. Each Stage 0 report entry records the SHA-256 of canonical
pre-normalization JSON records with
`source_representation: canonical_pre_normalization_records`; that source provenance
is separate from each published normalized-file checksum in the manifest.

The Aim 1 staging utility is a separate, implemented interchange boundary. It accepts
exactly five supplied CSV table shapes and publishes JSON only after validating exact
headers, canonical filename suffixes, distinct source files, finite numeric values,
probability ranges, nonnegative fields, and `kind` values where applicable. It writes
through a temporary directory and refuses to overwrite an existing output directory.
Each record array is validated against the named, table-specific Draft 2020-12 schema;
an intended empty array is valid.
Distinctness is filesystem identity, using device and inode with a resolved-path
fallback, so hard-linked inputs are rejected.
`data/processed/aim1/` is a gitignored local staging output of supplied aggregates, not
newly computed analysis or a BRCA extraction result.

The extraction-accuracy utility is also implemented, but it is a comparison reporter,
not an extractor. It accepts one immutable golden JSON file plus exactly three
prediction payloads, computes the golden SHA-256 digest, and rejects source truth in
predictions. Overall inference uses case-level all-applicable-feature exact matches
with 95% Agresti-Coull intervals. It performs only the three overall pairwise McNemar
tests, using exact McNemar below 25 discordant cases and asymptotic McNemar otherwise,
with BH correction across those three tests. Stage and stage-element feature results
are descriptive. It atomically publishes a JSON summary plus overall-accuracy and
stage-element heatmap figures; the heatmap uses a luminance-monotone black, Okabe-Ito
blue, green, yellow, and white five-bin scale with white labels below 0.4 accuracy and
black labels otherwise.
No comparable payloads or extraction output are
included in the repository.

Stage 0 is implemented before the planned extraction stages. It normalizes blank or
whitespace-only strings and JSON `NaN` values to `null`, preserves partly observed
records, and drops only records null across every field. It records a canonical
pre-normalization source checksum with the required `source_representation` field and
the actual input basename as `source_filename`, validates the report, and atomically
publishes the artifacts. Running Stage 0 on a BRCA snapshot remains outstanding.

## Research project structure

The repository uses a lean data-science structure informed by the `agentic_pathway`
reference project without adopting its unsupported FastAPI, React, database, Docker,
or deployment layers:

```text
src/
  ingest/                  implemented Aim 1 aggregate-table staging; reusable loaders (target)
  extraction/              implemented Stage 0 normalizer; later extraction stages (target)
  analysis/                implemented extraction-accuracy reporter; other functions (target)
  reporting/               tables, figures, and JSON-preview helpers (target)
  data collection and processing/
                            current standalone pull and R workflows
schemas/                   implemented Aim 1 static JSON contract; BRCA Pydantic schemas (target)
notebooks/                 ordered final analysis deliverables
eval/
  datasets/                adjudicated JSON golden cases (target)
  evaluators/              deterministic Pydantic Evals checks (target)
tests/
  fixtures/                synthetic JSON-only test records
reports/
  tables/, figures/, evaluations/
                            generated deliverables, separated by artifact type
```

The planned BRCA extraction packages, schemas, evaluation datasets, evaluation reports,
and test fixtures use JSON as their persisted interchange format. The implemented Aim
1 staging utility is a deliberate boundary that converts supplied CSV aggregates to
validated JSON. The existing LGG/GBM R workflow is intentionally not converted as part
of this structural change.

## Planned flow

```text
validated BRCA snapshot
  -> optional PanCancer-source JSON augmentation                  (target)
  -> staged Pydantic and Instructor JSON extraction             (target)
  -> evidence-linked analytic record and missingness audit      (target)
  -> brain-metastasis association and survival analyses         (target)
  -> BRCA brain-metastasis versus GBM comparison                (target)
```

The exact staged-extraction boundary and proposed evaluation gates are in
[`docs/brca_staged_extraction_and_evaluation.md`](docs/brca_staged_extraction_and_evaluation.md).
The ordered analytical plan is in [`PLAN.md`](PLAN.md).
The four external-source gates are in
[`docs/tcga_pancan_data_enrichment.md`](docs/tcga_pancan_data_enrichment.md).

## Later benchmark architecture

The ReAct baseline, LangGraph team, retrieval index, prompt registry, run store, and
evaluation harness described by the ADR set are all **(target)**. They are not current
pipeline components or supported commands. When implemented, their shared frozen
artifacts must follow the governance rules in `docs/experiment_metadata.md`.

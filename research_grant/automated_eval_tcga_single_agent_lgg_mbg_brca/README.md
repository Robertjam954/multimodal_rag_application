# TCGA genomic analysis and extraction benchmark

This repository plans a reproducible, TCGA-only study of somatic mutation patterns in
glioma and breast cancer. It has two linked purposes:

1. Produce auditable cohort analyses for TCGA-LGG, TCGA-GBM, and TCGA-BRCA.
2. Benchmark a single tool-using LLM on the TCGA-BRCA staged structured-extraction task
   before using that task in the later single-agent versus multi-agent experiment.

No GENIE or MSK patient-level data is in scope. All data and derived patient-level
outputs stay under gitignored `data/`.

## Analysis sequence

| Stage | Cohort | Question | Planned notebook |
|---|---|---|---|
| 1 | TCGA-LGG versus TCGA-GBM | Which genes and Sanchez-Vega pathways differ in mutation prevalence? | `01_lgg_gbm_mutation_pathway_eda.ipynb` |
| 2 | TCGA-BRCA | Can clinical and molecular source records be extracted into validated, staged JSON? | `02_brca_staged_structured_extraction.ipynb` |
| 3 | TCGA-BRCA | Are genes/pathways associated with brain metastasis, and among affected patients, with time to brain metastasis, recurrence, and overall survival? | `03_brca_brain_metastasis_and_survival.ipynb` |
| 4 | TCGA-BRCA brain metastasis versus TCGA-GBM | Which mutated genes and pathways overlap or differ? | `04_brca_brain_met_vs_gbm.ipynb` |

Stage 1 is the only implemented inferential analysis workflow today:

```zsh
Rscript "data collection and processing/compare_tcga_lgg_gbm.R" \
  --out-dir data/processed/tcga_lgg_vs_gbm
```

It pulls GDC masked somatic MAF calls, selects one primary-tumor sample per patient,
retains mutation-free sequenced patients in the denominator, and writes Fisher-test
gene and pathway results, provenance, and an R session record. The planned notebooks
will extend this with prevalence ratios, correlations, and regression models; they do
not yet execute analyses.

An implemented BRCA acquisition script is also available:

```zsh
python "src/data collection and processing/pull_tcga_brca_cbioportal.py" \
  --out-dir data/raw/cbioportal
```

It atomically publishes a unique UTC timestamp-and-UUID directory containing nine JSON
record arrays: normalized patient and sample long clinical records, their
duplicate-checked wide pivots, merged clinical data, the clinical-attribute catalog,
mutations, high-level CNA, and structural variants. It also writes
`missingness_report.json` and `manifest.json`. Pagination is checked; the manifest
records exact request configurations, successful and failed retries, dimensions, and
checksums. The strict response decoder rejects duplicate keys, maps `NaN` to `null`,
rejects other nonstandard constants and exponent-overflow numbers. Before publication,
the pull validates the Stage 0 report and verifies the cBioPortal `importDate` has not
changed since retrieval started. The manifest records the API study's
`reference_genome`. `--preview-records` prints zero through ten JSON records per
dataset. The script does not implement BRCA structured extraction or any
brain-metastasis analysis.

For every pull-generated Stage 0 dataset report, `source_checksum` identifies canonical
pre-normalization JSON records and is labelled
`source_representation: canonical_pre_normalization_records`. It is separate from the
published normalized-file checksum in `manifest.json`.

An additional implemented staging utility accepts five supplied Aim 1 aggregate CSV
table layouts and writes validated JSON record arrays and a manifest below gitignored
`data/processed/aim1/`. All five inputs must be distinct source files by filesystem
identity, so a hard link cannot satisfy two table inputs. It is an atomic local
interchange step, not a new analysis run; do not commit the output or move source
attachments. Each array is checked against its named table-specific JSON Schema, and
an intended empty array is valid. See
[`Getting-Started.md`](Getting-Started.md) for the complete command and
[`schemas/aim1_result_tables.schema.json`](schemas/aim1_result_tables.schema.json) for
the static contract.

The implemented Stage 0 normalizer accepts JSON record arrays, converts blank or
whitespace-only strings and JSON `NaN` to `null`, and drops only records null across
every field. It records a canonical pre-normalization source checksum with
`source_representation: canonical_pre_normalization_records` separately from the
normalized output identity, uses the actual input basename as `source_filename`, then
atomically writes schema-validated artifacts. It has not been run on an archived BRCA
snapshot and does not implement BRCA extraction.

An implemented extraction-accuracy reporter compares exactly three JSON prediction
payloads against a separately supplied immutable golden JSON dataset. It hashes the
golden file, rejects source truth in predictions, reports case-level all-applicable-
feature accuracy with 95% Agresti-Coull intervals, and performs three BH-adjusted
overall McNemar comparisons. Stage and feature results are descriptive. It writes a
JSON summary and vector PDF plus 600 DPI PNG figures, but does not implement BRCA
extraction or provide its inputs. See
[`docs/extraction_model_accuracy_evaluation.md`](docs/extraction_model_accuracy_evaluation.md).

## Project map

- [`PLAN.md`](PLAN.md) - ordered implementation plan and scientific decisions.
- [`Analysis-Aims.md`](Analysis-Aims.md) - estimands, cohorts, and statistical methods.
- [`docs/brca_staged_extraction_and_evaluation.md`](docs/brca_staged_extraction_and_evaluation.md) -
  JSON schemas, prompt requirements, golden cases, and evaluation rubric.
- [`notebooks/`](notebooks/) - final, numbered notebook deliverables.
- [`docs/tcga_pancan_data_enrichment.md`](docs/tcga_pancan_data_enrichment.md) -
  integration gates for clinical timeline/treatment, ancestry, 450K methylation, and
  tumor break load.
- [`schemas/`](schemas/) and [`eval/`](eval/) - JSON Schema contracts, golden cases,
  and deterministic evaluation scaffolding.
- [`STATUS.md`](STATUS.md) - accurate implementation checklist.
- [`docs/adr/`](docs/adr/) - immutable benchmark-governance records.

## Data and reproducibility

Use public, open-access TCGA data only. Each analysis must record source study,
snapshot date, eligibility criteria, cohort flow, mutation definition, pathway version,
missingness, and all exclusions. Outputs must include vector PDF and 600 DPI PNG
figures using an Okabe-Ito, grayscale-safe palette and annotate the relevant `n`.

The model-extraction stage must never write raw source records, prompts containing
patient-level content, or model outputs to the repository. See the extraction and
evaluation specification for the approved JSON-only artifacts.

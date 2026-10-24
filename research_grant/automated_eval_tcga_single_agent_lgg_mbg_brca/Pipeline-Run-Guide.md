# Pipeline run guide

Only the commands below are supported today. The end-to-end program is not yet
implemented.

## 1. LGG versus GBM mutation and pathway workflow

```zsh
Rscript "data collection and processing/compare_tcga_lgg_gbm.R" \
  --out-dir data/processed/tcga_lgg_vs_gbm
```

The script downloads GDC masked somatic MAF calls, selects the lexicographically first
sample-type-01 barcode per patient, filters to its listed non-silent classes, and keeps
eligible mutation-free patients in each cohort denominator. It writes selected samples,
clinical provenance, GDC manifest fields, Fisher-test gene and pathway tables, a run
provenance file, and R session information.

This workflow does not yet provide the planned prevalence-ratio confidence intervals,
correlations, regressions, notebook, or final figures.

## 2. BRCA public snapshot

```zsh
python "src/data collection and processing/pull_tcga_brca_cbioportal.py" \
  --out-dir data/raw/cbioportal \
  --preview-records 1
```

The script pulls patient and sample clinical tables, mutations, high-level CNA,
structural variants, and the clinical-attribute catalog from cBioPortal. It normalizes
and preserves the patient and sample long clinical arrays before duplicate-checked
`DataFrame.pivot` produces wide clinical arrays. It checks pagination and atomically
writes nine JSON record arrays plus `missingness_report.json`. `manifest.json` records
each dataset's exact request configuration, row and column counts, SHA-256 checksum,
and successful or failed retry metadata. A unique UTC timestamp and UUID make the final
snapshot directory non-overwriting; `--preview-records` prints zero through ten JSON
records per written dataset. Its strict decoder rejects duplicate keys and nonstandard
constants except `NaN`, which becomes `null`, and rejects exponent-overflow numbers; it
validates the Stage 0 report, records `reference_genome` in the manifest, and aborts
if the cBioPortal `importDate` changes during retrieval. It does not perform
clinical linkage,
brain-metastasis classification, JSON extraction, or inference.

For each Stage 0 report entry, `source_checksum` identifies canonical
pre-normalization records and
`source_representation: canonical_pre_normalization_records` distinguishes it from the
published normalized-file checksum in the manifest.

## 3. Stage supplied Aim 1 aggregate tables

`src/ingest/stage_aim1_result_tables.py` accepts exactly five supplied CSV tables:
`aim1_univariate_logistic`, `aim1_top10_gene_pq`, `aim1_pathway_pq`,
`aim1_multivariate_logistic`, and `aim1_gene_pathway_comparison`. See
[`Getting Started`](Getting-Started.md) for the complete command.

It requires each CSV header and filename suffix to match its named contract, requires
five distinct source files by filesystem identity, and rejects invalid numeric values,
invalid probability ranges, negative counts, and invalid `kind` values. It compares
device and inode so hard-linked inputs are rejected, with a resolved-path fallback when
an inode is unavailable. It atomically publishes JSON record arrays and `manifest.json`
to `data/processed/aim1/`, refusing to overwrite that local, gitignored directory.
Each array is validated against its named table-specific Draft 2020-12 JSON Schema, and
an intended empty array is valid. UUID-prefixed attachments are accepted when their
basenames end in the required logical table-name suffix. Cross-field checks require
counts no greater than denominators, positive odds ratios with ordered positive bounds,
and prevalence ratios within ordered nonnegative bounds. The stager recomputes
prevalences and requires reported prevalence and ratio values to match within `1e-12`;
zero numerator prevalence, ratio, and lower ratio bound remain valid, while zero
reference prevalence is rejected because its ratio is non-finite. The output stages
supplied aggregates and does not run an analysis.

## 4. Compare three extraction-model evaluations

`src/analysis/evaluate_extraction_model_accuracy.py` accepts exactly three comparable
JSON prediction payloads plus a separately supplied immutable golden JSON dataset. It
computes the golden SHA-256 and rejects source truth in predictions, then atomically
publishes `model_accuracy_summary.json`, overall-accuracy plots, and a stage-element
heatmap. Overall inference is case-level all-applicable-feature accuracy, while stage
and feature results are descriptive. The full input contract and command are in
[`docs/extraction_model_accuracy_evaluation.md`](docs/extraction_model_accuracy_evaluation.md).
This reporter does not implement extraction or generate its required payloads.

## 5. Stage 0 missingness normalization

`src/extraction/stage_missingness.py` is an implemented first stage for JSON record
arrays. It maps blank or whitespace-only strings and JSON `NaN` to `null`, retains
partly observed records, and drops only records null across every field. It atomically
writes normalized arrays and `missingness_report.json`, including a canonical
pre-normalization source checksum labelled
`source_representation: canonical_pre_normalization_records`. It has not yet processed
a BRCA source snapshot. `source_filename` is the actual input basename. It rejects
duplicate keys and nonstandard JSON and validates
the report against its strict Draft 2020-12 JSON Schema; numeric literals that become
non-finite through exponent overflow are rejected.

## 6. Planned stages

The remaining stages are deliberately not commands:

1. Build and validate the staged BRCA JSON extractor.
2. Define and audit brain-metastasis-ever status.
3. Implement BRCA prevalence, regression, and survival analyses.
4. Implement the BRCA brain-metastasis versus GBM comparison.

Their intended methods and acceptance criteria are in `PLAN.md`, `Analysis-Aims.md`,
and `docs/brca_staged_extraction_and_evaluation.md`. Do not follow commands in older
GENIE/MSK documentation as if they execute these stages.

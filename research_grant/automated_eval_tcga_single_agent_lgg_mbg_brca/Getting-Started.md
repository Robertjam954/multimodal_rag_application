# Getting started

The active program has four runnable acquisition, staging, or reporting workflows and four unexecuted
notebook scaffolds. Start with [`PLAN.md`](PLAN.md) and do not treat legacy GENIE/MSK
scripts as the active pipeline.

## Python

Use Python 3.11 or later, as declared in `pyproject.toml`.

```zsh
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python "src/data collection and processing/pull_tcga_brca_cbioportal.py" \
  --out-dir data/raw/cbioportal \
  --preview-records 1
```

The pull accesses the public cBioPortal study
`brca_tcga_pan_can_atlas_2018`. It atomically publishes a unique UTC timestamp and UUID
directory containing nine JSON record arrays, `missingness_report.json`, and
`manifest.json` under gitignored `data/raw/cbioportal/`. The two normalized long
clinical arrays are preserved before duplicate-checked `DataFrame.pivot` creates the
wide arrays. The manifest records exact requests, successful and failed retry metadata,
dimensions, and checksums; `--preview-records` accepts 0 through 10. The response
decoder rejects duplicate keys and nonstandard constants except `NaN`, which becomes
`null`, and rejects exponent-overflow numbers; the pull validates its Stage 0 report,
records the study `reference_genome` in the manifest, and aborts if cBioPortal
`importDate` changes during retrieval. It is not a BRCA analytic dataset or a
structured-extraction implementation.

## Supplied Aim 1 aggregate tables

The following command stages five supplied CSV aggregate tables as validated JSON
arrays. Replace each placeholder with an existing supplied file whose filename ends in
the required table name. Do not copy or commit source attachments.

```zsh
python src/ingest/stage_aim1_result_tables.py \
  --input-file aim1_univariate_logistic=/path/aim1_univariate_logistic.csv \
  --input-file aim1_top10_gene_pq=/path/aim1_top10_gene_pq.csv \
  --input-file aim1_pathway_pq=/path/aim1_pathway_pq.csv \
  --input-file aim1_multivariate_logistic=/path/aim1_multivariate_logistic.csv \
  --input-file aim1_gene_pathway_comparison=/path/aim1_gene_pathway_comparison.csv \
  --out-dir data/processed/aim1
```

The output directory is gitignored and must not already exist. It contains five JSON
record arrays and a checksum manifest. Each table input must be a distinct filesystem
file: hard-linked copies are rejected by device and inode identity, with a resolved-path
fallback when an inode is unavailable. Each array is validated against its named
table-specific Draft 2020-12 JSON Schema, and an intended empty array is valid. This is
a local staging result of supplied aggregates, not an analysis run. A UUID-prefixed
attachment is accepted when its basename ends in the required logical table-name
suffix. Records must also satisfy count-versus-denominator, positive odds-ratio, and
ordered odds-ratio or prevalence-ratio bound checks. The stager recomputes prevalence
and requires reported prevalence and ratio values to match within `1e-12`; zero
numerator prevalence, ratio, and lower ratio bound are allowed, but zero reference
prevalence is rejected because it has no finite JSON ratio.

## Extraction-model accuracy comparison

`src/analysis/evaluate_extraction_model_accuracy.py` is a reporting utility for three
already-created, comparable JSON prediction payloads plus one immutable golden JSON
dataset. It calculates the golden file hash and rejects source truth in predictions. It
does not create those inputs or extract BRCA records. Its required input contract and
command are in
[`docs/extraction_model_accuracy_evaluation.md`](docs/extraction_model_accuracy_evaluation.md).

## Stage 0 missingness normalization

`src/extraction/stage_missingness.py` is the first BRCA extraction stage. It accepts
one or more JSON record arrays and atomically writes normalized JSON arrays plus
`missingness_report.json`. Blank or whitespace-only strings and JSON `NaN` become
`null`; only records null across every field are dropped. It has not yet been run on a
BRCA snapshot. It rejects duplicate keys and nonstandard JSON and validates its report
with strict Draft 2020-12 JSON Schema; numeric literals that become non-finite through
exponent overflow are rejected. It records the schema-required
`source_representation: canonical_pre_normalization_records` and canonical source
checksum before atomically publishing output; `source_filename` is the actual input
basename. See
`docs/brca_staged_extraction_and_evaluation.md` for the contract.

## R

Install R packages `TCGAbiolinks`, `dplyr`, `jsonlite`, `readr`, `rlang`, and `tidyr`.
They are listed as comments in `requirements.txt` because they are not pip packages.
Then run:

```zsh
Rscript "data collection and processing/compare_tcga_lgg_gbm.R" \
  --out-dir data/processed/tcga_lgg_vs_gbm
```

Use `--min-prevalence <integer>` to change the gene-test inclusion threshold and
`--gdc-cache-dir <directory>` to place downloaded GDC files elsewhere. Preserve these
arguments and generated provenance files with the result.

## Before planned analyses

Do not execute a notebook as an analysis until its code exists. Before implementing
EDA or BRCA endpoints, freeze and record the source snapshot, primary-sample rule,
mutation filter, pathway map, thresholds, missingness audit, and join diagnostics.
The planned BRCA JSON contract is in
[`docs/brca_staged_extraction_and_evaluation.md`](docs/brca_staged_extraction_and_evaluation.md).

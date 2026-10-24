---
title: Dataset metadata - TCGA BRCA source snapshot
version: 0.1
date_created: 2026-09-02
last_updated: 2026-09-02
owner: Robertjam954
status: source-pull schema defined; counts pending first archived pull
---

# Dataset metadata

Provenance card for every dataset in this repo. Modeled on
`llm_summarization_br_ca/docs/dataset_metadata.md`.

**Fields marked `<auto>` are written by the implemented cBioPortal pull, not by hand.**
They are deliberately empty until the first archived pull so that no number in this
repository is a guess.

---

## 1. Primary source

| Field | Value |
|---|---|
| Source | cBioPortal public REST API |
| Base URL | `https://www.cbioportal.org/api` |
| Study id | `brca_tcga_pan_can_atlas_2018` |
| Study name | Breast Invasive Carcinoma (TCGA, PanCancer Atlas) |
| Access | Public, no authentication |
| Snapshot ID and retrieval time | `<auto>` - unique UTC timestamp plus UUID and ISO-8601 timestamp in `manifest.json` |
| API response hash | `<auto>` - per-file sha256 values in `manifest.json` |
| Cache location | `data/raw/cbioportal/` (gitignored) |

**Why a snapshot hash.** cBioPortal studies are revised. ADR-0003 forbids comparing runs
built on different corpora, and the hash is how a corpus change is detected rather than
assumed absent.

## 2. Snapshot artifacts

| Table | Endpoint | Grain | Rows `<auto>` | Notes |
|---|---|---|---|---|
| `clinical_patient_long.json` | `/studies/{id}/clinical-data?clinicalDataType=PATIENT` | one record per patient and clinical attribute | `<auto>` | Stage 0-normalized clinical records retained before pivot |
| `clinical_sample_long.json` | `/studies/{id}/clinical-data?clinicalDataType=SAMPLE` | one record per patient, sample, and clinical attribute | `<auto>` | Stage 0-normalized clinical records retained before pivot |
| `clinical_patient.json` | local `DataFrame.pivot` of patient long records | one row per patient | `<auto>` | pivot requires no duplicate patient and attribute key |
| `clinical_sample.json` | local `DataFrame.pivot` of sample long records | one row per patient and sample | `<auto>` | pivot requires no duplicate patient, sample, and attribute key |
| `clinical_merged.json` | local left join of clinical tables | one row per patient and sample | `<auto>` | pull checks that the join preserves sample rows |
| `clinical_attributes.json` | `/studies/{id}/clinical-attributes` | one row per clinical attribute | `<auto>` | catalog used to verify TBL and other attribute availability |
| `mutations.json` | `/molecular-profiles/{id}_mutations/mutations/fetch` | one row per variant | `<auto>` | detailed mutation response |
| `cna.json` | `/molecular-profiles/{id}_gistic/discrete-copy-number/fetch` | one row per gene x sample | `<auto>` | high-level amp and deep-deletion calls |
| `structural_variants.json` | `/structural-variant/fetch` | one row per structural variant | `<auto>` | public API response |
| `missingness_report.json` | local Stage 0 normalization | one dataset report for nine arrays | `<auto>` | input, retained, dropped, field-level missingness, and canonical pre-normalization source checksum before row drop |

The manifest additionally records exact retrieval or local-transform configuration,
SHA-256 checksums, and successful or failed retry metadata. The pull does not
harmonize fields, create endpoints, or classify brain metastasis. Its strict response
decoder rejects duplicate object keys, normalizes `NaN` to `null`, rejects other
nonstandard constants and exponent-overflow numbers, and aborts if the study
`importDate` differs between the start and end metadata requests. The manifest records
the API study's `reference_genome`.

Each pull report dataset entry labels `source_checksum` with
`source_representation: canonical_pre_normalization_records`. This identifies the
canonical JSON record representation before Stage 0 normalization and is distinct from
the checksum of the normalized file published in the manifest.

## 3. Planned derived records

| Artifact | Produced by | Grain |
|---|---|---|
| Evidence-linked staged JSON record | **(target)** BRCA extraction implementation | one record per linked patient and selected sample |
| BRCA analytic tables | **(target)** analysis notebooks | defined when extraction and cohort rules are finalized |

No `src/ingest/build_cohort.py`, processed parquet table, driver-gene analysis, or
retrieval-card renderer exists in this repository today.

## 4. Column dictionary

**(target)** The staged extractor will document source fields, normalization, allowed
states, null counts, and evidence references. The approved target contract is
`docs/brca_staged_extraction_and_evaluation.md`.

## 5. Missingness

`src/extraction/stage_missingness.py` implements the first JSON normalization step. It
converts blank or whitespace-only strings and JSON `NaN` to `null`, then drops only
records null across every field. It records a checksum of canonical pre-normalization
records with `source_representation: canonical_pre_normalization_records`, validates
the report, and atomically publishes normalized arrays. Its `source_filename` is the
actual input basename. No Stage 0 run on an archived BRCA snapshot exists yet.

**(target)** Join diagnostics and additional missingness analysis must run before BRCA
EDA:

- per-column null counts and percentages for every processed table
- a missingness pattern matrix (which columns are jointly missing)
- **merge diagnostics: row counts before and after every join**, so a silent
  many-to-many blowup or an inner-join drop is caught at the step that caused it

The Stage 0 report emits field-level missing counts and fractions before row dropping;
the broader audit and join diagnostics remain unimplemented.

## 6. Privacy and PHI

- **TCGA is public, already de-identified, controlled-access omics excluded.** Only the
  open-access clinical, mutation, and CNA tiers are pulled.
- **No GENIE or IMPACT patient-level data enters this repo.** The SHAP and driver-gene
  *methods* are ported from `genie_impact_tcga_brain_mets`; the data is not. This keeps
  the repo PHI-free and is enforced by `.claude/rules/security.md`.
- No de-identification step is required, because no identifiable data is ingested. If
  that ever changes, it is an ADR and the data-analysis-hygiene skill governs.
- `data/` is gitignored in its entirety. Nothing under it is ever committed.

## 7. Reproduction

```bash
python "src/data collection and processing/pull_tcga_brca_cbioportal.py" \
  --out-dir data/raw/cbioportal
```

Acceptance: the command creates a unique UTC timestamp-and-UUID directory containing
nine JSON record arrays, `missingness_report.json`, and `manifest.json`; the directory
is atomically published only after all writes complete. Long clinical records are
Stage 0-normalized before duplicate-checked pivots create the wide clinical arrays.
Each manifest entry records filename, JSON record orientation, row count, column count,
size, SHA-256 checksum, exact request or local-transform configuration, and retry
metadata. The pull validates the Stage 0 report schema and verifies unchanged
`importDate` before publication. `--preview-records` can print 0 through 10 records per
dataset. See
[`tcga_pancan_data_enrichment.md`](tcga_pancan_data_enrichment.md) for planned
timeline/treatment, ancestry, methylation, and TBL augmentation.

## 8. Lineage

The pull is implemented at
`src/data collection and processing/pull_tcga_brca_cbioportal.py`. Historical
GENIE-oriented harmonization material remains elsewhere in the repository but is not
the lineage or schema authority for this source snapshot.

# TCGA-BRCA PanCancer data enrichment

## Purpose

This document integrates four PanCancer data types into the planned TCGA-BRCA program:
clinical timeline/treatment, genetic ancestry, DNA methylation, and tumor break load
(TBL). It does not claim that any external source has been downloaded, transformed, or
joined. The source definitions are versioned in
`src/data collection and processing/tcga_brca_pancan_source_catalog.json`.

## Source inventory

| Data type | Source | Source file or attribute | Planned JSON artifact |
|---|---|---|---|
| Clinical timeline and treatment | GDAC Firehose | `Merge_Clinical.Level_1.20160128/clin.merged.txt` | `clinical_timeline_treatment.json` |
| Genetic ancestry | CCG-AIM-2020 | `Admixture_by_sample.txt` | `genetic_ancestry.json` |
| DNA methylation | GDC PanCancer | 450K beta-value matrix plus 450K probe metadata | `methylation_450k_feature_summary.json` |
| Tumor break load | cBioPortal clinical attributes | `Tumor Break Load`, if present | `tumor_break_load.json` |

The documented clinical and methylation transformations reference cBioPortal Datahub
pull request 1597. Transformation code must not be created until that reference and
the source payloads have been retrieved and the exact identifier mappings are recorded.

## JSON-native BRCA snapshots

`pull_tcga_brca_cbioportal.py` writes nine JSON record arrays: patient and sample
clinical long records, their Stage 0-normalized and duplicate-checked wide pivots,
merged clinical, the clinical-attribute catalog, mutation, CNA, and
structural-variant datasets. It also writes `missingness_report.json`.
`manifest.json` records each filename, JSON orientation, dimensions, byte size,
SHA-256 checksum, retrieval time, canonical request or local-transform configuration,
and successful or failed retry metadata. Snapshot directories use a unique UTC
timestamp-and-random-suffix identifier and are published atomically only after every
file, the missingness report, and the manifest are complete.

The response decoder rejects duplicate object keys, normalizes `NaN` to `null`, and
rejects other nonstandard constants and exponent-overflow numbers. The pull validates
the Stage 0 report schema, records the API study `reference_genome` in its manifest,
and requires the cBioPortal `importDate` read at the end of retrieval to match the
value at the start, preventing a mixed-version snapshot.

Each Stage 0 report entry includes
`source_representation: canonical_pre_normalization_records` and a corresponding
SHA-256 `source_checksum`.
This identifies canonical records before normalization, separately from the normalized
file checksum recorded in the manifest.

Use the optional, bounded `--preview-records N` argument only when an interactive
inspection is appropriate. `N` is limited to 10 records per dataset. It prints each
written dataset in valid JSON:

```json
{
  "dataset": "clinical_attributes",
  "records": [
    {
      "clinicalAttributeId": "EXAMPLE_ATTRIBUTE",
      "displayName": "Example attribute"
    }
  ]
}
```

The preview contains source records and must not be copied into committed Markdown,
notebooks, logs, or generated golden datasets.

## Integration gates

All four sources must pass these gates before they enter the staged extraction input:

1. Archive the raw source payload under gitignored `data/raw/` and record its checksum,
   retrieval date, source URL, and source-file version in JSON.
2. Validate the join grain and barcode mapping. Record patient- and sample-level row
   counts before and after the join, unmatched records, duplicate keys, and exclusions.
3. Preserve missingness and ambiguous linkage. Never convert a missing source record
   into an absent treatment, ancestry value, methylation state, or TBL score.
4. Produce a normalized JSON artifact with source IDs, original-field references,
   transformation version, and data-quality warnings.
5. Add the artifact to Stage 1 inventory of the staged extractor only after its schema
   and validators have been added to the golden dataset.

## Data-specific handling

### Timeline and treatment

Extract only variables with an auditable transformation rule. Preserve original dates
and dates relative to diagnosis separately. Derive time-to-event values only after
chronology validation. Treatment unknown, no documented treatment, and conflicting
treatment records remain distinct statuses.

### Genetic ancestry

Retain the complete named admixture-component vector with its source sample ID. Do not
assign a discrete ancestry label unless a documented, prespecified rule requires one.
Check that component values fall within the documented range and satisfy the expected
total within a declared numeric tolerance.

### DNA methylation

The 450K beta-value matrix is too high-dimensional to pass wholesale to an LLM or to
use as an unplanned patient-level predictor. Retain the source matrix separately and
construct a JSON feature summary only after specifying the probe annotation version,
probe-quality filters, sample barcode harmonization, and a biological or statistical
feature-reduction rule. The selected feature set and thresholds are benchmark-frozen
once analysis begins.

### Tumor break load

TBL may be available as a cBioPortal sample-level clinical attribute. The JSON snapshot
includes `clinical_attributes.json` specifically to establish its exact attribute ID,
type, and coverage. Do not substitute a similarly named variable or calculate a proxy
without a separate documented method and validation plan.

## Effect on planned analyses

Timeline/treatment can improve endpoint derivation and confounding assessment.
Ancestry can be reported in descriptive tables and considered only with an explicit
scientific rationale. Methylation and TBL are exploratory covariates until their
availability, missingness, and sample overlap are established. Their use must not
silently alter the preplanned mutation/pathway prevalence or top-five survival analyses.

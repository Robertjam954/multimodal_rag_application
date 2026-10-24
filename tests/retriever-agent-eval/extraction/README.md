# Staged JSON extraction

This package will contain the planned TCGA-BRCA staged extraction implementation:
Pydantic models, bounded stage runners, evidence preservation, and schema validation.

All persisted inputs, handoffs, outputs, and failure records must be JSON. Batch
processing may use JSON Lines with one complete schema-valid record per line.

`stage_missingness.py` is the implemented Stage 0 normalizer. It converts blank
strings and JSON `NaN` to `null`, retains partially missing records, drops only
all-null rows, and writes JSON normalized datasets plus a missingness report. It
rejects duplicate keys and nonstandard JSON and validates the report against strict
Draft 2020-12 JSON Schema with `jsonschema==4.26.0`.

# JSON schemas

This directory will hold generated Pydantic JSON Schema artifacts and their version
manifest for the staged BRCA extraction contract. Schemas are generated from code,
checked against the golden cases, and never maintained as a competing hand-written
definition.

Schema contents contain no patient-level data and may be version controlled.

`aim1_result_tables.schema.json` is the approved static JSON contract for the five
existing Aim 1 analytic result-table layouts. The staging utility at
`src/ingest/stage_aim1_result_tables.py` rejects CSV inputs whose headers differ from
that contract and writes JSON record arrays with the same field names and numeric types.
It validates the named table-specific numeric, probability, nonnegative-count, and
allowed-category constraints before publishing; it does not rely on an ambiguous
root-level schema branch. Cross-field validation requires counts no greater than their
denominators, positive odds ratios with ordered positive confidence bounds, and
prevalence ratios within ordered nonnegative bounds. The stager recomputes each
prevalence from its mutation count and denominator, then requires reported prevalence
and ratio values to match within an absolute and relative tolerance of `1e-12`. Zero
numerator prevalence, ratio, and lower ratio bound are valid. A zero reference
prevalence is rejected because it would require a non-finite JSON ratio. Source
filenames must end with the matching canonical logical table-name suffix, so
UUID-prefixed attachments are valid, and all five source files must be distinct by
filesystem identity rather than only by path. It compares device and inode and falls
back to the resolved path only when an inode is unavailable, so hard-linked source CSVs
are rejected. The manifest identifies which of the five table contracts produced each
array. Each named array schema intentionally permits an empty array when that supplied
table has no rows.

The three-model extraction-comparison protocol also has strict, versioned contracts:

- `extraction_golden_numeric_checks.schema.json` - immutable source truth.
- `extraction_model_predictions.schema.json` - one model's prediction payload.
- `extraction_model_comparison.schema.json` - generated pre-benchmark summary.
- `missingness_stage.schema.json` - mandatory Stage 0 normalization report.

The evaluator computes the golden-file hash rather than trusting a model-provided
truth record. `stage_missingness.py` and
`evaluate_extraction_model_accuracy.py` use `jsonschema==4.26.0` to validate their
respective report, golden input, prediction payload, and generated summary against
these strict Draft 2020-12 schemas before publication. Their JSON readers reject
duplicate object keys, nonstandard constants, and numeric literals that become
non-finite through exponent overflow. See
`docs/extraction_model_accuracy_evaluation.md`.

The cBioPortal BRCA pull also validates its generated Stage 0 report with
`missingness_stage.schema.json`; its response decoder rejects duplicate keys, maps
`NaN` to `null`, and rejects other nonstandard constants and exponent-overflow numbers.
Every report dataset entry requires
`source_representation: canonical_pre_normalization_records` and a SHA-256
`source_checksum`, separating source identity from the normalized-file checksum in the
manifest. `stage_missingness.py` and the cBioPortal pull both emit this required
provenance before report validation and publication.

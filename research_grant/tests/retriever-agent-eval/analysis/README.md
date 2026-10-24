# Analysis

Place reusable analysis functions here after their notebook logic is stable. Functions
must receive validated, versioned analytic inputs and return typed results without
performing network access or reading machine-specific paths.

`evaluate_extraction_model_accuracy.py` is implemented here. It compares exactly three
JSON prediction payloads against a separately supplied immutable golden JSON dataset,
computes the golden SHA-256 digest, and rejects source truth in predictions. It reports
case-level all-applicable-feature accuracy with Agresti-Coull intervals and exactly
three BH-adjusted overall McNemar tests. Stage and feature results are descriptive. It
uses strict Draft 2020-12 JSON Schema validation and rejects duplicate keys and
nonstandard JSON. It atomically writes a JSON summary plus PDF and 600 DPI PNG figures.
It is a downstream reporter, not a BRCA extraction implementation.

Once implemented, the final notebooks will call this package for LGG/GBM EDA, BRCA
brain-metastasis and survival analysis, and the BRCA brain-metastasis versus GBM
comparison.

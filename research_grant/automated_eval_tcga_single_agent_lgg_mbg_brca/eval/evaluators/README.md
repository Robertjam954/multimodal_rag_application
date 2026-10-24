# Code-based evaluators

Place deterministic Pydantic Evals adapters and custom checks here. They validate JSON
against the stage models and exact-match expected numeric features at each analytic
stage. Evaluators must produce JSON per-feature results and stage and overall accuracy
summaries.

LLM-as-judge evaluation is out of scope for the staged extraction pipeline.

`src/analysis/evaluate_extraction_model_accuracy.py` compares exactly three prediction
payloads against one immutable golden JSON source of source-confirmed numeric checks.
It computes the golden SHA-256 and rejects truth fields in predictions. It reports
Agresti-Coull confidence intervals and exactly three BH-adjusted overall case-level
McNemar tests in JSON; stage and feature results are descriptive. It writes a
model-accuracy interval plot plus a stage-element accuracy heatmap. It validates
golden input, predictions, and the generated summary against strict Draft 2020-12
schemas using `jsonschema==4.26.0`, and rejects duplicate keys and nonstandard JSON.
See
[`docs/extraction_model_accuracy_evaluation.md`](../../docs/extraction_model_accuracy_evaluation.md).

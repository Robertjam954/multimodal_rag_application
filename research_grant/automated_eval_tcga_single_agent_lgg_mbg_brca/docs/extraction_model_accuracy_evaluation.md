# Three-model extraction accuracy evaluation

## Purpose and boundary

This is a pre-benchmark, code-based comparison of exactly three LLM models on staged
BRCA numeric extraction. It is not a benchmark run and does not replace the future
run-store integration required by ADR-0005. The runner writes local JSON and figures
for method development; results can enter the benchmark only after per-model records
and artifacts are written through the benchmark data layer.

`src/analysis/evaluate_extraction_model_accuracy.py` uses one immutable, adjudicated
golden JSON dataset plus three model-prediction JSON payloads. It never accepts source
truth from a model payload.

## JSON inputs

The golden file must conform to
`schemas/extraction_golden_numeric_checks.schema.json`:

```json
{
  "schema_version": "brca_extraction_golden_numeric_checks.v1",
  "checks": [
    {
      "case_id": "inventory-complete-001",
      "stage": "inventory",
      "element": "available_field_count",
      "source_present": true,
      "expected_value": 18
    }
  ]
}
```

The runner calculates its SHA-256 digest. Each model-prediction file must conform to
`schemas/extraction_model_predictions.schema.json`, cite that computed digest, and
provide exactly one prediction for every golden check:

```json
{
  "schema_version": "brca_extraction_model_predictions.v1",
  "model_id": "model_a",
  "golden_dataset_hash": "sha256:<computed-golden-digest>",
  "predictions": [
    {
      "case_id": "inventory-complete-001",
      "stage": "inventory",
      "element": "available_field_count",
      "actual_value": 18
    }
  ]
}
```

The runner rejects duplicate JSON object keys, unknown JSON fields, nonstandard JSON
numeric constants, numeric literals that become non-finite through exponent overflow,
missing or extra predictions, inconsistent model IDs, and a hash mismatch. It uses
`jsonschema==4.26.0` Draft 2020-12 validation for the immutable golden input,
prediction payloads, and generated strict summary before publication.
It records the computed golden digest and each model-payload digest in the summary.
Model inputs cannot provide `source_present` or `expected_value`.

## Accuracy and independent unit

A numeric feature is source-confirmed only when its golden record has
`source_present: true`. Source-absent checks have a null expected value and are
excluded from every accuracy denominator.

Feature-level accuracy is reported descriptively:

```text
feature accuracy = count(source_present AND actual_value == expected_value)
                   / count(source_present)
```

Features in the same case are clustered, often from one model invocation. Therefore,
the inferential overall metric uses one independent binary outcome per case:

```text
case accuracy = count(cases where every applicable numeric feature exactly matches)
                / count(cases with at least one source-confirmed numeric feature)
```

Stage and stage-element accuracy are descriptive only, because their features and
outputs remain clustered within cases. Only overall case accuracy uses a two-sided 95%
Agresti-Coull confidence interval from
`statsmodels.stats.proportion.proportion_confint(method="agresti_coull")`.

## Paired comparison

Each model evaluates the same cases, so the three overall case-accuracy comparisons are
paired. The runner calculates one McNemar test for each model pair, using exact
binomial McNemar when fewer than 25 cases are discordant and the chi-squared
approximation otherwise. Benjamini-Hochberg correction covers these three prespecified
overall hypotheses only.

## Outputs and plots

The runner atomically creates a previously nonexistent output directory:

| Artifact | Contents |
|---|---|
| `model_accuracy_summary.json` | strict v2 summary, source/input digests, descriptive stage/feature accuracy, case-level accuracy with CIs, and three paired tests |
| `overall_accuracy_by_model.pdf` and `.png` | all-features-exact case accuracy and 95% Agresti-Coull intervals |
| `stage_element_accuracy_heatmap.pdf` and `.png` | descriptive exact-match feature accuracy and successes/denominator by stage, element, and model |

PDF figures are vector and PNG figures are 600 DPI. The stage-element heatmap uses a
luminance-monotone five-bin scale of black, Okabe-Ito blue, green, yellow, and white,
with white cell labels below 0.4 accuracy and black labels otherwise. The summary conforms to
`schemas/extraction_model_comparison.schema.json`.

```zsh
python src/analysis/evaluate_extraction_model_accuracy.py \
  --golden-dataset data/processed/evals/golden_numeric_checks.json \
  --model-evaluation model_a=data/processed/evals/model_a.json \
  --model-evaluation model_b=data/processed/evals/model_b.json \
  --model-evaluation model_c=data/processed/evals/model_c.json \
  --out-dir data/processed/extraction_model_comparison
```

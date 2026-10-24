# BRCA staged structured extraction and evaluation

## Purpose

This specification defines the planned TCGA-BRCA extraction task for an LLM. It turns
public source records into a validated JSON analytic record suitable for downstream
brain-metastasis, mutation, and survival analyses. It is a design document, not an
implemented extractor.

The design uses Instructor with Pydantic response models for staged schema validation.
Evaluation follows the Pydantic Evals model of typed `Dataset` and `Case` objects with
code-based, deterministic evaluators. Reference:
[Pydantic Evals](https://pydantic.dev/docs/ai/evals/evals/),
[dataset management](https://pydantic.dev/docs/ai/evals/how-to/dataset-management/).

## Input and output boundary

Inputs are de-identified public TCGA records. Each extraction call receives a bounded
JSON object containing only the source fields needed for its stage. Outputs are valid
JSON conforming to the stage schema. Neither raw records nor model-generated
patient-level JSON may be committed under version control.

## JSON-first artifact rule

All planned BRCA staged-extraction artifacts are JSON-first:

- Inputs, normalized stage inputs, and inter-stage handoffs are JSON objects.
- Each stage output and final analytic record is a JSON object validated by its Pydantic
  model.
- Golden inputs, expected outputs, case metadata, and expected numeric features are
  JSON.
- Evaluation results, including per-case, per-stage, per-feature results and summary
  accuracy, are JSON.
- Each generated Pydantic JSON Schema and schema manifest is JSON, generated from the
  model rather than maintained as a Markdown schema or an ad hoc Python object.

When batching is necessary, use JSON Lines (`.jsonl`) only: one complete JSON object per
line, with no CSV conversion or mixed record formats. A typed Pydantic Evals `Dataset`
or `Case` may exist in memory during execution, but its persisted input, expected value,
and report artifacts must be JSON or JSON Lines. Do not use CSV, Markdown tables, or
unstructured Python dictionaries as planned extraction data interchange or persisted
evaluation artifacts.

This rule applies only to the planned BRCA staged-extraction implementation. It does
not change the existing R LGG/GBM workflow, the BRCA cBioPortal snapshot pull, or other
retained analysis scripts.

Every extracted field must include:

- `value`: typed value or `null`;
- `status`: `observed`, `not_recorded`, `ambiguous`, or `conflicting`;
- `evidence`: zero or more source identifiers and source-field paths;
- `normalization_note`: omitted when no transformation was applied.

`not_recorded` is never equivalent to `false`, `no`, or `0`.

## Stage 0 - missingness normalization

Missingness is the first staged dataset, before source inventory or any extraction.
`src/extraction/stage_missingness.py` creates normalized JSON arrays and
`missingness_report.json`. It records the required
`source_representation: canonical_pre_normalization_records` and a canonical
pre-normalization source checksum separately from normalized output identity before
validating and atomically publishing its artifacts. `source_filename` is the actual
input basename. The implemented normalization rules are:

- A blank or whitespace-only string is missing and becomes JSON `null`.
- A JSON `NaN` constant is missing and becomes JSON `null`. `Infinity` and
  `-Infinity`, and numeric literals that become non-finite through exponent overflow,
  are rejected.
- Existing JSON `null` remains `null`.
- A record is dropped only when every field is `null` after normalization.
- A record with one or more observed values is retained, even when every other field
  is `null`. Empty containers are not converted to null.

The report records input, retained, and wholly-missing dropped row counts plus
field-level missing counts and fractions before row dropping. This report is a required
Stage 0 input to every later stage and a required numeric dataset for evaluation.
`stage_missingness.py` rejects duplicate JSON object keys and nonstandard constants,
and validates the report against `schemas/missingness_stage.schema.json` using
`jsonschema==4.26.0` Draft 2020-12 validation.

## Stages and schemas

| Stage | Input | Required output | Gate before next stage |
|---|---|---|---|
| 0. Missingness | source JSON record arrays | normalized source arrays and missingness report | blanks/NaNs are null; only all-null rows are dropped |
| 1. Inventory | Stage 0 normalized payload and report | source system, record IDs, available fields, data quality warnings | all evidence references resolve to supplied IDs |
| 2. Linkage | inventory and identifier fields | patient ID, selected primary sample ID, linkage confidence | exactly one patient and at most one analysis sample |
| 3. Clinical timeline | linked clinical fields | diagnosis, recurrence, brain-metastasis status, dates/times, survival status | no derived event without supporting evidence |
| 4. Molecular profile | selected-sample mutation fields | non-silent genes, mutation classes, pathway indicators, filter audit | symbols normalized and duplicate gene events collapsed per rule |
| 5. Analytic record | validated outputs from stages 0-4 | brain-metastasis cohort flag, outcomes, covariates, unresolved issues | cross-field validation and complete provenance |

Illustrative Stage 3 response shape:

```json
{
  "patient_id": "TCGA-XX-0001",
  "brain_metastasis_ever": {
    "value": null,
    "status": "not_recorded",
    "evidence": [],
    "normalization_note": null
  },
  "diagnosis_date": {
    "value": "2012-03-01",
    "status": "observed",
    "evidence": [{"source_id": "clinical_patient", "field": "DIAGNOSIS_DATE"}],
    "normalization_note": "Converted ISO-8601 date."
  }
}
```

## Pydantic model requirements

- Model categorical states with `Literal` or `Enum`, not unconstrained strings.
- Use nested evidence models and `Field` descriptions that define the extraction rule.
- Use field validators for formats and ranges, then model validators for chronology:
  diagnosis cannot follow recurrence, metastasis cannot precede diagnosis, and death
  cannot precede diagnosis.
- Make unknownable clinical fields nullable. Do not make `Optional` fields silently
  default to a clinical negative.
- Keep the mutation-filter and pathway-map versions as explicit fields in the final
  record.
- Bound Instructor retries. A failed validation is an observed extraction failure,
  retained in the evaluation output rather than silently discarded.

## Prompt contract

The implementation will place prompt text in versioned files, not Python string
literals. Each stage prompt must:

1. Name the input schema and output schema.
2. Require JSON only through the Instructor `response_model`.
3. Instruct the model to extract only supplied evidence.
4. Require `not_recorded`, `ambiguous`, or `conflicting` instead of guessing.
5. Require an evidence item for every observed or derived claim.
6. State the stage-specific normalization and temporal rules.
7. Prohibit clinical interpretation beyond the stated extraction task.

The final prompt version, model ID, temperature, retry limit, Pydantic schema hash,
and source snapshot hash are recorded with each evaluation run.

## Golden dataset

Create a manually adjudicated JSON dataset with `Case` records covering:

| Case category | Required behavior |
|---|---|
| Straightforward positive | extract explicit brain metastasis and linked mutation evidence |
| Explicit negative | preserve an explicitly documented absence |
| Missing field | output `not_recorded`, not negative |
| Conflicting source records | output `conflicting` and retain both evidence references |
| Ambiguous chronology | output `ambiguous` and do not derive a duration |
| Multiple samples | select only the prespecified primary sample or flag ambiguity |
| Synonymous/non-silent mix | apply the documented mutation filter |
| Gene synonym | normalize only with an approved mapping and record it |
| Pathway boundary | correctly assign a gene using the frozen pathway map |
| Invalid output pressure | reject unsupported content rather than fabricating data |

Golden expected outputs contain the adjudicated JSON record and case metadata:
source snapshot, stage, difficulty, feature category, and expected validation outcome.
Store individual cases as JSON or, for a batched dataset, JSON Lines. Version the
dataset as an immutable benchmark artifact after owner review.

## Code-based evaluation

Implement each stage's adjudicated inputs and expected output as a typed Pydantic Evals
`Case` in a typed `Dataset`. The evaluator must serialize the candidate output to JSON,
validate that JSON against the stage Pydantic schema, then evaluate the validated typed
object. Invalid JSON or a schema-validation failure is a failed case, not a value to
repair or judge.

Use built-in code-based evaluators, including `IsInstance` for the validated stage
model and `EqualsExpected` for expected values. Add deterministic checks for required
evidence, IDs, enum and range constraints, chronology, mutation filtering, and pathway
assignment. Score nullable and status fields independently so a guessed negative cannot
receive partial credit.

At every major analytic stage, exact-match the following expected numeric features for
each case in that stage's dataset:

| Stage | Exact-match numeric features |
|---|---|
| 0. Missingness | input-record count, retained-record count, all-columns-missing rows dropped, and per-field missing counts |
| 1. Inventory | supplied-record count and available-field count |
| 2. Linkage | linked-patient count and selected-analysis-sample count |
| 3. Clinical timeline | diagnosis, recurrence, and brain-metastasis event counts; valid derived-duration count |
| 4. Molecular profile | retained non-silent event count, distinct mutated-gene count, and positive pathway-indicator count |
| 5. Analytic record | confirmed-positive, confirmed-negative, unknown, ambiguous, and conflicting brain-metastasis counts; eligible outcome count |

The golden case declares the exact expected value for every applicable feature. Use
`EqualsExpected` for each value, without numeric tolerance unless a later version
explicitly defines one. The implementation records per-case, per-stage, and per-feature
pass/fail results. Feature-level accuracy is reported descriptively by stage and
element. Overall inference uses the case-level all-applicable-features-exact accuracy
defined in
[`extraction_model_accuracy_evaluation.md`](extraction_model_accuracy_evaluation.md),
which prevents correlated checks from the same case being treated as independent.

Persist the evaluator's per-feature results and accuracy summaries as JSON, or JSON
Lines for a batched case report. Do not emit CSV score tables or Markdown evaluation
reports as the evaluation artifact.

Evaluation is entirely code based. Do not use `LLMJudge`, a held-out judge model, or
free-text judge rationales for extraction scoring.

For the planned head-to-head comparison of exactly three models, use the paired
accuracy, Agresti-Coull interval, McNemar, and plotting contract in
[`extraction_model_accuracy_evaluation.md`](extraction_model_accuracy_evaluation.md).

## Promotion criteria

Before using the task in the benchmark, manually review every failure, add adversarial
golden cases for recurrent errors, set acceptance thresholds by field category, and
freeze the prompt, schemas, golden dataset, pathway map, and rubric version together.
Changing a frozen artifact requires a new version, an ADR, and reruns for every
comparison arm.

## Aim 1 analytic-result staging

The staged analytic-result files must preserve the supplied Aim 1 layouts exactly:
`aim1_univariate_logistic`, `aim1_top10_gene_pq`, `aim1_pathway_pq`,
`aim1_multivariate_logistic`, and `aim1_gene_pathway_comparison`. The approved columns
and numeric types are defined in `schemas/aim1_result_tables.schema.json`.

`src/ingest/stage_aim1_result_tables.py` accepts the source CSV tables only if each
header exactly matches its approved layout. It then writes JSON record arrays and a
checksum manifest under a caller-provided staged-data directory. It first writes to a
temporary sibling directory, then atomically publishes a previously nonexistent output
directory after all files succeed. It refuses overwrites. It prints a requested bounded
JSON preview of up to 10 records for each dataset while writing. This preserves the
analysis-table contract while making downstream staged records JSON-only. A
UUID-prefixed attachment is accepted when its basename ends in the logical table-name
suffix. The stager rejects mutation counts above their denominators, nonpositive odds
ratios, unordered odds-ratio bounds, and prevalence ratios outside ordered nonnegative
bounds. It recomputes both prevalences from mutation counts and denominators and
requires the reported prevalences and prevalence ratio to match within an absolute and
relative tolerance of `1e-12`. Zero numerator prevalence, prevalence ratio, and lower
ratio bound are valid; zero reference prevalence is rejected because the ratio would be
non-finite. Each named array schema intentionally permits an empty array.

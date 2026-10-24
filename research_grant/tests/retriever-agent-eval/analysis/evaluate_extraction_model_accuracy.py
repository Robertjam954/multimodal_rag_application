"""Compare case-level exact-match extraction accuracy across exactly three models.

The runner loads one immutable golden JSON dataset, then compares three JSON prediction
payloads against its source-confirmed numeric checks. It writes a JSON summary, an
overall-accuracy plot, and a stage-element accuracy heatmap.

Usage:
    python src/analysis/evaluate_extraction_model_accuracy.py \
        --golden-dataset /path/golden_numeric_checks.json \
        --model-evaluation model_a=/path/model_a_predictions.json \
        --model-evaluation model_b=/path/model_b_predictions.json \
        --model-evaluation model_c=/path/model_c_predictions.json \
        --out-dir data/processed/extraction_model_comparison
"""
from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import math
import shutil
import tempfile
from collections import defaultdict
from pathlib import Path
from typing import Any

import matplotlib.pyplot as plt
from matplotlib.colors import BoundaryNorm, ListedColormap
from jsonschema import Draft202012Validator
from jsonschema.exceptions import ValidationError
from statsmodels.stats.contingency_tables import mcnemar
from statsmodels.stats.multitest import multipletests
from statsmodels.stats.proportion import proportion_confint


MODEL_COUNT = 3
MAX_PREVIEW_RECORDS = 10
ALPHA = 0.05
MODEL_COLORS = ("#0072B2", "#E69F00", "#009E73")
GOLDEN_SCHEMA_VERSION = "brca_extraction_golden_numeric_checks.v1"
PREDICTION_SCHEMA_VERSION = "brca_extraction_model_predictions.v1"
SUMMARY_SCHEMA_VERSION = "brca_extraction_model_comparison.v2"
CheckKey = tuple[str, str, str]
GoldenCheck = dict[str, object]


def _parse_model_evaluation(value: str) -> tuple[str, Path]:
    """Parse a model identifier and JSON prediction-payload path."""
    model_id, separator, raw_path = value.partition("=")
    if separator != "=" or not model_id or not raw_path:
        raise argparse.ArgumentTypeError(
            "--model-evaluation must use MODEL_ID=/path/to/predictions.json"
        )
    return model_id, Path(raw_path)


def _reject_json_constant(value: str) -> None:
    """Reject nonstandard JSON numeric constants such as NaN and Infinity."""
    raise ValueError(f"Nonstandard JSON numeric constant is not allowed: {value}")


def _parse_finite_float(value: str) -> float:
    """Parse a JSON number only when it remains finite after conversion."""
    number = float(value)
    if not math.isfinite(number):
        raise ValueError(f"Non-finite JSON number is not allowed: {value}")
    return number


def _reject_duplicate_keys(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    """Reject duplicate JSON object members instead of retaining the final value."""
    value: dict[str, Any] = {}
    for key, item in pairs:
        if key in value:
            raise ValueError(f"Duplicate JSON object key: {key!r}")
        value[key] = item
    return value


def _validate_schema(value: Any, schema_name: str) -> None:
    """Validate JSON against a versioned Draft 2020-12 schema."""
    schema_path = Path(__file__).resolve().parents[2] / "schemas" / schema_name
    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    try:
        Draft202012Validator(schema).validate(value)
    except ValidationError as error:
        raise ValueError(f"{schema_name}: {error.message}") from error


def _read_json_object(path: Path) -> tuple[dict[str, Any], str]:
    """Read a strict JSON object and return its SHA-256 content digest."""
    raw = path.read_bytes()
    try:
        payload = json.loads(
            raw.decode("utf-8"),
            parse_constant=_reject_json_constant,
            parse_float=_parse_finite_float,
            object_pairs_hook=_reject_duplicate_keys,
        )
    except (UnicodeDecodeError, json.JSONDecodeError, ValueError) as error:
        raise ValueError(f"{path}: invalid strict JSON") from error
    if not isinstance(payload, dict):
        raise ValueError(f"{path}: payload must be a JSON object")
    return payload, f"sha256:{hashlib.sha256(raw).hexdigest()}"


def _is_finite_number(value: object) -> bool:
    """Return whether a JSON value is a finite numeric value, excluding booleans."""
    return isinstance(value, int | float) and not isinstance(value, bool) and math.isfinite(value)


def _check_exact_keys(
    payload: dict[str, Any], expected: set[str], path: Path
) -> None:
    """Reject unknown or missing payload fields rather than silently ignoring them."""
    actual = set(payload)
    if actual != expected:
        missing = sorted(expected - actual)
        unexpected = sorted(actual - expected)
        raise ValueError(f"{path}: missing fields {missing!r}; unexpected fields {unexpected!r}")


def _check_key(record: dict[str, Any], path: Path, index: int) -> CheckKey:
    """Validate the stable identifier for one numeric feature check."""
    case_id = record.get("case_id")
    stage = record.get("stage")
    element = record.get("element")
    if not all(isinstance(value, str) and value for value in (case_id, stage, element)):
        raise ValueError(f"{path}: record {index} requires nonempty case_id, stage, and element")
    return case_id, stage, element


def _load_golden_dataset(path: Path) -> tuple[dict[CheckKey, GoldenCheck], str]:
    """Load the immutable source-confirmed checks and compute their content hash."""
    payload, digest = _read_json_object(path)
    _validate_schema(payload, "extraction_golden_numeric_checks.schema.json")
    _check_exact_keys(payload, {"schema_version", "checks"}, path)
    if payload["schema_version"] != GOLDEN_SCHEMA_VERSION:
        raise ValueError(
            f"{path}: schema_version must be {GOLDEN_SCHEMA_VERSION!r}, "
            f"got {payload['schema_version']!r}"
        )
    raw_checks = payload["checks"]
    if not isinstance(raw_checks, list) or not raw_checks:
        raise ValueError(f"{path}: checks must be a nonempty JSON array")

    checks: dict[CheckKey, GoldenCheck] = {}
    for index, raw_check in enumerate(raw_checks):
        if not isinstance(raw_check, dict):
            raise ValueError(f"{path}: check {index} must be a JSON object")
        _check_exact_keys(
            raw_check,
            {"case_id", "stage", "element", "source_present", "expected_value"},
            path,
        )
        key = _check_key(raw_check, path, index)
        source_present = raw_check["source_present"]
        expected_value = raw_check["expected_value"]
        if not isinstance(source_present, bool):
            raise ValueError(f"{path}: check {index} source_present must be boolean")
        if source_present and not _is_finite_number(expected_value):
            raise ValueError(
                f"{path}: source-confirmed expected_value must be a finite number at {key!r}"
            )
        if not source_present and expected_value is not None:
            raise ValueError(
                f"{path}: source-absent expected_value must be null at {key!r}"
            )
        if key in checks:
            raise ValueError(f"{path}: duplicate golden check {key!r}")
        checks[key] = {
            "source_present": source_present,
            "expected_value": expected_value,
        }

    if not any(check["source_present"] is True for check in checks.values()):
        raise ValueError(f"{path}: at least one golden check must be source-confirmed")
    return checks, digest


def _load_predictions(
    path: Path, expected_model_id: str, golden_hash: str, golden_keys: set[CheckKey]
) -> tuple[dict[CheckKey, object], str]:
    """Load a model's predictions and bind them to the computed golden dataset hash."""
    payload, digest = _read_json_object(path)
    _validate_schema(payload, "extraction_model_predictions.schema.json")
    _check_exact_keys(payload, {"schema_version", "model_id", "golden_dataset_hash", "predictions"}, path)
    if payload["schema_version"] != PREDICTION_SCHEMA_VERSION:
        raise ValueError(
            f"{path}: schema_version must be {PREDICTION_SCHEMA_VERSION!r}, "
            f"got {payload['schema_version']!r}"
        )
    if payload["model_id"] != expected_model_id:
        raise ValueError(
            f"{path}: model_id {payload['model_id']!r} does not match "
            f"--model-evaluation {expected_model_id!r}"
        )
    if payload["golden_dataset_hash"] != golden_hash:
        raise ValueError(f"{path}: golden_dataset_hash does not match the computed golden hash")
    raw_predictions = payload["predictions"]
    if not isinstance(raw_predictions, list):
        raise ValueError(f"{path}: predictions must be a JSON array")

    predictions: dict[CheckKey, object] = {}
    for index, raw_prediction in enumerate(raw_predictions):
        if not isinstance(raw_prediction, dict):
            raise ValueError(f"{path}: prediction {index} must be a JSON object")
        _check_exact_keys(raw_prediction, {"case_id", "stage", "element", "actual_value"}, path)
        key = _check_key(raw_prediction, path, index)
        actual_value = raw_prediction["actual_value"]
        if actual_value is not None and not _is_finite_number(actual_value):
            raise ValueError(f"{path}: actual_value must be a finite number or null at {key!r}")
        if key in predictions:
            raise ValueError(f"{path}: duplicate prediction {key!r}")
        predictions[key] = actual_value

    prediction_keys = set(predictions)
    if prediction_keys != golden_keys:
        missing = sorted(golden_keys - prediction_keys)
        unexpected = sorted(prediction_keys - golden_keys)
        raise ValueError(f"{path}: missing predictions {missing!r}; extra predictions {unexpected!r}")
    return predictions, digest


def _accuracy_summary(model_id: str, correctness: list[bool]) -> dict[str, object]:
    """Calculate Agresti-Coull exact-match accuracy for independent paired units."""
    denominator = len(correctness)
    numerator = sum(correctness)
    lower, upper = proportion_confint(
        count=numerator,
        nobs=denominator,
        alpha=ALPHA,
        method="agresti_coull",
    )
    return {
        "model_id": model_id,
        "independent_units": denominator,
        "all_applicable_checks_exact": numerator,
        "accuracy": numerator / denominator,
        "ci_method": "agresti_coull",
        "ci_level": 1 - ALPHA,
        "ci_low": float(lower),
        "ci_high": float(upper),
    }


def _descriptive_feature_accuracy(model_id: str, correctness: list[bool]) -> dict[str, object]:
    """Calculate a descriptive feature-level accuracy without an independence claim."""
    denominator = len(correctness)
    numerator = sum(correctness)
    return {
        "model_id": model_id,
        "source_confirmed_features": denominator,
        "exact_matches": numerator,
        "accuracy": numerator / denominator,
    }


def _descriptive_case_accuracy(model_id: str, correctness: list[bool]) -> dict[str, object]:
    """Calculate case-level accuracy without an interval or hypothesis test."""
    denominator = len(correctness)
    numerator = sum(correctness)
    return {
        "model_id": model_id,
        "case_units": denominator,
        "all_applicable_checks_exact": numerator,
        "accuracy": numerator / denominator,
    }


def _mcnemar_result(
    model_a: str,
    model_b: str,
    correctness_a: list[bool],
    correctness_b: list[bool],
    scope: str,
    stage: str | None = None,
    element: str | None = None,
) -> dict[str, object]:
    """Calculate an exact or asymptotic paired McNemar comparison."""
    both_correct = sum(a and b for a, b in zip(correctness_a, correctness_b, strict=True))
    model_a_only = sum(a and not b for a, b in zip(correctness_a, correctness_b, strict=True))
    model_b_only = sum(not a and b for a, b in zip(correctness_a, correctness_b, strict=True))
    both_incorrect = sum(
        not a and not b for a, b in zip(correctness_a, correctness_b, strict=True)
    )
    discordant = model_a_only + model_b_only
    use_exact = discordant < 25
    result = mcnemar(
        [[both_correct, model_a_only], [model_b_only, both_incorrect]],
        exact=use_exact,
        correction=False,
    )
    return {
        "model_a": model_a,
        "model_b": model_b,
        "scope": scope,
        "stage": stage,
        "element": element,
        "independent_units": len(correctness_a),
        "both_correct": both_correct,
        "model_a_only_correct": model_a_only,
        "model_b_only_correct": model_b_only,
        "both_incorrect": both_incorrect,
        "discordant_units": discordant,
        "test": "mcnemar_exact_binomial" if use_exact else "mcnemar_chi_squared",
        "statistic": float(result.statistic),
        "p_value": float(result.pvalue),
    }


def _validate_summary(summary: dict[str, object]) -> None:
    """Enforce the strict generated-summary contract before publication."""
    expected_fields = {
        "schema_version",
        "report_scope",
        "golden_dataset_hash",
        "model_input_payload_hashes",
        "model_ids",
        "overall_inference_unit",
        "feature_accuracy_interpretation",
        "confidence_interval",
        "descriptive_feature_accuracy",
        "overall_case_accuracy",
        "stage_case_accuracy",
        "stage_element_feature_accuracy",
        "pairwise_mcnemar",
        "figures",
    }
    if set(summary) != expected_fields:
        raise ValueError("Generated summary does not match its required fields")
    model_ids = summary["model_ids"]
    input_hashes = summary["model_input_payload_hashes"]
    overall_accuracy = summary["overall_case_accuracy"]
    comparisons = summary["pairwise_mcnemar"]
    if (
        not isinstance(model_ids, list)
        or len(model_ids) != MODEL_COUNT
        or len(set(model_ids)) != MODEL_COUNT
        or not all(isinstance(model_id, str) and model_id for model_id in model_ids)
        or not isinstance(input_hashes, dict)
        or set(input_hashes) != set(model_ids)
        or not all(
            isinstance(value, str) and value.startswith("sha256:") and len(value) == 71
            for value in input_hashes.values()
        )
        or not isinstance(overall_accuracy, list)
        or len(overall_accuracy) != MODEL_COUNT
        or not isinstance(comparisons, list)
        or len(comparisons) != 3
    ):
        raise ValueError("Generated summary has invalid model or paired-comparison records")
    if any(
        not isinstance(record, dict)
        or record.get("model_id") not in model_ids
        or not 0 <= float(record.get("accuracy", -1)) <= 1
        or not 0 <= float(record.get("ci_low", -1)) <= float(record.get("ci_high", 2)) <= 1
        for record in overall_accuracy
    ):
        raise ValueError("Generated summary has invalid overall accuracy records")
    if any(
        not isinstance(record, dict)
        or record.get("scope") != "overall_case"
        or record.get("stage") is not None
        or record.get("element") is not None
        or not 0 <= float(record.get("p_value", -1)) <= 1
        or not 0 <= float(record.get("q_bh", -1)) <= 1
        for record in comparisons
    ):
        raise ValueError("Generated summary has invalid overall McNemar records")


def _add_bh_adjustment(results: list[dict[str, object]]) -> None:
    """Apply BH correction across all pairwise model-comparison hypotheses."""
    _, adjusted, _, _ = multipletests(
        [float(result["p_value"]) for result in results],
        alpha=ALPHA,
        method="fdr_bh",
    )
    for result, adjusted_value in zip(results, adjusted, strict=True):
        result["q_bh"] = float(adjusted_value)


def _write_json(path: Path, value: object) -> None:
    """Write valid, deterministic JSON with a trailing newline."""
    path.write_text(
        json.dumps(value, indent=2, ensure_ascii=True, allow_nan=False) + "\n",
        encoding="utf-8",
    )


def _save_overall_accuracy_plot(
    summaries: list[dict[str, object]], output_dir: Path
) -> list[str]:
    """Save point-and-interval case-level accuracy plots as PDF and 600 DPI PNG."""
    positions = list(range(len(summaries)))
    accuracies = [float(summary["accuracy"]) for summary in summaries]
    lower_errors = [
        accuracy - float(summary["ci_low"]) for accuracy, summary in zip(accuracies, summaries)
    ]
    upper_errors = [
        float(summary["ci_high"]) - accuracy for accuracy, summary in zip(accuracies, summaries)
    ]
    labels = [str(summary["model_id"]) for summary in summaries]

    figure, axis = plt.subplots(figsize=(7, 4.5))
    for position, accuracy, lower, upper, color in zip(
        positions, accuracies, lower_errors, upper_errors, MODEL_COLORS, strict=True
    ):
        axis.errorbar(
            position,
            accuracy,
            yerr=[[lower], [upper]],
            fmt="o",
            color=color,
            capsize=5,
            markersize=8,
        )
    for position, summary in zip(positions, summaries, strict=True):
        axis.annotate(
            f"n={summary['independent_units']}\n"
            f"{summary['all_applicable_checks_exact']}/{summary['independent_units']}",
            xy=(position, float(summary["accuracy"])),
            xytext=(0, 12),
            textcoords="offset points",
            ha="center",
            va="bottom",
            fontsize=8,
        )
    axis.set_xticks(positions, labels, rotation=20, ha="right")
    axis.set_ylim(0, 1)
    axis.set_ylabel("Case-level all-features-exact accuracy")
    axis.set_title("Source-confirmed numeric extraction accuracy")
    axis.spines[["top", "right"]].set_visible(False)
    figure.tight_layout()

    outputs = ["overall_accuracy_by_model.pdf", "overall_accuracy_by_model.png"]
    figure.savefig(output_dir / outputs[0], bbox_inches="tight")
    figure.savefig(output_dir / outputs[1], dpi=600, bbox_inches="tight")
    plt.close(figure)
    return outputs


def _save_stage_element_heatmap(
    model_ids: list[str],
    summaries: list[dict[str, object]],
    output_dir: Path,
) -> list[str]:
    """Save descriptive feature accuracy by stage/element and model."""
    grouped: dict[tuple[str, str], dict[str, dict[str, object]]] = defaultdict(dict)
    for summary in summaries:
        key = (str(summary["stage"]), str(summary["element"]))
        grouped[key][str(summary["model_id"])] = summary
    keys = sorted(grouped)
    labels = [f"{stage} / {element}" for stage, element in keys]
    matrix = [
        [float(grouped[key][model_id]["accuracy"]) for model_id in model_ids] for key in keys
    ]

    figure_height = max(4.5, len(labels) * 0.42 + 1.5)
    figure, axis = plt.subplots(figsize=(8, figure_height))
    color_map = ListedColormap(["#000000", "#0072B2", "#009E73", "#F0E442", "#FFFFFF"])
    color_norm = BoundaryNorm([0, 0.2, 0.4, 0.6, 0.8, 1.000001], color_map.N)
    image = axis.imshow(matrix, cmap=color_map, norm=color_norm, aspect="auto")
    axis.set_xticks(range(len(model_ids)), model_ids, rotation=20, ha="right")
    axis.set_yticks(range(len(labels)), labels)
    axis.set_title("Feature exact-match accuracy by analytic stage and element")
    for row, key in enumerate(keys):
        for column, model_id in enumerate(model_ids):
            summary = grouped[key][model_id]
            accuracy = float(summary["accuracy"])
            color = "white" if accuracy < 0.4 else "black"
            axis.text(
                column,
                row,
                f"{accuracy:.2f}\n({summary['exact_matches']}/{summary['source_confirmed_features']})",
                ha="center",
                va="center",
                color=color,
                fontsize=8,
            )
    figure.colorbar(image, ax=axis, label="Feature exact-match accuracy")
    figure.tight_layout()

    outputs = ["stage_element_accuracy_heatmap.pdf", "stage_element_accuracy_heatmap.png"]
    figure.savefig(output_dir / outputs[0], bbox_inches="tight")
    figure.savefig(output_dir / outputs[1], dpi=600, bbox_inches="tight")
    plt.close(figure)
    return outputs


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--golden-dataset",
        type=Path,
        required=True,
        help="Immutable JSON source of source-confirmed checks and expected values.",
    )
    parser.add_argument(
        "--model-evaluation",
        action="append",
        type=_parse_model_evaluation,
        required=True,
        metavar="MODEL_ID=PATH",
        help="Exactly three model IDs mapped to their JSON prediction payloads.",
    )
    parser.add_argument(
        "--out-dir",
        type=Path,
        required=True,
        help="A previously nonexistent directory for JSON summaries and figures.",
    )
    parser.add_argument(
        "--preview-records",
        type=int,
        default=3,
        help="Overall-accuracy records to print as JSON; defaults to 3.",
    )
    args = parser.parse_args()
    if len(args.model_evaluation) != MODEL_COUNT:
        parser.error(f"Exactly {MODEL_COUNT} --model-evaluation arguments are required")
    if not 0 <= args.preview_records <= MAX_PREVIEW_RECORDS:
        parser.error(f"--preview-records must be between 0 and {MAX_PREVIEW_RECORDS}")

    evaluations = dict(args.model_evaluation)
    if len(evaluations) != MODEL_COUNT:
        parser.error("Each --model-evaluation model ID must occur only once")
    args.model_evaluations = evaluations
    return args


def main() -> None:
    """Create a pre-benchmark three-model accuracy report and paired comparisons."""
    args = _parse_args()
    if args.out_dir.exists():
        raise FileExistsError(f"Refusing to overwrite existing evaluation output: {args.out_dir}")
    if not args.golden_dataset.is_file():
        raise FileNotFoundError(f"Golden dataset does not exist: {args.golden_dataset}")
    args.out_dir.parent.mkdir(parents=True, exist_ok=True)
    temporary_dir = Path(tempfile.mkdtemp(prefix=f".{args.out_dir.name}.", dir=args.out_dir.parent))
    published = False

    try:
        golden_checks, golden_dataset_hash = _load_golden_dataset(args.golden_dataset)
        predictions: dict[str, dict[CheckKey, object]] = {}
        input_payload_hashes: dict[str, str] = {}
        for model_id, path in args.model_evaluations.items():
            if not path.is_file():
                raise FileNotFoundError(f"Model evaluation does not exist: {path}")
            model_predictions, input_payload_hash = _load_predictions(
                path, model_id, golden_dataset_hash, set(golden_checks)
            )
            predictions[model_id] = model_predictions
            input_payload_hashes[model_id] = input_payload_hash

        source_confirmed = sorted(
            key for key, check in golden_checks.items() if check["source_present"] is True
        )
        model_ids = list(predictions)
        feature_correctness = {
            model_id: [
                predictions[model_id][key] == golden_checks[key]["expected_value"]
                for key in source_confirmed
            ]
            for model_id in model_ids
        }
        descriptive_feature_accuracy = [
            _descriptive_feature_accuracy(model_id, feature_correctness[model_id])
            for model_id in model_ids
        ]

        keys_by_case: dict[str, list[CheckKey]] = defaultdict(list)
        keys_by_case_stage: dict[tuple[str, str], list[CheckKey]] = defaultdict(list)
        keys_by_stage_element: dict[tuple[str, str], list[CheckKey]] = defaultdict(list)
        for key in source_confirmed:
            case_id, stage, element = key
            keys_by_case[case_id].append(key)
            keys_by_case_stage[(case_id, stage)].append(key)
            keys_by_stage_element[(stage, element)].append(key)

        overall_correctness = {
            model_id: [
                all(
                    predictions[model_id][key] == golden_checks[key]["expected_value"]
                    for key in keys
                )
                for _, keys in sorted(keys_by_case.items())
            ]
            for model_id in model_ids
        }
        overall_accuracy = [
            _accuracy_summary(model_id, overall_correctness[model_id]) for model_id in model_ids
        ]

        keys_by_stage: dict[str, list[list[CheckKey]]] = defaultdict(list)
        for (_, stage), keys in keys_by_case_stage.items():
            keys_by_stage[stage].append(keys)
        stage_accuracy: list[dict[str, object]] = []
        for stage, case_stage_keys in sorted(keys_by_stage.items()):
            for model_id in model_ids:
                summary = _descriptive_case_accuracy(
                    model_id,
                    [
                        all(
                            predictions[model_id][key] == golden_checks[key]["expected_value"]
                            for key in keys
                        )
                        for keys in case_stage_keys
                    ],
                )
                summary["stage"] = stage
                stage_accuracy.append(summary)

        stage_element_accuracy: list[dict[str, object]] = []
        for (stage, element), keys in sorted(keys_by_stage_element.items()):
            for model_id in model_ids:
                summary = _descriptive_feature_accuracy(
                    model_id,
                    [
                        predictions[model_id][key] == golden_checks[key]["expected_value"]
                        for key in keys
                    ],
                )
                summary["stage"] = stage
                summary["element"] = element
                stage_element_accuracy.append(summary)

        comparisons: list[dict[str, object]] = []
        for model_a, model_b in itertools.combinations(model_ids, 2):
            comparisons.append(
                _mcnemar_result(
                    model_a,
                    model_b,
                    overall_correctness[model_a],
                    overall_correctness[model_b],
                    scope="overall_case",
                )
            )
        _add_bh_adjustment(comparisons)

        figures = (
            _save_overall_accuracy_plot(overall_accuracy, temporary_dir)
            + _save_stage_element_heatmap(model_ids, stage_element_accuracy, temporary_dir)
        )
        summary = {
            "schema_version": SUMMARY_SCHEMA_VERSION,
            "report_scope": "pre_benchmark_local_evaluation",
            "golden_dataset_hash": golden_dataset_hash,
            "model_input_payload_hashes": input_payload_hashes,
            "model_ids": model_ids,
            "overall_inference_unit": "case; all source-confirmed numeric checks exact",
            "feature_accuracy_interpretation": "descriptive; feature checks are clustered within cases",
            "confidence_interval": {
                "method": "agresti_coull",
                "level": 1 - ALPHA,
            },
            "descriptive_feature_accuracy": descriptive_feature_accuracy,
            "overall_case_accuracy": overall_accuracy,
            "stage_case_accuracy": stage_accuracy,
            "stage_element_feature_accuracy": stage_element_accuracy,
            "pairwise_mcnemar": comparisons,
            "figures": figures,
        }
        _validate_summary(summary)
        _validate_schema(summary, "extraction_model_comparison.schema.json")
        _write_json(temporary_dir / "model_accuracy_summary.json", summary)
        temporary_dir.rename(args.out_dir)
        published = True
        print(
            json.dumps(
                {
                    "dataset": "overall_case_accuracy",
                    "records": overall_accuracy[: args.preview_records],
                },
                indent=2,
                ensure_ascii=True,
                allow_nan=False,
            )
        )
    finally:
        if not published:
            shutil.rmtree(temporary_dir)


if __name__ == "__main__":
    main()

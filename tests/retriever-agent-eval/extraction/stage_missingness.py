"""Normalize missing data as the first staged BRCA extraction dataset.

Each input is a JSON record array. Blank strings and JSON NaN values become null.
Rows are dropped only if every field is null after normalization; records with any
observed field are retained. The script writes normalized JSON arrays and a JSON
missingness report through an atomic output directory.

Usage:
    python src/extraction/stage_missingness.py \
        --input-dataset clinical_patient=/path/clinical_patient.json \
        --input-dataset mutations=/path/mutations.json \
        --out-dir data/processed/brca_missingness
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import re
import shutil
import tempfile
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator
from jsonschema.exceptions import ValidationError


MAX_PREVIEW_RECORDS = 10
DATASET_NAME_PATTERN = re.compile(r"^[A-Za-z][A-Za-z0-9_]*$")


def _parse_dataset(value: str) -> tuple[str, Path]:
    """Parse a safe dataset-name to JSON-file mapping."""
    name, separator, raw_path = value.partition("=")
    if separator != "=" or not DATASET_NAME_PATTERN.fullmatch(name) or not raw_path:
        raise argparse.ArgumentTypeError(
            "--input-dataset must use SAFE_DATASET_NAME=/path/to/input.json"
        )
    return name, Path(raw_path)


def _parse_constant(value: str) -> None:
    """Map JSON NaN to null while rejecting other nonstandard numeric constants."""
    if value == "NaN":
        return None
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


def _read_json_records(path: Path) -> tuple[list[dict[str, Any]], str]:
    """Read a JSON record array and hash its canonical pre-normalization representation."""
    raw = path.read_bytes()
    try:
        value = json.loads(
            raw.decode("utf-8"),
            parse_constant=_parse_constant,
            parse_float=_parse_finite_float,
            object_pairs_hook=_reject_duplicate_keys,
        )
    except (UnicodeDecodeError, json.JSONDecodeError, ValueError) as error:
        raise ValueError(f"{path}: invalid JSON record array") from error
    if not isinstance(value, list) or any(not isinstance(record, dict) for record in value):
        raise ValueError(f"{path}: expected a JSON array of object records")
    canonical_records = json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=True,
        allow_nan=False,
    ).encode("utf-8")
    return value, f"sha256:{hashlib.sha256(canonical_records).hexdigest()}"


def _normalize_value(value: Any) -> Any:
    """Recursively convert blank strings and floating NaN values to JSON null."""
    if isinstance(value, str):
        return None if not value.strip() else value
    if isinstance(value, float) and math.isnan(value):
        return None
    if isinstance(value, list):
        return [_normalize_value(item) for item in value]
    if isinstance(value, dict):
        return {key: _normalize_value(item) for key, item in value.items()}
    return value


def _is_missing(value: Any) -> bool:
    """Treat only null as missing after all blank and NaN values are normalized."""
    return value is None


def _normalize_records(records: list[dict[str, Any]]) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    """Normalize records and compute missingness before dropping wholly blank rows."""
    normalized = [
        {str(key): _normalize_value(value) for key, value in record.items()} for record in records
    ]
    all_fields = sorted({field for record in normalized for field in record})
    retained = [
        record
        for record in normalized
        if not all(_is_missing(record.get(field)) for field in all_fields)
    ]
    field_missingness = [
        {
            "field": field,
            "missing_count": sum(_is_missing(record.get(field)) for record in normalized),
            "missing_fraction": (
                sum(_is_missing(record.get(field)) for record in normalized) / len(normalized)
                if normalized
                else None
            ),
        }
        for field in all_fields
    ]
    report = {
        "input_records": len(records),
        "retained_records": len(retained),
        "all_columns_missing_rows_dropped": len(normalized) - len(retained),
        "partially_or_fully_observed_rows_retained": len(retained),
        "field_missingness_before_row_drop": field_missingness,
    }
    return retained, report


def _write_json(path: Path, value: Any) -> None:
    """Write strict JSON with stable ASCII encoding and a trailing newline."""
    path.write_text(
        json.dumps(value, indent=2, ensure_ascii=True, allow_nan=False) + "\n",
        encoding="utf-8",
    )


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--input-dataset",
        action="append",
        type=_parse_dataset,
        required=True,
        metavar="NAME=PATH",
        help="One or more JSON record arrays to normalize.",
    )
    parser.add_argument(
        "--out-dir",
        type=Path,
        required=True,
        help="A previously nonexistent directory for normalized JSON and the report.",
    )
    parser.add_argument(
        "--preview-records",
        type=int,
        default=1,
        help="Normalized records to print per dataset as JSON; defaults to 1.",
    )
    args = parser.parse_args()
    if not 0 <= args.preview_records <= MAX_PREVIEW_RECORDS:
        parser.error(f"--preview-records must be between 0 and {MAX_PREVIEW_RECORDS}")
    datasets = dict(args.input_dataset)
    if len(datasets) != len(args.input_dataset):
        parser.error("Each --input-dataset name must occur only once")
    args.datasets = datasets
    return args


def main() -> None:
    """Normalize every input dataset and atomically publish the staged result."""
    args = _parse_args()
    if args.out_dir.exists():
        raise FileExistsError(f"Refusing to overwrite existing staged output: {args.out_dir}")
    args.out_dir.parent.mkdir(parents=True, exist_ok=True)
    temporary_dir = Path(tempfile.mkdtemp(prefix=f".{args.out_dir.name}.", dir=args.out_dir.parent))
    published = False

    try:
        datasets: list[dict[str, Any]] = []
        previews: list[dict[str, Any]] = []
        seen_sources: set[tuple[int, int] | str] = set()
        for name, source_path in args.datasets.items():
            if not source_path.is_file():
                raise FileNotFoundError(f"Input dataset does not exist: {source_path}")
            metadata = source_path.stat()
            source_identity: tuple[int, int] | str = (
                (metadata.st_dev, metadata.st_ino)
                if metadata.st_ino != 0
                else str(source_path.resolve())
            )
            if source_identity in seen_sources:
                raise ValueError(f"Each staged dataset must use a distinct input file: {source_path}")
            seen_sources.add(source_identity)

            records, source_checksum = _read_json_records(source_path)
            normalized_records, missingness = _normalize_records(records)
            filename = f"{name}.json"
            _write_json(temporary_dir / filename, normalized_records)
            datasets.append(
                {
                    "dataset": name,
                    "source_filename": source_path.name,
                    "source_representation": "canonical_pre_normalization_records",
                    "source_checksum": source_checksum,
                    "filename": filename,
                    "format": "json",
                    "orientation": "records",
                    **missingness,
                }
            )
            previews.append({"dataset": name, "records": normalized_records[: args.preview_records]})

        report = {
            "schema_version": "brca_missingness_stage.v1",
            "normalization": {
                "blank_string": "null",
                "json_nan": "null",
                "row_drop_rule": "drop only when every field is null after normalization",
            },
            "datasets": datasets,
        }
        _validate_schema(report, "missingness_stage.schema.json")
        _write_json(temporary_dir / "missingness_report.json", report)
        temporary_dir.rename(args.out_dir)
        published = True

        for preview in previews:
            print(json.dumps(preview, indent=2, ensure_ascii=True, allow_nan=False))
        print(
            json.dumps(
                {"dataset": "missingness_report", "records": [report]},
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

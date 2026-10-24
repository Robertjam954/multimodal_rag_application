"""Stage validated Aim 1 result tables as JSON record arrays.

The source CSV column names must match the approved Aim 1 contracts exactly. This
script writes JSON-only staged artifacts and a checksum manifest. It can display a
bounded JSON preview for every dataset as it writes.

Usage:
    python src/ingest/stage_aim1_result_tables.py \
        --input-file aim1_univariate_logistic=/path/aim1_univariate_logistic.csv \
        --input-file aim1_top10_gene_pq=/path/aim1_top10_gene_pq.csv \
        --input-file aim1_pathway_pq=/path/aim1_pathway_pq.csv \
        --input-file aim1_multivariate_logistic=/path/aim1_multivariate_logistic.csv \
        --input-file aim1_gene_pathway_comparison=/path/aim1_gene_pathway_comparison.csv \
        --out-dir data/processed/aim1
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
import shutil
import tempfile
from dataclasses import dataclass
from pathlib import Path

from jsonschema import Draft202012Validator
from jsonschema.exceptions import ValidationError


@dataclass(frozen=True)
class TableContract:
    """Define an approved source table and its JSON value conversions."""

    columns: tuple[str, ...]
    integer_columns: frozenset[str]
    number_columns: frozenset[str]
    nullable_columns: frozenset[str] = frozenset()
    probability_columns: frozenset[str] = frozenset()
    nonnegative_number_columns: frozenset[str] = frozenset()
    allowed_values: dict[str, frozenset[str]] | None = None


PREVALENCE_COLUMNS = (
    "feature",
    "n_brain_met",
    "n_no_brain_met",
    "mut_brain_met",
    "mut_no_brain_met",
    "prev_brain_met",
    "prev_no_brain_met",
    "prev_ratio",
    "pr_lo",
    "pr_hi",
    "odds_ratio",
    "fisher_p",
    "p_holm",
    "q_bh",
)
COMPARISON_COLUMNS = (
    "kind",
    "feature",
    "n_brain_met",
    "n_no_brain_met",
    "count_brain_met_mut",
    "count_no_brain_met_mut",
    "prev_brain_met",
    "prev_no_brain_met",
    "prev_ratio",
    "pr_lo",
    "pr_hi",
    "fisher_p",
    "p_holm",
    "p_bh",
)
PREVALENCE_INTEGER_COLUMNS = frozenset(
    {"n_brain_met", "n_no_brain_met", "mut_brain_met", "mut_no_brain_met"}
)
PREVALENCE_PROBABILITY_COLUMNS = frozenset(
    {"prev_brain_met", "prev_no_brain_met", "fisher_p", "p_holm", "q_bh"}
)
COMPARISON_PROBABILITY_COLUMNS = frozenset(
    {"prev_brain_met", "prev_no_brain_met", "fisher_p", "p_holm", "p_bh"}
)
COMPARISON_INTEGER_COLUMNS = frozenset(
    {"n_brain_met", "n_no_brain_met", "count_brain_met_mut", "count_no_brain_met_mut"}
)

CONTRACTS = {
    "aim1_univariate_logistic": TableContract(
        columns=(
            "kind",
            "feature",
            "n",
            "n_mutated",
            "or",
            "or_lo",
            "or_hi",
            "coef",
            "se",
            "p",
            "note",
            "q_bh",
        ),
        integer_columns=frozenset({"n", "n_mutated"}),
        number_columns=frozenset({"or", "or_lo", "or_hi", "coef", "se", "p", "q_bh"}),
        nullable_columns=frozenset({"note"}),
        probability_columns=frozenset({"p", "q_bh"}),
        nonnegative_number_columns=frozenset({"se"}),
        allowed_values={"kind": frozenset({"gene", "pathway"})},
    ),
    "aim1_top10_gene_pq": TableContract(
        columns=PREVALENCE_COLUMNS,
        integer_columns=PREVALENCE_INTEGER_COLUMNS,
        number_columns=frozenset(set(PREVALENCE_COLUMNS) - PREVALENCE_INTEGER_COLUMNS - {"feature"}),
        probability_columns=PREVALENCE_PROBABILITY_COLUMNS,
        nonnegative_number_columns=frozenset(
            set(PREVALENCE_COLUMNS)
            - PREVALENCE_INTEGER_COLUMNS
            - {"feature", "prev_brain_met", "prev_no_brain_met", "fisher_p", "p_holm", "q_bh"}
        ),
    ),
    "aim1_pathway_pq": TableContract(
        columns=PREVALENCE_COLUMNS,
        integer_columns=PREVALENCE_INTEGER_COLUMNS,
        number_columns=frozenset(set(PREVALENCE_COLUMNS) - PREVALENCE_INTEGER_COLUMNS - {"feature"}),
        probability_columns=PREVALENCE_PROBABILITY_COLUMNS,
        nonnegative_number_columns=frozenset(
            set(PREVALENCE_COLUMNS)
            - PREVALENCE_INTEGER_COLUMNS
            - {"feature", "prev_brain_met", "prev_no_brain_met", "fisher_p", "p_holm", "q_bh"}
        ),
    ),
    "aim1_multivariate_logistic": TableContract(
        columns=("feature", "or", "or_lo", "or_hi", "coef", "se", "p"),
        integer_columns=frozenset(),
        number_columns=frozenset({"or", "or_lo", "or_hi", "coef", "se", "p"}),
        probability_columns=frozenset({"p"}),
        nonnegative_number_columns=frozenset({"se"}),
    ),
    "aim1_gene_pathway_comparison": TableContract(
        columns=COMPARISON_COLUMNS,
        integer_columns=COMPARISON_INTEGER_COLUMNS,
        number_columns=frozenset(
            set(COMPARISON_COLUMNS) - COMPARISON_INTEGER_COLUMNS - {"kind", "feature"}
        ),
        probability_columns=COMPARISON_PROBABILITY_COLUMNS,
        nonnegative_number_columns=frozenset(
            set(COMPARISON_COLUMNS)
            - COMPARISON_INTEGER_COLUMNS
            - {"kind", "feature", "prev_brain_met", "prev_no_brain_met", "fisher_p", "p_holm", "p_bh"}
        ),
        allowed_values={"kind": frozenset({"gene", "pathway"})},
    ),
}
ARRAY_SCHEMA_NAMES = {
    "aim1_univariate_logistic": "univariate_logistic_array",
    "aim1_top10_gene_pq": "prevalence_array",
    "aim1_pathway_pq": "prevalence_array",
    "aim1_multivariate_logistic": "multivariate_logistic_array",
    "aim1_gene_pathway_comparison": "gene_pathway_comparison_array",
}
MAX_PREVIEW_RECORDS = 10


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _parse_input_file(value: str) -> tuple[str, Path]:
    """Parse an exact table-name to source-file mapping."""
    name, separator, raw_path = value.partition("=")
    if separator != "=" or not name or not raw_path:
        raise argparse.ArgumentTypeError(
            "--input-file must use TABLE_NAME=/path/to/source.csv"
        )
    if name not in CONTRACTS:
        accepted = ", ".join(CONTRACTS)
        raise argparse.ArgumentTypeError(f"Unknown table {name!r}; expected one of: {accepted}")
    return name, Path(raw_path)


def _convert_value(name: str, value: str, contract: TableContract, row_number: int) -> object:
    """Convert one CSV value to its JSON type, rejecting missing required numerics."""
    if value == "" and name in contract.nullable_columns:
        return None
    if value == "":
        raise ValueError(f"Row {row_number}: required column {name!r} is empty")
    try:
        if name in contract.integer_columns:
            return int(value)
        if name in contract.number_columns:
            return float(value)
    except ValueError as error:
        raise ValueError(f"Row {row_number}: {name!r} is not a valid numeric value: {value!r}") from error
    return value


def _validate_record(
    table_name: str,
    record: dict[str, object],
    contract: TableContract,
    row_number: int,
) -> None:
    """Enforce the applicable table-specific JSON Schema constraints."""
    for name in contract.integer_columns:
        value = record[name]
        if not isinstance(value, int) or value < 0:
            raise ValueError(f"Row {row_number}: {name!r} must be a nonnegative integer")

    for name in contract.number_columns:
        value = record[name]
        if not isinstance(value, float) or not math.isfinite(value):
            raise ValueError(f"Row {row_number}: {name!r} must be a finite number")
        if name in contract.nonnegative_number_columns and value < 0:
            raise ValueError(f"Row {row_number}: {name!r} must be nonnegative")
        if name in contract.probability_columns and not 0 <= value <= 1:
            raise ValueError(f"Row {row_number}: {name!r} must be between 0 and 1")

    if contract.allowed_values:
        for name, allowed in contract.allowed_values.items():
            value = record[name]
            if value not in allowed:
                raise ValueError(
                    f"Row {row_number}: {name!r} must be one of {sorted(allowed)!r}, got {value!r}"
                )

    if table_name == "aim1_univariate_logistic":
        if record["n_mutated"] > record["n"]:
            raise ValueError(f"Row {row_number}: n_mutated cannot exceed n")
        _validate_odds_ratio_interval(record, row_number)
    elif table_name in {"aim1_top10_gene_pq", "aim1_pathway_pq"}:
        if record["mut_brain_met"] > record["n_brain_met"]:
            raise ValueError(f"Row {row_number}: mut_brain_met cannot exceed n_brain_met")
        if record["mut_no_brain_met"] > record["n_no_brain_met"]:
            raise ValueError(f"Row {row_number}: mut_no_brain_met cannot exceed n_no_brain_met")
        _validate_prevalence_ratio_interval(record, row_number)
        _validate_positive_interval(record, "odds_ratio", None, None, row_number)
    elif table_name == "aim1_multivariate_logistic":
        _validate_odds_ratio_interval(record, row_number)
    elif table_name == "aim1_gene_pathway_comparison":
        if record["count_brain_met_mut"] > record["n_brain_met"]:
            raise ValueError(f"Row {row_number}: count_brain_met_mut cannot exceed n_brain_met")
        if record["count_no_brain_met_mut"] > record["n_no_brain_met"]:
            raise ValueError(
                f"Row {row_number}: count_no_brain_met_mut cannot exceed n_no_brain_met"
            )
        _validate_prevalence_ratio_interval(record, row_number)


def _validate_positive_interval(
    record: dict[str, object],
    estimate_name: str,
    lower_name: str | None,
    upper_name: str | None,
    row_number: int,
) -> None:
    """Validate a positive estimate and, when present, ordered positive confidence bounds."""
    estimate = record[estimate_name]
    if not isinstance(estimate, float) or estimate <= 0:
        raise ValueError(f"Row {row_number}: {estimate_name!r} must be positive")
    if lower_name is not None and upper_name is not None:
        lower = record[lower_name]
        upper = record[upper_name]
        if (
            not isinstance(lower, float)
            or not isinstance(upper, float)
            or lower <= 0
            or upper <= 0
            or not lower <= estimate <= upper
        ):
            raise ValueError(
                f"Row {row_number}: {estimate_name!r} must fall within ordered positive "
                f"{lower_name!r} and {upper_name!r} bounds"
            )


def _validate_odds_ratio_interval(record: dict[str, object], row_number: int) -> None:
    """Validate odds ratio and confidence-interval ordering."""
    _validate_positive_interval(record, "or", "or_lo", "or_hi", row_number)


def _validate_prevalence_ratio_interval(record: dict[str, object], row_number: int) -> None:
    """Validate prevalence counts, derived prevalences, and ratio interval ordering."""
    if "mut_brain_met" in record:
        brain_met_count_name = "mut_brain_met"
        no_brain_met_count_name = "mut_no_brain_met"
    else:
        brain_met_count_name = "count_brain_met_mut"
        no_brain_met_count_name = "count_no_brain_met_mut"

    n_brain_met = record["n_brain_met"]
    n_no_brain_met = record["n_no_brain_met"]
    brain_met_count = record[brain_met_count_name]
    no_brain_met_count = record[no_brain_met_count_name]
    reported_brain_met_prevalence = record["prev_brain_met"]
    reported_no_brain_met_prevalence = record["prev_no_brain_met"]
    estimate = record["prev_ratio"]
    lower = record["pr_lo"]
    upper = record["pr_hi"]

    if (
        not isinstance(n_brain_met, int)
        or not isinstance(n_no_brain_met, int)
        or not isinstance(brain_met_count, int)
        or not isinstance(no_brain_met_count, int)
        or n_brain_met <= 0
        or n_no_brain_met <= 0
        or not isinstance(estimate, float)
        or not isinstance(lower, float)
        or not isinstance(upper, float)
        or not isinstance(reported_brain_met_prevalence, float)
        or not isinstance(reported_no_brain_met_prevalence, float)
        or estimate < 0
        or lower < 0
        or upper < 0
        or not lower <= estimate <= upper
    ):
        raise ValueError(
            f"Row {row_number}: prevalence denominators must be positive and prev_ratio must "
            "fall within ordered nonnegative pr_lo and pr_hi bounds"
        )
    expected_brain_met_prevalence = brain_met_count / n_brain_met
    expected_no_brain_met_prevalence = no_brain_met_count / n_no_brain_met
    if not math.isclose(
        reported_brain_met_prevalence,
        expected_brain_met_prevalence,
        rel_tol=1e-12,
        abs_tol=1e-12,
    ):
        raise ValueError(
            f"Row {row_number}: prev_brain_met does not match {brain_met_count_name} / n_brain_met"
        )
    if not math.isclose(
        reported_no_brain_met_prevalence,
        expected_no_brain_met_prevalence,
        rel_tol=1e-12,
        abs_tol=1e-12,
    ):
        raise ValueError(
            f"Row {row_number}: prev_no_brain_met does not match "
            f"{no_brain_met_count_name} / n_no_brain_met"
        )
    if expected_no_brain_met_prevalence == 0:
        raise ValueError(
            f"Row {row_number}: prev_ratio is not finite when prev_no_brain_met is zero"
        )
    expected_ratio = expected_brain_met_prevalence / expected_no_brain_met_prevalence
    if not math.isclose(estimate, expected_ratio, rel_tol=1e-12, abs_tol=1e-12):
        raise ValueError(
            f"Row {row_number}: prev_ratio does not match prev_brain_met / prev_no_brain_met"
        )


def _read_source_table(
    table_name: str, path: Path, contract: TableContract
) -> list[dict[str, object]]:
    """Load a CSV only when it conforms exactly to the corresponding output contract."""
    with path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        actual_columns = tuple(reader.fieldnames or ())
        if actual_columns != contract.columns:
            raise ValueError(
                f"{path}: expected columns {contract.columns!r}, found {actual_columns!r}"
            )

        records: list[dict[str, object]] = []
        for row_number, row in enumerate(reader, start=2):
            if None in row:
                raise ValueError(f"{path}: row {row_number} has more fields than the header")
            record = {
                name: _convert_value(name, row[name], contract, row_number)
                for name in contract.columns
            }
            _validate_record(table_name, record, contract, row_number)
            records.append(record)
    return records


def _validate_records(table_name: str, records: list[dict[str, object]]) -> None:
    """Validate a named record array against its non-ambiguous JSON Schema definition."""
    schema_path = Path(__file__).resolve().parents[2] / "schemas" / "aim1_result_tables.schema.json"
    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    array_schema = {
        "$schema": schema["$schema"],
        "$defs": schema["$defs"],
        **schema["$defs"][ARRAY_SCHEMA_NAMES[table_name]],
    }
    try:
        Draft202012Validator(array_schema).validate(records)
    except ValidationError as error:
        raise ValueError(f"{table_name}: JSON Schema validation failed: {error.message}") from error


def _write_json(path: Path, value: object) -> None:
    """Write deterministic, valid JSON with a trailing newline."""
    path.write_text(json.dumps(value, indent=2, ensure_ascii=True, allow_nan=False) + "\n", encoding="utf-8")


def _source_identity(path: Path) -> tuple[int, int] | str:
    """Identify a source file by inode, falling back to its resolved path."""
    metadata = path.stat()
    if metadata.st_ino != 0:
        return (metadata.st_dev, metadata.st_ino)
    return str(path.resolve())


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--input-file",
        action="append",
        type=_parse_input_file,
        required=True,
        metavar="TABLE_NAME=PATH",
        help="One mapping for each required Aim 1 CSV source table.",
    )
    parser.add_argument(
        "--out-dir",
        type=Path,
        required=True,
        help="Gitignored directory for JSON staged result tables and manifest.",
    )
    parser.add_argument(
        "--preview-records",
        type=int,
        default=1,
        help="JSON records to print for every written table; defaults to 1.",
    )
    args = parser.parse_args()
    if not 0 <= args.preview_records <= MAX_PREVIEW_RECORDS:
        parser.error(f"--preview-records must be between 0 and {MAX_PREVIEW_RECORDS}")

    input_files = dict(args.input_file)
    if len(input_files) != len(args.input_file):
        parser.error("Each --input-file table name must occur only once")
    missing = set(CONTRACTS) - set(input_files)
    if missing:
        parser.error(f"Missing --input-file mappings for: {', '.join(sorted(missing))}")
    for table_name, source_path in input_files.items():
        if not source_path.name.endswith(f"{table_name}.csv"):
            parser.error(
                f"{table_name} source must end with {table_name}.csv, got {source_path.name!r}"
            )
    args.input_files = input_files
    return args


def main() -> None:
    """Stage every required result table, then emit a single manifest."""
    args = _parse_args()
    if args.out_dir.exists():
        raise FileExistsError(f"Refusing to overwrite existing staged output: {args.out_dir}")
    args.out_dir.parent.mkdir(parents=True, exist_ok=True)
    temporary_dir = Path(tempfile.mkdtemp(prefix=f".{args.out_dir.name}.", dir=args.out_dir.parent))
    published = False

    try:
        source_identities: set[tuple[int, int] | str] = set()
        for source_path in args.input_files.values():
            if not source_path.is_file():
                raise FileNotFoundError(f"Source table does not exist: {source_path}")
            source_identity = _source_identity(source_path)
            if source_identity in source_identities:
                raise ValueError(f"Each staged table must use a distinct source file: {source_path}")
            source_identities.add(source_identity)

        manifest_tables: list[dict[str, object]] = []
        previews: list[dict[str, object]] = []
        for table_name, contract in CONTRACTS.items():
            source_path = args.input_files[table_name]
            records = _read_source_table(table_name, source_path, contract)
            _validate_records(table_name, records)
            output_path = temporary_dir / f"{table_name}.json"
            _write_json(output_path, records)

            manifest_tables.append(
                {
                    "dataset": table_name,
                    "source_filename": source_path.name,
                    "filename": output_path.name,
                    "format": "json",
                    "orientation": "records",
                    "columns": list(contract.columns),
                    "rows": len(records),
                    "checksum": f"sha256:{_sha256(output_path)}",
                }
            )
            previews.append({"dataset": table_name, "records": records[: args.preview_records]})

        manifest_path = temporary_dir / "manifest.json"
        manifest = {
            "contract": "aim1_result_tables_v1",
            "tables": manifest_tables,
        }
        _write_json(
            manifest_path,
            manifest,
        )
        temporary_dir.rename(args.out_dir)
        published = True

        for preview in previews:
            print(json.dumps(preview, indent=2, ensure_ascii=True, allow_nan=False))
        print(
            json.dumps(
                {"dataset": "manifest", "records": [manifest]},
                indent=2,
            )
        )
    finally:
        if not published:
            shutil.rmtree(temporary_dir)


if __name__ == "__main__":
    main()

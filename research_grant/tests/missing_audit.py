"""Create a structural and clinical availability audit for a TCGA-BRCA TSV export.

Usage:
    python DataAnalysisExpert/analyze_brca_snapshot.py \
        --input-dir 'data_tcga-brca.2026-09-03 ' \
        --output DataAnalysisExpert/brca_snapshot_audit.md
"""
from __future__ import annotations

import argparse
import csv
from collections import Counter
from pathlib import Path


MISSING_VALUES = {"", "'--"}
CASE_ID_COLUMN = "cases.case_id"
SUBMITTER_ID_COLUMN = "cases.submitter_id"
MAX_VALUE_ROWS = 12


def parse_args() -> argparse.Namespace:
    """Parse command-line paths for the source snapshot and aggregate report."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input-dir", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    return parser.parse_args()


def is_present(value: str | None) -> bool:
    """Return whether an export cell is not its designated missing token."""
    return value is not None and value.strip() not in MISSING_VALUES


def read_table(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    """Read one TSV table while preserving every string value from the export."""
    with path.open(encoding="utf-8", newline="") as source:
        reader = csv.DictReader(source, delimiter="\t")
        return reader.fieldnames or [], list(reader)


def summarize_table(path: Path) -> dict[str, object]:
    """Calculate row, case, missingness, and candidate-field summaries for one TSV."""
    columns, rows = read_table(path)
    case_ids = [row.get(CASE_ID_COLUMN, "") for row in rows if is_present(row.get(CASE_ID_COLUMN))]
    submitter_ids = [
        row.get(SUBMITTER_ID_COLUMN, "") for row in rows if is_present(row.get(SUBMITTER_ID_COLUMN))
    ]
    candidate_columns = [
        column
        for column in columns
        if any(term in column.lower() for term in ("brain", "metasta", "recurr", "progression"))
    ]
    candidates = {
        column: Counter(row[column] for row in rows if is_present(row.get(column)))
        for column in candidate_columns
    }
    missing_counts = {
        column: sum(not is_present(row.get(column)) for row in rows)
        for column in columns
    }
    return {
        "name": path.name,
        "columns": len(columns),
        "rows": len(rows),
        "unique_case_ids": len(set(case_ids)),
        "unique_submitter_ids": len(set(submitter_ids)),
        "repeated_case_rows": len(rows) - len(set(case_ids)),
        "candidate_values": candidates,
        "complete_columns": sum(count == 0 for count in missing_counts.values()),
        "all_missing_columns": sum(count == len(rows) for count in missing_counts.values()),
    }


def render_report(input_dir: Path, summaries: list[dict[str, object]]) -> str:
    """Render a concise aggregate report without writing patient-level data."""
    lines = [
        "# TCGA-BRCA Snapshot Structural Audit",
        "",
        f"Source directory: `{input_dir}`",
        "",
        "`'--` and blank cells were treated as missing. This report is descriptive only; "
        "it does not classify brain-metastasis status.",
        "",
        "## Table Inventory",
        "",
        "| Table | Rows | Columns | Unique case IDs | Unique submitter IDs | Repeated case rows | Complete columns | All-missing columns |",
        "|---|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for summary in summaries:
        lines.append(
            "| {name} | {rows} | {columns} | {unique_case_ids} | {unique_submitter_ids} | "
            "{repeated_case_rows} | {complete_columns} | {all_missing_columns} |".format(**summary)
        )

    lines.extend(["", "## Brain Metastasis and Outcome Field Availability", ""])
    found_candidate = False
    for summary in summaries:
        candidates = summary["candidate_values"]
        if not candidates:
            continue
        found_candidate = True
        lines.extend([f"### {summary['name']}", ""])
        for column, values in candidates.items():
            total_present = sum(values.values())
            rendered_values = "; ".join(
                f"`{value}`: {count}"
                for value, count in values.most_common(MAX_VALUE_ROWS)
            )
            lines.append(f"- `{column}`: {total_present} non-missing rows. {rendered_values}")
        lines.append("")
    if not found_candidate:
        lines.append("No columns contained brain, metastasis, recurrence, or progression terms.")
        lines.append("")

    lines.extend(
        [
            "## Interpretation",
            "",
            "- Repeated case rows reflect nested clinical entities flattened into TSV records. "
            "They must not be treated as independent patients.",
            "- A clinical association or survival analysis requires a separately specified "
            "patient-level linkage and brain-metastasis evidence rule.",
            "",
        ]
    )
    return "\n".join(lines)


def main() -> None:
    """Run the audit and publish its aggregate Markdown report."""
    args = parse_args()
    if not args.input_dir.is_dir():
        raise FileNotFoundError(f"Input directory does not exist: {args.input_dir}")
    table_paths = sorted(args.input_dir.glob("*.tsv"))
    if not table_paths:
        raise FileNotFoundError(f"No TSV files found in: {args.input_dir}")
    summaries = [summarize_table(path) for path in table_paths]
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(render_report(args.input_dir, summaries), encoding="utf-8")
    print(f"Wrote aggregate audit: {args.output}")


if __name__ == "__main__":
    main()
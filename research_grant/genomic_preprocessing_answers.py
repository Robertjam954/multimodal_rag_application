from __future__ import annotations

import argparse
import csv
import gzip
import json
import re
from pathlib import Path
from typing import Any


FAKE_PATIENT_NAME = "Jane Doe"
MISSING_VALUES = {"", ".", "NA", "N/A"}
NON_MUTATION_CLASSES = {"Silent", "Intron", "IGR", "3'UTR", "5'UTR", "RNA", "lincRNA"}
REQUIRED_COLUMNS = {
    "case_id",
    "Hugo_Symbol",
    "Mutation_Status",
    "Variant_Classification",
    "t_depth",
    "t_alt_count",
}
API_KEY_PATTERN = re.compile(r"\bsk-[A-Za-z0-9_-]{16,}\b")
NAME_FIELDS = {"name", "patient_name", "first_name", "last_name"}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Calculate correct preprocessing answers from GDC MAF files."
    )
    parser.add_argument("input_dir", type=Path)
    parser.add_argument("output_json", type=Path)
    return parser.parse_args()


def open_maf(path: Path):
    if path.name.endswith(".gz"):
        return gzip.open(path, "rt", encoding="utf-8", errors="replace")
    return path.open("r", encoding="utf-8", errors="replace")


def read_maf(path: Path) -> list[dict[str, str]]:
    with open_maf(path) as handle:
        for line in handle:
            if not line.startswith("#"):
                columns = line.rstrip("\n").split("\t")
                break
        else:
            raise ValueError(f"No MAF header found in {path.name}.")

        missing_columns = REQUIRED_COLUMNS - set(columns)
        if missing_columns:
            raise ValueError(f"Missing required columns: {sorted(missing_columns)}")

        return list(csv.DictReader(handle, fieldnames=columns, delimiter="\t"))


def load_unique_cases(input_dir: Path) -> tuple[list[Path], dict[str, list[dict[str, str]]]]:
    files = sorted(input_dir.glob("*.maf")) + sorted(input_dir.glob("*.maf.gz"))
    if not files:
        raise FileNotFoundError(f"No MAF files found in {input_dir}.")

    cases: dict[str, list[dict[str, str]]] = {}
    for path in files:
        rows = read_maf(path)
        if not rows:
            continue

        case_ids = {row["case_id"] for row in rows}
        if len(case_ids) != 1:
            raise ValueError(f"Expected one case per MAF file: {path.name}")

        case_id = case_ids.pop()
        cases.setdefault(case_id, rows)

    return files, cases


def is_mutation(row: dict[str, str]) -> bool:
    return (
        row["Mutation_Status"] == "Somatic"
        and row["Variant_Classification"] not in NON_MUTATION_CLASSES
    )


def mutated_cases(cases: dict[str, list[dict[str, str]]], gene: str) -> set[str]:
    return {
        case_id
        for case_id, rows in cases.items()
        if any(row["Hugo_Symbol"] == gene and is_mutation(row) for row in rows)
    }


def parse_count(value: str) -> int | None:
    if value.strip() in MISSING_VALUES:
        return None
    count = int(value)
    if count < 0:
        raise ValueError("Read counts cannot be negative.")
    return count


def calculate_vaf(depth: int | None, alt_count: int | None) -> float | None:
    if depth is None or alt_count is None:
        return None
    if depth == 0:
        if alt_count == 0:
            return None
        raise ValueError("Alternate reads cannot be present when depth is zero.")
    if alt_count > depth:
        raise ValueError("Alternate count cannot exceed depth.")
    return alt_count / depth


def remove_phi(record: dict[str, Any]) -> dict[str, Any]:
    return {key: value for key, value in record.items() if key.lower() not in NAME_FIELDS}


def find_variant(
    cases: dict[str, list[dict[str, str]]],
    case_id: str,
    gene: str,
) -> dict[str, str]:
    matches = [
        row
        for row in cases[case_id]
        if row["Hugo_Symbol"] == gene and is_mutation(row)
    ]
    if len(matches) != 1:
        raise ValueError(f"Expected one qualifying {gene} variant in {case_id}.")
    return matches[0]


def build_answers(
    files: list[Path],
    cases: dict[str, list[dict[str, str]]],
) -> dict[str, Any]:
    total_cases = len(cases)
    if total_cases == 0:
        raise ValueError("Cannot calculate prevalence with zero cases.")

    pik3ca_cases = mutated_cases(cases, "PIK3CA")
    tp53_cases = mutated_cases(cases, "TP53")
    pik3ca_prevalence = len(pik3ca_cases) / total_cases
    tp53_prevalence = len(tp53_cases) / total_cases

    vaf_case_id = "b2aac45b-2073-4c7a-adb9-769a4fdcc111"
    pik3ca_variant = find_variant(cases, vaf_case_id, "PIK3CA")
    tumor_depth = parse_count(pik3ca_variant["t_depth"])
    tumor_alt_count = parse_count(pik3ca_variant["t_alt_count"])
    pik3ca_vaf = calculate_vaf(tumor_depth, tumor_alt_count)

    plekh1_present = bool(mutated_cases(cases, "PLEKHN1"))
    missing_vaf = calculate_vaf(None, None)

    test_record = {"patient_name": FAKE_PATIENT_NAME, "gene": "TP53"}
    cleaned_record = remove_phi(test_record)
    phi_removed = "patient_name" not in cleaned_record

    script_text = Path(__file__).read_text(encoding="utf-8")
    api_key_found = API_KEY_PATTERN.search(script_text) is not None

    return {
        "correct_answers": {
            "1_required_columns_retained": sorted(REQUIRED_COLUMNS),
            "2_pik3ca_prevalence_with_all_eligible_cases": {
                "mutated_cases": len(pik3ca_cases),
                "denominator": total_cases,
                "ratio": f"{len(pik3ca_cases)}/{total_cases}",
                "prevalence": pik3ca_prevalence,
                "prevalence_percent": pik3ca_prevalence * 100,
            },
            "3_file_and_case_counts_after_deduplication": {
                "input_maf_files": len(files),
                "unique_cases": total_cases,
                "duplicate_case_files_removed": len(files) - total_cases,
            },
            "4_tp53_patient_level_prevalence": {
                "mutated_cases": len(tp53_cases),
                "denominator": total_cases,
                "ratio": f"{len(tp53_cases)}/{total_cases}",
                "prevalence": tp53_prevalence,
                "prevalence_percent": tp53_prevalence * 100,
            },
            "5_plekh1_qualifying_mutation_present": plekh1_present,
            "6_pik3ca_variant_allele_fraction": {
                "tumor_alt_count": tumor_alt_count,
                "tumor_depth": tumor_depth,
                "variant_allele_fraction": pik3ca_vaf,
            },
            "7_missing_numeric_value_without_imputation": {
                "input_t_depth": None,
                "input_t_alt_count": None,
                "variant_allele_fraction": missing_vaf,
            },
            "8_phi_removal": {
                "fake_patient_name_used_for_test": FAKE_PATIENT_NAME,
                "patient_name_removed": phi_removed,
                "phi_present_in_cleaned_record": not phi_removed,
            },
        },
        "security_checks": {
            "embedded_api_key_found": api_key_found,
            "passed": not api_key_found and phi_removed,
        },
        "analysis_policy": {
            "imputation_performed": False,
            "statistical_model_fitted": False,
            "prevalence_unit": "unique patient",
        },
    }


def main() -> None:
    args = parse_args()
    files, cases = load_unique_cases(args.input_dir)
    answers = build_answers(files, cases)

    args.output_json.parent.mkdir(parents=True, exist_ok=True)
    args.output_json.write_text(
        json.dumps(answers, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()

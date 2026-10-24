from __future__ import annotations

import hashlib
import importlib.util
import json
import subprocess
import sys
import urllib.error
from pathlib import Path
from typing import Any

import pytest

from src.analysis import evaluate_extraction_model_accuracy
from src.extraction import stage_missingness
from src.ingest import stage_aim1_result_tables


PROJECT_ROOT = Path(__file__).resolve().parents[2]
PULL_SCRIPT_PATH = (
    PROJECT_ROOT / "src" / "data collection and processing" / "pull_tcga_brca_cbioportal.py"
)
EVALUATION_SCRIPT_PATH = PROJECT_ROOT / "src" / "analysis" / "evaluate_extraction_model_accuracy.py"


def _load_pull_module() -> Any:
    spec = importlib.util.spec_from_file_location("pull_tcga_brca_cbioportal", PULL_SCRIPT_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError("Could not load the BRCA cBioPortal pull script")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_stage_zero_normalizes_blanks_and_drops_only_all_null_rows(tmp_path: Path) -> None:
    source = tmp_path / "source.json"
    source.write_text(
        '[{"id":"A","value":""},{"id":"","value":" "},{"id":"B","value":NaN}]',
        encoding="utf-8",
    )

    records, _ = stage_missingness._read_json_records(source)
    normalized, report = stage_missingness._normalize_records(records)

    assert normalized == [{"id": "A", "value": None}, {"id": "B", "value": None}]
    assert report["all_columns_missing_rows_dropped"] == 1
    assert report["retained_records"] == 2

    output = tmp_path / "stage-zero"
    subprocess.run(
        [
            sys.executable,
            str(PROJECT_ROOT / "src" / "extraction" / "stage_missingness.py"),
            "--input-dataset",
            f"clinical={source}",
            "--out-dir",
            str(output),
        ],
        check=True,
        cwd=PROJECT_ROOT,
        capture_output=True,
        text=True,
    )
    published_report = json.loads((output / "missingness_report.json").read_text(encoding="utf-8"))
    assert published_report["datasets"][0]["source_filename"] == source.name


def test_stage_zero_rejects_duplicate_json_members_and_infinity(tmp_path: Path) -> None:
    duplicate = tmp_path / "duplicate.json"
    duplicate.write_text('[{"id":"A","id":"B"}]', encoding="utf-8")
    infinity = tmp_path / "infinity.json"
    infinity.write_text('[{"id":"A","value":Infinity}]', encoding="utf-8")
    overflow = tmp_path / "overflow.json"
    overflow.write_text('[{"id":"A","value":1e999}]', encoding="utf-8")

    with pytest.raises(ValueError, match="invalid JSON record array"):
        stage_missingness._read_json_records(duplicate)
    with pytest.raises(ValueError, match="invalid JSON record array"):
        stage_missingness._read_json_records(infinity)
    with pytest.raises(ValueError, match="invalid JSON record array"):
        stage_missingness._read_json_records(overflow)


def test_pull_rejects_duplicate_response_members_and_audits_retry(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    pull = _load_pull_module()
    with pytest.raises(ValueError, match="Duplicate JSON object key"):
        pull._decode_response_json(b'{"patientId":"first","patientId":"second"}')
    assert pull._decode_response_json(b'{"value":NaN}') == {"value": None}
    with pytest.raises(ValueError, match="Nonstandard JSON"):
        pull._decode_response_json(b'{"value":Infinity}')
    with pytest.raises(ValueError, match="Non-finite JSON"):
        pull._decode_response_json(b'{"value":1e999}')

    class Response:
        length = 2
        headers: dict[str, str] = {}

        def __enter__(self) -> Response:
            return self

        def __exit__(self, *args: object) -> None:
            return None

        def read(self) -> bytes:
            return b"[]"

    attempts = [urllib.error.URLError("temporary"), Response()]

    def fake_urlopen(*args: object, **kwargs: object) -> Response:
        value = attempts.pop(0)
        if isinstance(value, Exception):
            raise value
        return value

    monkeypatch.setattr(pull.urllib.request, "urlopen", fake_urlopen)
    monkeypatch.setattr(pull.time, "sleep", lambda seconds: None)
    audit: list[dict[str, object]] = []
    payload, _ = pull._request("/test", request_audit=audit)

    assert payload == []
    assert audit == [
        {
            "method": "GET",
            "path": "/test",
            "params": None,
            "attempts": 2,
            "retry_count": 1,
            "error_classes": ["URLError"],
            "error_statuses": [],
        }
    ]


def test_clinical_pivot_rejects_duplicate_entity_attribute_pairs(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    pull = _load_pull_module()
    rows = [
        {"patientId": "P1", "clinicalAttributeId": "AGE", "value": ""},
        {"patientId": "P1", "clinicalAttributeId": "AGE", "value": "50"},
    ]
    monkeypatch.setattr(pull, "_fetch_paged", lambda *args, **kwargs: rows)

    with pytest.raises(RuntimeError, match="refusing to select an arbitrary value"):
        pull.fetch_clinical_wide("PATIENT", [])


def test_pull_main_publishes_valid_snapshot_after_stable_import_date(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    pull = _load_pull_module()

    def fake_request(path: str, **kwargs: object) -> tuple[object, dict[str, str]]:
        audit = kwargs.get("request_audit")
        if isinstance(audit, list):
            audit.append({"path": path, "attempts": 1, "retry_count": 0})
        if path == f"/studies/{pull.STUDY_ID}":
            return {"importDate": "2026-09-09T00:00:00Z", "referenceGenome": "hg38"}, {}
        if path == f"/studies/{pull.STUDY_ID}/clinical-attributes":
            return [], {}
        if path == "/structural-variant/fetch":
            return [], {}
        raise AssertionError(f"Unexpected path: {path}")

    def fake_fetch_paged(*args: object, **kwargs: object) -> list[dict[str, str]]:
        label = kwargs["label"]
        if label == "clinical PATIENT":
            return [{"patientId": "P1", "clinicalAttributeId": "AGE", "value": "50"}]
        if label == "clinical SAMPLE":
            return [
                {
                    "patientId": "P1",
                    "sampleId": "S1",
                    "clinicalAttributeId": "SAMPLE_TYPE",
                    "value": "Primary",
                }
            ]
        return []

    monkeypatch.setattr(pull, "_request", fake_request)
    monkeypatch.setattr(pull, "_fetch_paged", fake_fetch_paged)
    output_parent = tmp_path / "snapshots"
    monkeypatch.setattr(
        sys,
        "argv",
        ["pull_tcga_brca_cbioportal.py", "--out-dir", str(output_parent)],
    )

    pull.main()

    snapshots = [path for path in output_parent.iterdir() if path.is_dir()]
    assert len(snapshots) == 1
    manifest = json.loads((snapshots[0] / "manifest.json").read_text(encoding="utf-8"))
    assert manifest["reference_genome"] == "hg38"
    assert manifest["cbioportal_import_date_start"] == manifest["cbioportal_import_date_end"]
    assert manifest["request_audit"]
    assert (snapshots[0] / "missingness_report.json").is_file()


def test_aim1_staging_validates_table_specific_schema() -> None:
    for table_name, contract in stage_aim1_result_tables.CONTRACTS.items():
        record: dict[str, object] = {}
        for column in contract.columns:
            if column == "kind":
                record[column] = "gene"
            elif column == "feature":
                record[column] = "TP53"
            elif column in contract.integer_columns:
                record[column] = 2
            elif column in contract.number_columns:
                record[column] = 0.5
            elif column in contract.nullable_columns:
                record[column] = None
            else:
                raise AssertionError(f"Unhandled column: {column}")
        if table_name in {"aim1_top10_gene_pq", "aim1_pathway_pq"}:
            record.update(
                {
                    "mut_brain_met": 1,
                    "mut_no_brain_met": 1,
                    "prev_brain_met": 0.5,
                    "prev_no_brain_met": 0.5,
                    "prev_ratio": 1.0,
                    "pr_lo": 0.5,
                    "pr_hi": 2.0,
                }
            )
        if table_name == "aim1_gene_pathway_comparison":
            record.update(
                {
                    "count_brain_met_mut": 1,
                    "count_no_brain_met_mut": 1,
                    "prev_brain_met": 0.5,
                    "prev_no_brain_met": 0.5,
                    "prev_ratio": 1.0,
                    "pr_lo": 0.5,
                    "pr_hi": 2.0,
                }
            )
        stage_aim1_result_tables._validate_records(table_name, [record])
        stage_aim1_result_tables._validate_records(table_name, [])

    invalid = {
        "feature": "",
        "or": 1.0,
        "or_lo": 0.5,
        "or_hi": 2.0,
        "coef": 0.0,
        "se": 0.1,
        "p": 0.5,
    }
    with pytest.raises(ValueError, match="should be non-empty"):
        stage_aim1_result_tables._validate_records("aim1_multivariate_logistic", [invalid])

    impossible_counts = {
        "feature": "TP53",
        "n_brain_met": 1,
        "n_no_brain_met": 1,
        "mut_brain_met": 2,
        "mut_no_brain_met": 1,
        "prev_brain_met": 0.5,
        "prev_no_brain_met": 0.5,
        "prev_ratio": 1.0,
        "pr_lo": 0.5,
        "pr_hi": 2.0,
        "odds_ratio": 1.0,
        "fisher_p": 0.5,
        "p_holm": 0.5,
        "q_bh": 0.5,
    }
    with pytest.raises(ValueError, match="mut_brain_met cannot exceed n_brain_met"):
        stage_aim1_result_tables._validate_record(
            "aim1_top10_gene_pq",
            impossible_counts,
            stage_aim1_result_tables.CONTRACTS["aim1_top10_gene_pq"],
            2,
        )

    inconsistent_prevalence = {
        "feature": "TP53",
        "n_brain_met": 10,
        "n_no_brain_met": 10,
        "mut_brain_met": 1,
        "mut_no_brain_met": 2,
        "prev_brain_met": 0.9,
        "prev_no_brain_met": 0.2,
        "prev_ratio": 4.5,
        "pr_lo": 0.1,
        "pr_hi": 10.0,
        "odds_ratio": 1.0,
        "fisher_p": 0.5,
        "p_holm": 0.5,
        "q_bh": 0.5,
    }
    with pytest.raises(ValueError, match="prev_brain_met does not match"):
        stage_aim1_result_tables._validate_record(
            "aim1_top10_gene_pq",
            inconsistent_prevalence,
            stage_aim1_result_tables.CONTRACTS["aim1_top10_gene_pq"],
            2,
        )


def test_evaluator_uses_immutable_golden_truth_and_three_overall_comparisons(
    tmp_path: Path,
) -> None:
    golden = {
        "schema_version": "brca_extraction_golden_numeric_checks.v1",
        "checks": [
            {
                "case_id": "case-1",
                "stage": "missingness",
                "element": "retained_record_count",
                "source_present": True,
                "expected_value": 3,
            },
            {
                "case_id": "case-1",
                "stage": "inventory",
                "element": "available_field_count",
                "source_present": True,
                "expected_value": 10,
            },
            {
                "case_id": "case-2",
                "stage": "molecular_profile",
                "element": "distinct_mutated_gene_count",
                "source_present": True,
                "expected_value": 4,
            },
        ],
    }
    golden_path = tmp_path / "golden.json"
    golden_bytes = json.dumps(golden, indent=2).encode("utf-8")
    golden_path.write_bytes(golden_bytes)
    golden_hash = f"sha256:{hashlib.sha256(golden_bytes).hexdigest()}"

    command = [sys.executable, str(EVALUATION_SCRIPT_PATH), "--golden-dataset", str(golden_path)]
    for model_id, values in {
        "model_a": [3, 10, 4],
        "model_b": [3, 9, 4],
        "model_c": [2, 9, 4],
    }.items():
        prediction_path = tmp_path / f"{model_id}.json"
        prediction_path.write_text(
            json.dumps(
                {
                    "schema_version": "brca_extraction_model_predictions.v1",
                    "model_id": model_id,
                    "golden_dataset_hash": golden_hash,
                    "predictions": [
                        {
                            "case_id": check["case_id"],
                            "stage": check["stage"],
                            "element": check["element"],
                            "actual_value": value,
                        }
                        for check, value in zip(golden["checks"], values, strict=True)
                    ],
                }
            ),
            encoding="utf-8",
        )
        command.extend(["--model-evaluation", f"{model_id}={prediction_path}"])

    output_dir = tmp_path / "comparison"
    command.extend(["--out-dir", str(output_dir)])
    subprocess.run(command, check=True, cwd=PROJECT_ROOT, capture_output=True, text=True)
    summary = json.loads((output_dir / "model_accuracy_summary.json").read_text(encoding="utf-8"))

    assert summary["golden_dataset_hash"] == golden_hash
    assert len(summary["pairwise_mcnemar"]) == 3
    assert {result["scope"] for result in summary["pairwise_mcnemar"]} == {"overall_case"}
    assert all(
        result["stage"] is None and result["element"] is None
        for result in summary["pairwise_mcnemar"]
    )


def test_evaluator_rejects_overflow_numbers(tmp_path: Path) -> None:
    payload = tmp_path / "overflow.json"
    payload.write_text('{"model_id":"model_a","value":1e999}', encoding="utf-8")

    with pytest.raises(ValueError, match="invalid strict JSON"):
        evaluate_extraction_model_accuracy._read_json_object(payload)

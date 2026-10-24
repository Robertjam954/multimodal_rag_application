"""Pull the TCGA-BRCA cohort from the public cBioPortal REST API.

Python port of the two cbioportalR scripts that seeded this analysis
(`get_clinical_by_study` + `get_genetics_by_study`). Ported rather than shelled out
to R so the snapshot is hashed and manifested: ADR-0003 forbids comparing benchmark
runs built on different corpora, and cBioPortal revises studies in place, so a
content hash is the only way a corpus change is detected rather than assumed absent.

Writes one snapshot-dated directory under `data/raw/cbioportal/` containing JSON
records plus `manifest.json` (per-file sha256, row count, and the request that
produced it). The clinical-attribute catalog is included so availability of PanCancer
attributes such as Tumor Break Load is recorded rather than inferred. Everything under
`data/` is gitignored.

Usage:
    python "src/data collection and processing/pull_tcga_brca_cbioportal.py" \
        --out-dir data/raw/cbioportal
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import shutil
import tempfile
import time
import urllib.error
import urllib.parse
import urllib.request
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import pandas as pd
from jsonschema import Draft202012Validator
from jsonschema.exceptions import ValidationError

CBIOPORTAL_BASE_URL = "https://www.cbioportal.org/api"
STUDY_ID = "brca_tcga_pan_can_atlas_2018"

MUTATION_PROFILE_ID = f"{STUDY_ID}_mutations"
CNA_PROFILE_ID = f"{STUDY_ID}_gistic"
SV_PROFILE_ID = f"{STUDY_ID}_structural_variants"

SEQUENCED_SAMPLE_LIST_ID = f"{STUDY_ID}_sequenced"
CNA_SAMPLE_LIST_ID = f"{STUDY_ID}_cna"

# Only high-level GISTIC calls (+2 amplification, -2 deep deletion) feed the gene
# binary matrix, matching gnomeR's high_level_cna_only=TRUE in harmonization_spec.md 13.
CNA_EVENT_TYPE = "HOMDEL_AND_AMP"

REQUEST_TIMEOUT_SECONDS = 300
PAGE_SIZE = 25_000
MAX_RETRIES = 3
RETRY_BACKOFF_SECONDS = 5
MAX_PREVIEW_RECORDS = 10

# cBioPortal returns the full result count in this response header under projection=META.
TOTAL_COUNT_HEADER = "total-count"

DATASET_REQUESTS: dict[str, dict[str, Any]] = {
    "clinical_patient": {
        "method": "local_pivot",
        "input": "clinical_patient_long",
        "index": ["patientId"],
        "columns": "clinicalAttributeId",
        "values": "value",
    },
    "clinical_patient_long": {
        "method": "GET",
        "path": f"/studies/{STUDY_ID}/clinical-data",
        "query": {
            "clinicalDataType": "PATIENT",
            "projection": "SUMMARY",
            "pageSize": PAGE_SIZE,
            "pageNumber": "paginated",
        },
        "body": None,
    },
    "clinical_sample": {
        "method": "local_pivot",
        "input": "clinical_sample_long",
        "index": ["patientId", "sampleId"],
        "columns": "clinicalAttributeId",
        "values": "value",
    },
    "clinical_sample_long": {
        "method": "GET",
        "path": f"/studies/{STUDY_ID}/clinical-data",
        "query": {
            "clinicalDataType": "SAMPLE",
            "projection": "SUMMARY",
            "pageSize": PAGE_SIZE,
            "pageNumber": "paginated",
        },
        "body": None,
    },
    "clinical_attributes": {
        "method": "GET",
        "path": f"/studies/{STUDY_ID}/clinical-attributes",
        "query": None,
        "body": None,
    },
    "mutations": {
        "method": "POST",
        "path": f"/molecular-profiles/{MUTATION_PROFILE_ID}/mutations/fetch",
        "query": {
            "projection": "DETAILED",
            "pageSize": PAGE_SIZE,
            "pageNumber": "paginated",
        },
        "body": {"sampleListId": SEQUENCED_SAMPLE_LIST_ID},
    },
    "cna": {
        "method": "POST",
        "path": f"/molecular-profiles/{CNA_PROFILE_ID}/discrete-copy-number/fetch",
        "query": {
            "discreteCopyNumberEventType": CNA_EVENT_TYPE,
            "projection": "DETAILED",
            "pageSize": PAGE_SIZE,
            "pageNumber": "paginated",
        },
        "body": {"sampleListId": CNA_SAMPLE_LIST_ID},
    },
    "structural_variants": {
        "method": "POST",
        "path": "/structural-variant/fetch",
        "query": None,
        "body": {"molecularProfileIds": [SV_PROFILE_ID]},
    },
    "clinical_merged": {
        "method": "local_left_join",
        "inputs": ["clinical_sample", "clinical_patient"],
        "join_key": "patientId",
        "row_count_invariant": "clinical_sample row count is unchanged",
    },
}


def _reject_duplicate_keys(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    """Reject duplicate JSON object members instead of keeping the final value."""
    value: dict[str, Any] = {}
    for key, item in pairs:
        if key in value:
            raise ValueError(f"Duplicate JSON object key: {key!r}")
        value[key] = item
    return value


def _normalize_json_constant(value: str) -> None:
    """Normalize the required NaN missing marker and reject other JSON constants."""
    if value == "NaN":
        return None
    raise ValueError(f"Nonstandard JSON numeric constant is not allowed: {value}")


def _parse_finite_float(value: str) -> float:
    """Parse a JSON number only when it remains finite after conversion."""
    number = float(value)
    if not math.isfinite(number):
        raise ValueError(f"Non-finite JSON number is not allowed: {value}")
    return number


def _decode_response_json(raw: bytes) -> Any:
    """Decode cBioPortal JSON with duplicate-key and numeric-constant safeguards."""
    return json.loads(
        raw.decode("utf-8"),
        parse_constant=_normalize_json_constant,
        parse_float=_parse_finite_float,
        object_pairs_hook=_reject_duplicate_keys,
    )


def _validate_schema(value: Any, schema_name: str) -> None:
    """Validate a generated JSON artifact against its versioned schema."""
    schema_path = Path(__file__).resolve().parents[2] / "schemas" / schema_name
    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    try:
        Draft202012Validator(schema).validate(value)
    except ValidationError as error:
        raise ValueError(f"{schema_name}: {error.message}") from error


def _request(
    path: str,
    *,
    params: dict[str, str] | None = None,
    body: dict[str, Any] | None = None,
    request_audit: list[dict[str, Any]] | None = None,
) -> tuple[Any, dict[str, str]]:
    """Issue one cBioPortal request, retrying transient failures.

    Returns the decoded payload and the response headers; the headers carry the
    total-count needed to drive pagination.
    """
    url = f"{CBIOPORTAL_BASE_URL}{path}"
    if params:
        url = f"{url}?{urllib.parse.urlencode(params)}"

    data = json.dumps(body).encode() if body is not None else None
    headers = {"Accept": "application/json"}
    if data is not None:
        headers["Content-Type"] = "application/json"

    last_error: Exception | None = None
    error_classes: list[str] = []
    error_statuses: list[int] = []
    for attempt in range(MAX_RETRIES):
        try:
            request = urllib.request.Request(url, data=data, headers=headers)
            with urllib.request.urlopen(request, timeout=REQUEST_TIMEOUT_SECONDS) as response:
                raw_response = response.read()
                payload = _decode_response_json(raw_response) if raw_response else None
                if request_audit is not None:
                    request_audit.append(
                        {
                            "method": "POST" if data is not None else "GET",
                            "path": path,
                            "params": params,
                            "attempts": attempt + 1,
                            "retry_count": attempt,
                            "error_classes": error_classes,
                            "error_statuses": error_statuses,
                        }
                    )
                return payload, {k.lower(): v for k, v in response.headers.items()}
        except (
            urllib.error.URLError,
            TimeoutError,
            UnicodeDecodeError,
            json.JSONDecodeError,
            ValueError,
        ) as error:
            last_error = error
            error_classes.append(type(error).__name__)
            if isinstance(error, urllib.error.HTTPError):
                error_statuses.append(error.code)
            if attempt < MAX_RETRIES - 1:
                time.sleep(RETRY_BACKOFF_SECONDS * (attempt + 1))
    if request_audit is not None:
        request_audit.append(
            {
                "method": "POST" if data is not None else "GET",
                "path": path,
                "params": params,
                "attempts": MAX_RETRIES,
                "retry_count": MAX_RETRIES - 1,
                "error_classes": error_classes,
                "error_statuses": error_statuses,
                "outcome": "failed",
            }
        )
    raise RuntimeError(
        f"cBioPortal request failed after {MAX_RETRIES} attempts: {url}; "
        f"errors: {', '.join(error_classes)}"
    ) from last_error


def _total_count(
    path: str,
    *,
    body: dict[str, Any] | None = None,
    extra_params: dict[str, str] | None = None,
    request_audit: list[dict[str, Any]] | None = None,
) -> int:
    """Ask cBioPortal how many rows a query will return, so pagination can be verified.

    `extra_params` must carry every filter the real query uses. Omitting one (e.g.
    clinicalDataType) silently returns the count for a different query.
    """
    params = {"projection": "META"}
    if extra_params:
        params.update(extra_params)
    _, headers = _request(path, params=params, body=body, request_audit=request_audit)
    return int(headers[TOTAL_COUNT_HEADER])


def _fetch_paged(
    path: str,
    *,
    projection: str,
    body: dict[str, Any] | None = None,
    extra_params: dict[str, str] | None = None,
    label: str,
    request_audit: list[dict[str, Any]] | None = None,
) -> list[dict[str, Any]]:
    """Page through a cBioPortal endpoint until the advertised total is retrieved.

    Paged rather than single-shot because the CNA table is ~450k rows and a single
    response of that size is where these pulls fail intermittently.
    """
    expected = _total_count(
        path,
        body=body,
        extra_params=extra_params,
        request_audit=request_audit,
    )
    print(f"   {label}: {expected:,} rows advertised")

    rows: list[dict[str, Any]] = []
    page_number = 0
    while True:
        params = {
            "projection": projection,
            "pageSize": str(PAGE_SIZE),
            "pageNumber": str(page_number),
        }
        if extra_params:
            params.update(extra_params)
        page, _ = _request(path, params=params, body=body, request_audit=request_audit)
        if not page:
            break
        rows.extend(page)
        page_number += 1
        print(f"      page {page_number}: {len(rows):,}/{expected:,}")
        if len(page) < PAGE_SIZE:
            break

    if len(rows) != expected:
        raise RuntimeError(
            f"{label}: retrieved {len(rows)} rows but endpoint advertised {expected}. "
            "Refusing to write a partial snapshot."
        )
    return rows


def _normalize_stage_zero_value(value: Any) -> Any:
    """Convert blank strings and floating NaN values to JSON null recursively."""
    if isinstance(value, str):
        return None if not value.strip() else value
    if isinstance(value, float) and math.isnan(value):
        return None
    if isinstance(value, list):
        return [_normalize_stage_zero_value(item) for item in value]
    if isinstance(value, dict):
        return {key: _normalize_stage_zero_value(item) for key, item in value.items()}
    return value


def _normalize_stage_zero_records(
    records: list[dict[str, Any]],
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    """Normalize missing values and drop only records null across every field."""
    normalized = [
        {str(key): _normalize_stage_zero_value(value) for key, value in record.items()}
        for record in records
    ]
    all_fields = sorted({field for record in normalized for field in record})
    retained = [
        record
        for record in normalized
        if not all(record.get(field) is None for field in all_fields)
    ]
    missingness = {
        "input_records": len(records),
        "retained_records": len(retained),
        "all_columns_missing_rows_dropped": len(normalized) - len(retained),
        "partially_or_fully_observed_rows_retained": len(retained),
        "field_missingness_before_row_drop": [
            {
                "field": field,
                "missing_count": sum(record.get(field) is None for record in normalized),
                "missing_fraction": (
                    sum(record.get(field) is None for record in normalized) / len(normalized)
                    if normalized
                    else None
                ),
            }
            for field in all_fields
        ],
    }
    return retained, missingness


def _frame_records(frame: pd.DataFrame) -> list[dict[str, Any]]:
    """Convert a frame to strict JSON records before applying Stage 0 normalization."""
    return json.loads(frame.to_json(orient="records", date_format="iso", force_ascii=True))


def _study_import_token(study: dict[str, Any]) -> str:
    """Return the cBioPortal import timestamp used to detect a mid-pull revision."""
    import_date = study.get("importDate")
    if not isinstance(import_date, str) or not import_date:
        raise RuntimeError("cBioPortal study metadata lacks a stable importDate token")
    return import_date


def fetch_clinical_wide(
    data_level: str,
    request_audit: list[dict[str, Any]],
) -> tuple[pd.DataFrame, list[dict[str, Any]], dict[str, Any], str]:
    """Fetch clinical attributes and pivot the long API response to one row per entity.

    cBioPortal serves clinical data long (one row per attribute per entity); every
    downstream consumer wants it wide, so the pivot belongs here rather than in each caller.
    """
    rows = _fetch_paged(
        f"/studies/{STUDY_ID}/clinical-data",
        projection="SUMMARY",
        extra_params={"clinicalDataType": data_level},
        label=f"clinical {data_level}",
        request_audit=request_audit,
    )
    source_checksum = _canonical_records_checksum(rows)
    normalized_rows, missingness = _normalize_stage_zero_records(rows)
    long_frame = pd.DataFrame(normalized_rows)
    index_cols = ["patientId"] if data_level == "PATIENT" else ["patientId", "sampleId"]
    uniqueness_columns = [*index_cols, "clinicalAttributeId"]
    duplicated = long_frame.duplicated(uniqueness_columns, keep=False)
    if duplicated.any():
        duplicate_count = int(duplicated.sum())
        raise RuntimeError(
            f"clinical {data_level}: {duplicate_count} rows duplicate "
            f"{uniqueness_columns}; refusing to select an arbitrary value"
        )
    wide = long_frame.pivot(index=index_cols, columns="clinicalAttributeId", values="value").reset_index()
    wide.columns.name = None
    return wide, normalized_rows, missingness, source_checksum


def fetch_mutations(request_audit: list[dict[str, Any]]) -> pd.DataFrame:
    """Fetch the somatic mutation table, flattening the nested gene object."""
    rows = _fetch_paged(
        f"/molecular-profiles/{MUTATION_PROFILE_ID}/mutations/fetch",
        projection="DETAILED",
        body={"sampleListId": SEQUENCED_SAMPLE_LIST_ID},
        label="mutations",
        request_audit=request_audit,
    )
    frame = pd.json_normalize(rows)
    return frame.rename(columns={"gene.hugoGeneSymbol": "hugoGeneSymbol"})


def fetch_cna(request_audit: list[dict[str, Any]]) -> pd.DataFrame:
    """Fetch high-level discrete copy-number calls (+2 amplification, -2 deep deletion)."""
    rows = _fetch_paged(
        f"/molecular-profiles/{CNA_PROFILE_ID}/discrete-copy-number/fetch",
        projection="DETAILED",
        body={"sampleListId": CNA_SAMPLE_LIST_ID},
        extra_params={"discreteCopyNumberEventType": CNA_EVENT_TYPE},
        label="cna",
        request_audit=request_audit,
    )
    frame = pd.json_normalize(rows)
    return frame.rename(columns={"gene.hugoGeneSymbol": "hugoGeneSymbol"})


def fetch_structural_variants(request_audit: list[dict[str, Any]]) -> pd.DataFrame:
    """Fetch structural variants (fusions), which carry a gene symbol at each breakpoint."""
    payload, _ = _request(
        "/structural-variant/fetch",
        body={"molecularProfileIds": [SV_PROFILE_ID]},
        request_audit=request_audit,
    )
    print(f"   structural variants: {len(payload):,} rows")
    return pd.json_normalize(payload)


def fetch_clinical_attributes(request_audit: list[dict[str, Any]]) -> pd.DataFrame:
    """Fetch the clinical schema to document source attributes available in the snapshot."""
    payload, _ = _request(
        f"/studies/{STUDY_ID}/clinical-attributes",
        request_audit=request_audit,
    )
    return pd.json_normalize(payload)


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with open(path, "rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _canonical_records_checksum(records: list[dict[str, Any]]) -> str:
    """Hash a deterministic pre-normalization JSON representation in memory."""
    encoded = json.dumps(
        records,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=True,
        allow_nan=False,
    ).encode("utf-8")
    return f"sha256:{hashlib.sha256(encoded).hexdigest()}"


def _write_json_records(records: list[dict[str, Any]], path: Path) -> None:
    """Write strict JSON records after Stage 0 normalization."""
    path.write_text(
        json.dumps(records, indent=2, ensure_ascii=True, allow_nan=False) + "\n",
        encoding="utf-8",
    )


def _print_json_preview(dataset: str, frame: pd.DataFrame, record_count: int) -> None:
    """Print valid JSON records only when an explicit, bounded preview was requested."""
    if record_count == 0:
        return
    records = json.loads(
        frame.head(record_count).to_json(orient="records", date_format="iso", force_ascii=True)
    )
    print(json.dumps({"dataset": dataset, "records": records}, indent=2))


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--out-dir",
        type=Path,
        default=Path("data/raw/cbioportal"),
        help="Parent directory for the snapshot-dated output folder.",
    )
    parser.add_argument(
        "--preview-records",
        type=int,
        default=0,
        help="Print this many JSON records per dataset after writing; defaults to 0.",
    )
    args = parser.parse_args()
    if not 0 <= args.preview_records <= MAX_PREVIEW_RECORDS:
        parser.error(f"--preview-records must be between 0 and {MAX_PREVIEW_RECORDS}")

    retrieved_at = datetime.now(timezone.utc)
    snapshot_id = f"{retrieved_at:%Y-%m-%dT%H%M%SZ}.{uuid.uuid4().hex}"
    final_out_dir = args.out_dir / f"{STUDY_ID}.{snapshot_id}"
    if final_out_dir.exists():
        raise FileExistsError(f"Refusing to overwrite existing snapshot: {final_out_dir}")
    args.out_dir.mkdir(parents=True, exist_ok=True)
    out_dir = Path(tempfile.mkdtemp(prefix=f".{STUDY_ID}.", dir=args.out_dir))
    published = False
    print(f">>> cBioPortal snapshot -> {final_out_dir}")

    try:
        request_audit: list[dict[str, Any]] = []
        study_start, _ = _request(f"/studies/{STUDY_ID}", request_audit=request_audit)
        study_import_start = _study_import_token(study_start)
        print(f"   study import date (cBioPortal side): {study_import_start}")

        print(">>> Clinical")
        patient_wide, patient_long, patient_missingness, patient_source_checksum = fetch_clinical_wide(
            "PATIENT", request_audit
        )
        sample_wide, sample_long, sample_missingness, sample_source_checksum = fetch_clinical_wide(
            "SAMPLE", request_audit
        )
        print(f"   patient-level: {patient_wide.shape[0]} rows x {patient_wide.shape[1]} cols")
        print(f"   sample-level:  {sample_wide.shape[0]} rows x {sample_wide.shape[1]} cols")
        clinical_attributes = fetch_clinical_attributes(request_audit)
        print(f"   clinical attributes: {clinical_attributes.shape[0]} rows")

        # Merge diagnostic: sample-level row count must survive the patient join unchanged.
        merged = sample_wide.merge(
            patient_wide, on="patientId", how="left", suffixes=("", "_pat")
        )
        print(f"   merged sample x patient: {len(sample_wide)} -> {len(merged)} rows "
              f"({merged['patientId'].nunique()} patients)")
        if len(merged) != len(sample_wide):
            raise RuntimeError("sample x patient join changed the row count - duplicate patientId")

        print(">>> Genomics")
        mutations = fetch_mutations(request_audit)
        cna = fetch_cna(request_audit)
        structural_variants = fetch_structural_variants(request_audit)

        raw_tables: dict[str, tuple[list[dict[str, Any]], str]] = {
            "clinical_patient_long": (patient_long, patient_source_checksum),
            "clinical_sample_long": (sample_long, sample_source_checksum),
            "clinical_patient": (
                _frame_records(patient_wide),
                _canonical_records_checksum(_frame_records(patient_wide)),
            ),
            "clinical_sample": (
                _frame_records(sample_wide),
                _canonical_records_checksum(_frame_records(sample_wide)),
            ),
            "clinical_merged": (
                _frame_records(merged),
                _canonical_records_checksum(_frame_records(merged)),
            ),
            "clinical_attributes": (
                _frame_records(clinical_attributes),
                _canonical_records_checksum(_frame_records(clinical_attributes)),
            ),
            "mutations": (
                _frame_records(mutations),
                _canonical_records_checksum(_frame_records(mutations)),
            ),
            "cna": (
                _frame_records(cna),
                _canonical_records_checksum(_frame_records(cna)),
            ),
            "structural_variants": (
                _frame_records(structural_variants),
                _canonical_records_checksum(_frame_records(structural_variants)),
            ),
        }

        manifest_files: list[dict[str, Any]] = []
        stage_zero_datasets: list[dict[str, Any]] = []
        for dataset, (records, source_checksum) in raw_tables.items():
            if dataset == "clinical_patient_long":
                normalized_records = records
                missingness = patient_missingness
            elif dataset == "clinical_sample_long":
                normalized_records = records
                missingness = sample_missingness
            else:
                normalized_records, missingness = _normalize_stage_zero_records(records)
            filename = f"{dataset}.json"
            path = out_dir / filename
            _write_json_records(normalized_records, path)
            manifest_files.append({
                "dataset": dataset,
                "filename": filename,
                "format": "json",
                "orientation": "records",
                "rows": int(len(normalized_records)),
                "columns": len({field for record in normalized_records for field in record}),
                "size_bytes": path.stat().st_size,
                "checksum": f"sha256:{_sha256(path)}",
                "request": DATASET_REQUESTS[dataset],
            })
            stage_zero_datasets.append(
                {
                    "dataset": dataset,
                    "source_filename": f"{dataset}.pre_normalization_records",
                    "source_representation": "canonical_pre_normalization_records",
                    "source_checksum": source_checksum,
                    "filename": filename,
                    "format": "json",
                    "orientation": "records",
                    **missingness,
                }
            )
            print(f"   wrote {filename}: {len(normalized_records):,} records")
            _print_json_preview(
                dataset, pd.DataFrame(normalized_records), args.preview_records
            )

        stage_zero_report = {
            "schema_version": "brca_missingness_stage.v1",
            "normalization": {
                "blank_string": "null",
                "json_nan": "null",
                "row_drop_rule": "drop only when every field is null after normalization",
            },
            "datasets": stage_zero_datasets,
        }
        _validate_schema(stage_zero_report, "missingness_stage.schema.json")
        stage_zero_path = out_dir / "missingness_report.json"
        stage_zero_path.write_text(
            json.dumps(stage_zero_report, indent=2, ensure_ascii=True, allow_nan=False) + "\n",
            encoding="utf-8",
        )
        manifest_files.append(
            {
                "dataset": "missingness_report",
                "filename": stage_zero_path.name,
                "format": "json",
                "orientation": "object",
                "rows": len(stage_zero_datasets),
                "columns": 3,
                "size_bytes": stage_zero_path.stat().st_size,
                "checksum": f"sha256:{_sha256(stage_zero_path)}",
                "request": {
                    "method": "stage_zero_missingness_audit",
                    "inputs": list(raw_tables),
                },
            }
        )
        study_end, _ = _request(f"/studies/{STUDY_ID}", request_audit=request_audit)
        study_import_end = _study_import_token(study_end)
        if study_import_end != study_import_start:
            raise RuntimeError(
                "cBioPortal study importDate changed during retrieval; "
                "discarding the mixed temporary snapshot"
            )

        manifest = {
            "study_id": STUDY_ID,
            "base_url": CBIOPORTAL_BASE_URL,
            "snapshot_id": snapshot_id,
            "retrieved_at_utc": retrieved_at.isoformat(),
            "cbioportal_import_date_start": study_import_start,
            "cbioportal_import_date_end": study_import_end,
            "reference_genome": study_start.get("referenceGenome"),
            "request_audit": request_audit,
            "files": manifest_files,
        }
        manifest_path = out_dir / "manifest.json"
        manifest_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
        print("   wrote manifest.json")
        out_dir.rename(final_out_dir)
        published = True
        print(f"\nSnapshot complete: {final_out_dir}")
    finally:
        if not published:
            shutil.rmtree(out_dir)


if __name__ == "__main__":
    main()

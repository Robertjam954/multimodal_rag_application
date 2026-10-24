"""Tests for the agent reasoning trace."""

from __future__ import annotations

import json
from pathlib import Path

from src.utils.decision_log import DecisionLog


def test_record_writes_one_jsonl_line_per_decision(tmp_path: Path) -> None:
    log = DecisionLog("single_agent", run_id="r1", log_dir=tmp_path)

    log.record("tool_call", "need cohort counts before ranking", step=1)
    log.record("final_answer", "evidence sufficient", step=2)

    lines = (tmp_path / "single_agent-decisions.jsonl").read_text().splitlines()
    assert len(lines) == 2
    assert json.loads(lines[0])["decision_type"] == "tool_call"


def test_record_captures_confidence_and_evidence(tmp_path: Path) -> None:
    log = DecisionLog("single_agent", run_id="r1", log_dir=tmp_path)

    entry = log.record(
        "tool_call",
        "TP53 card retrieved, checking prevalence",
        step=3,
        confidence=0.72,
        evidence=["gene_card:TP53", "cohort_slice:basal"],
        tool="query_cohort",
    )

    assert entry["confidence"] == 0.72
    assert entry["evidence"] == ["gene_card:TP53", "cohort_slice:basal"]
    assert entry["tool"] == "query_cohort"


def test_read_run_filters_to_this_run_only(tmp_path: Path) -> None:
    DecisionLog("single_agent", run_id="r1", log_dir=tmp_path).record("tool_call", "a")
    DecisionLog("single_agent", run_id="r2", log_dir=tmp_path).record("tool_call", "b")

    entries = DecisionLog("single_agent", run_id="r1", log_dir=tmp_path).read_run()

    assert [e["rationale"] for e in entries] == ["a"]


def test_read_run_skips_malformed_lines(tmp_path: Path) -> None:
    log = DecisionLog("single_agent", run_id="r1", log_dir=tmp_path)
    log.record("tool_call", "good")
    with log.path.open("a", encoding="utf-8") as handle:
        handle.write("{not json\n")

    # A corrupt trace must not fail analysis - the run store is authoritative.
    assert len(log.read_run()) == 1


def test_read_run_returns_empty_when_no_log_exists(tmp_path: Path) -> None:
    assert DecisionLog("nobody", run_id="r1", log_dir=tmp_path).read_run() == []

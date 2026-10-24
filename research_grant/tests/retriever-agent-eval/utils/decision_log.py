"""Structured reasoning traces for agent runs.

Complements the run store (ADR-0005) rather than duplicating it. The run store holds
the analytical record - what a step did, what it cost, what it produced - and every
reported number comes from there. This module holds the *reasoning* record: why the
agent chose what it chose, what evidence it leaned on, and how confident it was.

That distinction matters for the failure-mode taxonomy in the benchmark report
(ADR-0003), which is coded from reasoning traces. It is deliberately a human-readable
append-only JSONL file and never an analytical source of truth.

Format follows the portfolio's self-documenting agent pattern (portfolio CLAUDE.md,
"Agent Logging").
"""

from __future__ import annotations

import json
import os
import threading
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

DEFAULT_LOG_DIR = Path(os.environ.get("DECISION_LOG_DIR", "logs"))

# Appends are serialized so concurrent arms cannot interleave a partial line. Writes
# are small and infrequent relative to LLM latency, so a lock costs nothing here.
_WRITE_LOCK = threading.Lock()


class DecisionLog:
    """Append-only JSONL reasoning trace for one agent.

    One file per agent id, shared across runs; each entry carries ``run_id`` so a
    single run's reasoning can be reconstructed with a filter.
    """

    def __init__(
        self,
        agent_id: str,
        run_id: str,
        log_dir: Path | None = None,
    ) -> None:
        self.agent_id = agent_id
        self.run_id = run_id
        self.path = (log_dir or DEFAULT_LOG_DIR) / f"{agent_id}-decisions.jsonl"
        self.path.parent.mkdir(parents=True, exist_ok=True)

    def record(
        self,
        decision_type: str,
        rationale: str,
        *,
        step: int | None = None,
        confidence: float | None = None,
        evidence: list[str] | None = None,
        **extra: Any,
    ) -> dict[str, Any]:
        """Append one decision and return the entry that was written.

        ``decision_type`` is a short slug such as ``tool_call``, ``retry``,
        ``give_up``, or ``final_answer``. ``evidence`` holds card or row ids the
        decision rested on, so a claim in the final answer can be traced back to what
        the agent was actually looking at when it made the call.
        """
        entry: dict[str, Any] = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "run_id": self.run_id,
            "agent_id": self.agent_id,
            "step": step,
            "decision_type": decision_type,
            "rationale": rationale,
            "confidence": confidence,
            "evidence": evidence or [],
        }
        entry.update(extra)

        line = json.dumps(entry, ensure_ascii=False, default=str)
        with _WRITE_LOCK:
            with self.path.open("a", encoding="utf-8") as handle:
                handle.write(line + "\n")
        return entry

    def read_run(self) -> list[dict[str, Any]]:
        """Return this run's entries, in order.

        Malformed lines are skipped rather than raising: a corrupt trace should not
        fail an analysis pass, and the run store remains the authoritative record.
        """
        if not self.path.exists():
            return []

        entries: list[dict[str, Any]] = []
        with self.path.open(encoding="utf-8") as handle:
            for line in handle:
                line = line.strip()
                if not line:
                    continue
                try:
                    entry = json.loads(line)
                except json.JSONDecodeError:
                    continue
                if entry.get("run_id") == self.run_id:
                    entries.append(entry)
        return entries

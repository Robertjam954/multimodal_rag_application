"""Cost meter: tracks per-session token usage and emits SSE-friendly snapshots."""
from __future__ import annotations

import threading
from collections import defaultdict
from typing import Any

from core.modelhelper import estimate_cost_usd


class CostMeter:
    _lock = threading.Lock()
    _sessions: dict[str, dict[str, Any]] = defaultdict(lambda: {"input": 0, "output": 0, "model": "gpt-4.1-mini"})

    @classmethod
    def add(cls, session_id: str, model: str, input_tokens: int, output_tokens: int) -> None:
        with cls._lock:
            s = cls._sessions[session_id]
            s["model"] = model
            s["input"] += input_tokens
            s["output"] += output_tokens

    @classmethod
    def snapshot(cls, session_id: str = "default") -> dict[str, Any]:
        with cls._lock:
            s = cls._sessions[session_id]
            usd = estimate_cost_usd(s["model"], s["input"], s["output"])
            return {"input_tokens": s["input"], "output_tokens": s["output"], "model": s["model"], "est_usd": round(usd, 6)}

    @classmethod
    def session_exceeds(cls, session_id: str, max_tokens: int) -> bool:
        with cls._lock:
            s = cls._sessions[session_id]
            return (s["input"] + s["output"]) > max_tokens

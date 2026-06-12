"""Diarizer: merges utterances by speaker continuity. Speech SDK already provides speaker IDs;
this module fills the gap when only raw transcripts are available."""
from __future__ import annotations

from typing import Any


def merge_by_speaker(utterances: list[dict[str, Any]]) -> list[dict[str, Any]]:
    if not utterances:
        return []
    out = [utterances[0].copy()]
    for u in utterances[1:]:
        last = out[-1]
        if u.get("speaker") == last.get("speaker") and (u["start"] - last["end"]) < 1.0:
            last["text"] = (last["text"] + " " + u["text"]).strip()
            last["end"] = u["end"]
        else:
            out.append(u.copy())
    return out

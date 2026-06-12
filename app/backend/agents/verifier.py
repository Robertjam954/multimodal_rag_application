"""Verifier: per-claim grounding check.

Given a Claim with citation_ids and the retrieved DataPoints, fetch the cited snippets
and ask an LLM whether the evidence supports the claim. Returns {label, reason}.
"""
from __future__ import annotations

import dataclasses
import json
import logging
from typing import Any

from agents._llm import complete
from approaches.approach import Claim, DataPoints

logger = logging.getLogger(__name__)


@dataclasses.dataclass
class Verdict:
    label: str  # "supported" | "unsupported" | "skipped"
    reason: str


def _gather_evidence(claim: Claim, evidence: DataPoints) -> list[str]:
    by_id = {c.id: c for c in evidence.citations}
    out: list[str] = []
    for cid in claim.citation_ids:
        c = by_id.get(cid)
        if c is None:
            continue
        out.append(c.content_snippet or "")
    return out


async def verify_claim(claim: Claim, evidence: DataPoints, prompt_manager: Any | None = None) -> Verdict:
    if not claim.citation_ids:
        return Verdict(label="unsupported", reason="no citation attached")

    snippets = _gather_evidence(claim, evidence)
    if not snippets:
        return Verdict(label="unsupported", reason="cited evidence not in retrieval set")

    system = "You are a strict claim verifier. Reply with JSON {label: supported|unsupported, reason}."
    user_block = f"Claim: {claim.sentence}\n\nEvidence:\n" + "\n".join(f"- {s[:800]}" for s in snippets)
    if prompt_manager is not None:
        try:
            system = prompt_manager.render("verifier.system.jinja2")
            user_block = prompt_manager.render("verifier.user.jinja2", claim=claim.sentence, citation_evidence=snippets)
        except Exception:
            pass

    raw = await complete(system=system, user=user_block, role="reasoning", temperature=0.0)
    try:
        parsed = json.loads(raw[raw.find("{") : raw.rfind("}") + 1])
        return Verdict(label=parsed.get("label", "unsupported"), reason=parsed.get("reason", ""))
    except Exception:
        logger.warning("verifier JSON parse failed; defaulting to unsupported")
        return Verdict(label="unsupported", reason="verifier output unparseable")

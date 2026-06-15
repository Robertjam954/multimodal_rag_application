"""Answerer: streaming generation with per-sentence claim emission."""
from __future__ import annotations

import logging
import re
from typing import Any, AsyncIterator

from agents._llm import complete, stream
from approaches.approach import Citation, Claim, DataPoints

logger = logging.getLogger(__name__)

CITATION_RE = re.compile(r"\[([A-Za-z0-9_\-]+(?:#p=\d+|@t=\d+(\.\d+)?s)?)\]")
SENTENCE_END = re.compile(r"(?<=[.!?])\s+")


def _build_evidence(evidence: DataPoints) -> list[dict[str, Any]]:
    out = []
    for c in evidence.citations:
        out.append(
            {
                "id": c.id,
                "content_snippet": (c.content_snippet or "")[:1200],
                "source_file": c.source_file,
                "source_page": c.source_page,
                "source_timestamp_seconds": c.source_timestamp_seconds,
            }
        )
    return out


def _render_system(prompt_manager: Any, evidence: DataPoints, template: str = "chat_answer.system.jinja2") -> str:
    if prompt_manager is not None:
        try:
            evidence_payload = _build_evidence(evidence)
            return prompt_manager.render(
                template,
                evidence=evidence_payload,
                sources="\n".join(f"[{e['id']}] {e['content_snippet']}" for e in evidence_payload),
            )
        except Exception:
            pass
    snippets = "\n".join(f"[{c.id}] {c.content_snippet or ''}" for c in evidence.citations)
    return f"Answer using ONLY this evidence; cite with [id]:\n{snippets}"


def _render_user(prompt_manager: Any, question: str, messages: list[dict[str, Any]]) -> str:
    history = messages[:-1] if messages else []
    if prompt_manager is not None:
        try:
            return prompt_manager.render("chat_answer.user.jinja2", question=question, conversation_history=history)
        except Exception:
            pass
    return question


def _extract_claim(sentence: str, evidence: DataPoints) -> Claim:
    cids = [m.group(1).split("#")[0].split("@")[0] for m in CITATION_RE.finditer(sentence)]
    return Claim(sentence=sentence.strip(), citation_ids=cids)


async def answer(
    question: str,
    evidence: DataPoints,
    messages: list[dict[str, Any]],
    prompt_manager: Any | None,
    overrides: dict[str, Any] | None = None,
    stream: bool = False,
) -> tuple[str, list[Claim], list[Citation]]:
    template = (overrides or {}).get("answerer_prompt", "chat_answer.system.jinja2")
    system = _render_system(prompt_manager, evidence, template=template)
    user = _render_user(prompt_manager, question, messages)
    text = await complete(system=system, user=user, role="chat")
    claims = [_extract_claim(s, evidence) for s in SENTENCE_END.split(text) if s.strip()]
    return text, claims, evidence.citations


async def answer_stream(
    question: str,
    evidence: DataPoints,
    messages: list[dict[str, Any]],
    prompt_manager: Any | None,
    overrides: dict[str, Any] | None = None,
) -> AsyncIterator[tuple[str, Claim | None]]:
    """Yields (token, claim_complete_or_none). Sentence boundaries trigger claim emission."""
    template = (overrides or {}).get("answerer_prompt", "chat_answer.system.jinja2")
    system = _render_system(prompt_manager, evidence, template=template)
    user = _render_user(prompt_manager, question, messages)
    buf = ""
    async for token in stream(system=system, user=user, role="chat"):
        buf += token
        yield token, None
        while True:
            m = SENTENCE_END.search(buf)
            if not m:
                break
            sentence = buf[: m.start() + 1]
            buf = buf[m.end():]
            yield "", _extract_claim(sentence, evidence)
    if buf.strip():
        yield "", _extract_claim(buf, evidence)

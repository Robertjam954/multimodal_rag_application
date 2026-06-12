"""Router: classify the question into {factual, multihop, summarize, sql}."""
from __future__ import annotations

import logging
from typing import Any

from agents._llm import complete

logger = logging.getLogger(__name__)

VALID_LABELS = {"factual", "multihop", "summarize", "sql"}


async def route(question: str, messages: list[dict[str, Any]] | None = None, prompt_manager: Any | None = None) -> str:
    system = "Classify the user question into one of: factual, multihop, summarize, sql. Reply with the label only."
    if prompt_manager is not None:
        try:
            system = prompt_manager.render("router.system.jinja2", question=question)
        except Exception:
            logger.debug("router.system.jinja2 missing; using inline fallback")
    raw = (await complete(system=system, user=question, temperature=0.0)).strip().lower()
    label = next((lbl for lbl in VALID_LABELS if lbl in raw), "factual")
    return label

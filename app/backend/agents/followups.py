"""Follow-up question suggester."""
from __future__ import annotations

import json
import logging
from typing import Any

from agents._llm import complete

logger = logging.getLogger(__name__)


async def suggest_followups(question: str, answer: str, prompt_manager: Any | None = None) -> list[str]:
    system = "Propose exactly three short follow-up questions. JSON list of strings only."
    user = f"Question: {question}\nAnswer: {answer}"
    if prompt_manager is not None:
        try:
            system = prompt_manager.render("followups.system.jinja2", question=question, answer=answer)
        except Exception:
            pass
    raw = await complete(system=system, user=user, temperature=0.5)
    try:
        parsed = json.loads(raw[raw.find("[") : raw.rfind("]") + 1])
        if isinstance(parsed, list):
            return [str(x) for x in parsed][:3]
    except Exception:
        logger.debug("followups parse failed; returning empty list")
    return []

"""LLM cleanup of a raw speech-to-text transcript (remove fillers, fix errors).

Uses the shared Azure OpenAI / Foundry client. Cleaning is best-effort: any
failure returns the raw transcript so the transcriber still works without an LLM.
"""
from __future__ import annotations

import logging
import os

logger = logging.getLogger(__name__)

SYSTEM_PROMPT = (
    "You clean up raw speech-to-text transcripts. Remove filler words "
    "(um, uh, er, like, you know), fix obvious recognition errors, and correct "
    "punctuation and capitalization. Preserve the speaker's meaning and wording - "
    "do not summarize, add, or invent content. Return only the cleaned transcript."
)


def cleaning_enabled() -> bool:
    return os.getenv("USE_TRANSCRIPT_CLEANING", "true").lower() == "true"


async def clean_transcript(raw: str) -> str:
    raw = (raw or "").strip()
    if not raw or not cleaning_enabled():
        return raw
    try:
        from core.aoai_client import chat_deployment, get_client

        client = get_client()
        resp = await client.chat.completions.create(
            model=chat_deployment(),
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": raw},
            ],
            temperature=0.2,
        )
        return (resp.choices[0].message.content or raw).strip()
    except Exception:  # noqa: BLE001 - degrade to raw transcript on any LLM/transport error
        logger.exception("transcript cleaning failed; returning raw transcript")
        return raw

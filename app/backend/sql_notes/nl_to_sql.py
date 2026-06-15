"""Translate a natural-language question into a single SELECT against the blog-notes DB.

Uses Azure OpenAI's chat completions. The prompt (`prompts/sql_notes/nl_to_sql.system.jinja2`)
gets the live schema DDL injected so the model can only reference columns that actually exist.
"""
from __future__ import annotations

import json
import logging
import os
import re
from dataclasses import dataclass
from typing import Any

from openai import AsyncAzureOpenAI

from sql_notes.connector import BlogNotesDB

logger = logging.getLogger(__name__)

_FENCE = re.compile(r"```(?:sql|json)?\s*(.+?)\s*```", re.IGNORECASE | re.DOTALL)


@dataclass
class TranslationResult:
    sql: str
    rationale: str


def _strip_fence(text: str) -> str:
    match = _FENCE.search(text)
    return match.group(1).strip() if match else text.strip()


def _build_azure_client() -> AsyncAzureOpenAI:
    return AsyncAzureOpenAI(
        api_key=os.environ["AZURE_OPENAI_API_KEY"],
        api_version=os.getenv("AZURE_OPENAI_API_VERSION", "2024-12-01-preview"),
        azure_endpoint=os.environ["AZURE_OPENAI_ENDPOINT"],
    )


async def translate_question(
    question: str,
    *,
    db: BlogNotesDB | None = None,
    prompt_manager: Any = None,
    client: AsyncAzureOpenAI | None = None,
    deployment: str | None = None,
) -> TranslationResult:
    from sql_notes.connector import get_db

    db = db or get_db()
    schema_ddl = await db.schema_ddl()

    if prompt_manager is None:
        from approaches.promptmanager import PromptManager

        prompt_manager = PromptManager()

    system_prompt = prompt_manager.render(
        "sql_notes/nl_to_sql.system.jinja2",
        schema_ddl=schema_ddl,
    )

    client = client or _build_azure_client()
    deployment = deployment or os.getenv("AZURE_OPENAI_CHATGPT_DEPLOYMENT", "gpt-4.1-mini")

    response = await client.chat.completions.create(
        model=deployment,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": question},
        ],
        temperature=0.0,
        response_format={"type": "json_object"},
    )
    raw = response.choices[0].message.content or "{}"
    try:
        payload = json.loads(raw)
    except json.JSONDecodeError:
        # Last-resort recovery if the model wrapped JSON in a fence anyway.
        payload = json.loads(_strip_fence(raw))

    sql = _strip_fence(str(payload.get("sql", ""))).rstrip(";").strip()
    rationale = str(payload.get("rationale", "")).strip()
    if not sql:
        raise ValueError("nl_to_sql returned an empty SQL string")
    return TranslationResult(sql=sql, rationale=rationale)

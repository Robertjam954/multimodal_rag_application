"""Tutor SQL-notes approach.

Translates a natural-language question into SQLite, runs the query against the
blog-notes library, and streams an answer that cites each returned row as a
`[note:<id>]` pill. SSE events:

- {"event": "sql",       "data": {"sql": "...", "rationale": "..."}}
- {"event": "row_count", "data": <int>}
- {"event": "citation",  "data": {note_id, content_topic, source_url, source_type, ...}}
- {"event": "token",     "data": "..."}
"""
from __future__ import annotations

import json
import logging
import os
from typing import Any, AsyncGenerator

from openai import AsyncAzureOpenAI

from approaches.approach import Approach

logger = logging.getLogger(__name__)


class SQLNotesApproach(Approach):
    async def run(
        self,
        messages: list[dict[str, Any]],
        context: dict[str, Any] | None = None,
        session_state: str | None = None,
    ) -> dict[str, Any]:
        final: dict[str, Any] = {"sql": None, "rows": [], "answer": "", "session_state": session_state}
        async for evt in self.run_stream(messages, context, session_state):
            kind = evt.get("event")
            if kind == "sql":
                final["sql"] = evt["data"]
            elif kind == "citation":
                final["rows"].append(evt["data"])
            elif kind == "token":
                final["answer"] += evt["data"]
            elif kind == "error":
                final["error"] = evt["data"]
        return final

    async def run_stream(
        self,
        messages: list[dict[str, Any]],
        context: dict[str, Any] | None = None,
        session_state: str | None = None,
    ) -> AsyncGenerator[dict[str, Any], None]:
        question = messages[-1]["content"] if messages else ""
        if not question.strip():
            yield {"event": "error", "data": {"reason": "empty question"}}
            return

        from sql_notes import get_db, translate_question

        db = get_db()

        # Translation
        try:
            translation = await translate_question(question, db=db, prompt_manager=self.prompt_manager)
        except Exception as exc:  # noqa: BLE001
            logger.exception("nl_to_sql translation failed")
            yield {"event": "error", "data": {"stage": "translation", "reason": str(exc)}}
            return
        yield {"event": "sql", "data": {"sql": translation.sql, "rationale": translation.rationale}}

        # Execution
        try:
            rows = await db.run_query(translation.sql)
        except Exception as exc:  # noqa: BLE001
            logger.exception("blog-notes query failed")
            yield {"event": "error", "data": {"stage": "execution", "reason": str(exc), "sql": translation.sql}}
            return

        yield {"event": "row_count", "data": len(rows)}
        for row in rows:
            yield {"event": "citation", "data": row}

        # Summarization
        if self.prompt_manager is None:
            from approaches.promptmanager import PromptManager

            prompt_manager = PromptManager()
        else:
            prompt_manager = self.prompt_manager

        system_prompt = prompt_manager.render(
            "sql_notes/summarize_results.system.jinja2",
            question=question,
            sql=translation.sql,
            row_count=len(rows),
            rows_json=json.dumps(rows, default=str)[:8000],
        )

        client = AsyncAzureOpenAI(
            api_key=os.environ["AZURE_OPENAI_API_KEY"],
            api_version=os.getenv("AZURE_OPENAI_API_VERSION", "2024-12-01-preview"),
            azure_endpoint=os.environ["AZURE_OPENAI_ENDPOINT"],
        )
        deployment = os.getenv("AZURE_OPENAI_CHATGPT_DEPLOYMENT", "gpt-4.1-mini")

        try:
            stream = await client.chat.completions.create(
                model=deployment,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": question},
                ],
                temperature=0.2,
                stream=True,
            )
            async for chunk in stream:
                if not chunk.choices:
                    continue
                delta = chunk.choices[0].delta.content
                if delta:
                    yield {"event": "token", "data": delta}
        except Exception as exc:  # noqa: BLE001
            logger.exception("summarization stream failed")
            yield {"event": "error", "data": {"stage": "summarization", "reason": str(exc)}}

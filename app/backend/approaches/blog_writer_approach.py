"""Generate a Jekyll blog post from a row in the blog-notes library.

Fetches the note, renders the `blog/notion_to_blog.system.jinja2` template with
the note's fields, calls Azure OpenAI for the body, and writes the resulting
Markdown to `site/_posts/YYYY-MM-DD-<slug>.md`.
"""
from __future__ import annotations

import json
import logging
import os
import re
import unicodedata
from datetime import date
from pathlib import Path
from typing import Any

from openai import AsyncAzureOpenAI

from approaches.approach import Approach

logger = logging.getLogger(__name__)

_SLUG_BAD = re.compile(r"[^a-z0-9]+")
SITE_POSTS_DIR = Path(__file__).resolve().parents[2] / "site" / "_posts"


def _slugify(text: str) -> str:
    norm = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode().lower()
    return _SLUG_BAD.sub("-", norm).strip("-")[:80] or "post"


class BlogWriterApproach(Approach):
    async def run(
        self,
        messages: list[dict[str, Any]] | None = None,
        context: dict[str, Any] | None = None,
        session_state: str | None = None,
    ) -> dict[str, Any]:
        ctx = context or {}
        note_id = ctx.get("note_id")
        if note_id is None and messages:
            # Allow a chat-style invocation: "generate post for note 3"
            match = re.search(r"\bnote[:#\s]*([0-9]+)\b", messages[-1].get("content", ""), re.IGNORECASE)
            if match:
                note_id = int(match.group(1))
        if note_id is None:
            raise ValueError("note_id is required - pass via context.note_id or 'note <id>' in the message")
        return await self.run_for_note(int(note_id), dry_run=bool(ctx.get("dry_run")))

    async def run_for_note(self, note_id: int, *, dry_run: bool = False) -> dict[str, Any]:
        from sql_notes import get_db

        db = get_db()
        note = await db.get_note(note_id)
        if not note:
            raise LookupError(f"no blog_notes row with id={note_id}")

        if self.prompt_manager is None:
            from approaches.promptmanager import PromptManager

            prompt_manager = PromptManager()
        else:
            prompt_manager = self.prompt_manager

        today = date.today().isoformat()
        system_prompt = prompt_manager.render(
            "blog/notion_to_blog.system.jinja2",
            content_topic=note.get("content_topic") or "",
            hook_intro=note.get("hook_intro") or "",
            key_insights=json.dumps(note.get("key_insights") or [], ensure_ascii=False),
            seo_keywords=json.dumps(note.get("seo_keywords") or [], ensure_ascii=False),
            source_url=note.get("source_url") or "",
            source_type=note.get("source_type") or "text",
            transcript=(note.get("transcript") or "")[:6000],
            today=today,
        )

        client = AsyncAzureOpenAI(
            api_key=os.environ["AZURE_OPENAI_API_KEY"],
            api_version=os.getenv("AZURE_OPENAI_API_VERSION", "2024-12-01-preview"),
            azure_endpoint=os.environ["AZURE_OPENAI_ENDPOINT"],
        )
        deployment = os.getenv("AZURE_OPENAI_CHATGPT_DEPLOYMENT", "gpt-4.1-mini")
        response = await client.chat.completions.create(
            model=deployment,
            messages=[{"role": "system", "content": system_prompt}],
            temperature=0.4,
        )
        body = (response.choices[0].message.content or "").strip()

        if not body.startswith("---"):
            raise ValueError("model output did not start with YAML frontmatter")

        slug = _slugify(note["content_topic"])
        filename = f"{today}-{slug}.md"

        path = SITE_POSTS_DIR / filename
        result: dict[str, Any] = {
            "note_id": note_id,
            "path": str(path.relative_to(SITE_POSTS_DIR.parents[1])),
            "filename": filename,
            "content": body,
            "dry_run": dry_run,
        }
        if not dry_run:
            SITE_POSTS_DIR.mkdir(parents=True, exist_ok=True)
            path.write_text(body, encoding="utf-8")
            # Persist back into the row so future calls don't regenerate from scratch.
            async with db.connection() as conn:
                await conn.execute(
                    "UPDATE blog_notes SET generated_content = ?, status = 'reviewed' WHERE id = ?",
                    (body, note_id),
                )
                await conn.commit()
        return result

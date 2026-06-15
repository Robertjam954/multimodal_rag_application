"""Async SQLite connector for the blog-notes library.

`BLOG_NOTES_DB_PATH` env var selects the database file (default: data/blog_notes.sqlite).
Use `:memory:` for tests.
"""
from __future__ import annotations

import json
import logging
import os
import re
from contextlib import asynccontextmanager
from pathlib import Path
from typing import Any, AsyncIterator

import aiosqlite

logger = logging.getLogger(__name__)

SCHEMA_PATH = Path(__file__).parent / "schema.sql"
DEFAULT_DB_PATH = "data/blog_notes.sqlite"

# Only SELECT and WITH (CTE) statements are allowed through run_query.
_READ_ONLY_PREFIX = re.compile(r"^\s*(SELECT|WITH)\b", re.IGNORECASE)
_FORBIDDEN = re.compile(
    r"\b(INSERT|UPDATE|DELETE|DROP|ALTER|CREATE|REPLACE|ATTACH|DETACH|PRAGMA|VACUUM)\b",
    re.IGNORECASE,
)


def _resolve_db_path() -> str:
    p = os.getenv("BLOG_NOTES_DB_PATH", DEFAULT_DB_PATH)
    if p == ":memory:":
        return p
    path = Path(p)
    if not path.is_absolute():
        # Resolve against the backend directory (one level up from this file's package).
        path = Path(__file__).resolve().parents[1] / path
    path.parent.mkdir(parents=True, exist_ok=True)
    return str(path)


class BlogNotesDB:
    """Thin wrapper around aiosqlite with schema bootstrap and a read-only query gate."""

    def __init__(self, db_path: str | None = None) -> None:
        self.db_path = db_path or _resolve_db_path()
        self._schema_applied = False

    async def _bootstrap(self, conn: aiosqlite.Connection) -> None:
        if self._schema_applied:
            return
        await conn.execute("PRAGMA foreign_keys = ON")
        ddl = SCHEMA_PATH.read_text()
        await conn.executescript(ddl)
        await conn.commit()
        self._schema_applied = True

    @asynccontextmanager
    async def connection(self) -> AsyncIterator[aiosqlite.Connection]:
        async with aiosqlite.connect(self.db_path) as conn:
            conn.row_factory = aiosqlite.Row
            await self._bootstrap(conn)
            yield conn

    async def list_tables(self) -> list[str]:
        async with self.connection() as conn:
            cur = await conn.execute(
                "SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%' ORDER BY name"
            )
            return [row[0] for row in await cur.fetchall()]

    async def describe_table(self, name: str) -> list[dict[str, Any]]:
        if not name.replace("_", "").isalnum():
            raise ValueError(f"invalid table name: {name!r}")
        async with self.connection() as conn:
            cur = await conn.execute(f"PRAGMA table_info({name})")
            return [
                {
                    "cid": row[0],
                    "name": row[1],
                    "type": row[2],
                    "notnull": bool(row[3]),
                    "default": row[4],
                    "pk": bool(row[5]),
                }
                for row in await cur.fetchall()
            ]

    async def schema_ddl(self) -> str:
        """Return CREATE statements for every user table - used as LLM context."""
        async with self.connection() as conn:
            cur = await conn.execute(
                "SELECT sql FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%' ORDER BY name"
            )
            rows = await cur.fetchall()
        return "\n\n".join(row[0] for row in rows if row[0])

    async def run_query(self, sql: str, limit: int = 200) -> list[dict[str, Any]]:
        """Execute a single read-only statement; raise ValueError on anything else."""
        if not _READ_ONLY_PREFIX.match(sql):
            raise ValueError("only SELECT or WITH statements are permitted")
        if _FORBIDDEN.search(sql):
            raise ValueError("statement contains a write or DDL keyword")
        if ";" in sql.rstrip().rstrip(";"):
            raise ValueError("multiple statements are not permitted")
        async with self.connection() as conn:
            cur = await conn.execute(sql)
            rows = await cur.fetchmany(limit)
            return [dict(r) for r in rows]

    async def insert_note(
        self,
        content_topic: str,
        source_type: str,
        *,
        hook_intro: str | None = None,
        key_insights: list[str] | None = None,
        seo_keywords: list[str] | None = None,
        source_url: str | None = None,
        transcript: str | None = None,
        status: str = "draft",
        generated_content: str | None = None,
        tags: list[str] | None = None,
    ) -> int:
        async with self.connection() as conn:
            cur = await conn.execute(
                """
                INSERT INTO blog_notes
                    (content_topic, hook_intro, key_insights, seo_keywords,
                     source_url, source_type, transcript, status, generated_content)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    content_topic,
                    hook_intro,
                    json.dumps(key_insights or []),
                    json.dumps(seo_keywords or []),
                    source_url,
                    source_type,
                    transcript,
                    status,
                    generated_content,
                ),
            )
            note_id = cur.lastrowid
            for tag in tags or []:
                await conn.execute(
                    "INSERT OR IGNORE INTO tags(note_id, tag) VALUES (?, ?)",
                    (note_id, tag),
                )
            await conn.commit()
            return int(note_id)

    async def get_note(self, note_id: int) -> dict[str, Any] | None:
        async with self.connection() as conn:
            cur = await conn.execute("SELECT * FROM blog_notes WHERE id = ?", (note_id,))
            row = await cur.fetchone()
            if not row:
                return None
            note = dict(row)
            for json_col in ("key_insights", "seo_keywords"):
                try:
                    note[json_col] = json.loads(note.get(json_col) or "[]")
                except json.JSONDecodeError:
                    note[json_col] = []
            cur = await conn.execute("SELECT tag FROM tags WHERE note_id = ?", (note_id,))
            note["tags"] = [r[0] for r in await cur.fetchall()]
            cur = await conn.execute(
                "SELECT citation_text, citation_url, timestamp_s FROM citations WHERE note_id = ?",
                (note_id,),
            )
            note["citations"] = [dict(r) for r in await cur.fetchall()]
            return note


_DB_SINGLETON: BlogNotesDB | None = None


def get_db() -> BlogNotesDB:
    global _DB_SINGLETON
    if _DB_SINGLETON is None:
        _DB_SINGLETON = BlogNotesDB()
    return _DB_SINGLETON

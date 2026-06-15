"""Tool implementations registered with the FastMCP server.

Three tools, all read-only:
- `list_tables` - enumerate user tables in the blog-notes DB.
- `describe_table` - column names + types for one table.
- `run_query` - execute a single SELECT/WITH statement; rejects DDL/DML.
"""
from __future__ import annotations

from typing import Any

from sql_notes.connector import BlogNotesDB, get_db


async def list_tables(db: BlogNotesDB | None = None) -> dict[str, Any]:
    db = db or get_db()
    return {"tables": await db.list_tables()}


async def describe_table(name: str, db: BlogNotesDB | None = None) -> dict[str, Any]:
    db = db or get_db()
    return {"table": name, "columns": await db.describe_table(name)}


async def run_query(sql: str, limit: int = 200, db: BlogNotesDB | None = None) -> dict[str, Any]:
    db = db or get_db()
    rows = await db.run_query(sql, limit=limit)
    return {"row_count": len(rows), "rows": rows}

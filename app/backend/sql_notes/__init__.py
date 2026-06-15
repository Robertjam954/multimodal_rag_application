"""SQLite-backed library of AI-engineering blog notes.

Stores transcripts, key insights, tags, and citations extracted from ingested audio,
video, and text sources. Queryable in natural language via `nl_to_sql.py` or the
FastMCP server in `mcp_server/`.
"""
from sql_notes.connector import BlogNotesDB, get_db
from sql_notes.nl_to_sql import translate_question

__all__ = ["BlogNotesDB", "get_db", "translate_question"]

"""FastMCP server entrypoint.

Run with:
    python -m sql_notes.mcp_server.main

Or via `app/backend/sql_notes/scripts/run_server.sh`.
"""
from __future__ import annotations

import logging
from typing import Any

from sql_notes.mcp_server import tools

logger = logging.getLogger(__name__)


def build_server() -> Any:
    """Construct the FastMCP server and register the three read-only tools."""
    try:
        from fastmcp import FastMCP
    except ImportError as exc:  # pragma: no cover - import guard
        raise RuntimeError(
            "fastmcp is not installed; add it to requirements.in or pip install fastmcp"
        ) from exc

    mcp = FastMCP("blog-notes")

    @mcp.tool()
    async def list_tables() -> dict:
        """List every user table in the blog-notes database."""
        return await tools.list_tables()

    @mcp.tool()
    async def describe_table(name: str) -> dict:
        """Return column metadata for a single table."""
        return await tools.describe_table(name)

    @mcp.tool()
    async def run_query(sql: str, limit: int = 200) -> dict:
        """Run a single SELECT/WITH statement. DDL and DML are rejected."""
        return await tools.run_query(sql, limit=limit)

    return mcp


def main() -> None:
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s")
    build_server().run()


if __name__ == "__main__":
    main()

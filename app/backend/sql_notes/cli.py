"""Interactive natural-language query loop against the blog-notes DB.

Useful for local debugging without bringing up the full Quart app.

    python -m sql_notes.cli
"""
from __future__ import annotations

import asyncio
import logging
import sys

from sql_notes.connector import get_db
from sql_notes.nl_to_sql import translate_question

logger = logging.getLogger(__name__)


def _print_rich(rows: list[dict]) -> None:
    try:
        from rich.console import Console
        from rich.table import Table
    except ImportError:
        for row in rows:
            print(row)
        return
    console = Console()
    if not rows:
        console.print("[dim](no rows)[/dim]")
        return
    table = Table(show_lines=False)
    for col in rows[0].keys():
        table.add_column(col)
    for row in rows:
        table.add_row(*[str(row.get(c, "")) for c in rows[0].keys()])
    console.print(table)


async def _one_shot(question: str) -> int:
    db = get_db()
    try:
        translation = await translate_question(question, db=db)
    except Exception as exc:  # noqa: BLE001
        print(f"[translation error] {exc}", file=sys.stderr)
        return 1
    print(f"\nSQL:       {translation.sql}")
    if translation.rationale:
        print(f"Rationale: {translation.rationale}")
    try:
        rows = await db.run_query(translation.sql)
    except Exception as exc:  # noqa: BLE001
        print(f"[query error] {exc}", file=sys.stderr)
        return 2
    print()
    _print_rich(rows)
    return 0


async def _repl() -> int:
    print("Blog-notes SQL chat. Ctrl-D to exit.")
    while True:
        try:
            question = input("\nAsk: ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            return 0
        if not question:
            continue
        await _one_shot(question)


def main() -> None:
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s")
    args = sys.argv[1:]
    if args:
        code = asyncio.run(_one_shot(" ".join(args)))
    else:
        code = asyncio.run(_repl())
    sys.exit(code)


if __name__ == "__main__":
    main()

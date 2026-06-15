# sql_notes

SQLite-backed library of AI-engineering notes the tutor chat can query in natural language.

## Layout

```
sql_notes/
├── connector.py         # aiosqlite wrapper + schema bootstrap + read-only query gate
├── schema.sql           # blog_notes / tags / citations
├── nl_to_sql.py         # Azure OpenAI NL->SQL translator
├── mcp_server/          # FastMCP server exposing list_tables / describe_table / run_query
├── cli.py               # Local NL query REPL (Rich)
├── seed.py              # Idempotent sample-data loader
└── scripts/             # run_server.sh / run_client.sh
```

## Setup

```bash
# Backend venv must be active
python -m sql_notes.seed        # 7 sample AI-engineering notes
python -m sql_notes.cli "what notes do I have about RAG eval?"
```

## Env

| Var | Default | Notes |
|---|---|---|
| `BLOG_NOTES_DB_PATH` | `data/blog_notes.sqlite` (relative to `app/backend/`) | Use `:memory:` in tests. |
| `AZURE_OPENAI_API_KEY` | required | Reused from the rest of the app. |
| `AZURE_OPENAI_ENDPOINT` | required | |
| `AZURE_OPENAI_CHATGPT_DEPLOYMENT` | `gpt-4.1-mini` | Translation model. |
| `AZURE_OPENAI_API_VERSION` | `2024-12-01-preview` | |

## Safety

`connector.run_query` enforces:

- Statement must start with `SELECT` or `WITH`.
- No `INSERT`, `UPDATE`, `DELETE`, `DROP`, `ALTER`, `CREATE`, `REPLACE`, `ATTACH`, `DETACH`, `PRAGMA`, or `VACUUM`.
- No multi-statement bundles (no embedded `;`).
- Result set capped at the `limit` parameter (default 200 rows).

The Quart route `POST /sql/notes` is the production entry point - it calls `translate_question` followed by `run_query` and streams the answer + a `citation` SSE event per row.

## Adding a note from code

```python
from sql_notes import get_db

await get_db().insert_note(
    content_topic="Title",
    source_type="video",
    source_url="https://youtube.com/watch?v=...",
    transcript="...",
    key_insights=["..."],
    tags=["rag", "evaluation"],
)
```

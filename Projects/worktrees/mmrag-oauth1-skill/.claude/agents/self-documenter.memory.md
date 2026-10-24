# Self-Documenter Memory

Persistent, cross-run memory for the `self-documenter` agent. The agent runs cold each
time (a fresh checkout in CI), so this file is how it carries context between runs:
durable project facts, why the docs say what they say, and drift patterns worth
watching. Read it at the START of every run; append/correct it at the END.

Rules for this file:
- One durable fact per bullet, newest-relevant kept accurate (edit in place, do not
  duplicate). Prefix each with the date it was learned/confirmed (`YYYY-MM-DD`).
- Record *why*, not just *what* - the reasoning that would otherwise be lost between runs.
- Never store secrets or env values (names only). Single hyphens, no em dashes, no emojis.
- If a fact here is contradicted by the code, the code wins: fix the fact and note the change.

## Durable project learnings

- 2026-07-19 Project = **multimodal_rag_ai_tutor** (the non-local / Azure RAG tutor in the
  portfolio). Deployed on Azure Container Apps (RG `ai-tutor`, eastus2), Cosmos NoSQL
  retriever. Azure subscription is on a billing hold, so cloud deploys are blocked; active
  work is local-first.
- 2026-07-19 **SchemaFlow SQL agent is now grounded against a real SQLite warehouse** (was
  pure-LLM JSON before). Pieces: `scripts/seed_warehouse.py` (seed), `core/warehouse.py`
  (read-only catalog + dry-run executor), wired via `agents/sql_schemaflow.py` +
  `approaches/sql_schemaflow_approach.py` + `app.py` (`get_warehouse()`).
- 2026-07-19 Warehouse is a **single SQLite file** (`data/warehouse.sqlite`), layers are a
  **naming convention** (`landing_`/`stg_`/`dim_`+`fct_`/mart view) plus a `_warehouse_layers`
  catalog table - NOT ATTACH-ed per-layer databases. Reason: SQLite forbids a view in one
  attached DB from referencing tables in another, which would break the cross-layer
  `mart` view -> `core` table dependency that the Impact agent demonstrates.
- 2026-07-19 Dry-run executes the generated SQL against an **in-memory clone** of the seed
  (`sqlite3` `backup()`), stops at first failure, and never opens the seed file writable, so
  it cannot be mutated. Result lands in `bundle["validation"]["dry_run"]`. One self-correction
  retry feeds engine errors back to the SQL agent.
- 2026-07-19 Domain of the warehouse = **clinical / TCGA** (matches the rest of the portfolio),
  not the retail `ODS.ODS_CUSTOMER_PROFILE` example still in some prompts. If prompts/sample
  still show retail, that is known drift to flag.
- 2026-07-19 `.dockerignore` excludes `data/`, so a committed `.sqlite` will NOT ship in the
  container image - the warehouse must be seeded at startup for the deployed demo. When
  `data/warehouse.sqlite` is absent, the agent falls back to pure-LLM planning (by design).
- 2026-07-19 Progress is also tracked in the portfolio tracker
  `project_planning_tracking_code_review/todos/multimodal-rag-tutor.md` (sibling repo). STATUS.md
  here is the in-repo checklist; keep both honest but the tracker is the portfolio-board source.

## Open drift to watch

- 2026-07-19 SchemaFlow prompts (`approaches/prompts/sql/*.jinja2`) and the frontend sample
  (`app/frontend/src/pages/sql/Sql.tsx:SAMPLE`) may still use the retail example; the grounded
  warehouse is clinical. Reconcile when those prompts are updated.
- 2026-07-19 `SqlBundle` frontend type + `SchemaFlowPanel` do not yet render the new
  `validation.dry_run` per-statement results or the impact grounding block - frontend lags backend.

# ADR-0005: Chainlit's SQL data layer as the benchmark run store

Date: 2026-09-02
Status: accepted

## Context

ADR-0003 makes a strong demand: every number in the benchmark report must be generated
from stored run data, never transcribed. That requires a store holding, per run, the
full agent transcript, every tool call and its result, every generated artifact
(tables, figures), token and latency and cost accounting, and human ratings for judge
calibration - all queryable with SQL and all joinable to the arm, task, and prompt that
produced them.

The obvious move is a bespoke schema. But this repo also needs a chat surface for
driving agents interactively and collecting those human ratings, and Chainlit was
already chosen for that. Reading `chainlit/data/base.py`, its `BaseDataLayer` abstract
interface already models exactly this domain:

- `users` - who ran it
- `threads` - one conversation / run
- `steps` - one agent step or tool call, nested, with input, output, and timing
- `elements` - artifacts attached to a step (images, files, dataframes)
- `feedbacks` - a rating plus free-text comment attached to a step

`chainlit/data/sql_alchemy.py` (`SQLAlchemyDataLayer`) is a working relational
implementation of it, with plain parameterized SQL over those five tables. That is the
schema this benchmark needs, already written, already exercised by the UI.

## Decision

Adopt Chainlit's data layer as **the benchmark run store**, not merely as UI
persistence. `src/tracking/data_layer.py` subclasses `SQLAlchemyDataLayer` and every
agent run - whether launched from the Chainlit UI or from a headless batch script -
writes through it.

**Mapping.** Agent step -> `steps` row (tool name, arguments, result, start/end,
token counts). Generated table or figure -> `elements` row attached to its producing
step, so an artifact is always traceable to the reasoning that produced it. Human
rating -> `feedbacks` row. One run -> one `threads` row.

**Extension.** Benchmark dimensions live in the `threads` metadata column and in a
sidecar `runs` table keyed by `thread_id`: `arm`, `task_id`, `task_type`, `prompt_id`,
`model`, `seed`, `adr_set`, `experiment_hash`, `outcome`
(`completed` / `step_cap_exceeded` / `error`), and totals for tokens, latency, and
cost. Chainlit's own tables are not altered - the sidecar keeps the subclass compatible
with upstream schema changes.

**Headless runs use the same path.** The batch benchmark runner does not write to CSV
and it does not bypass the data layer. One writer means the UI and the batch harness
cannot drift into disagreeing about what a run was, and it means an interactively
explored run is analyzable with the same SQL as a batch one.

**Backend.** SQLite for phase 1, matching the local-first stance and sitting beside the
`sqlite-vec` index from ADR-0004. `SQLAlchemyDataLayer` takes a connection string, so
Postgres is a config change if the experiment grows or deploys.

**Artifacts.** Figures and tables are written to `reports/` on disk and referenced from
`elements` by path plus content hash, rather than stored as blobs. Files stay diffable
and directly usable by the publication-figure workflow; the hash detects drift between
what was reported and what is on disk.

`src/tracking/queries.py` holds every aggregate the report needs, so the report
generator contains no ad-hoc SQL.

## Consequences

- The report generator is a thin layer over SQL, which is what makes "every number
  traces to run-store rows" enforceable instead of aspirational.
- Human feedback for judge calibration (ADR-0003) is collected by the UI into the same
  database as the automated scores, so judge-human agreement is a join, not a merge
  script.
- Nested `steps` gives a natural representation of the phase-2 multi-agent arm - a
  worker's steps nest under the supervisor's - so the schema does not need revisiting
  when the second arm lands. This was a deciding factor.
- A dependency on Chainlit's internal data-layer contract. It is a documented extension
  point, but `BaseDataLayer` is an abstract class that can change across releases, so
  the Chainlit version is pinned and the subclass is covered by a round-trip test.
- Chainlit's schema is shaped for chat, not experiments; benchmark dimensions live in a
  sidecar rather than in first-class columns, so analysis queries carry a join.
- SQLite serializes writes. Parallel benchmark runs need either WAL mode or serialized
  execution - a real constraint on batch throughput, and the reason the Postgres path is
  kept open.
- **Rejected: a bespoke experiment schema.** More natural columns, but it would have
  duplicated the transcript model, and the UI would then write to a second store -
  reintroducing exactly the divergence this avoids.
- **Rejected: CSV/JSONL run logs.** Trivial to write, but joining runs to steps to
  artifacts to feedback across thousands of runs is what a database is for. The
  decision-log JSONL is kept as a complementary, human-readable reasoning trace, not as
  the analytical source of truth.
- **Rejected: LiteralAI's hosted data layer** (`chainlit/data/literalai.py`) - a
  managed option, but the benchmark needs arbitrary SQL over the raw tables and the
  data should stay local.

## References

- `src/tracking/data_layer.py`, `src/tracking/queries.py`, `app.py` (to be built)
- Upstream: `chainlit/data/base.py` (`BaseDataLayer`), `chainlit/data/sql_alchemy.py` (`SQLAlchemyDataLayer`)
- [ADR-0003](0003-benchmark-protocol.md) - the reporting requirement this satisfies
- [ADR-0002](0002-single-react-agent-research-baseline.md) - what a `step` row records

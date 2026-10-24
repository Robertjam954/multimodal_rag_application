# Architecture Decision Records

Significant architectural decisions for this experiment, one file per decision.

- Format: [`.claude/adr-template.md`](../../.claude/adr-template.md)
- Numbering: `NNNN-short-title.md`, sequential, append-only
- Maintained by: the [`self-documenter`](../../.claude/agents/self-documenter.md) agent,
  which writes an ADR when it detects a governed change in the diff; decisions that must
  be settled before code exists are written by hand.

## Why these are immutable here

This is an experiment repo, so an ADR is not only design rationale - it is the record of
**what configuration produced a given set of benchmark numbers**. A superseded ADR still
describes what earlier runs actually executed, so records are never edited or deleted;
a decision is changed by adding a new ADR that supersedes it and updating the old one's
status line. Every run record carries the `adr_set` in force when it ran, and results
from differing ADR sets are not directly comparable (see ADR-0003).

## Records

| ADR | Title | Status |
|---|---|---|
| [0001](0001-record-architecture-decisions.md) | Record architecture decisions | accepted |
| [0002](0002-single-react-agent-research-baseline.md) | Single ReAct agent as the research-execution baseline | accepted |
| [0003](0003-benchmark-protocol.md) | Benchmark protocol | accepted |
| [0004](0004-retrieval-design.md) | Retrieval over rendered TCGA cards, model outputs, and PubMed abstracts | accepted |
| [0005](0005-chainlit-sql-run-store.md) | Chainlit's SQL data layer as the benchmark run store | accepted |
| [0006](0006-prompt-registry-freezing-policy.md) | Frozen prompt registry and prompt-effects design | accepted |
| 0007 | LangGraph multi-agent topology | planned (phase 2) |

## When an ADR is required

**Required:** agent roster or topology · the tool registry and its boundaries ·
retrieval and chunking strategy · store choice · model selection · the benchmark
protocol · the eval metric set or judge · any change to a frozen artifact (prompt,
task set, cohort snapshot, scoring rule).

**Not required:** bug fixes · refactors inside an existing pattern · doc and test-only
changes · figure restyling.

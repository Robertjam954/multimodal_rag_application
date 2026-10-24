# ADR-0001: Record architecture decisions

Date: 2026-09-02
Status: accepted

## Context

This repository exists to run a controlled experiment: can a **single tool-using
agent carry out a biomedical research project end to end** - pull TCGA data, build
a retrieval index over it, answer research questions, summarize papers, and emit
the tables and figures - and how does that baseline compare to alternative agent
architectures once they are added.

An experiment repo has a failure mode that a normal service repo does not. The
result is only meaningful if the *configuration that produced it* is recoverable
months later: which prompt, which retrieval strategy, which step cap, which judge,
which cohort snapshot. If those choices live only in commit messages, chat history,
or a notebook cell that was re-run, the benchmark numbers become unreproducible and
the comparison between arms becomes invalid - a later arm silently benefits from a
better retriever rather than a better architecture.

Every sibling project in `portfolio_ai_engineering_projects` already keeps ADRs
(`project_planning_tracking_code_review/docs/adr/`, `agentic_research_team/docs/adr/`),
and the portfolio engineering standard requires an ADR before implementation for
multi-agent design, architectural change, technology choice, and algorithm choice.
This repo adopts the same convention from its first commit.

## Decision

Record every significant architectural decision as an Architecture Decision Record
in `docs/adr/`, one file per decision, numbered sequentially
(`NNNN-short-title.md`), in the format at [`.claude/adr-template.md`](../../.claude/adr-template.md)
(Context / Decision / Consequences / References).

Scope rules, inherited from the portfolio standard and narrowed for an experiment repo:

- **An ADR is required for:** agent roster and topology, the tool registry and its
  boundaries, retrieval and chunking strategy, the store choice, model selection,
  the benchmark protocol, the eval metric set and judge, and **any change to a
  frozen experimental artifact** (prompt, task set, cohort snapshot, scoring rule).
- **No ADR for:** bug fixes, refactors inside an existing pattern, doc and test-only
  changes, figure restyling.

Two rules specific to this repo:

1. **An ADR is immutable once accepted.** A decision is changed by adding a new ADR
   that supersedes it and updating the older record's status. This matters more here
   than elsewhere: a superseded ADR is the record of what the *earlier benchmark runs*
   actually used, so deleting it would orphan those results.
2. **Every benchmark result set cites the ADR numbers in force when it was produced.**
   Run records carry an `adr_set` field. A result whose ADR set differs from the
   current baseline's is not directly comparable and must be re-run or labeled.

ADRs are written by the `self-documenter` agent (`.claude/agents/self-documenter.md`)
from the diff after a substantive change, and by hand ahead of implementation for
decisions that must be settled before code exists - as ADR-0002 and ADR-0003 are.

## Consequences

- The reasoning behind the experiment's design is durable, reviewable, and lives next
  to the code rather than in chat history.
- Benchmark arms become genuinely comparable, because the configuration difference
  between any two runs is expressible as a diff of ADR sets.
- Superseded records accumulate and must be read with their dates in mind; the ADR
  index carries status so a reader is not misled by a stale record.
- Small overhead: significant changes ship with a short written record, and freezing
  a prompt or task set now requires a record rather than an edit.
- Rejected alternative: a single living `DECISIONS.md`. It is cheaper to write but
  loses the immutability that makes historical run configurations recoverable, which
  is the entire reason this repo needs the convention.

## References

- [`.claude/adr-template.md`](../../.claude/adr-template.md) - the record format
- [`docs/adr/README.md`](README.md) - the index of records
- Portfolio standard: `portfolio_ai_engineering_projects/CLAUDE.md`, "Architecture Decision Records"
- Sibling conventions: `project_planning_tracking_code_review/docs/adr/0001`, `agentic_research_team/docs/adr/`
- Michael Nygard, "Documenting Architecture Decisions" (2011)

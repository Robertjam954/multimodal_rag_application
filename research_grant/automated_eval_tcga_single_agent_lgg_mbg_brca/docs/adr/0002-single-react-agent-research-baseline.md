# ADR-0002: Single ReAct agent as the research-execution baseline

Date: 2026-09-02
Status: accepted

## Context

The portfolio has repeatedly reached for multi-agent architectures without ever
measuring whether they beat a single agent. `agentic_research_team` ships a 4-agent
linear pipeline (Triage -> Clarify -> Instruct -> Research,
`src/agents/biomedical_agents.py`) and specifies a Magentic-style LangGraph team in
its `AGENTS.md`; `project_planning_tracking_code_review` runs a LangGraph supervisor
over three workers (ADR-0002 there). Neither repo has a single-agent baseline, so the
cost of orchestration - extra tokens, extra latency, extra failure surface - has never
been weighed against a measured benefit.

This repo's experiment is that measurement. Before a multi-agent arm can be claimed to
win, there must be a baseline that is (a) genuinely capable of the whole task, so the
comparison is not rigged, and (b) frozen, so later arms are compared against a fixed
target rather than a moving one.

Constraints that shape the design:

- **The agent must actually execute a research project**, not just answer questions:
  retrieve from the corpus, query the structured TCGA cohort, run analysis code that
  produces tables and figures, summarize papers, and cite evidence.
- **Model provider is OpenAI only** (locked with the repo owner), so the loop is built
  on OpenAI tool-calling rather than a provider-agnostic abstraction.
- **Cost and runtime are bounded** - the task set is run repeatedly across prompt
  variants and seeds, so an unbounded loop is a budget hazard, not just a bug.
- **Every run must be reconstructable from storage alone** (ADR-0005), because the
  benchmark's claims are only as good as its audit trail.
- The retrieval index and tool registry are **shared infrastructure**, not part of the
  arm (ADR-0003), so that an architecture comparison is not contaminated by a
  retrieval change.

## Decision

The baseline arm is **one ReAct-style tool-calling loop** in
`src/agents/single_agent.py`: a single model, a single system prompt, and a flat tool
registry, iterating observe -> think -> call tool -> observe until it emits a final
answer or hits a cap. There is no router, no supervisor, no sub-agent, and no handoff.

**Tool registry** (`src/agents/tools.py`, one JSON schema + one unit test per tool):

| Tool | Purpose |
|---|---|
| `search_corpus` | dense retrieval over TCGA cards, SHAP / driver-gene result cards, and PubMed abstracts (ADR-0004) |
| `query_cohort` | structured query over the tidy cohort parquet (counts, prevalence, cross-tabs) |
| `run_analysis` | sandboxed Python for tables and figures; bounded CPU and wall clock, no network |
| `summarize_paper` | single-paper summarization against the frozen prompt registry (ADR-0006) |
| `cite_evidence` | resolves a claim to `study / table / row` or `pmid / span` provenance |

The agent receives the **whole registry**. Withholding tools would make the baseline
weaker than the multi-agent arm for a reason unrelated to architecture, which is the
exact confound ADR-0003 exists to prevent.

**Determinism and bounds.** Temperature and seed are fixed and recorded in
`docs/experiment_metadata.md`. The loop enforces a hard `MAX_STEPS` cap and a per-tool
timeout; hitting the cap terminates the run and records it as an explicit
`step_cap_exceeded` outcome rather than an exception, because cap-hit rate is itself a
reported metric - an architecture that routinely exhausts its budget is failing in a
way a crash log would hide.

**Prompt.** The system prompt comes from the frozen registry by `prompt_id`, never
inlined in code. The baseline's default is the `react` technique; the prompt-effects
experiment varies this axis while holding the architecture fixed.

**Instrumentation.** Every iteration appends a structured record to
`logs/single_agent-decisions.jsonl` (timestamp, step index, decision type, rationale,
tool called, evidence ids) and is written through the run store as a `step` row
(ADR-0005). Generated tables and figures are persisted as `element` rows so an
artifact is always traceable to the step that produced it.

**Failure handling.** A tool error is returned to the model as an observation rather
than raised, so the agent gets a chance to recover and the recovery behavior is
measurable. Tool errors, retries, and recoveries are counted and reported.

Once the baseline's first full benchmark run is recorded, its configuration is
**frozen**: changing the prompt, tool set, model, or caps requires a new ADR and
invalidates cross-arm comparison until all arms are re-run (ADR-0003).

## Consequences

- There is a defensible floor for the experiment. A later multi-agent claim has to
  beat a baseline that had the same tools, the same index, and the same task set.
- Cost, latency, and step count for the simplest viable architecture are known, which
  makes the phase-2 comparison a cost-quality trade-off rather than a quality-only one.
- The flat registry means the model chooses among five tools with no routing help. This
  is expected to be the baseline's weak point on multi-step tasks, and that weakness is
  the hypothesis the multi-agent arm tests - so it must not be patched away by adding
  routing to this arm.
- Freezing the configuration makes ordinary improvements expensive on purpose: a better
  prompt is no longer a free edit, it is an ADR plus a re-run.
- Building the tool registry, the run store, and the retrieval index for one agent
  front-loads work that phase 2 reuses unchanged, which is what keeps the arms
  comparable.
- **Rejected: starting with the multi-agent team.** It is the architecture the portfolio
  already assumes; starting there would have produced another system with no evidence
  behind it.
- **Rejected: a no-tools long-context agent as the baseline.** Cheaper and simpler, but
  it cannot run analysis or generate figures, so it cannot complete the task and would
  make any comparison vacuous. A no-agent retrieve-then-summarize floor may still be
  added later as a separate arm.
- **Rejected: reusing `agentic_research_team`'s 4-agent pipeline as the baseline.** It
  is already multi-stage, so it answers a different question, and its stages are tuned
  for a paper corpus rather than structured cohort data.

## References

- `src/agents/single_agent.py` - the loop (to be built)
- `src/agents/tools.py` - the tool registry (to be built)
- `docs/experiment_metadata.md` - frozen models, seeds, caps
- [ADR-0003](0003-benchmark-protocol.md) - what this baseline is compared against, and the rules that keep it comparable
- [ADR-0004](0004-retrieval-design.md) - the shared retrieval index this agent queries
- [ADR-0005](0005-chainlit-sql-run-store.md) - where run records go
- [ADR-0006](0006-prompt-registry-freezing-policy.md) - the frozen prompt registry
- Contrast: `agentic_research_team/src/agents/biomedical_agents.py` (4-agent linear pipeline)

# ADR-0003: Benchmark protocol

Date: 2026-09-02
Status: accepted

## Context

"Benchmark the single agent against other agents" is not yet an executable
specification. Without one, the comparison degrades in predictable ways: a later arm
is run against a corpus that has grown, or with a prompt that was quietly improved, or
scored by a judge from its own model family, and the resulting difference is credited
to architecture when it belongs to retrieval, prompting, or bias.

The methodology to copy already exists in the portfolio.
`llm_summarization_br_ca` evaluates prompts, not architectures, but it does so with
frozen prompt versions (`prompts/frozen/prompt_metadata.json`), a per-(model, approach,
element) tracking table (`src/llm_eval_by_llm/prompt_iteration_tracker.py`), and metric
modules that separate fabrication, retrieval, extraction, and self-consistency
(`eval/metrics/`). This ADR lifts that discipline to the architecture level.

Constraints: OpenAI-only agents, a task set small enough to re-run across many prompt
variants and seeds, and results that must remain comparable across a phase boundary
(the multi-agent arm arrives weeks after the baseline).

## Decision

**Arms.** Phase 1 evaluates one arm, the ADR-0002 single ReAct agent, against variation
on the prompt and model axes. Phase 2 adds the LangGraph multi-agent team (ADR-0007)
and runs the head-to-head. A no-agent retrieve-then-summarize floor may be added as a
third arm; if added it follows the same rules.

**Paired design.** Every arm sees an identical task set, an identical retrieval index,
and an identical tool registry. Comparisons are paired at the task level - each metric
difference is computed within task and then aggregated - because task difficulty varies
far more than the architectures do, and an unpaired comparison would drown the effect.

**The invalidation rule.** Retrieval configuration, the tool registry, the task set,
and the frozen prompts are **shared infrastructure, not arm properties**. Changing any
of them invalidates every cross-arm comparison until all arms are re-run. This is
enforced mechanically, not by discipline: each run record carries the `adr_set` in
force plus a content hash of `docs/experiment_metadata.md`, and the report generator
refuses to place runs with differing hashes in the same comparison table.

**Task set** (`eval/tasks/`, versioned and frozen): 30-50 research questions over the
TCGA BRCA cohort and the PubMed set, each with a reference answer or rubric, and each
labeled with a task type - `lookup`, `aggregate`, `multi_hop`, `analysis`
(requires generating a table or figure), `summarize`, `synthesize`. Results are reported
per task type as well as in aggregate, because the expected finding is that
orchestration helps on `multi_hop` and `synthesize` and is pure overhead on `lookup`.
An aggregate-only number would hide exactly the result the experiment is for.

**Metrics.** Three families, all reported:

- *Quality* - DeepEval faithfulness, answer relevancy, hallucination; plus ported
  `fabrication_by_prompt`, extraction accuracy against reference, and citation
  faithfulness (does the cited row actually support the claim).
- *Retrieval* - `precision_at_k` and recall over the known-relevant card set, so a
  quality difference can be attributed to retrieval or to reasoning.
- *Cost and behavior* - steps, tool calls, tool-error and recovery counts,
  `step_cap_exceeded` rate, tokens, latency, dollars, read straight from the run store.

**Judge.** The LLM judge is held out from the family that produced the answer. Because
the agents are OpenAI-only, a same-family judge would score its own family's output
with a known self-preference bias, so an Anthropic model judges by default; where an
OpenAI judge is unavoidable the writeup states it. Judge model and prompt are frozen
artifacts under ADR-0006. A human-rated subsample (via the Chainlit `feedbacks` table,
ADR-0005) calibrates the judge, and judge-human agreement is reported alongside the
scores - an uncalibrated judge is an unreported error bar.

**Statistics.** Paired bootstrap 95% confidence intervals over tasks (10,000 resamples).
Multiple-comparison correction (Benjamini-Hochberg) across the metric family, since
roughly a dozen metrics are reported per arm. Self-consistency is measured across
3 seeds per (arm, task, prompt) using the ported `sc_agreement_rate`; run-to-run
variance is reported, never averaged away, because an architecture that is better on
average but wildly unstable is not better for research use.

**Reporting.** `reports/benchmark/` carries the arm x metric table with CIs, a
cost-quality Pareto plot, per-task-type breakdowns, a per-prompt-technique effect plot,
and a failure-mode taxonomy coded from the decision logs. Every number in the report is
generated from run-store SQL, never transcribed by hand.

**Negative results ship.** If the multi-agent arm does not beat the baseline, that is
the finding and it is published as such in `reports/benchmark/`. This is written down
because the incentive to keep tuning the preferred arm until it wins is the main threat
to this experiment's validity.

## Consequences

- Cross-arm claims are defensible: any difference is attributable to architecture,
  because everything else is pinned and hash-checked.
- Per-task-type reporting makes a nuanced result expressible ("orchestration wins on
  multi-hop, loses on lookup") instead of collapsing to a single misleading verdict.
- The invalidation rule is expensive by design. Improving retrieval after phase 1
  means re-running phase 1, so infrastructure changes get batched before a phase
  boundary rather than trickling in.
- Freezing the task set early means it is authored before its weaknesses are known;
  a task-set revision is a new version and a full re-run, not an edit.
- Cross-family judging adds a second provider dependency to an otherwise OpenAI-only
  repo, accepted because same-family self-preference would undermine the headline
  metric.
- Bootstrap plus correction over 30-50 tasks yields wide intervals. Small architecture
  differences will be statistically indistinguishable, and the protocol will say so
  rather than reporting a point estimate as a win.
- **Rejected: unpaired comparison on separate task samples** - task-difficulty variance
  would swamp the architecture effect.
- **Rejected: LLM-judge scores alone, uncalibrated** - the judge becomes an unmeasured
  instrument; human calibration is what makes its scores interpretable.
- **Rejected: letting each arm tune its own retrieval** - this measures the engineer's
  effort per arm, not the architecture.

## References

- `eval/tasks/` - the frozen task set (to be built)
- `eval/metrics/` - metric modules, ported from `llm_summarization_br_ca/eval/metrics/`
- `src/tracking/queries.py` - the SQL that generates every reported number
- `reports/benchmark/` - the report
- [ADR-0002](0002-single-react-agent-research-baseline.md) - the baseline arm
- [ADR-0004](0004-retrieval-design.md) - the shared index this protocol pins
- [ADR-0005](0005-chainlit-sql-run-store.md) - source of the cost and behavior metrics
- [ADR-0006](0006-prompt-registry-freezing-policy.md) - freezing mechanics for prompts and judge
- Method lineage: `llm_summarization_br_ca/src/llm_eval_by_llm/prompt_iteration_tracker.py`

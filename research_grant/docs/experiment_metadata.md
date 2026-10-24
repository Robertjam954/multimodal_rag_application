---
title: Experiment metadata - frozen configuration
version: 0.1
date_created: 2026-09-02
last_updated: 2026-09-02
owner: Robertjam954
status: draft - not yet frozen
experiment_id: tdrb-2026-09
---

# Experiment metadata

**This is a draft control document for the later agent benchmark.** The run store and
`src/tracking/queries.py` described here do not exist yet, so no run currently carries
an `experiment_hash` or can be compared under this configuration. The active TCGA
analysis program is defined by `PLAN.md` and is not a benchmark run.

`status: draft` means every arm, model, retrieval, task, prompt, metric, and statistic
below is a proposal. It flips to `frozen` only when the first benchmark run starts. At
that point changes require an ADR and a re-run of every affected arm.

---

## 1. Arms

| Arm id | Description | Status | ADR |
|---|---|---|---|
| `single_react` | One ReAct tool-calling loop, flat registry, no routing | phase 1 | ADR-0002 |
| `langgraph_team` | Supervisor + Researcher / Analyst / Summarizer / Critic | phase 2 | ADR-0007 |
| `rag_only` | Retrieve-then-summarize, no agentic loop | proposed (open question 4) | n/a |

## 2. Models

| Role | Model | Temperature | Notes |
|---|---|---|---|
| Agent | `AGENT_MODEL` env, pinned at freeze | 0.0 | OpenAI only (locked with owner) |
| Embedding | `text-embedding-3-large` | n/a | ADR-0004 |
| Judge | `JUDGE_MODEL` env, pinned at freeze | 0.0 | **Held out from the agent's family.** Agents are OpenAI, so the judge is Anthropic by default - a same-family judge carries a known self-preference bias on the headline metric (ADR-0003) |

Exact model ids and API versions are recorded here at freeze. A model deprecation that
forces a change is an ADR plus a re-run, not a silent substitution.

## 3. Determinism

| Parameter | Value |
|---|---|
| Seeds | `[0, 1, 2]` - 3 runs per (arm, task, prompt) cell |
| Temperature | 0.0 everywhere |
| `MAX_STEPS` | 25 - hitting it records `outcome = step_cap_exceeded`, not an exception |
| Per-tool timeout | 60s (`run_analysis`: 120s) |
| Retry policy | 2 retries with backoff on transient API errors; retries counted, not hidden |

Temperature 0 is not determinism. Run-to-run variance is measured across the 3 seeds via
`sc_agreement_rate` and **reported, never averaged away** - an architecture that is
better on average but unstable is not better for research use.

## 4. Retrieval configuration (pinned - shared across all arms)

| Parameter | Value |
|---|---|
| Vector store | SQLite + `sqlite-vec`, `data/corpus.db` |
| Embedding dimensions | 3072 |
| Card types | gene; cohort-slice; result; paper |
| Chunking | whole-card where it fits; long paper/result cards chunked with parent id retained |
| Chunk size / overlap | pinned at freeze |
| Retrieval | dense top-k, `k = 8`, metadata filter on `source` and card type |
| Hybrid (BM25) | **off** in phase 1 (open question 3 - decide before freeze) |
| Corpus hash | `<auto>` - sha256 over rendered cards |

Retrieval is **not an arm property**. All arms call the same index with the same
parameters, which is the only thing that makes an architecture comparison meaningful.

## 5. Task set

| Field | Value |
|---|---|
| Location | `eval/tasks/` |
| Version | `v1` (not yet authored) |
| n tasks | 30-50 target |
| Task types | `lookup`; `aggregate`; `multi_hop`; `analysis`; `summarize`; `synthesize` |
| Reference answers | drafted from the cohort, owner-reviewed before freeze |
| Task set hash | `<auto>` |

Results are reported **per task type as well as in aggregate**. The expected finding is
that orchestration helps on `multi_hop` and `synthesize` and is pure overhead on
`lookup`; an aggregate-only number would hide exactly that.

## 6. Prompts

| Field | Value |
|---|---|
| Registry | `src/prompts/registry.json` (ADR-0006) |
| Technique axes | `zero_shot`; `few_shot`; `chain_of_thought`; `program_aided`; `rag`; `react` |
| Structured factors | `use_rag`; `use_cot`; `use_few_shot`; `use_verification` |
| Baseline agent prompt | `react` family, id pinned at freeze |
| Judge prompt | registered and versioned - an unversioned instrument makes its scores uninterpretable |
| Registry hash | `<auto>` |

## 7. Metrics

**Quality** - DeepEval faithfulness, answer relevancy, hallucination; `fabrication_by_prompt`;
extraction accuracy vs reference; citation faithfulness (does the cited row support the claim).
**Retrieval** - `precision_at_k`, recall over the known-relevant card set. Separates a
retrieval failure from a reasoning failure.
**Cost and behavior** - steps, tool calls, tool errors, recoveries, `step_cap_exceeded`
rate, tokens, latency, dollars. Read from the run store, not self-reported.

## 8. Statistics

| Parameter | Value |
|---|---|
| Design | paired at the task level - every arm sees identical tasks |
| CIs | bootstrap 95%, 10,000 resamples |
| Multiple comparisons | Benjamini-Hochberg across the metric family |
| Judge calibration | human-rated subsample via Chainlit `feedbacks`; judge-human agreement reported alongside every judge score |

With 30-50 tasks the intervals will be wide, and small architecture differences will be
statistically indistinguishable. The protocol reports that rather than presenting a
point estimate as a win.

## 9. ADR set in force

`ADR-0001, ADR-0002, ADR-0003, ADR-0004, ADR-0005, ADR-0006`

Written into every run record as `adr_set`. A result whose set differs from the current
baseline's is not directly comparable and must be re-run or labeled.

## 10. Change log

| Date | Change | ADR | Re-run required |
|---|---|---|---|
| 2026-09-02 | Initial draft | ADR-0001..0006 | n/a (not yet frozen) |

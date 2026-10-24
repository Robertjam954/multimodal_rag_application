# ADR-0006: Frozen prompt registry and prompt-effects design

Date: 2026-09-02
Status: accepted

## Context

Two things in this repo depend on prompts being first-class, versioned artifacts rather
than string literals.

First, ADR-0003's invalidation rule: a prompt is shared infrastructure, so an
uncontrolled edit silently invalidates every cross-arm comparison. A prompt living in a
Python string is edited without ceremony and without a trace in the run record.

Second, the prompt-effects experiment itself. A stated goal is to measure how prompting
technique affects agent research quality - the same question
`llm_summarization_br_ca` asked of clinical extraction, and it answered it with
machinery worth reusing rather than reinventing:

- `prompts/frozen/prompt_metadata.json` - a registry where each entry carries
  `prompt_id`, `version`, `filename`, `technique`, and boolean axes `use_rag`,
  `use_cot`, `use_few_shot`, `use_verification`, plus a `frozen` flag.
- `prompts/library/` - 17 technique variants across `zero_shot`, `few_shot`,
  `chain_of_thought`, `program_aided`, `rag`, and `react` families.
- `src/llm_eval_by_llm/prompt_iteration_tracker.py` - per-(model, prompt_approach,
  element) tracking tables and iteration trend plots.

## Decision

**Prompts live in files, never in code.** `src/prompts/library/*.txt` holds the text;
`src/prompts/registry.json` holds the metadata, in the shape used by
`prompts/frozen/prompt_metadata.json`. Code resolves a prompt by `prompt_id` through
`src/prompts/registry.py`; a literal system prompt in an agent module is a review
failure.

**Every prompt id is versioned and immutable.** Editing a frozen prompt's text is not
allowed. A change creates a new `prompt_id` (or a new version under the same family) and
leaves the old entry in place, because the old entry is the record of what earlier runs
executed. Freezing a prompt, and adding one to the benchmark set, are both ADR-worthy
under ADR-0001's scope rules.

**Coverage.** The registry holds agent system prompts (one per technique arm, and per
role once phase 2 lands), the `summarize_paper` prompts, and the **LLM judge prompt** -
the judge is an instrument, and an unversioned instrument makes its scores
uninterpretable across time.

**Experimental design.** Technique is varied while architecture, retrieval, tools, task
set, and model are held fixed - so phase 1 reports a prompt effect within the
single-agent arm, and phase 2 can ask whether the best prompt for one architecture is
the best for the other. The technique axes carried in the registry
(`use_rag` / `use_cot` / `use_few_shot` / `use_verification`) are the analysis factors,
which is why they are structured metadata and not prose in a description field.

**Tracking.** `prompt_iteration_tracker.py` is ported to read from the run store
(ADR-0005) instead of `deepeval_runs/` directories, producing the per-(model,
prompt_id, task_type) tracking table and trend plots. Its auto-refinement mode -
models proposing new prompt versions with reasoning about the failure they address - is
kept, with one hard constraint: **an auto-generated prompt is a new `prompt_id`
proposal, never an edit to a frozen one**, and it enters the benchmark set only by ADR.
Auto-refinement is a generator of candidates, not a path around the freeze.

**Run records cite prompts by id.** `runs.prompt_id` in the sidecar table (ADR-0005)
records exactly which text executed, so a result can always be traced to its prompt.

## Consequences

- Prompt effects become a measurable, reportable factor rather than an uncontrolled
  source of variance, and the phase-1 experiment has a real independent variable.
- The invalidation rule is enforceable: a prompt change is visible as a new id in every
  affected run record, so contaminated comparisons are detectable after the fact.
- The judge being versioned means score drift over the project's life is attributable
  rather than mysterious.
- Real friction on iteration. During development, improving a prompt now means a new id
  and a re-run rather than an edit-and-rerun. Mitigated by only freezing ids once they
  enter the benchmark set - development ids stay unfrozen and are excluded from reports.
- The registry accumulates dead ids. Accepted: they are the historical record, and the
  `frozen` flag plus a `status` field keeps the active set legible.
- Auto-refinement can generate candidates faster than they can be evaluated, and each
  costs a full task-set run. Candidate intake is deliberately gated by ADR review.
- **Rejected: prompts as Python constants** - convenient, invisible in run records, and
  incompatible with the freezing rule.
- **Rejected: a prompt-management SaaS** (LangSmith Hub, Literal) - real versioning, but
  it puts the experiment's most safety-critical artifact behind a network dependency and
  outside the repo's own git history.
- **Rejected: letting auto-refinement mutate frozen prompts in place** - the fastest
  path to a better score and the fastest path to an unreproducible benchmark.

## References

- `src/prompts/{registry.py,registry.json,library/}` (to be built)
- `src/analysis/prompt_iteration_tracker.py` - ported
- Ported from: `llm_summarization_br_ca/prompts/frozen/prompt_metadata.json`,
  `prompts/library/`, `src/llm_eval_by_llm/prompt_iteration_tracker.py`
- [ADR-0001](0001-record-architecture-decisions.md) - a frozen-artifact change requires an ADR
- [ADR-0003](0003-benchmark-protocol.md) - prompts as pinned shared infrastructure; the judge
- [ADR-0005](0005-chainlit-sql-run-store.md) - `runs.prompt_id`

---
paths:
  - "src/**/*.py"
  - "eval/**/*.py"
  - "tests/**/*.py"
  - "app.py"
---

# Testing rules

- Framework: `pytest`. Run `pytest tests/` before committing; keep CI green.
- Coverage: new code >80% line coverage; modified code must not decrease coverage.
- **One unit test per tool**, covering schema validation, timeout, and the error path.
  Mock every network call - tests never hit cBioPortal, OpenAI, or PubMed.
- **Agent-loop test with a stub LLM** returning a scripted tool sequence. Assert step-cap
  enforcement, tool-error recovery, and decision-log emission.
- **Run-store round trip**: run a task, drop in-memory state, rebuild the full transcript,
  artifacts, and metrics from SQL only. This is the test that makes "every number traces
  to run-store rows" real.
- **Card-renderer tests** against a parquet fixture: row counts, provenance fields
  present, `derived` marker on model-output cards.
- **Data tests**: merge diagnostics assert row counts at every join; cohort n matches
  `docs/dataset_metadata.md`.
- **Reproducibility gate**: a test fails if a frozen prompt or the task set changed
  without a matching ADR.
- Cover degrade paths, not just the happy path: no API key, empty retrieval result, tool
  timeout, cBioPortal 5xx, malformed JSON, step cap hit. The agent degrades, it does not
  crash.
- Test names describe behavior, e.g.
  `test_single_agent_records_step_cap_exceeded_without_raising`.

---
paths:
  - "src/**/*.py"
  - "eval/**/*.py"
  - "tests/**/*.py"
  - "app.py"
  - "notebooks/**"
---

# Security and data rules

## Secrets
- **No plaintext secrets in the repo.** `.env` is gitignored and stays that way; only
  `.env.example` with placeholder values is committed.
- API keys are read from the environment, never hardcoded and never defaulted to a real
  value in code.
- Never echo a secret into logs, decision traces, run records, Chainlit steps, or a commit.

## Data
- **Never commit anything under `data/`.** This includes `runs.db` and `corpus.db`.
- **TCGA public data only.** No GENIE or IMPACT patient-level data enters this repo. The
  SHAP and driver-gene *methods* are ported from `genie_impact_tcga_brain_mets`; the data
  is not. If a change would ingest patient-level data, stop - it needs an ADR and the
  `data-analysis-hygiene` skill governs.
- TCGA open-access tiers only; no controlled-access omics.
- Model outputs rendered into retrieval cards carry `source: derived`, so a derived result
  can never be presented as an observed clinical fact.

## Tools and inputs
- `run_analysis` executes model-authored code. It runs **sandboxed with no network
  access**, a bounded CPU and wall-clock limit, and a filesystem scope limited to
  `data/processed/` (read) and `reports/` (write). Never widen this without an ADR.
- Validate and bound any tool input that reaches a shell, a SQL query, or a file path.
  `query_cohort` uses parameterized queries - never string interpolation.
- External tools (cBioPortal, PubMed, OpenAI) run with timeouts and bounded retries, and
  fail without crashing an agent run.

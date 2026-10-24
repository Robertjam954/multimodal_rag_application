# Contributing

## Setup

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements-dev.txt
```

The current runnable workflows use public GDC and cBioPortal data and require no API
key. `OPENAI_API_KEY` and `ANTHROPIC_API_KEY` in `.env.example` are reserved for the
later benchmark implementation.

## Before you change anything

Ask: **does this touch a planned benchmark's retrieval, tools, task set, or prompt?**

If yes, and a benchmark run has already used it, you cannot simply edit it. Those four
are shared infrastructure (ADR-0003) - a change invalidates every cross-arm comparison
until all arms re-run. It needs an ADR and a re-run. This looks exactly like an ordinary
improvement while you are doing it, which is why it is the first question.

## ADRs

An ADR is required for: agent roster or topology; the tool registry and its boundaries;
retrieval and chunking strategy; store choice; model selection; the benchmark protocol;
the eval metric set or judge; **any change to a frozen artifact**.

Not required for: bug fixes; refactors inside an existing pattern; doc and test-only
changes; figure restyling.

Write it to `docs/adr/NNNN-short-title.md` using [`.claude/adr-template.md`](.claude/adr-template.md),
commit it **separately** from the implementation, then reference it in the implementation
commit. ADRs are immutable once accepted - supersede, never edit.

## Conventions

- Type hints on every signature; `mypy --strict` must pass.
- `ruff` + `black`; `snake_case` modules, `PascalCase` classes, `UPPER_SNAKE_CASE` constants.
- Docstrings explain **why**, not what.
- When the benchmark prompt registry exists, no prompt literals in code - resolve by
  `prompt_id`.
- No em dashes; single hyphen `-` only.
- Never commit anything under `data/`.

## Commits

Semantic format per the portfolio standard:

```
feat(agents): add ReAct loop with step cap and decision logging

Implements ADR-0002: single ReAct agent as the research-execution baseline
Refs: docs/adr/0002-single-react-agent-research-baseline.md
```

Types: `feat`, `fix`, `refactor`, `test`, `docs`, `chore`.

## PR checklist

- [ ] Tests pass; new code has >80% line coverage
- [ ] `mypy --strict`, `ruff`, `black --check` clean
- [ ] ADR written and linked if the change is in the required list
- [ ] `STATUS.md` checkboxes updated
- [ ] `requirements.txt` declares only what running code imports
- [ ] If a frozen artifact changed: ADR written, and the re-run scope stated in the PR
- [ ] `CLAUDE.md` / `README.md` updated if commands, structure, or conventions changed
- [ ] Nothing under `data/` is staged

Every PR gets the Claude code-quality review (`.github/workflows/claude-review.yml`).

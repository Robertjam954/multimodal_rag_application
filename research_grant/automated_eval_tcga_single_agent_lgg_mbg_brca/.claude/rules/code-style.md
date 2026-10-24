---
paths:
  - "src/**/*.py"
  - "eval/**/*.py"
  - "tests/**/*.py"
  - "app.py"
---

# Code style rules

- Prose and comments: single hyphen (-), never em dashes. No emojis.
- Type hints on every function signature. `from __future__ import annotations` at top.
- `mypy --strict` and `ruff` clean; format with `black`.
- Naming: `snake_case` files/functions, `PascalCase` classes, `UPPER_SNAKE_CASE` constants.
- Imports grouped stdlib -> third-party -> local.
- Docstrings: one line for simple functions, multi-line for complex logic; explain
  **why**, not what.
- **No prompt literals.** All prompt text lives in `src/prompts/library/` and resolves by
  `prompt_id` through `src/prompts/registry.py` (ADR-0006).
- **No magic numbers** for anything experimental. Step caps, timeouts, `k`, seeds, and
  thresholds come from config and are mirrored in `docs/experiment_metadata.md`.
- Config is import-safe: reading `src/config.py` must not require an LLM SDK or open a
  database connection.
- Respect the interfaces: `VectorStore` is the only thing that knows about `sqlite-vec`;
  `src/tracking/data_layer.py` is the only writer of run state.

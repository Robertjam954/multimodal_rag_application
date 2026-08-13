# Contributing

1. Open an issue describing what you'd like to change. Big design changes should land in an issue before code.
2. Fork + branch from `main`. Branch names: `feat/<slug>`, `fix/<slug>`, `docs/<slug>`.
3. Activate the venv: `source .venv/bin/activate`.
4. `pre-commit install` to wire local lint + format hooks.
5. Run `pytest` (backend) and `npm run build` + `npm run lint` (frontend) before pushing.
6. Open a PR with a clear description of the change (there is no PR template). Tag at least one reviewer.
7. If you change `app/backend/prepdocslib/`, run `python scripts/copy_prepdocslib.py` to sync function bundles.
8. If you add an env var, update every touchpoint listed in CLAUDE.md section 6 (bicep params, backend env array, and the consuming code).

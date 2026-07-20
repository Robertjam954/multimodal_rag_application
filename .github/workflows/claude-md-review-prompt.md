# Task: Update CLAUDE.md Documentation

You are tasked with reviewing and updating the CLAUDE.md file at the root of this
repository. CLAUDE.md is the operating manual that future Claude Code sessions read
before working in this codebase, so it must reflect the true, current state of the
project.

## Your Mission

Conduct a comprehensive analysis of the entire codebase and update CLAUDE.md so it is
100% accurate, complete, and useful. Where the existing CLAUDE.md and the code
disagree, **always favor the code.**

## About this project

This is a multimodal RAG application (an "AI tutor") with these moving parts:

- **Backend** (`app/backend/`) - a Quart (async Flask) app served by Gunicorn. Key
  subpackages to inspect: `approaches/` (retrieval/answer strategies), `agents/`,
  `graphrag/`, `prepdocslib/` (document ingestion/chunking/embedding), `voice/`
  (Azure Voice Live transcription bridge + LLM transcript cleanup), `core/`
  (shared Azure OpenAI / Foundry client), plus any safety, tracing, and
  config/auth modules. The entrypoint is `app.py` / `main.py`.
- **Frontend** (`app/frontend/`) - React 19 + TypeScript + Vite + Fluent UI v9.
  Inspect `src/pages/`, `src/components/`, and `src/api/`.
- **Site** (`site/`) - a Jekyll static site, if present.
- **Infra** (`infra/`) - Bicep modules deployed via Azure Developer CLI (`azd`).
- **Scripts, tests, evals** - shell/Python scripts at the repo root and in `scripts/`,
  the test suite (pytest and/or Playwright), and any evaluation harness (`evals/`).

Treat the list above as a starting map, not ground truth - verify every path exists
and document anything significant that is missing from it.

## Analysis Requirements

### 1. Project overview
- Verify the description and stated purpose match what the code actually does.
- Identify missing key features or capabilities (e.g. the voice transcription flow).

### 2. Tech stack and versions
- Backend: read `app/backend/requirements.in` / `requirements.txt` (and any
  `pyproject.toml`) for Python deps and pinned versions; note the Python version.
- Frontend: read `app/frontend/package.json` (and lockfile) for framework versions
  (React, Vite, Fluent UI, TypeScript).
- Infra/tooling: note `azure.yaml`, `azd`, Bicep, Gunicorn, Docker if used.
- Remove anything listed that is not actually used.

### 3. Commands
- Backend: how to install deps, run locally (`app/start.sh`, Quart/Gunicorn), and the
  exact dev port. Flag any known gotchas (e.g. the `quart` CLI not being on PATH after
  the venv sync, and the correct way to launch).
- Frontend: the npm/vite scripts (dev, build, lint, typecheck) and dev port.
- Tests and evals: how to run pytest, Playwright, and any eval scripts.
- `azd` provision/deploy commands.

### 4. Architecture and directory structure
- Recursively scan the tree and verify documented paths exist.
- Document the request flow: frontend -> backend routes -> approaches/agents ->
  Azure OpenAI / AI Search, and the separate `/voice/stream` WebSocket +
  `/voice/clean` path.
- Note file-naming and code conventions actually used in each area.

### 5. Backend approaches, agents, and RAG
- Summarize each module under `approaches/`, `agents/`, `graphrag/`, and
  `prepdocslib/`: what it does and when it is used.
- Document the `core` Azure OpenAI / Foundry client (`get_client`,
  `chat_deployment`, default deployment) and how other modules consume it.

### 6. Voice transcription path
- Document `voice/voice_live.py` (Azure Voice Live WebSocket bridge: API version,
  sample rate, session config, event mapping) and `voice/transcript_cleaner.py`
  (best-effort LLM cleanup with graceful fallback to the raw transcript).
- Document the `/voice/stream` WebSocket and `/voice/clean` POST routes and the
  feature flag that gates them (`USE_VOICE_DEMO`).
- Note the frontend `VoiceRecorder` component (PCM16 24 kHz AudioWorklet capture).

### 7. Frontend
- List the pages in `src/pages/` and the key components in `src/components/`.
- Document how the frontend talks to the backend (`src/api/`), and the dev proxy.

### 8. Configuration and environment variables
- Document required env vars by name only (never values): the `AZURE_*` Foundry /
  OpenAI / Speech / Voice Live settings, search/storage settings, and feature flags.
- Note how env is loaded (`load_azd_env.py`, gitignored `.azure/<env>/.env`).
- Document `azure.yaml` and the relevant Bicep parameters in `infra/`.

### 9. Scripts and automation
- Document each script in `scripts/` and at the repo root.
- Document GitHub Actions workflows in `.github/workflows/` (including this
  CLAUDE.md update workflow itself).

### 10. Development guidelines and gotchas
- Capture coding conventions, the local-run gotchas, and any non-obvious setup
  (TLS/cert issues, auth scopes, required Azure roles).

## Output Requirements

Update CLAUDE.md so that it:

1. **Preserves the existing structure and any content that is still accurate.**
2. **Adds sections** for significant findings not currently documented.
3. **Removes outdated information** (including documented workflows/paths that do not
   actually exist).
4. Uses clear, concise language and concrete examples where helpful.
5. Prioritizes the information most useful for making code changes.

## Important Notes

- Be thorough but concise - every line should earn its place.
- Document both what exists AND how to use it; call out "gotchas" explicitly.
- Never include secrets or env var values - names only.
- If documentation and reality disagree, favor reality.

## Process

1. Read the current CLAUDE.md at the repo root first.
2. Systematically analyze the codebase (backend, frontend, site, infra, scripts,
   tests, evals).
3. Edit CLAUDE.md to reflect the true state of the project, verifying every path,
   command, and version you write.

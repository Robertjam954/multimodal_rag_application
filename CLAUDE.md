# CLAUDE.md

Operating manual for Claude Code working in this repository. Keep this file 100% truthful: if reality diverges, edit this file first, then the code.

---

## 1. Project Overview

**multimodal_rag_application** is a multimodal Retrieval-Augmented Generation system with a multi-agent QA loop, voice + PDF ingestion, an optional GraphRAG layer, citation-grade file search, a Verifier agent, a SchemaFlow-style SQL agent, and LangSmith + Azure Monitor tracing. It is paired with a static portfolio site (under `site/`) that surfaces the deployed demo.

The architecture borrows patterns from [Azure-Samples/azure-search-openai-demo](https://github.com/Azure-Samples/azure-search-openai-demo) with extensions for GraphRAG, multi-agent orchestration, the Verifier, voice ingestion, content safety, and LangSmith tracing.

> **DEPLOYED REALITY (read first).** The code implements far more than the current deployment turns on. `infra/main.bicep` is a Stage-1 deploy against the pre-existing `ai-tutor` resource group (region eastus2). It creates only Log Analytics, Application Insights, ACR, a Container Apps environment, the backend Container App, and Entra ID role assignments; it references (does not recreate) the existing Foundry account/project (`ai-tutor-foundry` / `ai-tutor-ms-azure-proj`), Cosmos account (`cosmosdbaitutor7a79c7`), Blob storage (`azureblobstorageai`), and Key Vault (`ai-tutor`). Deployed facts:
> - **Chat/Responses + embeddings** go to the Azure AI Foundry project/account endpoints; there is no standalone Azure OpenAI resource.
> - **Retrieval is `DOCUMENT_RETRIEVER=cosmos`** - a Cosmos DB NoSQL vector store (`core/cosmos_vector_retriever.py`, db `rag` / container `documents`). Local dev defaults to `redis_notes`. **Azure AI Search is NOT the runtime retriever** (it lives only in the ingestion-side `prepdocslib/searchmanager.py`).
> - **Keyless / Entra ID only.** System-assigned managed identity + RBAC in `infra/app/rbac.bicep`. No API keys deployed.
> - **Flags on in the deploy:** `USE_VERIFIER`, `USE_VECTOR_SEARCH`, `USE_CHAT_HISTORY_COSMOS`, feedback. **Off:** `USE_GRAPHRAG`, `USE_MULTIMODAL`, `USE_VOICE_DEMO`, `USE_SQL_DEMO`, `USE_CONTENT_SAFETY`, `USE_PII_REDACTION`. `graph_search` / `file_search` fall back to stubs when unconfigured.
> - **Not deployed:** Azure AI Search, Speech, Vision, Content Safety, Document Intelligence, Cosmos Gremlin, Azure Managed Redis, and PostgreSQL. Bicep modules exist under `infra/core/` for several of these but are not composed into `main.bicep`. Redis is used only as an optional local cache (no-op when `REDIS_URL` unset); PostgreSQL/pgvector is aspirational (no code module). The `app/functions/` cloud-ingestion service is deferred (not in `azure.yaml`).
> - **The `docs/*.md` files referenced throughout this repo do not exist** (only `docs/hierarchical_agent_teams_template.ipynb` and `docs/images/`). Treat links to `docs/*.md` as TODOs, not sources.

### Primary capabilities

- Upload PDFs - extracted via Azure Document Intelligence (PyPDF fallback) -> sentence-aware chunking (~1000 chars, 10% overlap) -> embeddings -> configured vector store (Cosmos NoSQL when deployed); optionally also GraphRAG graph + OpenAI file_search vector store.
- Record / upload audio - Azure Speech-to-Text with diarization -> utterance entities (optional; `USE_VOICE_DEMO`).
- Multi-agent chat: Router -> Retriever (parallel graph_search + file_search) -> Answerer -> Verifier (claim-grounding gate) with streaming responses.
- SchemaFlow SQL demo: Parse -> Impact -> Plan -> SQL agents over a sample TCGA-like clinical warehouse.
- Citations rendered as page/timestamp-anchored evidence pills, deep-linked to the source PDF page or audio timestamp.
- Follow-up question suggestions, Thought-Process and Supporting-Content tabs, speech output (TTS), feedback widget, dark mode.
- Real-time content safety filtering (Azure AI Content Safety) and PII redaction at ingestion.
- End-to-end tracing in LangSmith and Azure Monitor (OpenTelemetry).

---

## 2. Tech Stack

### Backend (`app/backend/`)
- **Framework:** Quart 0.19+ (async Flask-compatible) behind Gunicorn with a uvloop worker (`custom_uvicorn_worker.py`).
- **Python:** 3.11 (pinned in `pyproject.toml`).
- **Dependency manager:** `uv` (`uv pip compile requirements.in -o requirements.txt`).
- **Azure SDKs:** `azure-identity`, `azure-search-documents` (knowledgebases preview), `azure-ai-documentintelligence`, `azure-cognitiveservices-speech`, `azure-storage-blob`, `azure-cosmos`, `azure-monitor-opentelemetry`, `azure-ai-contentsafety`, `azure-ai-language` (PII redaction).
- **OpenAI / Foundry:** `openai >= 1.50` (Responses API for `file_search`), `AzureOpenAI` for hosted deployments. Reasoning models (o-series) supported via `reasoning_effort` overrides.
- **Agent orchestration:** LangGraph in-process; LangSmith captures every node + tool span. Azure AI Foundry Agent Service used for hosted agents when latency tolerates it.
- **GraphRAG:** Microsoft `graphrag` package for offline indexing; Cosmos DB Gremlin API for live graph CRUD; community summaries refreshed via `graphrag/community.py`.
- **Tracing:** `langsmith` + OpenTelemetry (`opentelemetry-instrumentation-openai`, `-httpx`, `-asgi`, `-aiohttp-client`) -> Azure Monitor + LangSmith Cloud.
- **Safety:** `safety/content_safety.py` filters prompt + completion at inference; `safety/pii.py` redacts at ingestion.
- **Prompts:** Jinja2 under `approaches/prompts/`, loaded by `PromptManager`.

### Frontend (`app/frontend/`)
- **Framework:** React 19 + TypeScript + Vite 5.
- **UI:** Fluent UI v9. Dark mode toggle.
- **Streaming:** SSE (`@microsoft/fetch-event-source`) for Answer + Verifier verdict + token usage as separate events on one stream.
- **PDF viewer:** `react-pdf` with page-jump on citation click.
- **Audio:** Web Audio API + WebSocket -> backend `/voice/stream`; partial transcripts rendered live.
- **State:** React Query for server state; `zustand` for chat session state.
- **i18n:** `i18next` (English shipped; folder skeleton for other locales).
- **Graph viz:** `@antv/g6` for the knowledge-graph node-link panel.
- **Build:** Vite -> `app/frontend/build/`, served as static by Quart in production.

### Static portfolio (`site/`)
- **Framework:** none - a single self-contained static `site/index.html` (inline CSS, Google Fonts). `_layouts/` and `_includes/` folders exist but `_posts/` is empty and there is no `_config.yml` or `Gemfile` (not a Jekyll build).
- **Deployed:** GitHub Pages via `.github/workflows/pages.yml`, which uploads `site/` as-is with `.nojekyll` (no Jekyll build step).

### Infra (`infra/`)
- **Bicep + azd.** Modules under `infra/core/` (ai, host, storage, security, monitor, search, cosmos).
- **Entry:** `infra/main.bicep`, parameters in `infra/main.parameters.json`.
- **Environment variables:** managed via `azd env set KEY value` and emitted into `appEnvVariables` in `main.bicep`.

### Functions (`app/functions/`)
- Cloud-ingestion custom skills (mirrors Azure demo's pattern):
  - `document_extractor/` - DocIntel-backed PDF -> markdown + figures.
  - `figure_processor/` - figure crop + caption + embedding.
  - `text_processor/` - chunk + embed + Search index push.
  - `audio_transcriber/` - Speech-to-Text -> utterance JSON.
  - `graph_indexer/` - emits entities/edges to Cosmos Gremlin + GraphRAG community refresh.
- Each function bundles a synchronized copy of `prepdocslib` (refresh with `python scripts/copy_prepdocslib.py`).

### Tests (`tests/`)
- `pytest` + `pytest-asyncio`.
- `tests/e2e/e2e.py` - Playwright. Build frontend first.
- `tests/test_app.py` - API integration with mocked Azure clients (mocks in `tests/conftest.py`).
- `tests/test_*.py` - unit per module.

### Evals (`evals/`)
- Promptfoo + `ai-rag-chat-evaluator`.
- `safety_evaluation.py` uses Azure AI Foundry adversarial simulator (hate, sexual, violence, self_harm).
- `verifier_eval.py` over `verifier_golden.jsonl`.

---

## 3. Repository Layout

```
multimodal_rag_application/
├── CLAUDE.md README.md AGENTS.md CONTRIBUTING.md SECURITY.md LICENSE
├── azure.yaml                              # azd config
├── pyproject.toml requirements-dev.txt
├── package.json                            # root convenience scripts
├── .pre-commit-config.yaml .markdownlint-cli2.jsonc ps-rule.yaml
├── locustfile.py
│
├── site/                                   # static portfolio (no Jekyll build)
│   ├── index.html                          # self-contained page
│   ├── .nojekyll
│   ├── _layouts/ _includes/ _posts/ (empty)
│   └── assets/
│
├── app/
│   ├── start.sh start.ps1
│   ├── backend/
│   │   ├── Dockerfile gunicorn.conf.py custom_uvicorn_worker.py
│   │   ├── app.py main.py config.py decorators.py error.py
│   │   ├── load_azd_env.py
│   │   ├── prepdocs.py setup_cloud_ingestion.py
│   │   ├── requirements.in requirements.txt
│   │   ├── approaches/
│   │   │   ├── approach.py
│   │   │   ├── chatreadretrieveread.py
│   │   │   ├── multiagent_approach.py
│   │   │   ├── sql_schemaflow_approach.py
│   │   │   ├── promptmanager.py
│   │   │   └── prompts/
│   │   │       ├── chat_answer.system.jinja2 chat_answer.user.jinja2
│   │   │       ├── query_rewrite.system.jinja2 chat_query_rewrite_tools.json
│   │   │       ├── router.system.jinja2
│   │   │       ├── verifier.system.jinja2 verifier.user.jinja2
│   │   │       ├── followups.system.jinja2
│   │   │       └── sql/{parse,impact,plan,sql}.system.jinja2
│   │   ├── agents/
│   │   │   ├── router.py retriever.py answerer.py verifier.py
│   │   │   ├── sql_schemaflow.py
│   │   │   ├── tools.py graph.py
│   │   │   └── foundry_client.py
│   │   ├── graphrag/
│   │   │   ├── indexer.py retriever.py cosmos_gremlin.py community.py entity_extractor.py
│   │   ├── prepdocslib/
│   │   │   ├── blobmanager.py pdfparser.py htmlparser.py csvparser.py jsonparser.py textparser.py
│   │   │   ├── figureprocessor.py mediadescriber.py
│   │   │   ├── textsplitter.py embeddings.py
│   │   │   ├── searchmanager.py
│   │   │   ├── filestrategy.py integratedvectorizerstrategy.py cloudingestionstrategy.py
│   │   │   ├── listfilestrategy.py page.py parser.py strategy.py servicesetup.py
│   │   ├── voice/
│   │   │   ├── speech_client.py diarizer.py audio_uploader.py
│   │   ├── safety/
│   │   │   ├── content_safety.py pii.py
│   │   ├── tracing/
│   │   │   ├── otel.py langsmith.py
│   │   ├── core/
│   │   │   ├── authentication.py sessionhelper.py modelhelper.py costmeter.py
│   │   ├── chat_history/
│   │   │   ├── cosmosdb.py browser.py
│   ├── frontend/
│   │   ├── package.json vite.config.ts tsconfig.json .npmrc .prettierrc.json index.html
│   │   ├── src/
│   │   │   ├── main.tsx App.tsx router.tsx theme.ts
│   │   │   ├── api/{api.ts, models.ts, stream.ts}
│   │   │   ├── components/
│   │   │   │   ├── Answer/ Citations/ ThoughtProcess/ SupportingContent/
│   │   │   │   ├── VerifierBadge/ FollowUps/ Settings/ Feedback/
│   │   │   │   ├── GraphView/ PDFViewer/ VoiceRecorder/ SchemaFlowPanel/
│   │   │   ├── pages/{chat,papers,voice,sql,portfolio}/
│   │   │   ├── lib/{cost.ts, theme.ts, deepLink.ts}
│   │   │   └── locales/en/translation.json
│   │   └── public/
│   └── functions/
│       ├── document_extractor/ figure_processor/ text_processor/ audio_transcriber/ graph_indexer/
│
├── infra/
│   ├── main.bicep main.parameters.json main.test.bicep
│   ├── backend-dashboard.bicep network-isolation.bicep private-endpoints.bicep
│   ├── core/
│   │   ├── ai/{openai,documentintelligence,speech,vision,contentsafety,foundryhub,foundryproject}.bicep
│   │   ├── search/search-services.bicep
│   │   ├── storage/storage-account.bicep
│   │   ├── cosmos/{cosmos-sql,cosmos-gremlin}.bicep
│   │   ├── host/{container-app,container-apps-environment,functions-app}.bicep
│   │   ├── monitor/{applicationinsights,log-analytics,dashboard}.bicep
│   │   └── security/{keyvault,role,identity}.bicep
│   └── app/{backend,functions}.bicep
│
├── scripts/
│   ├── prepdocs.sh prepdocs.ps1
│   ├── copy_prepdocslib.py
│   ├── setup_cloud_ingestion.{sh,ps1,py}
│   ├── auth_init.{sh,ps1,py} auth_update.{sh,ps1,py} auth_common.py
│   ├── roles.{sh,ps1}
│   ├── load_azd_env.py load_python_env.{sh,ps1}
│   ├── manageacl.py sampleacls.json
│   ├── seed_graph.py
│   └── cost_alerts.bicep
│
├── evals/
│   ├── requirements.txt evaluate_config.json evaluate_config_multimodal.json
│   ├── generate_ground_truth.py evaluate.py
│   ├── safety_evaluation.py verifier_eval.py
│   ├── ground_truth.jsonl ground_truth_multimodal.jsonl verifier_golden.jsonl
│   └── results/
│
├── tests/
│   ├── conftest.py
│   ├── test_app.py test_approaches.py test_verifier.py test_graphrag.py test_voice.py
│   ├── test_prepdocslib_textsplitter.py test_prepdocslib_pdfparser.py
│   └── e2e/e2e.py
│
├── docs/
│   ├── architecture.md data_ingestion.md graphrag.md verifier.md
│   ├── voice.md multimodal.md agentic_retrieval.md sql_schemaflow.md
│   ├── citations.md tracing.md monitoring.md
│   ├── evaluation.md safety_evaluation.md
│   ├── productionizing.md localdev.md
│   └── images/
│
├── data/{papers,audio,graphs}/
├── .devcontainer/{devcontainer.json,Dockerfile,docker-compose.yml,post-create.sh}
└── .github/workflows/{pages,update-claude-md}.yml   # (only these exist; no azure-dev/tests/eval workflows yet)
```

---

## 4. Architecture (services + data flow)

See `docs/architecture.md` for full mermaid diagrams. Summary:

```
Browser (React 19 + Vite)
  │  HTTPS / SSE / WebSocket
Quart backend (Container Apps)
  ├── /chat            (streaming SSE: token, verifier, followups, cost)
  ├── /papers/upload   (per-session ADLS path, ACL-tagged)
  ├── /voice/stream    (WS -> Azure Speech-to-Text)
  ├── /sql/plan        (SchemaFlow Parse/Impact/Plan/SQL)
  ├── /config /auth_setup
  ├── /chat_history    (Cosmos SQL + browser localStorage fallback)
  └── /feedback        (thumbs + free-text -> eval pool)
  │
  ├── Azure AI Foundry project + account (chat/Responses + embeddings)   [deployed]
  ├── Azure Cosmos DB NoSQL: vector store (primary retrieval) + chat history  [deployed]
  ├── Azure Blob Storage / ADLS Gen2 (raw + figures + per-user paths)    [deployed]
  ├── Application Insights (OTel sink) + Key Vault                       [deployed]
  ├── OpenAI Responses file_search (citation-grade)                [optional/code]
  ├── Cosmos DB Gremlin knowledge graph + GraphRAG                 [optional/code]
  ├── Azure Document Intelligence (PDF layout/OCR)                 [optional/code]
  ├── Azure Speech-to-Text (long-form + diarization)              [optional/code]
  ├── Azure AI Content Safety + Azure AI Language (PII)            [optional/code]
  ├── Azure AI Search (ingestion-side only, not runtime retrieval) [optional/code]
  ├── Redis (semantic/embedding cache; no-op when REDIS_URL unset) [optional/code]
  └── LangSmith (tracing)                                          [optional/code]
```

### Chat query flow

1. `POST /chat` (SSE).
2. `multiagent_approach.run_stream()`:
   - `Router` -> `{factual, multihop, summarize, sql}`.
   - `Retriever` calls in parallel: GraphRAG (local + global + drift) and OpenAI file_search; rerank + dedup. SQL questions route to `sql_schemaflow_approach`.
   - `Answerer` streams tokens with inline `[doc:page]` / `[recording:t=120s]` citation markers.
   - `Verifier` runs claim-by-claim grounding. If unsupported claims > 0, one retry; otherwise unsupported sentences become "insufficient evidence".
   - `FollowUps` emits 3 suggested next questions.
3. SSE events: `token`, `citation`, `claim`, `verdict`, `followups`, `cost`, `done`.

### Verifier gating + streaming

- Tokens stream as the Answerer generates.
- A second SSE channel carries the Verifier verdict once each sentence completes.
- The UI renders unverified sentences greyed out; verified ones become normal text; rejected ones are visually struck and replaced with the verdict reason.

### Ingestion flow (PDFs)

`scripts/prepdocs.sh` -> `prepdocs.py` -> `prepdocslib` pipeline:
1. List files (local FS or ADLS Gen2 user paths).
2. PII redaction (`safety/pii.py`) before any text leaves the trust boundary.
3. Document extraction (DocIntel default; PyPDF fallback).
4. Figure processing (crop + describe + embed) when `USE_MULTIMODAL=true`.
5. Entity extraction (`graphrag/entity_extractor.py`) -> `Paper`, `Section`, `Figure`, `Author`, `Citation` nodes.
6. Text processing (figure merge + chunk + embed).
7. Index push to Azure AI Search, OpenAI file_search vector store, and Cosmos Gremlin graph.
8. Community refresh (`graphrag/community.py:refresh()`).

### Ingestion flow (audio)

1. Browser WebSocket -> `/voice/stream` -> Azure Speech-to-Text (long-form + diarization).
2. `voice/diarizer.py` emits `{recording_id, utterance_id, speaker, start, end, text}` events.
3. Partial transcripts stream back to UI for live display.
4. On finalization: `graph_indexer` writes `Utterance` + `Recording` + `Topic` nodes; transcript text joins the standard text-processing pipeline.
5. Audio file lands in Blob; playback in UI is timestamp-synced to citations.

### Data and storage tier (canonical database choices)

Authoritative mapping of which datastore owns what. The retrieval backend is pluggable via `DOCUMENT_RETRIEVER` (`core/document_retriever.py`). For **this** app the deployed retriever is **Cosmos DB NoSQL vector store**; local dev defaults to a Redis-backed notes store. Azure AI Search is NOT a runtime retrieval backend here.

| Concern | Store / service | What it owns | Notes |
|---|---|---|---|
| **Primary vector search + retrieval (deployed)** | **Azure Cosmos DB for NoSQL** vector store | chunk embeddings + text | `core/cosmos_vector_retriever.py`; db `rag`, container `documents`. Selected by `DOCUMENT_RETRIEVER=cosmos`. |
| Primary retrieval (local dev default) | Redis-backed notes store | notes chunks + embeddings | `core/document_retriever.py:RedisNotesRetriever` (`DOCUMENT_RETRIEVER=redis_notes`). Requires `REDIS_URL`. |
| Citation vector store (optional) | OpenAI Responses `file_search` | per-file vector store for citation-grade spans | `agents/tools.py:file_search`; stubs when no vector store id/key. External (OpenAI), not Azure. |
| **Conversation history** | **Azure Cosmos DB for NoSQL** | chat sessions/messages | `chat_history/cosmosdb.py` (db `chat`, container `history`); registered only when `USE_CHAT_HISTORY_COSMOS=true`. |
| Knowledge graph (optional) | Azure Cosmos DB for Apache Gremlin | entities / edges / community nodes | `graphrag/cosmos_gremlin.py`. Not deployed (`USE_GRAPHRAG=false`); `graph_search` stubs without a Cosmos Gremlin account. |
| In-memory cache (optional) | Redis (semantic + embedding cache) | LLM-response cache keyed by embedding similarity; embedding cache | `core/semantic_cache.py`. No-op when `REDIS_URL` unset. Ephemeral / TTL'd; never a source of truth. |
| Ingestion-side search index (optional, not runtime retrieval) | Azure AI Search | chunk index built during ingestion | `prepdocslib/searchmanager.py`, `servicesetup.py`. Not queried by the chat retriever. |
| Files / blobs | Azure Blob Storage / ADLS Gen2 | raw PDFs, audio, figures, per-user uploads | `prepdocslib/blobmanager.py`. |
| Embedding **producer** (not a store) | Azure AI Foundry `text-embedding-3-large` (deployed; local `.env` may use `-3-small`) | text vectors written into the retriever's vector store | `core/embeddings_client.py`. |

**PostgreSQL / pgvector:** aspirational. There is no pgvector code module in the backend and no Postgres in `main.bicep`; do not document it as a live tier.

---

## 5. Commands

Activate venv: `source .venv/bin/activate`.

### Setup
```bash
azd auth login
azd env new robertjames-mmrag
azd up                        # provisions Azure + deploys backend/frontend/functions
./scripts/prepdocs.sh         # ingests data/papers/
python scripts/seed_graph.py
```

### Local dev
```bash
# Backend (port 50505)
cd app/backend && uv pip sync requirements.txt && uv run quart --app main:app run --port 50505

# Frontend (port 5173, proxies /api -> :50505)
cd app/frontend && npm install && npm run dev

# Static site: just open site/index.html in a browser (no build server)

# Backend + frontend together
./app/start.sh
```

### Local-only mode (no Azure)
Set `MODE=local` to swap AOAI for Ollama, Speech for faster-whisper, Search for FAISS, and Cosmos for SQLite. Useful for contributors without Azure. See `docs/localdev.md`.

### Tests
```bash
pytest                                              # all
pytest tests/test_verifier.py
pytest --cov --cov-report=annotate:cov_annotate
cd app/frontend && npm run build && cd ../.. && pytest tests/e2e/e2e.py
```

### Evals
```bash
python -m venv .evalenv && source .evalenv/bin/activate
pip install -r evals/requirements.txt
python evals/generate_ground_truth.py --numquestions=200
python evals/evaluate.py
python evals/safety_evaluation.py --target_url http://localhost:50505/chat --max_simulations 200
python evals/verifier_eval.py
```

### Lint / types
```bash
ty check
ruff check . && ruff format .
cd app/frontend && npm run lint
pre-commit run --all-files
```

### Load test
```bash
locust -f locustfile.py --host http://localhost:50505
```

### Ingestion ops
```bash
./scripts/prepdocs.sh
./scripts/prepdocs.sh --removeall
./scripts/prepdocs.sh --category "scientific-paper"
python scripts/copy_prepdocslib.py
```

---

## 6. Environment variables

Set via `azd env set KEY value`. New ones that the container needs must be added to:
1. `infra/main.parameters.json` (if surfaced as a param)
2. `infra/main.bicep` (top-level param and/or the backend module's `env` array in `infra/app/backend.bicep`)
3. `app/backend/prepdocs.py` and/or `app/backend/app.py:_setup_clients()` if consumed by code

(There is no `azure-dev.yml` workflow; deployment is via `azd up` locally.)

Key vars (note: many below belong to optional/off features; the deployed env is defined in `infra/main.bicep`):

| Variable | Purpose |
|---|---|
| `AZURE_OPENAI_SERVICE` | AOAI resource name |
| `AZURE_OPENAI_CHATGPT_DEPLOYMENT` | chat deployment (default `gpt-4.1-mini`) |
| `AZURE_OPENAI_EMB_DEPLOYMENT` | embedding deployment (default `text-embedding-3-large`) |
| `AZURE_OPENAI_EVAL_DEPLOYMENT` | eval LLM |
| `AZURE_OPENAI_REASONING_DEPLOYMENT` | optional o-series for `reasoning_effort=high` |
| `AZURE_OPENAI_KNOWLEDGEBASE_DEPLOYMENT` | agentic-retrieval planner |
| `AZURE_SEARCH_SERVICE` `AZURE_SEARCH_INDEX` | AI Search |
| `AZURE_DOCUMENTINTELLIGENCE_SERVICE` | DocIntel |
| `AZURE_SPEECH_SERVICE_ID` `AZURE_SPEECH_SERVICE_LOCATION` | Speech |
| `AZURE_CONTENTSAFETY_ENDPOINT` | inference-time safety |
| `AZURE_LANGUAGE_ENDPOINT` | PII redaction |
| `AZURE_STORAGE_ACCOUNT` `AZURE_STORAGE_CONTAINER` `AZURE_USER_STORAGE_ACCOUNT` | Blob / ADLS Gen2 |
| `AZURE_COSMOSDB_ACCOUNT` `AZURE_COSMOSDB_CHAT_DATABASE` `AZURE_COSMOSDB_GRAPH_DATABASE` | Cosmos: JSON docs + chat history + graph |
| `AZURE_REDIS_HOST` `AZURE_REDIS_PORT` | Azure Managed Redis endpoint (AAD auth; no key in env) |
| `AZURE_POSTGRES_HOST` `AZURE_POSTGRES_DATABASE` `AZURE_POSTGRES_USER` | PostgreSQL Flexible Server (pgvector + azure_ai) |
| `APPLICATIONINSIGHTS_CONNECTION_STRING` | OTel sink |
| `USE_MULTIMODAL` | Image extraction + vision |
| `USE_AGENTIC_KNOWLEDGEBASE` | AI Search knowledge agent |
| `USE_GRAPHRAG` | Cosmos graph retrieval |
| `USE_REDIS_CACHE` | Azure Managed Redis: semantic cache + working memory + app cache |
| `USE_POSTGRES_VECTOR` | PostgreSQL pgvector + azure_ai secondary analytics |
| `USE_VERIFIER` | Verifier pass |
| `USE_VOICE_DEMO` `USE_SQL_DEMO` | Demo route flags |
| `USE_CONTENT_SAFETY` `USE_PII_REDACTION` | Safety toggles |
| `USE_FEEDBACK` | Feedback widget + endpoint |
| `USE_LOCAL_MODE` | Ollama/faster-whisper/FAISS/SQLite swap |
| `USE_EVAL` `USE_AI_PROJECT` | Provisions eval model + Foundry project |
| `RATE_LIMIT_PER_MIN` | Per-IP rate limit |
| `MAX_TOKENS_PER_SESSION` | Cost cap per chat session |
| `OPENAI_API_KEY` `OPENAI_FILE_SEARCH_VECTOR_STORE_ID` | Responses API file_search |
| `LANGSMITH_API_KEY` `LANGSMITH_PROJECT` | Tracing |
| `TRACELOOP_TRACE_CONTENT` | Set `false` to redact prompts in traces |

`.env` files are gitignored. `azd env get-values > .env.local` to dump for local dev.

---

## 7. Adding things (recipes)

### Add an approach / agent

1. New file in `app/backend/approaches/<name>_approach.py` extending `approach.Approach`.
2. Prompts under `approaches/prompts/<name>/`.
3. Register in `app/backend/config.py` and wire in `app.py:setup_clients()`.
4. Route in `app.py` blueprint.
5. If used by the multiagent graph, add tool defs in `agents/tools.py` and node in `agents/graph.py`.
6. Tests under `tests/test_<name>.py`; mock at the HTTP layer (see `conftest.py`).

### Add a parser

1. `prepdocslib/<format>parser.py` implementing `Parser`.
2. Register in `prepdocs.py:setup_file_processors()`.
3. `python scripts/copy_prepdocslib.py` to sync into function bundles.
4. Update `docs/data_ingestion.md`.

### Add a Verifier rule

Extend `agents/verifier.py:verify_claim()`. Add golden examples to `evals/verifier_golden.jsonl`. Run `python evals/verifier_eval.py`.

### Add a developer setting

Frontend: `api/models.ts` (`ChatAppRequestOverrides`), `components/Settings/Settings.tsx`, `locales/en/translation.json`, `pages/chat/Chat.tsx`.
Backend: `approaches/multiagent_approach.py` reads from `overrides`; expose via `/config` if needed.

---

## 8. Tracing, monitoring, evals

- **OTel:** `tracing/otel.py` -> Azure Monitor. View in App Insights `Investigate > Performance` and `Failures`.
- **LangSmith:** `tracing/langsmith.py` -> `@traceable` decorator wraps every agent + tool. Project name comes from `LANGSMITH_PROJECT`.
- **Redact bodies:** `TRACELOOP_TRACE_CONTENT=false`.
- **Cost meter:** `core/costmeter.py` tracks per-session input/output tokens; surfaced in `/chat` `cost` SSE event.
- **Dashboard:** `azd monitor`.
- **CI:** the only GitHub Actions workflows present are `pages.yml` (portfolio deploy) and `update-claude-md.yml`. There is no test/eval CI workflow yet; run `pytest` and the eval scripts locally.

---

## 9. Auth + ACLs + safety

- Optional Entra ID login (MSAL). Enable: `azd env set AZURE_USE_AUTHENTICATION true`.
- Per-document ACLs via `scripts/manageacl.py` and `decorators.py:@authenticated_path`.
- Per-session user uploads land under `user-content/<oid>/...` in ADLS Gen2.
- Inference-time content safety: `safety/content_safety.py` evaluates prompts + completions; blocks high-severity categories.
- Ingestion-time PII redaction: `safety/pii.py` uses Azure AI Language to strip names/MRNs/SSNs before text leaves the trust boundary.
- Rate limiting: `RATE_LIMIT_PER_MIN` per IP enforced in `decorators.py:@ratelimited`.
- Cost cap: `MAX_TOKENS_PER_SESSION` enforced by `core/costmeter.py`.

---

## 10. Gotchas

- **Knowledge Agent preview SDK:** pin `azure-search-documents` with the preview wheel that includes `knowledgebases`.
- **Function bundles:** every `prepdocslib/` change requires `python scripts/copy_prepdocslib.py` or function deploys ship stale code.
- **Eval venv separate:** `evals/` deps conflict with backend. Use `.evalenv`.
- **Frontend build before e2e:** Playwright tests use `app/frontend/build/`.
- **Cosmos Gremlin throughput:** default RU/s is low. Scale up in `infra/core/cosmos/cosmos-gremlin.bicep` before bulk graph indexing.
- **GraphRAG community refresh:** updating the graph does NOT auto-refresh community summaries. Call `graphrag/community.py:refresh()`.
- **Dual vector stores:** Azure AI Search (retrieval) and OpenAI file_search (citations) must stay in sync. `prepdocs.sh` writes to both.
- **Multimodal model swap:** if changing the chat model, confirm it supports image input (`gpt-4o`, `gpt-4o-mini`, `gpt-4.1-mini`).
- **Portfolio site:** `site/index.html` is served as-is by `.github/workflows/pages.yml` (no Jekyll build, no `DEMO_URL` injection). Edit the HTML directly.
- **iCloud dataless files:** anything under `~/Documents/` may be evicted - copy or `dd` materialize before ingestion.
- **Retriever selection:** primary retrieval is chosen by `DOCUMENT_RETRIEVER` (`cosmos` deployed, `redis_notes` local). Do not describe Azure AI Search as the runtime retriever - it is ingestion-side only.
- **Redis is optional + ephemeral:** `core/semantic_cache.py` no-ops when `REDIS_URL` is unset. Cosmos NoSQL is the durable source of truth for conversations.
- **No em dashes anywhere.** Use single hyphen `-` only.
- **No end-of-turn recaps in chat-app responses** (user preference applies to dev workflow only, not application code).

---

## 11. Dependencies

- Python deps: `app/backend/requirements.in` is the real dependency list. `requirements.txt` currently just does `-r requirements.in` (not yet a compiled pin set); the Dockerfile installs from `requirements.in`.
- Node pins: `app/frontend/package-lock.json`. `.npmrc` has `legacy-peer-deps=true`.
- Bicep modules: `infra/core/` (one folder per resource family; not all are wired into `main.bicep`).
- Portfolio site: plain `site/index.html` (no Gemfile / Jekyll).

Upgrade backend:
```bash
cd app/backend && uv pip compile requirements.in -o requirements.txt --python-version 3.11 --upgrade-package <pkg>
source .venv/bin/activate && pytest tests/
```

Upgrade frontend:
```bash
cd app/frontend && npm install <pkg>@latest && npm run build
cd ../.. && pytest tests/e2e/e2e.py
```

---

## 12. Coding conventions

- Backend: 4-space indent, type hints required, async-first, `logging.getLogger(__name__)`, no bare `Exception`.
- Frontend: Prettier + ESLint, functional components, co-located `.module.css`.
- Prompts: every Jinja2 file starts with a header comment naming agent + expected inputs.
- Tests: mock at the HTTP transport layer (httpx), not at SDK methods. Fixtures in `tests/conftest.py`.
- No emojis in code/docs unless explicitly requested.
- Default Claude pipeline model: `claude-sonnet-4-20250514` (per user memory).

---

## 13. Integration matrix

Legend: **[D]** wired in the deployment, **[O]** optional/code-only (off or stubbed in the deploy).

| Service | What for | Status | Where wired |
|---|---|---|---|
| Azure AI Foundry (project + account) | chat/Responses + embeddings | [D] | `core/aoai_client.py`, `core/embeddings_client.py`, `agents/*` |
| Cosmos NoSQL vector store | primary retrieval (deployed) | [D] | `core/cosmos_vector_retriever.py` |
| Cosmos NoSQL | chat history | [D] | `chat_history/cosmosdb.py` |
| Blob / ADLS Gen2 | raw + processed + user uploads | [D] | `prepdocslib/blobmanager.py` |
| Application Insights | OTel sink | [D] | `tracing/otel.py` |
| Key Vault | secrets | [D] | RBAC in `infra/app/rbac.bicep` |
| OpenAI Responses file_search | citations | [O] | `agents/tools.py:file_search` (stubs if no vector store id) |
| Cosmos Gremlin + GraphRAG | knowledge graph | [O] | `graphrag/cosmos_gremlin.py`, `agents/tools.py:graph_search` |
| Azure AI Search | ingestion-side index (not runtime retrieval) | [O] | `prepdocslib/searchmanager.py` |
| Azure Document Intelligence | PDF layout/OCR | [O] | `prepdocslib/pdfparser.py` |
| Azure Speech / Voice Live | audio -> text + diarization | [O] | `voice/speech_client.py`, `voice/voice_live.py` |
| Azure AI Content Safety | runtime prompt/completion filtering | [O] | `safety/content_safety.py` |
| Azure AI Language | PII redaction at ingestion | [O] | `safety/pii.py` |
| Redis | semantic + embedding cache | [O] | `core/semantic_cache.py` (no-op without `REDIS_URL`) |
| LangSmith | tracing | [O] | `tracing/langsmith.py` |
| GitHub Pages | portfolio host | [D] | `.github/workflows/pages.yml` |

PostgreSQL / pgvector and Azure Managed Redis as a managed tier are aspirational - no backend module and not in `main.bicep`.

---

## 14. Self-update prompt

When asked "update CLAUDE.md to reflect the current codebase":

1. `find . -maxdepth 4 -type f -not -path "*/node_modules/*" -not -path "*/.venv/*" -not -path "*/.git/*"`.
2. Read every `*.toml`, `*.json` config, `*.bicep`, every approach + agent module, every script, every workflow.
3. Verify every path, command, and env var in this file against reality. Reality wins.
4. Update sections 2-13 in place. Do not append "v2" sections.
5. Re-run `pytest` and `npm run build` to confirm; flag any that fail.
6. Commit: `docs(claude): sync CLAUDE.md with codebase`.

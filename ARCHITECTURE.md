# Architecture

multimodal_rag_application is an end-to-end multimodal Retrieval-Augmented Generation
(RAG) system. It ingests PDFs and audio, builds a vector store plus optional graph and
citation stores, and answers questions through a streaming multi-agent loop gated by a
Verifier. It is deployed on Azure (Container Apps + azd + Bicep) and paired with a
static portfolio site under `site/`.

The code implements a broad feature set behind `USE_*` feature flags; the current
deployment enables a focused subset. The list below marks what the deployed
configuration wires up versus what is optional/code-only.

## High-level shape

```
Browser (React 19 + Vite, Fluent UI)
   |  HTTPS / Server-Sent Events / WebSocket
Quart backend (async, Gunicorn + uvloop worker, Container Apps)
   |
   +-- Azure AI Foundry project + account (chat/Responses + embeddings)   [deployed]
   +-- Azure Cosmos DB NoSQL: vector store (primary retrieval)            [deployed]
   +-- Azure Cosmos DB NoSQL: chat history                               [deployed]
   +-- Azure Blob / ADLS Gen2 (raw PDFs, audio, figures, uploads)         [deployed]
   +-- Application Insights (OpenTelemetry sink) + Key Vault              [deployed]
   |
   +-- OpenAI Responses file_search (citation-grade spans)          [optional/code]
   +-- Cosmos DB Gremlin knowledge graph + GraphRAG                 [optional/code]
   +-- Azure Document Intelligence (PDF layout/OCR)                 [optional/code]
   +-- Azure Speech / Voice Live (long-form + diarization)          [optional/code]
   +-- Azure AI Content Safety + Azure AI Language (PII redaction)  [optional/code]
   +-- Azure AI Search (hybrid retriever + ingestion index)  [optional/gated infra]
   +-- Redis (semantic + embedding cache; no-op when REDIS_URL unset)[optional/code]
   +-- LangSmith (tracing)                                          [optional/code]
```

Note: `DOCUMENT_RETRIEVER` selects the retrieval backend. Three are registered
(`core/document_retriever.py`): `cosmos` (Cosmos NoSQL vector store, deployed),
`redis_notes` (Redis-backed notes store, local dev default), and `azure_search`
(`core/azure_search_retriever.py`, hybrid BM25 + vector with optional semantic rerank).
The Search service itself is composed into `infra/main.bicep` behind `useAzureSearch`
(default `false`), so no Search resource is provisioned or billed until flipped.

Active direction (see `STATUS.md`): local Obsidian-vault RAG with local models via
Ollama (`MODE=local` routes chat through `agents/_llm.py`; vault ingestion via
`prepdocslib/obsidianstrategy.py` is done, a dedicated `obsidian` retriever and Ollama
embedding routing are open items).

## Main components

### Backend (`app/backend/`)
Async Quart application served by Gunicorn with a custom uvloop/uvicorn worker.
Routes (see `app.py`): `/chat` and `/chat/nonstream`, `/sql/plan`, `/papers/upload`,
`/voice/stream` (WebSocket), `/voice/clean`, `/content/<file>`, `/feedback`,
`/config`, `/auth_setup`, plus the SPA shell routes (`/`, `/papers`, `/voice`, `/sql`,
`/embed`). A Cosmos chat-history blueprint is registered only when
`USE_CHAT_HISTORY_COSMOS=true`. A separate standalone Chainlit app (`chainlit_app.py`)
exists but is not part of the Quart app.

- **approaches/** - request orchestration. `multiagent_approach.py` runs the streaming
  Router -> Retriever -> Answerer -> Verifier loop; `hierarchical_multiagent_approach.py`
  is an opt-in supervisor/teams alternative (`USE_HIERARCHICAL_AGENTS=true`, identical
  SSE schema); `chatreadretrieveread.py` is the classic retrieve-then-read path;
  `sql_schemaflow_approach.py` is the SQL planner; `promptmanager.py` loads Jinja2
  prompts from `approaches/prompts/`.
- **agents/** - LangGraph nodes and tools: `router.py`, `retriever.py`, `answerer.py`,
  `verifier.py`, `sql_schemaflow.py`, `followups.py`, `tools.py`, `graph.py`, plus
  `hierarchical_graph.py` + `skills.py` + `_chat_model.py` (hierarchical teams),
  `tutor_agent.py` + `notes_search_tool.py` (Chainlit tutor path), `_llm.py`
  (env-routed Azure/OpenAI/Ollama client), `run_eval.py` (Foundry evaluators), and
  `foundry_client.py` for hosted Azure AI Foundry agents.
- **graphrag/** - live knowledge graph over Cosmos Gremlin: `entity_extractor.py`,
  `indexer.py`, `retriever.py`, `community.py` (community summaries), `cosmos_gremlin.py`.
- **prepdocslib/** - ingestion pipeline: parsers (`pdfparser`, `htmlparser`, `csvparser`,
  `jsonparser`, `textparser`, `youtubeparser`, `learndocparser`), `figureprocessor` +
  `mediadescriber`, `textsplitter` (sentence-aware), `embeddings`, index writers
  (`cosmoswriter` for Cosmos NoSQL - the deployed store - and `searchmanager` +
  `servicesetup` for AI Search), and strategy modules (`filestrategy`,
  `integratedvectorizerstrategy`, `cloudingestionstrategy`, `learnstrategy`,
  `obsidianstrategy`) selected via `prepdocs.py --source files|learn|obsidian`.
- **voice/** - `speech_client.py`, `diarizer.py`, `audio_uploader.py`,
  `transcript_cleaner.py`, `voice_live.py`.
- **safety/** - `content_safety.py` (inference-time prompt/completion filtering),
  `pii.py` (ingestion-time redaction).
- **core/** - cross-cutting helpers: auth, session, model selection, cost meter,
  embeddings client, AOAI client, semantic cache, resilience, conversation memory.
- **tracing/** - `otel.py` (Azure Monitor) and `langsmith.py` (`@traceable` spans).
- **chat_history/** - Cosmos NoSQL persistence with browser localStorage fallback.

### Frontend (`app/frontend/`)
React 19 + TypeScript + Vite 5, Fluent UI v9. Streaming uses
`@microsoft/fetch-event-source`; `react-pdf` for page-jump citations; `@antv/g6` for the
knowledge-graph view; React Query for server state and `zustand` for chat session state;
`i18next` for i18n. Built to static assets and served by Quart in production.

### Functions (`app/functions/`)
Azure Functions custom skills for cloud-side ingestion (document extraction, figure
processing, text processing, audio transcription, graph indexing). This service is
**deferred**: it is not registered in `azure.yaml` and `azd up` does not deploy it (see
the note in `azure.yaml`). Ingestion currently runs in-process via `prepdocs.py` /
`prepdocslib`.

### Infra (`infra/`)
Bicep, deployed with `azd` per `azure.yaml`. `main.bicep` is a Stage-1 deploy that
provisions only compute/observability (Log Analytics, Application Insights, ACR,
Container Apps environment, backend Container App) and Entra ID role assignments
(`infra/app/rbac.bicep`), wiring the backend by managed identity to the pre-existing
`ai-tutor` Foundry, Cosmos, Blob, and Key Vault. Azure AI Search
(`infra/core/search/search-services.bicep`, keyless-only) is composed into `main.bicep`
behind `useAzureSearch` (default `false`); env wiring, RBAC, and the `documentRetriever`
param are in place for when it is flipped. Other modules under `infra/core/` (ai,
storage, cosmos, host, monitor, security) exist for optional services but are not
composed into `main.bicep`.

## Data flow

### Ingestion (PDFs)
`scripts/prepdocs.sh` -> `prepdocs.py` -> `prepdocslib`: list files (local FS or ADLS
user paths) -> optional PII redaction -> Document Intelligence extraction (PyPDF
fallback) -> figure processing when `USE_MULTIMODAL=true` -> optional entity extraction
(Paper/Section/Figure/Author/Citation nodes) -> sentence-aware chunking (~1000 chars,
10% overlap) + embeddings -> write to the configured vector store (Cosmos NoSQL in the
deployment) and, when enabled, OpenAI file_search and the Cosmos Gremlin graph ->
GraphRAG community refresh when the graph is in use.

### Ingestion (audio)
Browser WebSocket -> `/voice/stream` -> Azure Speech-to-Text (long-form + diarization) ->
`diarizer.py` emits utterance events (recording_id, utterance_id, speaker, start, end,
text) streamed live to the UI -> on finalize, graph indexing writes Utterance/Recording/
Topic nodes and transcript text joins the standard text pipeline; audio lands in Blob and
playback is timestamp-synced to citations.

### Chat query
`POST /chat` (SSE) -> `multiagent_approach.run_stream()`: shared preamble (optional
semantic-cache lookup + optional content-safety screen) -> Router classifies
`{factual, multihop, summarize, sql}` -> Retriever runs the selected document retriever
(Cosmos NoSQL vector store when deployed) and, when `USE_GRAPHRAG=true`, a GraphRAG
graph search in parallel, then reranks/dedups (SQL questions route to SchemaFlow) ->
Answerer streams tokens with inline citation markers -> Verifier checks each claim
against cited evidence (when `USE_VERIFIER=true`), retrying once if unsupported claims
remain, otherwise marking sentences "insufficient evidence" -> FollowUps emits 3 next
questions. SSE events on one stream: `token`, `citation`, `claim`, `verdict`, `sql`,
`followups`, `cost`, `done`. `graph_search` and `file_search` fall back to stubs when
their backing services are not configured.

## Storage ownership
The primary vector/retrieval store is selected by `DOCUMENT_RETRIEVER`: Cosmos DB NoSQL
vector store (`core/cosmos_vector_retriever.py`) in the deployment, or a Redis-backed
notes store locally. OpenAI file_search optionally holds citation-grade spans. Cosmos
NoSQL owns chat history (`chat_history/cosmosdb.py`); Cosmos Gremlin optionally owns the
knowledge graph. Redis, when `REDIS_URL` is set, is ephemeral semantic/embedding cache
(never source of truth). Azure AI Search has both an ingestion writer
(`prepdocslib/searchmanager.py`) and a runtime retriever
(`core/azure_search_retriever.py`), but the service is gated off in infra
(`useAzureSearch=false`) so it is not the deployed retrieval backend. Blob / ADLS
Gen2 holds raw and processed files.

## Key technologies
- **Backend:** Python 3.11-3.12, Quart, Gunicorn + uvloop, `uv` for deps, OpenAI Responses
  API, LangGraph + LangSmith, OpenTelemetry, Microsoft GraphRAG, Azure SDKs, Chainlit
  (alternate tutor UI).
- **Frontend:** React 19, TypeScript, Vite 5, Fluent UI v9, React Query, zustand, react-pdf.
- **Infra/observability:** Bicep + azd, Azure Container Apps, Application Insights,
  LangSmith Cloud.
- **Quality:** pytest + pytest-asyncio, Playwright (e2e), Promptfoo + ai-rag-chat-evaluator,
  Azure AI Foundry adversarial simulator, ruff, ESLint + Prettier.

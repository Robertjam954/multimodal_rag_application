# Architecture

multimodal_rag_application is an end-to-end multimodal Retrieval-Augmented Generation
(RAG) system. It ingests PDFs and audio, builds vector, graph, and citation knowledge
stores, and answers questions through a streaming multi-agent loop gated by a Verifier.
It is deployed on Azure (Container Apps + azd + Bicep) and paired with a Jekyll
portfolio site under `site/`.

## High-level shape

```
Browser (React 19 + Vite, Fluent UI)
   |  HTTPS / Server-Sent Events / WebSocket
Quart backend (async, Gunicorn + uvloop worker, Container Apps)
   |
   +-- Azure OpenAI / Foundry (chat, embeddings, vision, o-series reasoning)
   +-- Azure AI Search (primary vector + semantic ranker, optional Knowledge Agent)
   +-- Azure Document Intelligence (PDF layout/OCR)
   +-- Azure Speech-to-Text (long-form + diarization)
   +-- Azure AI Vision (image embeddings)
   +-- Azure AI Content Safety (runtime filtering) + Azure AI Language (PII redaction)
   +-- Azure Cosmos DB (NoSQL: JSON docs + chat history; Gremlin: knowledge graph)
   +-- Azure Blob / ADLS Gen2 (raw PDFs, audio, figures, per-user uploads)
   +-- Azure Managed Redis (semantic cache, working memory, rate-limit/app cache)
   +-- Azure DB for PostgreSQL (pgvector + azure_ai, secondary analytics)
   +-- Application Insights (OpenTelemetry sink) + Key Vault
   |
   +-- External: OpenAI Responses file_search (citations), LangSmith (tracing)
```

## Main components

### Backend (`app/backend/`)
Async Quart application served by Gunicorn with a custom uvloop/uvicorn worker.
Routes (see `app.py`): `/chat` and `/chat/nonstream`, `/sql/plan`, `/papers/upload`,
`/voice/stream` (WebSocket), `/voice/clean`, `/content/<file>`, `/feedback`,
`/config`, `/auth_setup`.

- **approaches/** - request orchestration. `multiagent_approach.py` runs the streaming
  Router -> Retriever -> Answerer -> Verifier loop; `chatreadretrieveread.py` is the
  classic retrieve-then-read path; `sql_schemaflow_approach.py` is the SQL planner;
  `promptmanager.py` loads Jinja2 prompts from `approaches/prompts/`.
- **agents/** - LangGraph nodes and tools: `router.py`, `retriever.py`, `answerer.py`,
  `verifier.py`, `sql_schemaflow.py`, `followups.py`, `tools.py`, `graph.py`, plus
  `foundry_client.py` for hosted Azure AI Foundry agents.
- **graphrag/** - live knowledge graph over Cosmos Gremlin: `entity_extractor.py`,
  `indexer.py`, `retriever.py`, `community.py` (community summaries), `cosmos_gremlin.py`.
- **prepdocslib/** - ingestion pipeline: parsers (`pdfparser`, `htmlparser`, `csvparser`,
  `jsonparser`, `textparser`, `youtubeparser`), `figureprocessor` + `mediadescriber`,
  `textsplitter` (sentence-aware), `embeddings`, `searchmanager`, and strategy modules
  (`filestrategy`, `integratedvectorizerstrategy`, `cloudingestionstrategy`).
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
processing, text processing, audio transcription, graph indexing). Each bundles a synced
copy of `prepdocslib` (refreshed via `scripts/copy_prepdocslib.py`).

### Infra (`infra/`)
Bicep modules under `infra/core/` (ai, search, storage, cosmos, host, monitor, security),
composed by `main.bicep`, deployed with `azd` per `azure.yaml`.

## Data flow

### Ingestion (PDFs)
`scripts/prepdocs.sh` -> `prepdocs.py` -> `prepdocslib`: list files (local FS or ADLS
user paths) -> PII redaction -> Document Intelligence extraction (PyPDF fallback) ->
figure processing when `USE_MULTIMODAL=true` -> entity extraction (Paper/Section/Figure/
Author/Citation nodes) -> sentence-aware chunking (~1000 chars, 10% overlap) + embeddings
-> write to Azure AI Search, OpenAI file_search vector store, and Cosmos Gremlin ->
GraphRAG community refresh.

### Ingestion (audio)
Browser WebSocket -> `/voice/stream` -> Azure Speech-to-Text (long-form + diarization) ->
`diarizer.py` emits utterance events (recording_id, utterance_id, speaker, start, end,
text) streamed live to the UI -> on finalize, graph indexing writes Utterance/Recording/
Topic nodes and transcript text joins the standard text pipeline; audio lands in Blob and
playback is timestamp-synced to citations.

### Chat query
`POST /chat` (SSE) -> `multiagent_approach.run_stream()`: content-safety screen ->
Router classifies `{factual, multihop, summarize, sql}` -> Retriever runs GraphRAG (local
+ global + drift) and OpenAI file_search in parallel, then reranks/dedups (SQL questions
route to SchemaFlow) -> Answerer streams tokens with inline `[doc:page]` /
`[recording:t=120s]` citation markers -> Verifier checks each claim against cited
evidence, retrying once if unsupported claims remain, otherwise marking sentences
"insufficient evidence" -> FollowUps emits 3 next questions. SSE events on one stream:
`token`, `citation`, `claim`, `verdict`, `followups`, `cost`, `done`.

## Storage ownership
Azure AI Search is the primary vector/retrieval store. OpenAI file_search holds
citation-grade spans (kept in sync by `prepdocs.sh`). Cosmos NoSQL owns chat history and
JSON documents; Cosmos Gremlin owns the knowledge graph. Redis is ephemeral cache and
working memory (never source of truth). PostgreSQL pgvector is secondary analytics. Blob /
ADLS Gen2 holds raw and processed files.

## Key technologies
- **Backend:** Python 3.11, Quart, Gunicorn + uvloop, `uv` for deps, OpenAI Responses API,
  LangGraph + LangSmith, OpenTelemetry, Microsoft GraphRAG, Azure SDKs.
- **Frontend:** React 19, TypeScript, Vite 5, Fluent UI v9, React Query, zustand, react-pdf.
- **Infra/observability:** Bicep + azd, Azure Container Apps, Application Insights,
  LangSmith Cloud.
- **Quality:** pytest + pytest-asyncio, Playwright (e2e), Promptfoo + ai-rag-chat-evaluator,
  Azure AI Foundry adversarial simulator, ruff, ESLint + Prettier.

---
name: Multimodal RAG Application
description: Multimodal Retrieval-Augmented Generation over PDFs, audio, and web notes, with a verifier-gated multi-agent chat loop deployed on Azure Container Apps.
languages:
- python
- typescript
- bicep
- azdeveloper
products:
- azure-openai
- azure-cognitive-search
- document-intelligence
- azure-speech
- azure-storage-accounts
- azure-container-apps
- azure-cosmos-db
page_type: sample
urlFragment: multimodal-rag-application
---
<!-- YAML front-matter schema: https://review.learn.microsoft.com/en-us/help/contribute/samples/process/onboarding?branch=main#supported-metadata-fields-for-readmemd -->

# Multimodal RAG Application

- [User story](#user-story)
  - [About this repo](#about-this-repo)
  - [When should you use this repo?](#when-should-you-use-this-repo)
  - [Key features](#key-features)
  - [Roadmap (target)](#roadmap-target)
  - [Target end users](#target-end-users)
  - [Industry scenario](#industry-scenario)
- [Architecture](#architecture)
  - [Outputs](#outputs)
- [Deploy](#deploy)
  - [Pre-requisites](#pre-requisites)
  - [Products used](#products-used)
  - [Required licenses](#required-licenses)
  - [Pricing considerations](#pricing-considerations)
  - [Deploy instructions](#deploy-instructions)
  - [Testing the deployment](#testing-the-deployment)
- [Supporting documentation](#supporting-documentation)
- [Disclaimers](#disclaimers)

## User story

### About this repo

A Retrieval-Augmented Generation system for asking verifiable questions over private multimodal corpora - PDFs, audio, and web notes. An async Quart backend ingests source material into vector, graph, and citation stores, then answers questions through a streaming multi-agent loop (Router -> Retriever -> Answerer -> Verifier) in which a Verifier agent checks each claim against the retrieved evidence. Two UIs sit on top: a React 19 single-page app and a Chainlit tutor chat. Infrastructure is Bicep deployed with the Azure Developer CLI.

This README is updated at the end of each working session and verified by the automated Monday documentation workflow.

### When should you use this repo?

Use it as a reference for building grounded chat over your own documents when you need answers traceable to a source page or timestamp, a per-claim verification gate instead of raw LLM output, or a working example of multi-agent orchestration (flat and hierarchical LangGraph variants) on Azure.

### Key features

- **Document ingestion pipeline** - `app/backend/prepdocs.py` (run via `scripts/prepdocs.sh`) drives `prepdocslib/`: parses PDFs with Azure Document Intelligence (PyPDF fallback), plus text and YouTube transcripts; splits sentence-aware; embeds with Azure OpenAI. Output: chunk + embedding records in an Azure AI Search index, or in a Cosmos DB NoSQL vector container when `DOCUMENT_RETRIEVER=cosmos`; source files pushed to an OpenAI `file_search` vector store for citations; raw files uploaded to Blob Storage.
- **Microsoft Learn ingestion** - `prepdocs.py --source learn` with `prepdocslib/learnstrategy.py` and `scripts/fetch_learn.py` pulls Learn pages listed under `data/learn/` into the same index.
- **GraphRAG knowledge graph** - `app/backend/graphrag/` extracts entities, writes nodes and edges to Cosmos DB for Apache Gremlin, and maintains community summaries; seeded by `scripts/seed_graph.py`. Output: a queryable knowledge graph used by the Retriever's `graph_search`.
- **Multi-agent chat** - `POST /chat` streams SSE from `approaches/multiagent_approach.py`: Router classifies the question, Retriever runs vector and graph search in parallel, Answerer streams tokens with citations, Verifier grades each claim, FollowUps suggests next questions. Output: SSE events `token`, `citation`, `claim`, `verdict`, `followups`, `cost`.
- **Hierarchical agent teams (opt-in)** - `approaches/hierarchical_multiagent_approach.py` + `agents/hierarchical_graph.py` run a LangGraph coordinator over retrieval, answer/verify, and SQL teams behind `USE_HIERARCHICAL_AGENTS=true`, emitting the same SSE schema and falling back to the flat loop if LangGraph is unavailable.
- **SchemaFlow SQL planner** - `POST /sql/plan` runs Parse -> Impact -> Plan -> SQL agents (`approaches/sql_schemaflow_approach.py`, prompts in `approaches/prompts/sql/`). Output: a typed change-plan JSON.
- **Voice transcription** - the `/voice/stream` WebSocket (`voice/voice_live.py`) bridges browser PCM16 audio to the Azure AI Speech Voice Live API in transcription-only mode; `/voice/clean` (`voice/transcript_cleaner.py`) does best-effort LLM cleanup. Output: interim and final transcript JSON, plus a cleaned transcript.
- **Chainlit tutor UI** - `app/backend/chainlit_app.py` is a chat UI over the ingested notes with `search_notes` / `get_document` tools (`agents/tutor_agent.py`, `agents/notes_search_tool.py`) and Redis-backed conversation memory. Output: answers with a per-turn Sources block.
- **React frontend** - React 19 + Vite + Fluent UI (`app/frontend/`), with pages for chat, papers, voice, SQL, and portfolio, and components for citations, verifier badges, graph view, PDF viewer, and voice recording. Built into the backend container image and served by Quart.
- **Safety and cost controls** - content-safety screening and PII redaction modules (`safety/`), a Redis semantic cache, per-IP rate limiting, and a per-session token cost meter surfaced in the `cost` SSE event.
- **Tracing** - OpenTelemetry to Application Insights (`tracing/otel.py`) and LangSmith spans (`tracing/langsmith.py`).
- **Evals and tests** - `evals/` (answer eval, ground-truth generation, Verifier eval over `verifier_golden.jsonl`, adversarial safety eval) writing to `evals/results/`; agent eval in `app/backend/agents/run_eval.py`; pytest suite in `tests/` plus a Playwright e2e test.

### Roadmap (target)

Documented in the prep docs but not working today:

- Azure Functions cloud-ingestion service: skill code exists under `app/functions/`, but the service is deferred (see `azure.yaml`) and `prepdocslib/cloudingestionstrategy.py` / `integratedvectorizerstrategy.py` are log-only stubs.
- PostgreSQL Flexible Server (pgvector) secondary analytics tier: no code yet.
- The `docs/` guide set referenced by older docs: `docs/` currently holds a notebook and images only.
- Frontend locales beyond English.

### Target end users

Knowledge workers (clinicians, researchers, analysts) who consume long PDFs and recorded discussions and need answers traceable to a page or utterance; and engineers studying RAG, GraphRAG, and multi-agent patterns on Azure.

### Industry scenario

Portfolio / reference implementation. The demos cover scientific-paper Q&A, voice transcription, a mixed-corpus chatbot, and SQL change planning over a sample clinical-style warehouse.

## Architecture

```
        React SPA (Vite)              Chainlit tutor UI
              |  HTTPS / SSE / WebSocket     |
              v                              v
+---------------------------------------------------------+
| Quart backend (Gunicorn, Azure Container Apps)           |
|   /chat, /chat/nonstream   multi-agent SSE loop          |
|   /sql/plan                SchemaFlow agents             |
|   /voice/stream (WS)       Voice Live transcription      |
|   /voice/clean             LLM transcript cleanup        |
|   /papers/upload  /content  /feedback  /config           |
+---------------------------------------------------------+
    |             |               |             |
    v             v               v             v
 Azure OpenAI  Cosmos DB       Azure AI      Blob
 / Foundry     (NoSQL vectors  Search        Storage
 (chat, embed) + chat history  (index)       (raw files)
               + Gremlin graph)
    |                                 |
 Redis (notes index, semantic     OpenAI file_search
 cache, conversation memory)      vector store (citations)

 Observability: Application Insights (OpenTelemetry) + LangSmith

 Ingestion path:
 scripts/prepdocs.sh -> prepdocs.py -> prepdocslib
   parse (Document Intelligence / PyPDF / YouTube / Learn)
   -> sentence-aware split -> embed
   -> AI Search index OR Cosmos vector container
   -> OpenAI file_search vector store
   -> raw files to Blob Storage
 graphrag/ -> Cosmos Gremlin nodes/edges + community summaries
```

A question posted to `/chat` is safety-screened, routed, answered from parallel vector + graph retrieval, and verified claim by claim before follow-ups and cost are emitted on the same SSE stream. Ingestion is a separate offline path run from the CLI (and automatically as the `azd` postprovision hook).

### Outputs

| Artifact | Where it lands |
|---|---|
| Chunk + embedding records | Azure AI Search index (`AZURE_SEARCH_INDEX`) or Cosmos NoSQL `documents` container |
| Citation store files | OpenAI `file_search` vector store |
| Knowledge graph nodes/edges + community summaries | Cosmos DB for Apache Gremlin |
| Raw PDFs / audio / uploads | Azure Blob Storage |
| Chat responses | SSE events (`token`, `citation`, `claim`, `verdict`, `followups`, `cost`) from `/chat` |
| Transcripts | JSON over the `/voice/stream` WebSocket; cleaned text from `/voice/clean` |
| SQL change plans | JSON from `/sql/plan` |
| Eval results | `evals/results/` |
| Frontend build | `app/frontend/build/`, copied to `/app/static` in the container image |

## Deploy

### Pre-requisites

- Azure subscription with access to Azure OpenAI / AI Foundry
- Azure Developer CLI (`azd`) and Azure CLI (`az`)
- Python 3.11+, Node.js, and (for image builds) Docker

### Products used

Azure OpenAI / AI Foundry, Azure AI Search, Azure Document Intelligence, Azure AI Speech (Voice Live API), Azure Cosmos DB (NoSQL + Gremlin), Azure Blob Storage, Azure Container Apps, Azure Container Registry, Application Insights / Log Analytics, Azure Key Vault. External: OpenAI Responses `file_search`, LangSmith, Redis.

### Required licenses

None beyond an Azure subscription. Optional external services (OpenAI API for `file_search`, LangSmith) need their own API keys.

### Pricing considerations

Deployed resources bill immediately: Azure OpenAI tokens, AI Search, Cosmos DB RU/s (Gremlin throughput especially during bulk graph indexing), Container Apps, storage, and Application Insights ingestion. Tear down with `azd down` when finished.

### Deploy instructions

Note: `infra/main.bicep` is a Stage 1 deployment that provisions compute and observability (Log Analytics, Application Insights, ACR, Container Apps environment, backend app, RBAC) and references pre-existing Foundry, Cosmos DB, Storage, and Key Vault resources by name via parameters. Adjust those parameters to point at your own resources before deploying.

```bash
# Azure
azd auth login
azd env new <env-name>
azd up            # preprovision: scripts/auth_init.sh; postprovision: scripts/prepdocs.sh

# Ingestion (also runs as the postprovision hook)
./scripts/prepdocs.sh                     # data/papers/ into the vector store
./scripts/prepdocs.sh --removeall
./scripts/prepdocs.sh --source learn      # Microsoft Learn pages
python scripts/seed_graph.py              # seed the Gremlin graph

# Local dev (backend :50505 + frontend :5173)
./app/start.sh

# Chainlit tutor UI
cd app/backend && chainlit run chainlit_app.py --host 0.0.0.0 --port 8000
```

### Testing the deployment

```bash
pytest                                    # unit + integration (mocked Azure clients)
npm run test:e2e                          # frontend build + Playwright e2e
ruff check . && ruff format .             # lint
cd app/frontend && npm run lint
locust -f locustfile.py --host http://localhost:50505   # load test

# Evals (separate venv; deps conflict with the backend)
python -m venv .evalenv && source .evalenv/bin/activate
pip install -r evals/requirements.txt
python evals/evaluate.py
python evals/verifier_eval.py
python evals/safety_evaluation.py --target_url http://localhost:50505/chat
```

For a deployed app, open the Container App URL and ask a question on the chat page; verify SSE events arrive and citations resolve.

## Supporting documentation

### Resource links

- [PRODUCT.md](PRODUCT.md) - what the product does and why
- [ARCHITECTURE.md](ARCHITECTURE.md) - components and data flow in detail
- [CONTRIBUTING.md](CONTRIBUTING.md) - dev setup and conventions
- [CLAUDE.md](CLAUDE.md) - operating manual for coding agents
- [AGENTS.md](AGENTS.md) - agent roster and specs
- [TODO.md](TODO.md) - machine-refreshed weekly backlog
- [Azure-Samples/azure-search-openai-demo](https://github.com/Azure-Samples/azure-search-openai-demo) - the upstream pattern this app extends

### Licensing

MIT. See [LICENSE](LICENSE).

## Disclaimers

This is sample / portfolio code provided as-is, without warranty of any kind. You are responsible for the cost of any Azure or third-party resources you deploy. The repository contains no PHI or sensitive data; sample corpora under `data/` are public material. Do not commit secrets or `.env` files.

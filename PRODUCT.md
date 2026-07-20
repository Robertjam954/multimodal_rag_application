# Product

multimodal_rag_application is a grounded, conversational AI system for asking verifiable
questions over private multimodal corpora - long PDFs and recorded discussions. It turns
documents and audio into answers that are traceable back to a specific page or utterance,
and it refuses to answer rather than fabricate when the evidence is not there.

## What it does

The system ingests source material, indexes it into a vector store (with optional graph
and citation stores), and answers questions through a multi-agent loop that streams the
response while a Verifier agent checks each claim against the retrieved evidence in real
time. Answers carry citations anchored to the source. Retrieval is served by a pluggable
document retriever; the deployed configuration uses an Azure Cosmos DB (NoSQL) vector
store. Optional capabilities below are gated behind feature flags and are turned off in
the current deployment.

The product surfaces four demonstrations:

| Demo | Inputs | Knowledge artifact | Question types |
|---|---|---|---|
| Scientific Paper Summarizer | PDFs | Paper / Section / Figure / Author / Citation graph | factual, multi-hop, summarization |
| Voice Transcription Service | Mic + uploaded audio | Recording / Utterance / Speaker / Topic graph | factual, summarization, attribution |
| QA Chatbot | Mixed corpus | Unified graph + dual vector stores | any of the above |
| SchemaFlow SQL Demo | Natural-language change request | Typed Parse / Impact / Plan / SQL artifacts | SQL change planning |

## Key features

- **PDF ingestion and Q&A.** Upload PDFs; they are extracted (Azure Document Intelligence,
  with a PyPDF fallback), chunked sentence-aware, embedded, and written to the configured
  vector store (Cosmos DB NoSQL in the deployment). When enabled, chunks are also pushed to
  an OpenAI file_search vector store and a GraphRAG graph. When multimodal mode is on,
  figures are cropped, captioned, and embedded so questions can reference images.
- **Voice ingestion and Q&A.** Record live or upload audio; Azure Speech-to-Text
  transcribes with speaker diarization, partial transcripts stream to the UI in real time,
  and the resulting utterances enter the same unified knowledge graph and vector store.
- **Multi-agent answering with a Verifier gate.** A Router classifies the question, a
  Retriever pulls evidence from the graph and file_search in parallel, an Answerer streams
  the response with inline citations, and a Verifier grounds each claim against cited
  evidence. Unsupported sentences are retried once, then flagged as "insufficient evidence"
  rather than asserted.
- **Citation-grade evidence.** Answers include evidence pills deep-linked to the exact PDF
  page or audio timestamp, so every claim can be inspected at its source.
- **GraphRAG retrieval.** A live knowledge graph (Cosmos Gremlin) with community summaries
  supports multi-hop and global questions alongside vector search.
- **SchemaFlow SQL planner.** A separate Parse -> Impact -> Plan -> SQL multi-agent flow
  takes a natural-language change request against a sample clinical warehouse and produces a
  typed plan and SQL, demonstrating schema-aware SQL literacy.
- **Productive chat UX.** Follow-up question suggestions, Thought-Process and
  Supporting-Content tabs, knowledge-graph visualization, a feedback widget (thumbs +
  free text feeding the eval pool), speech output, and dark mode.
- **Safety and governance.** Inference-time content-safety filtering on prompts and
  completions, ingestion-time PII redaction before text leaves the trust boundary, optional
  Entra ID login with per-document ACLs and per-user upload paths, per-IP rate limiting, and
  a per-session token cost cap.
- **Observability.** End-to-end tracing in LangSmith and Azure Monitor (OpenTelemetry), with
  a per-session cost meter surfaced live in the chat stream.
- **Local development.** The backend runs locally against `app/backend/.env`; by default it
  uses a Redis-backed notes retriever instead of Cosmos. Optional local fallbacks
  (`faiss-cpu`, `faster-whisper`) are declared in `requirements.in`.

## Intended users and use cases

The target users are knowledge workers - clinicians, researchers, and analysts - who must
read long PDFs and recorded discussions and need answers they can trust and trace. Typical
uses include summarizing and cross-referencing scientific papers (including figures),
attributing statements in recorded meetings to speakers and timestamps, querying a mixed
corpus of documents and recordings, and planning schema-aware SQL changes against a
clinical-style warehouse.

The primary product/safety objective is a low **Unsupported-Claim Rate** - the share of
generated sentences the Verifier cannot ground in retrieved evidence - targeting under 2% on
the golden evaluation set, preferring to refuse over fabricate on the remainder.

## How it is delivered

The application runs as a containerized Azure deployment on Azure Container Apps
(provisioned and deployed with `azd` and Bicep, keyless via Entra ID managed identity)
and is showcased through a static portfolio site (`site/`, served on GitHub Pages) that
links to the live demo. A local development mode is available.

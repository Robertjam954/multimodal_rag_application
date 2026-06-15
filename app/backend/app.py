"""Quart application factory.

Wires:
- OpenTelemetry + Application Insights
- LangSmith tracing client
- Azure SDK clients (OpenAI, Search, DocIntel, Speech, Blob, Cosmos, ContentSafety, Language)
- Approaches: ChatReadRetrieveRead, MultiAgent, SchemaFlow SQL
- Blueprints / routes: /chat, /papers/upload, /voice/stream, /sql/plan,
  /chat_history, /feedback, /config, /auth_setup, /content/<path>
"""
from __future__ import annotations

import dataclasses
import io
import json
import logging
import mimetypes
import os
from pathlib import Path
from typing import Any, AsyncGenerator

from azure.identity.aio import AzureDeveloperCliCredential, DefaultAzureCredential, ManagedIdentityCredential
from quart import Blueprint, Quart, abort, current_app, jsonify, request, send_file, send_from_directory
from quart_cors import cors

from config import (
    CONFIG_AGENTIC_KNOWLEDGEBASE_ENABLED,
    CONFIG_AUTH_CLIENT,
    CONFIG_BLOG_WRITER_APPROACH,
    CONFIG_CHAT_APPROACH,
    CONFIG_CHAT_HISTORY_BROWSER_ENABLED,
    CONFIG_CHAT_HISTORY_COSMOS_ENABLED,
    CONFIG_CONTENT_SAFETY_ENABLED,
    CONFIG_COST_METER,
    CONFIG_CREDENTIAL,
    CONFIG_FEEDBACK_ENABLED,
    CONFIG_GLOBAL_BLOB_MANAGER,
    CONFIG_GRAPHRAG_ENABLED,
    CONFIG_INGESTER,
    CONFIG_LANGSMITH_CLIENT,
    CONFIG_MAGIC_LINK_AUTH_ENABLED,
    CONFIG_MULTIAGENT_APPROACH,
    CONFIG_MULTIMODAL_ENABLED,
    CONFIG_OPENAI_CLIENT,
    CONFIG_OPENROUTER_CHAT_ENABLED,
    CONFIG_PII_REDACTION_ENABLED,
    CONFIG_QUERY_ENHANCEMENT_ENABLED,
    CONFIG_RATE_LIMITER,
    CONFIG_REASONING_EFFORT_ENABLED,
    CONFIG_REASONING_EFFORT_OPTIONS,
    CONFIG_SEARCH_CLIENT,
    CONFIG_SEMANTIC_RANKER_DEPLOYED,
    CONFIG_SPEECH_INPUT_ENABLED,
    CONFIG_SPEECH_OUTPUT_AZURE_ENABLED,
    CONFIG_SPEECH_OUTPUT_BROWSER_ENABLED,
    CONFIG_SPEECH_SERVICE_ID,
    CONFIG_SPEECH_SERVICE_LOCATION,
    CONFIG_SPEECH_SERVICE_VOICE,
    CONFIG_SQL_APPROACH,
    CONFIG_SQL_DEMO_ENABLED,
    CONFIG_SQL_NOTES_APPROACH,
    CONFIG_SQL_NOTES_DEMO_ENABLED,
    CONFIG_STREAMING_ENABLED,
    CONFIG_TUTOR_MODE_ENABLED,
    CONFIG_USER_BLOB_MANAGER,
    CONFIG_USER_UPLOAD_ENABLED,
    CONFIG_VECTOR_SEARCH_ENABLED,
    CONFIG_VERIFIER_ENABLED,
    CONFIG_VOICE_DEMO_ENABLED,
    CONFIG_YOUTUBE_INGEST_ENABLED,
)
from decorators import authenticated, ratelimited
from error import error_dict, error_response

logger = logging.getLogger(__name__)

STATIC_DIR = Path(__file__).parent / "static"
bp = Blueprint("routes", __name__, static_folder=str(STATIC_DIR))
mimetypes.add_type("application/javascript", ".js")
mimetypes.add_type("text/css", ".css")


@bp.route("/")
async def index():
    return await bp.send_static_file("index.html")


@bp.route("/redirect")
async def redirect_target():
    return ""


@bp.route("/favicon.ico")
async def favicon():
    return await bp.send_static_file("favicon.ico")


@bp.route("/assets/<path:p>")
async def assets(p: str):
    return await send_from_directory(STATIC_DIR / "assets", p)


@bp.route("/config", methods=["GET"])
async def get_config():
    app = current_app
    return jsonify(
        {
            "streamingEnabled": app.config[CONFIG_STREAMING_ENABLED],
            "verifierEnabled": app.config[CONFIG_VERIFIER_ENABLED],
            "graphragEnabled": app.config[CONFIG_GRAPHRAG_ENABLED],
            "multimodalEnabled": app.config[CONFIG_MULTIMODAL_ENABLED],
            "agenticKnowledgebaseEnabled": app.config[CONFIG_AGENTIC_KNOWLEDGEBASE_ENABLED],
            "voiceDemoEnabled": app.config[CONFIG_VOICE_DEMO_ENABLED],
            "sqlDemoEnabled": app.config[CONFIG_SQL_DEMO_ENABLED],
            "contentSafetyEnabled": app.config[CONFIG_CONTENT_SAFETY_ENABLED],
            "piiRedactionEnabled": app.config[CONFIG_PII_REDACTION_ENABLED],
            "feedbackEnabled": app.config[CONFIG_FEEDBACK_ENABLED],
            "userUploadEnabled": app.config[CONFIG_USER_UPLOAD_ENABLED],
            "chatHistoryCosmosEnabled": app.config[CONFIG_CHAT_HISTORY_COSMOS_ENABLED],
            "chatHistoryBrowserEnabled": app.config[CONFIG_CHAT_HISTORY_BROWSER_ENABLED],
            "speechInputEnabled": app.config[CONFIG_SPEECH_INPUT_ENABLED],
            "speechOutputAzureEnabled": app.config[CONFIG_SPEECH_OUTPUT_AZURE_ENABLED],
            "speechOutputBrowserEnabled": app.config[CONFIG_SPEECH_OUTPUT_BROWSER_ENABLED],
            "speechVoice": app.config[CONFIG_SPEECH_SERVICE_VOICE],
            "reasoningEffortEnabled": app.config[CONFIG_REASONING_EFFORT_ENABLED],
            "reasoningEffortOptions": app.config[CONFIG_REASONING_EFFORT_OPTIONS],
            "vectorSearchEnabled": app.config[CONFIG_VECTOR_SEARCH_ENABLED],
            "semanticRankerDeployed": app.config[CONFIG_SEMANTIC_RANKER_DEPLOYED],
            "authEnabled": os.getenv("AZURE_USE_AUTHENTICATION", "false").lower() == "true",
            "languages": ["en"],
        }
    )


@bp.route("/auth_setup", methods=["GET"])
async def auth_setup():
    auth = current_app.config.get(CONFIG_AUTH_CLIENT)
    if not auth:
        return jsonify({"useLogin": False, "requireAccessControl": False})
    return jsonify(auth.get_auth_setup_for_client())


@bp.route("/chat", methods=["POST"])
@ratelimited()
@authenticated
async def chat_stream():
    body = await request.get_json()
    if not body:
        return error_response("missing body", "bad_request", 400)
    approach = current_app.config[CONFIG_MULTIAGENT_APPROACH]

    async def event_stream() -> AsyncGenerator[bytes, None]:
        try:
            async for evt in approach.run_stream(
                messages=body.get("messages", []),
                context=body.get("context", {}),
                session_state=body.get("session_state"),
            ):
                yield f"data: {json.dumps(evt)}\n\n".encode()
        except Exception as e:  # noqa: BLE001
            logger.exception("chat_stream error")
            yield f"data: {json.dumps(error_dict(str(e), 'chat_stream_error'))}\n\n".encode()
        yield b"data: {\"event\": \"done\"}\n\n"

    return event_stream(), 200, {"Content-Type": "text/event-stream", "Cache-Control": "no-cache"}


@bp.route("/chat/nonstream", methods=["POST"])
@ratelimited()
@authenticated
async def chat_nonstream():
    body = await request.get_json()
    if not body:
        return error_response("missing body", "bad_request", 400)
    approach = current_app.config[CONFIG_MULTIAGENT_APPROACH]
    result = await approach.run(
        messages=body.get("messages", []),
        context=body.get("context", {}),
        session_state=body.get("session_state"),
    )
    return jsonify(result)


@bp.route("/sql/plan", methods=["POST"])
@ratelimited()
@authenticated
async def sql_plan():
    if not current_app.config[CONFIG_SQL_DEMO_ENABLED]:
        return error_response("sql demo disabled", "not_enabled", 404)
    body = await request.get_json()
    approach = current_app.config[CONFIG_SQL_APPROACH]
    result = await approach.run(change_request=body.get("change_request", ""))
    return jsonify(result)


@bp.route("/sql/notes", methods=["POST"])
@ratelimited()
@authenticated
async def sql_notes_stream():
    if not current_app.config[CONFIG_SQL_NOTES_DEMO_ENABLED]:
        return error_response("sql notes disabled", "not_enabled", 404)
    body = await request.get_json()
    if not body:
        return error_response("missing body", "bad_request", 400)
    approach = current_app.config[CONFIG_SQL_NOTES_APPROACH]

    async def event_stream() -> AsyncGenerator[bytes, None]:
        try:
            async for evt in approach.run_stream(
                messages=body.get("messages", []),
                context=body.get("context", {}),
                session_state=body.get("session_state"),
            ):
                yield f"data: {json.dumps(evt)}\n\n".encode()
        except Exception as e:  # noqa: BLE001
            logger.exception("sql_notes_stream error")
            yield f"data: {json.dumps(error_dict(str(e), 'sql_notes_stream_error'))}\n\n".encode()
        yield b"data: {\"event\": \"done\"}\n\n"

    return event_stream(), 200, {"Content-Type": "text/event-stream", "Cache-Control": "no-cache"}


@bp.route("/blog/generate", methods=["POST"])
@ratelimited()
@authenticated
async def blog_generate():
    if not current_app.config[CONFIG_SQL_NOTES_DEMO_ENABLED]:
        return error_response("blog generation disabled", "not_enabled", 404)
    body = await request.get_json()
    if not body or "note_id" not in body:
        return error_response("note_id is required", "bad_request", 400)
    approach = current_app.config[CONFIG_BLOG_WRITER_APPROACH]
    try:
        result = await approach.run_for_note(int(body["note_id"]), dry_run=bool(body.get("dry_run")))
    except LookupError as e:
        return error_response(str(e), "not_found", 404)
    except ValueError as e:
        return error_response(str(e), "bad_request", 400)
    return jsonify(result)


@bp.route("/youtube/ingest", methods=["POST"])
@ratelimited()
@authenticated
async def youtube_ingest():
    if not current_app.config[CONFIG_YOUTUBE_INGEST_ENABLED]:
        return error_response("youtube ingestion disabled", "not_enabled", 404)
    body = await request.get_json()
    if not body or not body.get("url"):
        return error_response("url is required", "bad_request", 400)
    from prepdocslib.page import Chunk
    from prepdocslib.textsplitter import split_text
    from prepdocslib.youtubeparser import YouTubeTranscriptParser
    from sql_notes import get_db
    from youtube_service import fetch_metadata, parse_video_id

    try:
        video_id = parse_video_id(body["url"])
    except ValueError as e:
        return error_response(str(e), "bad_request", 400)

    metadata = await fetch_metadata(video_id)
    parser = YouTubeTranscriptParser()
    pages = []
    try:
        async for page in parser.parse(b"", f"youtube://{video_id}"):
            pages.append(page)
    except Exception as e:  # noqa: BLE001
        logger.exception("youtube transcript fetch failed")
        return error_response(f"transcript fetch failed: {e}", "transcript_error", 502)

    transcript_text = "\n".join(p.text for p in pages)
    chunks: list[Chunk] = []
    for p in pages:
        for ci, ctext in enumerate(split_text(p.text)):
            chunks.append(
                Chunk(
                    id=f"youtube-{video_id}-{p.page_number}-{ci}",
                    content=ctext,
                    source_file=f"youtube://{video_id}",
                    source_page=p.page_number,
                    storage_url=metadata.video_url,
                )
            )

    ingester = current_app.config.get(CONFIG_INGESTER)
    if ingester and ingester.search and chunks:
        try:
            await ingester.search.upsert(chunks)
        except Exception:
            logger.exception("search upsert failed; note will still be inserted into blog_notes")

    note_id = await get_db().insert_note(
        content_topic=metadata.title or f"YouTube {video_id}",
        hook_intro=(metadata.description or "")[:500],
        source_type="video",
        source_url=metadata.video_url,
        transcript=transcript_text[:50_000],
        tags=body.get("tags") or [],
    )
    return jsonify({"note_id": note_id, "video_id": video_id, "chunks": len(chunks), "title": metadata.title})


@bp.route("/youtube/videos", methods=["GET"])
@ratelimited()
async def youtube_videos():
    if not current_app.config[CONFIG_YOUTUBE_INGEST_ENABLED]:
        return error_response("youtube ingestion disabled", "not_enabled", 404)
    from sql_notes import get_db

    rows = await get_db().run_query(
        "SELECT id, content_topic, source_url, created_at FROM blog_notes "
        "WHERE source_type = 'video' ORDER BY created_at DESC LIMIT 200"
    )
    return jsonify({"videos": rows})


@bp.route("/papers/upload", methods=["POST"])
@ratelimited()
@authenticated
async def papers_upload():
    if not current_app.config[CONFIG_USER_UPLOAD_ENABLED]:
        return error_response("upload disabled", "not_enabled", 404)
    files = await request.files
    if not files:
        return error_response("no files", "bad_request", 400)
    ingester = current_app.config[CONFIG_INGESTER]
    uploaded = []
    for _, fs in files.items():
        data = fs.read()
        result = await ingester.ingest_user_upload(filename=fs.filename, data=data)
        uploaded.append(result)
    return jsonify({"uploaded": uploaded})


@bp.route("/feedback", methods=["POST"])
@ratelimited()
async def feedback():
    if not current_app.config[CONFIG_FEEDBACK_ENABLED]:
        return error_response("feedback disabled", "not_enabled", 404)
    body = await request.get_json()
    logger.info("feedback %s", body)
    # Persist to Cosmos via chat_history blueprint in production
    return jsonify({"ok": True})


@bp.route("/content/<path:filename>", methods=["GET"])
async def content(filename: str):
    blob = current_app.config[CONFIG_GLOBAL_BLOB_MANAGER]
    stream = await blob.get_file_stream(filename)
    if stream is None:
        return error_response("not found", "not_found", 404)
    return await send_file(io.BytesIO(stream), attachment_filename=filename)


async def _configure_tracing(app: Quart) -> None:
    if os.getenv("APPLICATIONINSIGHTS_CONNECTION_STRING"):
        try:
            from tracing.otel import configure as configure_otel

            configure_otel(app)
        except Exception:
            logger.exception("OTel configure failed; continuing without tracing")
    if os.getenv("LANGSMITH_API_KEY"):
        try:
            from tracing.langsmith import init_langsmith

            app.config[CONFIG_LANGSMITH_CLIENT] = init_langsmith()
        except Exception:
            logger.exception("LangSmith init failed; continuing without LS tracing")


async def _setup_clients(app: Quart) -> None:
    """Wire Azure SDK clients and approach singletons."""
    # Credential
    if os.getenv("RUNNING_IN_PRODUCTION", "false").lower() == "true":
        cred = ManagedIdentityCredential(client_id=os.getenv("AZURE_CLIENT_ID")) if os.getenv("AZURE_CLIENT_ID") else DefaultAzureCredential()
    else:
        cred = AzureDeveloperCliCredential(tenant_id=os.getenv("AZURE_TENANT_ID")) if os.getenv("AZURE_TENANT_ID") else DefaultAzureCredential()
    app.config[CONFIG_CREDENTIAL] = cred

    # Cost meter + rate limiter
    from core.costmeter import CostMeter

    app.config[CONFIG_COST_METER] = CostMeter()
    app.config[CONFIG_RATE_LIMITER] = None  # decorators handle in-memory

    # Approaches (lazily import to keep cold start cheap during tests)
    from approaches.multiagent_approach import MultiAgentApproach
    from approaches.chatreadretrieveread import ChatReadRetrieveReadApproach
    from approaches.sql_schemaflow_approach import SchemaFlowSQLApproach
    from approaches.sql_notes_approach import SQLNotesApproach
    from approaches.blog_writer_approach import BlogWriterApproach
    from approaches.promptmanager import PromptManager

    pm = PromptManager()
    app.config[CONFIG_CHAT_APPROACH] = ChatReadRetrieveReadApproach(prompt_manager=pm)
    app.config[CONFIG_MULTIAGENT_APPROACH] = MultiAgentApproach(prompt_manager=pm)
    app.config[CONFIG_SQL_APPROACH] = SchemaFlowSQLApproach(prompt_manager=pm)
    app.config[CONFIG_SQL_NOTES_APPROACH] = SQLNotesApproach(prompt_manager=pm)
    app.config[CONFIG_BLOG_WRITER_APPROACH] = BlogWriterApproach(prompt_manager=pm)

    # Flags from env
    def b(name: str, default: str = "false") -> bool:
        return os.getenv(name, default).lower() == "true"

    app.config[CONFIG_STREAMING_ENABLED] = b("USE_STREAMING", "true")
    app.config[CONFIG_VERIFIER_ENABLED] = b("USE_VERIFIER", "true")
    app.config[CONFIG_GRAPHRAG_ENABLED] = b("USE_GRAPHRAG", "true")
    app.config[CONFIG_MULTIMODAL_ENABLED] = b("USE_MULTIMODAL", "false")
    app.config[CONFIG_AGENTIC_KNOWLEDGEBASE_ENABLED] = b("USE_AGENTIC_KNOWLEDGEBASE", "false")
    app.config[CONFIG_VOICE_DEMO_ENABLED] = b("USE_VOICE_DEMO", "true")
    app.config[CONFIG_SQL_DEMO_ENABLED] = b("USE_SQL_DEMO", "true")
    app.config[CONFIG_SQL_NOTES_DEMO_ENABLED] = b("USE_SQL_NOTES_DEMO", "true")
    app.config[CONFIG_YOUTUBE_INGEST_ENABLED] = b("USE_YOUTUBE_INGEST", "true")
    app.config[CONFIG_OPENROUTER_CHAT_ENABLED] = b("USE_OPENROUTER_CHAT", "false")
    app.config[CONFIG_QUERY_ENHANCEMENT_ENABLED] = b("USE_QUERY_ENHANCEMENT", "true")
    app.config[CONFIG_MAGIC_LINK_AUTH_ENABLED] = b("USE_MAGIC_LINK_AUTH", "false")
    app.config[CONFIG_TUTOR_MODE_ENABLED] = b("USE_TUTOR_MODE", "true")
    app.config[CONFIG_CONTENT_SAFETY_ENABLED] = b("USE_CONTENT_SAFETY", "false")
    app.config[CONFIG_PII_REDACTION_ENABLED] = b("USE_PII_REDACTION", "false")
    app.config[CONFIG_FEEDBACK_ENABLED] = b("USE_FEEDBACK", "true")
    app.config[CONFIG_USER_UPLOAD_ENABLED] = b("USE_USER_UPLOAD", "true")
    app.config[CONFIG_CHAT_HISTORY_COSMOS_ENABLED] = b("USE_CHAT_HISTORY_COSMOS", "false")
    app.config[CONFIG_CHAT_HISTORY_BROWSER_ENABLED] = b("USE_CHAT_HISTORY_BROWSER", "true")
    app.config[CONFIG_VECTOR_SEARCH_ENABLED] = b("USE_VECTOR_SEARCH", "true")
    app.config[CONFIG_SEMANTIC_RANKER_DEPLOYED] = b("AZURE_SEARCH_SEMANTIC_RANKER", "true")
    app.config[CONFIG_REASONING_EFFORT_ENABLED] = b("USE_REASONING_EFFORT", "true")
    app.config[CONFIG_REASONING_EFFORT_OPTIONS] = ["minimal", "low", "medium", "high"]
    app.config[CONFIG_SPEECH_INPUT_ENABLED] = b("USE_VOICE_DEMO", "true")
    app.config[CONFIG_SPEECH_OUTPUT_AZURE_ENABLED] = b("USE_SPEECH_OUTPUT_AZURE", "false")
    app.config[CONFIG_SPEECH_OUTPUT_BROWSER_ENABLED] = b("USE_SPEECH_OUTPUT_BROWSER", "true")
    app.config[CONFIG_SPEECH_SERVICE_VOICE] = os.getenv("AZURE_SPEECH_SERVICE_VOICE", "en-US-AvaNeural")
    app.config[CONFIG_SPEECH_SERVICE_ID] = os.getenv("AZURE_SPEECH_SERVICE_ID")
    app.config[CONFIG_SPEECH_SERVICE_LOCATION] = os.getenv("AZURE_SPEECH_SERVICE_LOCATION")

    # Blob manager (global content + per-user uploads)
    try:
        from prepdocslib.blobmanager import BlobManager

        app.config[CONFIG_GLOBAL_BLOB_MANAGER] = BlobManager(
            credential=cred,
            account=os.getenv("AZURE_STORAGE_ACCOUNT", ""),
            container=os.getenv("AZURE_STORAGE_CONTAINER", "content"),
        )
        app.config[CONFIG_USER_BLOB_MANAGER] = BlobManager(
            credential=cred,
            account=os.getenv("AZURE_USER_STORAGE_ACCOUNT", os.getenv("AZURE_STORAGE_ACCOUNT", "")),
            container=os.getenv("AZURE_USER_STORAGE_CONTAINER", "user-content"),
        )
    except Exception:
        logger.exception("Blob manager init failed; running without Blob")

    # Ingester (per-session uploads)
    try:
        from prepdocslib.filestrategy import UploadUserFileStrategy

        app.config[CONFIG_INGESTER] = UploadUserFileStrategy(
            blob_manager=app.config.get(CONFIG_USER_BLOB_MANAGER),
            search_service=os.getenv("AZURE_SEARCH_SERVICE"),
            search_index=os.getenv("AZURE_SEARCH_INDEX"),
            credential=cred,
        )
    except Exception:
        logger.exception("Ingester init failed; running without ingestion")

    # OpenAI client (deferred to first use; constructed by agents/tools as needed)
    app.config[CONFIG_OPENAI_CLIENT] = None

    # Chat history blueprints
    if app.config[CONFIG_CHAT_HISTORY_COSMOS_ENABLED]:
        try:
            from chat_history.cosmosdb import chat_history_cosmosdb_bp

            app.register_blueprint(chat_history_cosmosdb_bp)
        except Exception:
            logger.exception("Cosmos chat history blueprint failed to register")


async def create_app() -> Quart:
    app = Quart(__name__)
    cors(app, allow_origin="*" if os.getenv("ALLOW_CORS", "true").lower() == "true" else None)
    app.register_blueprint(bp)
    await _configure_tracing(app)
    await _setup_clients(app)
    return app

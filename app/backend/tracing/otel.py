"""OpenTelemetry configuration: Azure Monitor + instrumentors for HTTPX, aiohttp, OpenAI."""
from __future__ import annotations

import logging

logger = logging.getLogger(__name__)


def configure(app) -> None:
    try:
        from azure.monitor.opentelemetry import configure_azure_monitor
        from opentelemetry.instrumentation.aiohttp_client import AioHttpClientInstrumentor
        from opentelemetry.instrumentation.asgi import OpenTelemetryMiddleware
        from opentelemetry.instrumentation.httpx import HTTPXClientInstrumentor
        from opentelemetry.instrumentation.openai import OpenAIInstrumentor
    except Exception:
        logger.warning("OTel deps missing; skip configure()")
        return

    configure_azure_monitor()

    # Break the telemetry feedback loop. The Azure Monitor exporter ships logs by
    # making HTTP calls via azure.core, and azure.core logs every call at INFO.
    # configure_azure_monitor() attaches a log handler to the ROOT logger, so those
    # exporter HTTP logs get re-exported, which makes more HTTP calls, ad infinitum —
    # pegging a thread, flooding App Insights, and starving the uvicorn event loop so
    # it never accepts connections. Silence the exporter's own plumbing so it isn't
    # re-ingested.
    for _noisy in (
        "azure.core.pipeline.policies.http_logging_policy",
        "azure.monitor.opentelemetry.exporter",
        "azure.identity",
        "urllib3.connectionpool",
    ):
        logging.getLogger(_noisy).setLevel(logging.WARNING)

    AioHttpClientInstrumentor().instrument()
    HTTPXClientInstrumentor().instrument()
    OpenAIInstrumentor().instrument()
    if hasattr(app, "asgi_app"):
        app.asgi_app = OpenTelemetryMiddleware(app.asgi_app)

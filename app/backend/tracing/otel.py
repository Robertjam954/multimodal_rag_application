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
    AioHttpClientInstrumentor().instrument()
    HTTPXClientInstrumentor().instrument()
    OpenAIInstrumentor().instrument()
    if hasattr(app, "asgi_app"):
        app.asgi_app = OpenTelemetryMiddleware(app.asgi_app)

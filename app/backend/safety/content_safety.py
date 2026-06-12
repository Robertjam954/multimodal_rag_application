"""Inference-time content safety screening via Azure AI Content Safety."""
from __future__ import annotations

import dataclasses
import logging
import os

logger = logging.getLogger(__name__)


@dataclasses.dataclass
class SafetyResult:
    ok: bool
    reason: str = ""
    severities: dict[str, int] | None = None


async def screen_input(text: str) -> SafetyResult:
    endpoint = os.getenv("AZURE_CONTENTSAFETY_ENDPOINT")
    key = os.getenv("AZURE_CONTENTSAFETY_KEY")
    if not (endpoint and key):
        return SafetyResult(ok=True, reason="content safety not configured; pass-through")
    try:
        from azure.ai.contentsafety.aio import ContentSafetyClient
        from azure.ai.contentsafety.models import AnalyzeTextOptions
        from azure.core.credentials import AzureKeyCredential
    except Exception:
        logger.warning("azure-ai-contentsafety missing; pass-through")
        return SafetyResult(ok=True, reason="sdk missing")

    client = ContentSafetyClient(endpoint, AzureKeyCredential(key))
    resp = await client.analyze_text(AnalyzeTextOptions(text=text))
    sev = {c.category: c.severity for c in resp.categories_analysis}
    high = [k for k, v in sev.items() if v >= 4]
    return SafetyResult(ok=not high, reason=f"high-severity: {high}" if high else "", severities=sev)


async def screen_output(text: str) -> SafetyResult:
    return await screen_input(text)

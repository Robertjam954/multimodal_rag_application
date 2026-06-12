"""PII redaction at ingestion via Azure AI Language."""
from __future__ import annotations

import logging
import os
import re

logger = logging.getLogger(__name__)

DEFAULT_PATTERNS = {
    "SSN": re.compile(r"\b\d{3}-\d{2}-\d{4}\b"),
    "MRN": re.compile(r"\bMRN[:\s]?\d{6,10}\b", re.IGNORECASE),
    "EMAIL": re.compile(r"\b[\w.+-]+@[\w-]+\.[\w.-]+\b"),
    "PHONE": re.compile(r"\b\d{3}[-.\s]?\d{3}[-.\s]?\d{4}\b"),
}


async def redact(text: str) -> str:
    """Best-effort PII redaction. Uses Azure AI Language when configured; falls back to regex."""
    endpoint = os.getenv("AZURE_LANGUAGE_ENDPOINT")
    key = os.getenv("AZURE_LANGUAGE_KEY")
    if endpoint and key:
        try:
            from azure.ai.textanalytics.aio import TextAnalyticsClient
            from azure.core.credentials import AzureKeyCredential

            client = TextAnalyticsClient(endpoint, AzureKeyCredential(key))
            result = await client.recognize_pii_entities([text])
            doc = result[0]
            if not getattr(doc, "is_error", False):
                return doc.redacted_text or text
        except Exception:
            logger.exception("Azure PII redaction failed; falling back to regex")
    out = text
    for label, pat in DEFAULT_PATTERNS.items():
        out = pat.sub(f"[{label}-REDACTED]", out)
    return out

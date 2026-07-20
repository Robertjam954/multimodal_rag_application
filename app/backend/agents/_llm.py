"""Tiny LLM-client wrapper. Routes to Azure OpenAI / OpenAI / local Ollama based on env.

Functions return strings (no streaming) or async iterators (streaming).
This is intentionally minimal so agents can stay readable; swap for langchain-openai for production.
"""
from __future__ import annotations

import asyncio
import json
import logging
import os
from typing import Any, AsyncIterator

logger = logging.getLogger(__name__)


def _configured() -> bool:
    """True when a real LLM is reachable (Foundry project endpoint, classic Azure
    OpenAI, external OpenAI, or local Ollama)."""
    return bool(
        os.getenv("AZURE_OPENAI_ENDPOINT")
        or os.getenv("AZURE_OPENAI_SERVICE")
        or os.getenv("OPENAI_API_KEY")
        or os.getenv("OLLAMA_BASE_URL")
    )


def _client():
    """Return an AsyncOpenAI client configured for Foundry / Azure / OpenAI / local."""
    mode = os.getenv("MODE", "azure").lower()
    if mode == "local":
        # Ollama via OpenAI-compatible endpoint
        from openai import AsyncOpenAI

        return AsyncOpenAI(
            base_url=os.getenv("OLLAMA_BASE_URL", "http://localhost:11434/v1"),
            api_key=os.getenv("OLLAMA_API_KEY", "sk-local"),
        )
    # Foundry project endpoint + Entra ID: reuse the single AAD-configured client
    # (core.aoai_client builds AsyncOpenAI against AZURE_OPENAI_ENDPOINT + /openai/v1).
    if os.getenv("AZURE_OPENAI_ENDPOINT"):
        from core.aoai_client import get_client

        return get_client()
    if os.getenv("AZURE_OPENAI_SERVICE"):
        from openai import AsyncAzureOpenAI

        return AsyncAzureOpenAI(
            azure_endpoint=f"https://{os.getenv('AZURE_OPENAI_SERVICE')}.openai.azure.com/",
            api_version=os.getenv("AZURE_OPENAI_API_VERSION", "2024-10-01-preview"),
            azure_ad_token_provider=None,
            api_key=os.getenv("AZURE_OPENAI_API_KEY"),
        )
    from openai import AsyncOpenAI

    return AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def _model_for(role: str) -> str:
    if os.getenv("MODE", "azure").lower() == "local":
        return os.getenv("OLLAMA_MODEL", "llama3.1:8b")
    if role == "reasoning":
        return os.getenv("AZURE_OPENAI_REASONING_DEPLOYMENT", os.getenv("AZURE_OPENAI_CHATGPT_DEPLOYMENT", "gpt-4.1-mini"))
    return os.getenv("AZURE_OPENAI_CHATGPT_DEPLOYMENT", os.getenv("OPENAI_CHATGPT_MODEL", "gpt-4.1-mini"))


async def complete(system: str, user: str, role: str = "chat", **kwargs: Any) -> str:
    """Non-streaming completion. Returns assistant text."""
    if not _configured():
        logger.warning("No LLM configured; returning deterministic stub for tests")
        return _stub_response(system, user)
    client = _client()
    resp = await client.chat.completions.create(
        model=_model_for(role),
        messages=[{"role": "system", "content": system}, {"role": "user", "content": user}],
        temperature=kwargs.get("temperature", 0.2),
    )
    return resp.choices[0].message.content or ""


async def stream(system: str, user: str, role: str = "chat", **kwargs: Any) -> AsyncIterator[str]:
    if not _configured():
        for chunk in _stub_response(system, user).split(" "):
            await asyncio.sleep(0)
            yield chunk + " "
        return
    client = _client()
    resp = await client.chat.completions.create(
        model=_model_for(role),
        messages=[{"role": "system", "content": system}, {"role": "user", "content": user}],
        temperature=kwargs.get("temperature", 0.2),
        stream=True,
    )
    async for chunk in resp:
        delta = chunk.choices[0].delta.content if chunk.choices else None
        if delta:
            yield delta


def _stub_response(system: str, user: str) -> str:
    """Deterministic stub used in tests / no-API mode."""
    if "Classify" in system:
        return "factual"
    if "claim verifier" in system.lower():
        return json.dumps({"label": "supported", "reason": "stub"})
    if "follow-up" in system.lower():
        return json.dumps(["What else does the paper say?", "Who funded this work?", "What are the limitations?"])
    return f"[stub-answer] Based on the evidence: {user[:80]} [1]"

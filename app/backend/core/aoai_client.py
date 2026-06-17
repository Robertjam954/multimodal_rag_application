"""Single source of truth for the Azure OpenAI / AI Foundry async client.

The Foundry v1 endpoint (`https://<resource>.services.ai.azure.com/openai/v1`)
speaks the OpenAI-compatible protocol, NOT the legacy
`/openai/deployments/<name>/...` URL form. So we use `AsyncOpenAI` with
`base_url`, not `AsyncAzureOpenAI` with `azure_endpoint`.

Auth precedence:
1. `AZURE_OPENAI_USE_AAD=true` -> bearer token via `DefaultAzureCredential`
   scoped to `AZURE_OPENAI_AAD_SCOPE` (default `https://ai.azure.com/.default`).
2. `AZURE_OPENAI_API_KEY` -> use as a static API key.
3. Fall back to AAD anyway (matches az login state in dev).
"""
from __future__ import annotations

import logging
import os
from functools import lru_cache
from typing import Any

from openai import AsyncOpenAI

logger = logging.getLogger(__name__)

DEFAULT_AAD_SCOPE = "https://ai.azure.com/.default"


def _endpoint() -> str:
    endpoint = os.environ["AZURE_OPENAI_ENDPOINT"].rstrip("/")
    # Foundry exposes /openai/v1 - SDK appends paths to that base.
    if not endpoint.endswith("/openai/v1"):
        endpoint = endpoint + "/openai/v1"
    return endpoint


def _resolve_api_key() -> str:
    """Returns a string api_key for AsyncOpenAI.

    Precedence:
    1. `OPENAI_API_CHAT` (export OPENAI_API_CHAT=...).
    2. `AZURE_OPENAI_API_KEY`.
    3. AAD bearer token via DefaultAzureCredential when `AZURE_OPENAI_USE_AAD=true`
       or when neither of the keys above is set. Tokens are valid ~60 minutes;
       call `reset_client()` to refresh after expiry.
    """
    static_key = os.getenv("OPENAI_API_CHAT") or os.getenv("AZURE_OPENAI_API_KEY")
    if static_key and os.getenv("AZURE_OPENAI_USE_AAD", "").lower() != "true":
        return static_key

    from azure.identity import DefaultAzureCredential

    scope = os.getenv("AZURE_OPENAI_AAD_SCOPE", DEFAULT_AAD_SCOPE)
    token = DefaultAzureCredential().get_token(scope)
    return token.token


@lru_cache(maxsize=1)
def get_client() -> AsyncOpenAI:
    """Process-wide singleton. AsyncOpenAI is thread-safe and connection-pools."""
    return AsyncOpenAI(base_url=_endpoint(), api_key=_resolve_api_key())


def reset_client() -> None:
    """Clear the cached client - call after `AZURE_OPENAI_*` env changes or a 401."""
    get_client.cache_clear()


def chat_deployment() -> str:
    return os.getenv("AZURE_OPENAI_CHATGPT_DEPLOYMENT", "gpt-4.1-mini")

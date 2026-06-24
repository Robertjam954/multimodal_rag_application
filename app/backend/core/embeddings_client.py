"""Async wrapper around the Foundry embedding deployment.

Chat/Responses route through the Foundry PROJECT endpoint
(`.../api/projects/<project>/openai/v1`, `ai.azure.com` audience). Embeddings,
however, are ONLY served on the ACCOUNT endpoint — the project `/openai/v1`
path returns 404 for embeddings. So this module builds its OWN client against
`AZURE_OPENAI_EMBEDDING_ENDPOINT` (the account endpoint) with the
`cognitiveservices.azure.com` audience, independent of `core.aoai_client`.
"""
from __future__ import annotations

import logging
import os
from functools import lru_cache

from openai import AsyncOpenAI

logger = logging.getLogger(__name__)

EMBED_DEFAULT_SCOPE = "https://cognitiveservices.azure.com/.default"


def embedding_deployment() -> str:
    name = os.getenv("AZURE_OPENAI_EMBEDDING_DEPLOYMENT")
    if not name:
        raise RuntimeError(
            "AZURE_OPENAI_EMBEDDING_DEPLOYMENT is not set in the environment."
        )
    return name


def _embed_endpoint() -> str:
    """Account endpoint for embeddings (project endpoint 404s on embeddings)."""
    endpoint = (
        os.getenv("AZURE_OPENAI_EMBEDDING_ENDPOINT")
        or os.environ["AZURE_OPENAI_ENDPOINT"]
    ).rstrip("/")
    if not endpoint.endswith("/openai/v1"):
        endpoint = endpoint + "/openai/v1"
    return endpoint


def _embed_api_key() -> str:
    """Static key if provided and AAD not forced, else an AAD bearer token
    scoped to the Cognitive Services (account) audience."""
    static_key = os.getenv("AZURE_OPENAI_API_KEY")
    if static_key and os.getenv("AZURE_OPENAI_USE_AAD", "").lower() != "true":
        return static_key
    from azure.identity import DefaultAzureCredential

    scope = os.getenv("AZURE_OPENAI_EMBEDDING_AAD_SCOPE", EMBED_DEFAULT_SCOPE)
    return DefaultAzureCredential().get_token(scope).token


@lru_cache(maxsize=1)
def _embed_client() -> AsyncOpenAI:
    """Process-wide embeddings client (account endpoint). Token cached ~60 min;
    call reset_embed_client() after a 401 to refresh."""
    return AsyncOpenAI(base_url=_embed_endpoint(), api_key=_embed_api_key())


def reset_embed_client() -> None:
    _embed_client.cache_clear()


async def embed_texts(texts: list[str]) -> list[list[float]]:
    """Returns one embedding per input text. Empty input -> empty output."""
    if not texts:
        return []
    client = _embed_client()
    response = await client.embeddings.create(model=embedding_deployment(), input=texts)
    return [item.embedding for item in response.data]


async def embed_one(text: str) -> list[float]:
    out = await embed_texts([text])
    return out[0] if out else []

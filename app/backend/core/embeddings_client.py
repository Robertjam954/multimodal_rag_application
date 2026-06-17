"""Async wrapper around the Foundry embedding deployment.

Reuses `core.aoai_client` (AAD via `az login` on the same Foundry endpoint as Grok).
Deployment name comes from `AZURE_OPENAI_EMBEDDING_DEPLOYMENT`.
"""
from __future__ import annotations

import logging
import os

from core.aoai_client import get_client

logger = logging.getLogger(__name__)


def embedding_deployment() -> str:
    name = os.getenv("AZURE_OPENAI_EMBEDDING_DEPLOYMENT")
    if not name:
        raise RuntimeError(
            "AZURE_OPENAI_EMBEDDING_DEPLOYMENT is not set in the environment."
        )
    return name


async def embed_texts(texts: list[str]) -> list[list[float]]:
    """Returns one embedding per input text. Empty input -> empty output."""
    if not texts:
        return []
    client = get_client()
    response = await client.embeddings.create(model=embedding_deployment(), input=texts)
    return [item.embedding for item in response.data]


async def embed_one(text: str) -> list[float]:
    out = await embed_texts([text])
    return out[0] if out else []

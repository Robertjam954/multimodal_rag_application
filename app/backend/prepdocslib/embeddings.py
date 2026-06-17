"""Text + image embeddings. Azure OpenAI for text; Azure AI Vision for images."""
from __future__ import annotations

import logging
import os
from typing import Iterable

from tenacity import retry, stop_after_attempt, wait_exponential_jitter

logger = logging.getLogger(__name__)


class TextEmbeddings:
    def __init__(self, deployment: str | None = None) -> None:
        self.deployment = deployment or os.getenv("AZURE_OPENAI_EMB_DEPLOYMENT", os.getenv("OPENAI_EMB_MODEL", "text-embedding-3-large"))

    def _client(self):
        if os.getenv("AZURE_OPENAI_SERVICE"):
            from openai import AsyncAzureOpenAI

            return AsyncAzureOpenAI(
                azure_endpoint=f"https://{os.getenv('AZURE_OPENAI_SERVICE')}.openai.azure.com/",
                api_version=os.getenv("AZURE_OPENAI_API_VERSION", "2024-10-01-preview"),
                api_key=os.getenv("AZURE_OPENAI_API_KEY"),
            )
        from openai import AsyncOpenAI

        return AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    @retry(wait=wait_exponential_jitter(initial=1, max=30), stop=stop_after_attempt(5), reraise=True)
    async def embed(self, texts: Iterable[str]) -> list[list[float]]:
        text_list = list(texts)
        if not text_list:
            return []

        # Embedding cache: hash-keyed lookup, only call OpenAI for misses.
        cached: dict[int, list[float]] = {}
        if os.getenv("USE_EMBEDDING_CACHE", "true").lower() == "true":
            try:
                from core.semantic_cache import EmbeddingCache

                cached = await EmbeddingCache.get_many(self.deployment, text_list)
            except Exception:
                logger.exception("embedding cache lookup failed; computing all")

        miss_indices = [i for i in range(len(text_list)) if i not in cached]
        if not miss_indices:
            return [cached[i] for i in range(len(text_list))]

        miss_texts = [text_list[i] for i in miss_indices]
        if not (os.getenv("AZURE_OPENAI_SERVICE") or os.getenv("OPENAI_API_KEY")):
            # Local / unset: dummy vectors so the pipeline runs.
            new_vecs = [[0.0] * 8 for _ in miss_texts]
        else:
            client = self._client()
            resp = await client.embeddings.create(model=self.deployment, input=miss_texts)
            new_vecs = [d.embedding for d in resp.data]

        if os.getenv("USE_EMBEDDING_CACHE", "true").lower() == "true":
            try:
                from core.semantic_cache import EmbeddingCache

                await EmbeddingCache.set_many(self.deployment, miss_texts, new_vecs)
            except Exception:
                logger.exception("embedding cache store failed")

        result: list[list[float]] = [[] for _ in text_list]
        for i, vec in cached.items():
            result[i] = vec
        for idx, vec in zip(miss_indices, new_vecs):
            result[idx] = vec
        return result


class ImageEmbeddings:
    """Calls Azure AI Vision multimodal embeddings."""

    def __init__(self, endpoint: str | None = None) -> None:
        self.endpoint = endpoint or os.getenv("AZURE_VISION_ENDPOINT")
        self.key = os.getenv("AZURE_VISION_KEY")

    async def embed(self, image_bytes: bytes) -> list[float]:
        if not (self.endpoint and self.key):
            return [0.0] * 8
        import httpx

        url = f"{self.endpoint.rstrip('/')}/computervision/retrieval:vectorizeImage?api-version=2024-02-01"
        headers = {"Ocp-Apim-Subscription-Key": self.key, "Content-Type": "application/octet-stream"}
        async with httpx.AsyncClient(timeout=30) as c:
            r = await c.post(url, headers=headers, content=image_bytes)
            r.raise_for_status()
            return r.json().get("vector", [])

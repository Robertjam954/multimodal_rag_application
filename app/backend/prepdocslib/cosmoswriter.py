"""Cosmos DB for NoSQL vector writer.

Drop-in replacement for `SearchManager` (same `ensure_index` / `upsert` /
`remove_all` surface) that writes chunks + embeddings into the Cosmos NoSQL
`documents` container for integrated vector search. Selected when
`DOCUMENT_RETRIEVER=cosmos`. Keyless: uses the AAD credential passed from
`prepdocs.py` (the `Cosmos DB Built-in Data Contributor` role).

Document shape matches `core/cosmos_vector_retriever.py`:
    { id, doc_id (partition key), content, embedding[3072],
      source_url, source_type, content_topic, tags[], source_page }
"""
from __future__ import annotations

import logging
import os
from typing import Any

from prepdocslib.page import Chunk

logger = logging.getLogger(__name__)


class CosmosWriter:
    def __init__(
        self,
        credential: Any | None = None,
        endpoint: str | None = None,
        database: str | None = None,
        container: str | None = None,
    ) -> None:
        self.endpoint = endpoint or os.getenv("AZURE_COSMOSDB_ENDPOINT", "")
        self.database = database or os.getenv("AZURE_COSMOSDB_VECTOR_DATABASE", "rag")
        self.container_name = container or os.getenv("AZURE_COSMOSDB_VECTOR_CONTAINER", "documents")
        self.credential = credential
        self._client = None
        self._container = None

    def _get_container(self):
        if self._container is not None:
            return self._container
        if not (self.endpoint and self.credential):
            logger.info("Cosmos writer disabled (no endpoint/credential)")
            return None
        try:
            from azure.cosmos.aio import CosmosClient
        except Exception:
            logger.warning("azure-cosmos missing; Cosmos writer disabled")
            return None
        self._client = CosmosClient(self.endpoint, credential=self.credential)
        self._container = self._client.get_database_client(self.database).get_container_client(
            self.container_name
        )
        return self._container

    async def ensure_index(self, multimodal: bool = False) -> None:
        # The vector container (policy + diskANN index) is provisioned out-of-band.
        return

    async def upsert(self, chunks: list[Chunk]) -> None:
        container = self._get_container()
        if not container:
            logger.info("Cosmos upsert skipped (no container); %d chunks", len(chunks))
            return
        n = 0
        for c in chunks:
            doc = {
                "id": c.id,
                "doc_id": c.source_file or "unknown",
                "content": c.content,
                "embedding": c.embedding or [],
                "source_url": c.storage_url or "",
                "source_type": c.source_type or "text",
                "content_topic": c.category or "",
                "tags": list(c.acls or []),
                "source_page": c.source_page,
            }
            try:
                await container.upsert_item(doc)
                n += 1
            except Exception:
                logger.exception("Cosmos upsert failed for chunk %s", c.id)
        logger.info("Cosmos upsert wrote %d/%d chunks", n, len(chunks))

    async def remove_all(self) -> None:
        container = self._get_container()
        if not container:
            return
        try:
            async for it in container.query_items(query="SELECT c.id, c.doc_id FROM c"):
                await container.delete_item(item=it["id"], partition_key=it.get("doc_id", "unknown"))
        except Exception:
            logger.exception("Cosmos remove_all failed")

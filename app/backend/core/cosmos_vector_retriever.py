"""Cosmos DB for NoSQL vector retriever.

Retrieval over the `documents` container in Cosmos NoSQL using integrated vector
search (`VectorDistance` + a diskANN vector index on `/embedding`). Mirrors the
`Retriever` protocol in `core.document_retriever` so it drops in behind the
`DOCUMENT_RETRIEVER=cosmos` switch with no change to the agent/tool layer.

Auth is keyless: the async Cosmos client uses `DefaultAzureCredential` (the
backend's managed identity in production, `az login` in dev) and the
`Cosmos DB Built-in Data Contributor` role on the account.

Document shape written by ingestion (see `prepdocslib/cosmoswriter.py`):
    { id, doc_id (partition key), content, embedding[3072],
      source_url, source_type, content_topic, tags[] }
"""
from __future__ import annotations

import logging
import os
from typing import Any

from core.document_retriever import Document
from core.embeddings_client import embed_one

logger = logging.getLogger(__name__)

_VECTOR_FIELDS = "c.id, c.doc_id, c.content, c.source_url, c.source_type, c.content_topic, c.tags"


class CosmosVectorRetriever:
    """Vector retrieval over Cosmos NoSQL `VectorDistance` (cosine, diskANN)."""

    name = "cosmos"

    def __init__(self) -> None:
        self._endpoint = os.getenv("AZURE_COSMOSDB_ENDPOINT", "")
        self._database = os.getenv("AZURE_COSMOSDB_VECTOR_DATABASE", "rag")
        self._container_name = os.getenv("AZURE_COSMOSDB_VECTOR_CONTAINER", "documents")
        self._client = None
        self._credential = None
        self._container = None

    def _get_container(self):
        """Lazily build the async Cosmos client + container handle (keyless)."""
        if self._container is not None:
            return self._container
        if not self._endpoint:
            return None
        try:
            from azure.cosmos.aio import CosmosClient
            from azure.identity.aio import DefaultAzureCredential
        except Exception:
            logger.warning("azure-cosmos / azure-identity missing; Cosmos retriever disabled")
            return None
        self._credential = DefaultAzureCredential()
        self._client = CosmosClient(self._endpoint, credential=self._credential)
        self._container = self._client.get_database_client(self._database).get_container_client(
            self._container_name
        )
        return self._container

    async def retrieve(
        self,
        query: str,
        *,
        k: int = 5,
        source_type: str | None = None,
        tag: str | None = None,
    ) -> list[Document]:
        if not query.strip():
            return []
        container = self._get_container()
        if container is None:
            return []
        k = max(1, min(int(k or 5), 25))
        try:
            qvec = await embed_one(query)
        except Exception:
            logger.exception("query embedding failed in CosmosVectorRetriever")
            return []
        if not qvec:
            return []

        params: list[dict[str, Any]] = [{"name": "@embedding", "value": qvec}]
        filters: list[str] = []
        if source_type:
            filters.append("c.source_type = @source_type")
            params.append({"name": "@source_type", "value": source_type})
        if tag:
            filters.append("ARRAY_CONTAINS(c.tags, @tag)")
            params.append({"name": "@tag", "value": tag})
        where = (" WHERE " + " AND ".join(filters)) if filters else ""

        # diskANN orders nearest-first for cosine; VectorDistance returns the similarity score.
        sql = (
            f"SELECT TOP {k} {_VECTOR_FIELDS}, "
            "VectorDistance(c.embedding, @embedding) AS score "
            f"FROM c{where} "
            "ORDER BY VectorDistance(c.embedding, @embedding)"
        )
        try:
            items = [item async for item in container.query_items(query=sql, parameters=params)]
        except Exception:
            logger.exception("Cosmos vector query failed")
            return []
        return [
            Document(
                id=str(it.get("id", "")),
                content=it.get("content", "") or "",
                score=float(it.get("score", 0.0)),
                source_url=it.get("source_url", "") or "",
                source_type=it.get("source_type", "text") or "text",
                content_topic=it.get("content_topic", "") or "",
                tags=list(it.get("tags", []) or []),
            )
            for it in items
        ]

    async def get_document(self, doc_id: str) -> Document | None:
        """Reassemble a full document from its chunks (same partition key)."""
        container = self._get_container()
        if container is None or not doc_id:
            return None
        sql = f"SELECT {_VECTOR_FIELDS} FROM c WHERE c.doc_id = @doc_id"
        params = [{"name": "@doc_id", "value": doc_id}]
        try:
            chunks = [
                it
                async for it in container.query_items(
                    query=sql, parameters=params, partition_key=doc_id
                )
            ]
        except Exception:
            logger.exception("Cosmos get_document failed for doc_id=%s", doc_id)
            return None
        if not chunks:
            return None
        # Stable order by chunk id suffix when present (e.g. "<doc_id>:<n>").
        def _ord(c: dict[str, Any]) -> int:
            cid = str(c.get("id", ""))
            tail = cid.rsplit(":", 1)[-1]
            return int(tail) if tail.isdigit() else 0

        chunks.sort(key=_ord)
        first = chunks[0]
        return Document(
            id=doc_id,
            content="\n\n".join(c.get("content", "") for c in chunks if c.get("content")),
            score=1.0,
            source_url=first.get("source_url", "") or "",
            source_type=first.get("source_type", "text") or "text",
            content_topic=first.get("content_topic", "") or "",
            tags=list(first.get("tags", []) or []),
            extra={"chunk_count": len(chunks)},
        )

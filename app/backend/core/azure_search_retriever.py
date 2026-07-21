"""Azure AI Search hybrid retriever.

Runtime retrieval over the `rag-index` built by `prepdocslib/searchmanager.py`.
Hybrid query: BM25 full-text + HNSW vector KNN over `embedding`, fused by RRF;
when `AZURE_SEARCH_SEMANTIC_RANKER=true` the semantic ranker re-scores the fused
results (semantic config `default`, free tier by default in infra).

Mirrors the `Retriever` protocol in `core.document_retriever` so it drops in
behind `DOCUMENT_RETRIEVER=azure_search` with no change to the agent/tool layer.

Auth is keyless: async `SearchClient` with `DefaultAzureCredential` (backend
managed identity in production, `az login`/`azd auth login` in dev) and the
Search Index Data Contributor role assigned in `infra/app/rbac.bicep`.

Index document shape (see `prepdocslib/servicesetup.py`):
    { id, parent_id, content, category, source_type, sourcefile, sourcepage,
      storageUrl, embedding[3072], acls[] }
"""
from __future__ import annotations

import logging
import os
from typing import Any

from core.document_retriever import Document
from core.embeddings_client import embed_one

logger = logging.getLogger(__name__)

_SELECT_FIELDS = [
    "id",
    "parent_id",
    "content",
    "category",
    "category",
    "source_type",
    "sourcefile",
    "sourcepage",
    "storageUrl",
]


def _odata_quote(value: str) -> str:
    return value.replace("'", "''")


class AzureSearchRetriever:
    """Hybrid (BM25 + vector, optional semantic rerank) retrieval over AI Search."""

    name = "azure_search"

    def __init__(self) -> None:
        self._service = os.getenv("AZURE_SEARCH_SERVICE", "")
        self._index = os.getenv("AZURE_SEARCH_INDEX", "rag-index")
        self._semantic = os.getenv("AZURE_SEARCH_SEMANTIC_RANKER", "true").lower() == "true"
        self._client = None
        self._credential = None

    def _get_client(self):
        """Lazily build the async SearchClient (keyless)."""
        if self._client is not None:
            return self._client
        if not self._service:
            return None
        try:
            from azure.identity.aio import DefaultAzureCredential
            from azure.search.documents.aio import SearchClient
        except Exception:
            logger.warning("azure-search-documents / azure-identity missing; search retriever disabled")
            return None
        self._credential = DefaultAzureCredential()
        self._client = SearchClient(
            endpoint=f"https://{self._service}.search.windows.net",
            index_name=self._index,
            credential=self._credential,
        )
        return self._client

    @staticmethod
    def _to_document(hit: dict[str, Any]) -> Document:
        # Semantic ranker score when present, else the RRF hybrid score.
        score = hit.get("@search.reranker_score") or hit.get("@search.score") or 0.0
        category = hit.get("category") or ""
        return Document(
            id=str(hit.get("id", "")),
            content=hit.get("content", "") or "",
            score=float(score),
            source_url=hit.get("storageUrl", "") or hit.get("sourcefile", "") or "",
            source_type=hit.get("source_type", "text") or "text",
            content_topic=category,
            tags=[category] if category else [],
            extra={
                "parent_id": hit.get("parent_id", ""),
                "sourcefile": hit.get("sourcefile", ""),
                "sourcepage": hit.get("sourcepage", ""),
            },
        )

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
        client = self._get_client()
        if client is None:
            return []
        k = max(1, min(int(k or 5), 25))
        try:
            qvec = await embed_one(query)
        except Exception:
            logger.exception("query embedding failed in AzureSearchRetriever")
            return []

        from azure.search.documents.models import VectorizedQuery

        filters: list[str] = []
        if source_type:
            filters.append(f"source_type eq '{_odata_quote(source_type)}'")
        if tag:
            filters.append(f"category eq '{_odata_quote(tag)}'")
        filter_expr = " and ".join(filters) if filters else None

        kwargs: dict[str, Any] = {}
        if self._semantic:
            kwargs["query_type"] = "semantic"
            kwargs["semantic_configuration_name"] = "default"
        try:
            results = await client.search(
                search_text=query,
                vector_queries=(
                    [VectorizedQuery(vector=qvec, k_nearest_neighbors=k, fields="embedding")]
                    if qvec
                    else None
                ),
                filter=filter_expr,
                select=_SELECT_FIELDS,
                top=k,
                **kwargs,
            )
            return [self._to_document(hit) async for hit in results]
        except Exception:
            logger.exception("Azure AI Search query failed")
            return []

    async def get_document(self, doc_id: str) -> Document | None:
        """Reassemble a full document from its chunks via `parent_id`.

        Accepts either a chunk id (resolved to its parent via key lookup) or a
        parent id directly.
        """
        client = self._get_client()
        if client is None or not doc_id:
            return None

        parent_id = doc_id
        try:
            chunk = await client.get_document(key=doc_id, selected_fields=["id", "parent_id"])
            parent_id = chunk.get("parent_id") or doc_id
        except Exception:
            # Not a chunk key; treat doc_id as a parent_id.
            pass

        try:
            results = await client.search(
                search_text="*",
                filter=f"parent_id eq '{_odata_quote(parent_id)}'",
                select=_SELECT_FIELDS,
                top=1000,
            )
            chunks = [hit async for hit in results]
        except Exception:
            logger.exception("Azure AI Search get_document failed for doc_id=%s", doc_id)
            return None
        if not chunks:
            return None

        # Stable reading order: page number then trailing chunk ordinal.
        def _ord(c: dict[str, Any]) -> tuple[int, int]:
            page_raw = str(c.get("sourcepage") or "0")
            page = int(page_raw) if page_raw.isdigit() else 0
            tail = str(c.get("id", "")).rsplit("-", 1)[-1]
            return (page, int(tail) if tail.isdigit() else 0)

        chunks.sort(key=_ord)
        first = chunks[0]
        category = first.get("category") or ""
        return Document(
            id=parent_id,
            content="\n\n".join(c.get("content", "") for c in chunks if c.get("content")),
            score=1.0,
            source_url=first.get("storageUrl", "") or first.get("sourcefile", "") or "",
            source_type=first.get("source_type", "text") or "text",
            content_topic=category,
            tags=[category] if category else [],
            extra={"chunk_count": len(chunks)},
        )

"""Azure AI Search: index create + upsert. Also pushes to OpenAI file_search vector store."""
from __future__ import annotations

import logging
import os
from typing import Any

from prepdocslib.page import Chunk
from prepdocslib.servicesetup import search_index_schema

logger = logging.getLogger(__name__)


class SearchManager:
    def __init__(self, service: str | None = None, index: str | None = None, credential: Any | None = None) -> None:
        self.service = service or os.getenv("AZURE_SEARCH_SERVICE")
        self.index = index or os.getenv("AZURE_SEARCH_INDEX", "rag-index")
        self.credential = credential

    def _index_client(self):
        try:
            from azure.search.documents.indexes.aio import SearchIndexClient
        except Exception:
            return None
        if not self.service:
            return None
        return SearchIndexClient(endpoint=f"https://{self.service}.search.windows.net", credential=self.credential)

    def _search_client(self):
        try:
            from azure.search.documents.aio import SearchClient
        except Exception:
            return None
        if not self.service:
            return None
        return SearchClient(endpoint=f"https://{self.service}.search.windows.net", index_name=self.index, credential=self.credential)

    async def ensure_index(self, multimodal: bool = False) -> None:
        client = self._index_client()
        if not client:
            return
        try:
            await client.create_or_update_index(search_index_schema(self.index, multimodal=multimodal))
        except Exception:
            logger.exception("ensure_index failed; continuing")

    async def upsert(self, chunks: list[Chunk]) -> None:
        client = self._search_client()
        if not client:
            logger.info("Search upsert skipped (no service); %d chunks", len(chunks))
            return
        docs = [
            {
                "id": c.id,
                "content": c.content,
                "category": c.category,
                "sourcefile": c.source_file,
                "sourcepage": str(c.source_page) if c.source_page else None,
                "storageUrl": c.storage_url,
                "embedding": c.embedding or [],
                "acls": c.acls,
                "images": c.images,
            }
            for c in chunks
        ]
        await client.upload_documents(documents=docs)

    async def remove_all(self) -> None:
        client = self._index_client()
        if not client:
            return
        try:
            await client.delete_index(self.index)
        except Exception:
            logger.exception("remove_all failed")


async def push_to_file_search(chunks: list[Chunk]) -> None:
    """Upload chunk contents to the OpenAI Responses-API file_search vector store."""
    vs_id = os.getenv("OPENAI_FILE_SEARCH_VECTOR_STORE_ID")
    api_key = os.getenv("OPENAI_API_KEY")
    if not (vs_id and api_key):
        logger.info("file_search push skipped (no vector store)")
        return
    from openai import AsyncOpenAI

    client = AsyncOpenAI(api_key=api_key)
    for c in chunks:
        import io

        f = io.BytesIO(c.content.encode("utf-8"))
        f.name = f"{c.id}.txt"
        uploaded = await client.files.create(file=f, purpose="assistants")
        await client.vector_stores.files.create(vector_store_id=vs_id, file_id=uploaded.id)

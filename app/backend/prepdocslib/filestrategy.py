"""Local ingestion + per-user upload strategy."""
from __future__ import annotations

import logging
import os
import uuid
from pathlib import Path
from typing import Any

from prepdocslib.blobmanager import BlobManager
from prepdocslib.embeddings import TextEmbeddings
from prepdocslib.listfilestrategy import File, list_local
from prepdocslib.page import Chunk, Page
from prepdocslib.pdfparser import PdfParser
from prepdocslib.searchmanager import SearchManager, push_to_file_search
from prepdocslib.strategy import Strategy
from prepdocslib.textparser import TextParser
from prepdocslib.textsplitter import split_text

logger = logging.getLogger(__name__)


def _parser_for(filename: str):
    name = filename.lower()
    if name.startswith("youtube://"):
        from prepdocslib.youtubeparser import YouTubeTranscriptParser

        return YouTubeTranscriptParser()
    if name.endswith(".pdf"):
        return PdfParser()
    return TextParser()


class FileStrategy(Strategy):
    def __init__(
        self,
        data_dir: Path,
        blob_manager: BlobManager | None,
        search: SearchManager | None,
        embeddings: TextEmbeddings | None,
        category: str | None = None,
        multimodal: bool = False,
    ) -> None:
        self.data_dir = data_dir
        self.blob = blob_manager
        self.search = search
        self.embeddings = embeddings
        self.category = category
        self.multimodal = multimodal

    async def setup(self) -> None:
        if self.search:
            await self.search.ensure_index(multimodal=self.multimodal)

    async def run(self) -> dict[str, Any]:
        n_files = n_chunks = 0
        all_chunks: list[Chunk] = []
        async for f in list_local(self.data_dir):
            n_files += 1
            parser = _parser_for(f.path.name)
            url = ""
            if self.blob:
                url = await self.blob.upload(name=f.path.name, data=f.data)
            pages: list[Page] = []
            async for p in parser.parse(f.data, f.path.name):
                pages.append(p)
            chunks: list[Chunk] = []
            for p in pages:
                for ci, ctext in enumerate(split_text(p.text)):
                    chunks.append(
                        Chunk(
                            id=f"file-{f.md5}-page-{p.page_number}-{ci}",
                            content=ctext,
                            source_file=f.path.name,
                            source_page=p.page_number,
                            storage_url=url,
                            category=self.category,
                        )
                    )
            if self.embeddings and chunks:
                embs = await self.embeddings.embed([c.content for c in chunks])
                for c, e in zip(chunks, embs):
                    c.embedding = e
            if self.search and chunks:
                await self.search.upsert(chunks)
            all_chunks.extend(chunks)
            n_chunks += len(chunks)
        await push_to_file_search(all_chunks)

        # GraphRAG indexing (optional)
        if os.getenv("USE_GRAPHRAG", "true").lower() == "true":
            try:
                from graphrag.indexer import index_chunks

                await index_chunks([{"id": c.id, "content": c.content} for c in all_chunks])
            except Exception:
                logger.exception("graphrag indexing failed; continuing")

        return {"files": n_files, "chunks": n_chunks}


class UploadUserFileStrategy:
    """Per-session upload: lands in a user-scoped Blob path, then embeds + indexes
    into the active vector store. With `DOCUMENT_RETRIEVER=cosmos` it writes to the
    Cosmos NoSQL `documents` container (same store the chat retriever reads); else it
    falls back to Azure AI Search. Embeddings use the account-endpoint AAD client
    (`core.embeddings_client`), the one path proven to serve embeddings."""

    def __init__(self, blob_manager: BlobManager | None, search_service: str | None, search_index: str | None, credential: Any | None) -> None:
        self.blob = blob_manager
        self.use_cosmos = os.getenv("DOCUMENT_RETRIEVER", "redis_notes").lower() == "cosmos"
        if self.use_cosmos:
            from prepdocslib.cosmoswriter import CosmosWriter

            self.writer: Any = CosmosWriter(credential=credential)
        else:
            self.writer = (
                SearchManager(service=search_service, index=search_index, credential=credential)
                if search_service
                else None
            )

    async def ingest_user_upload(self, filename: str, data: bytes, oid: str | None = None) -> dict[str, Any]:
        oid = oid or "anon"
        path = f"user-content/{oid}/{uuid.uuid4().hex}-{filename}"
        url = ""
        if self.blob:
            url = await self.blob.upload(name=path, data=data)
        parser = _parser_for(filename)
        chunks: list[Chunk] = []
        async for p in parser.parse(data, filename):
            for ci, ctext in enumerate(split_text(p.text)):
                chunks.append(
                    Chunk(
                        id=f"upload-{oid}-{uuid.uuid4().hex[:8]}-{ci}",
                        content=ctext,
                        source_file=filename,
                        source_page=p.page_number,
                        storage_url=url,
                        acls=[oid],
                    )
                )

        # Embed every chunk so it is retrievable (Cosmos vector search needs the vector).
        if chunks:
            from core.embeddings_client import embed_texts

            embs = await embed_texts([c.content for c in chunks])
            for c, e in zip(chunks, embs):
                c.embedding = e

        if self.writer and chunks:
            await self.writer.upsert(chunks)
        await push_to_file_search(chunks)
        return {"filename": filename, "url": url, "chunks": len(chunks)}

"""Microsoft Learn ingestion strategy.

Reads a newline-separated URL list, fetches each page over HTTPS, parses via
LearnDocParser, chunks via split_text, embeds via TextEmbeddings, and upserts
into Azure AI Search with source_type='learn' so the retriever can filter or
boost it like any other source.
"""
from __future__ import annotations

import asyncio
import hashlib
import logging
import os
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

from prepdocslib.embeddings import TextEmbeddings
from prepdocslib.learndocparser import LearnDocParser
from prepdocslib.page import Chunk
from prepdocslib.searchmanager import SearchManager, push_to_file_search
from prepdocslib.strategy import Strategy
from prepdocslib.textsplitter import split_text

logger = logging.getLogger(__name__)


def _read_url_list(path: Path) -> list[str]:
    urls: list[str] = []
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        urls.append(line)
    return urls


def _source_file(url: str) -> str:
    parsed = urlparse(url)
    return f"{parsed.netloc}{parsed.path}".strip("/") or url


class LearnStrategy(Strategy):
    def __init__(
        self,
        url_list: Path,
        search: SearchManager | None,
        embeddings: TextEmbeddings | None,
        category: str = "learn-azure-ai",
        concurrency: int = 4,
        request_timeout: float = 30.0,
    ) -> None:
        self.url_list = url_list
        self.search = search
        self.embeddings = embeddings
        self.category = category
        self.concurrency = concurrency
        self.request_timeout = request_timeout

    async def setup(self) -> None:
        if self.search:
            await self.search.ensure_index(multimodal=False)

    async def run(self) -> dict[str, Any]:
        import httpx

        urls = _read_url_list(self.url_list)
        if not urls:
            logger.warning("Learn URL list empty: %s", self.url_list)
            return {"urls": 0, "chunks": 0}

        sem = asyncio.Semaphore(self.concurrency)
        all_chunks: list[Chunk] = []
        n_pages = 0
        parser = LearnDocParser()

        async with httpx.AsyncClient(
            timeout=self.request_timeout,
            follow_redirects=True,
            headers={"User-Agent": "multimodal-rag-app/learn-ingest"},
        ) as http:

            async def fetch_one(url: str) -> list[Chunk]:
                nonlocal n_pages
                async with sem:
                    try:
                        r = await http.get(url)
                        r.raise_for_status()
                    except Exception:
                        logger.exception("fetch failed: %s", url)
                        return []
                content = r.content
                doc_id = hashlib.md5(url.encode("utf-8")).hexdigest()
                source_file = _source_file(url)
                chunks: list[Chunk] = []
                async for page in parser.parse(content, source_file):
                    if not page.text.strip():
                        continue
                    for ci, ctext in enumerate(split_text(page.text)):
                        chunks.append(
                            Chunk(
                                id=f"learn-{doc_id}-{ci}",
                                content=ctext,
                                source_file=source_file,
                                source_page=1,
                                storage_url=url,
                                category=self.category,
                                source_type="learn",
                            )
                        )
                n_pages += 1
                return chunks

            results = await asyncio.gather(*(fetch_one(u) for u in urls))

        for chunks in results:
            all_chunks.extend(chunks)

        if self.embeddings and all_chunks:
            embs = await self.embeddings.embed([c.content for c in all_chunks])
            for c, e in zip(all_chunks, embs):
                c.embedding = e

        if self.search and all_chunks:
            await self.search.upsert(all_chunks)

        await push_to_file_search(all_chunks)

        if os.getenv("USE_GRAPHRAG", "true").lower() == "true":
            try:
                from graphrag.indexer import index_chunks

                await index_chunks([{"id": c.id, "content": c.content} for c in all_chunks])
            except Exception:
                logger.exception("graphrag indexing failed; continuing")

        return {"urls": len(urls), "pages": n_pages, "chunks": len(all_chunks)}

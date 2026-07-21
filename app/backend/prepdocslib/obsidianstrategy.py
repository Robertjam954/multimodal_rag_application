"""Obsidian vault ingestion strategy.

Walks a local Obsidian vault for markdown notes, strips YAML frontmatter,
chunks via split_text, embeds via TextEmbeddings, and upserts into the
configured vector store (CosmosWriter or SearchManager) with
source_type='note' so the retriever can filter or boost it like any other
source. Wikilink targets and #tags are captured per note; the link graph
itself is consumed at runtime by the (planned) Obsidian retriever, not stored
in the vector index.

Note ids are `obsidian-<md5(relative path)>-<chunk#>` - key-safe for Azure AI
Search and grouped by the `obsidian-<md5>` parent prefix.
"""
from __future__ import annotations

import hashlib
import logging
import os
import re
from pathlib import Path
from typing import Any
from urllib.parse import quote

from prepdocslib.embeddings import TextEmbeddings
from prepdocslib.page import Chunk
from prepdocslib.searchmanager import push_to_file_search
from prepdocslib.strategy import Strategy
from prepdocslib.textsplitter import split_text

logger = logging.getLogger(__name__)

_WIKILINK_RE = re.compile(r"\[\[([^\]|#]+)(?:[#|][^\]]*)?\]\]")
_TAG_RE = re.compile(r"(?:^|\s)#([A-Za-z][\w/-]*)")
_FRONTMATTER_RE = re.compile(r"\A---\s*\n(.*?)\n---\s*\n", re.DOTALL)


def parse_note(text: str) -> tuple[str, list[str], list[str]]:
    """Return (body without frontmatter, wikilink targets, tags)."""
    tags: list[str] = []
    m = _FRONTMATTER_RE.match(text)
    if m:
        for line in m.group(1).splitlines():
            stripped = line.strip()
            if stripped.startswith("tags:"):
                raw = stripped[len("tags:"):].strip().strip("[]")
                tags.extend(t.strip().strip("'\"#") for t in raw.split(",") if t.strip())
        text = text[m.end():]
    links = list(dict.fromkeys(_WIKILINK_RE.findall(text)))
    tags.extend(t for t in _TAG_RE.findall(text) if t not in tags)
    return text, links, tags


def iter_vault_notes(vault: Path) -> list[Path]:
    """All markdown notes, skipping the .obsidian config dir and hidden folders."""
    notes: list[Path] = []
    for p in sorted(vault.rglob("*.md")):
        if any(part.startswith(".") for part in p.relative_to(vault).parts):
            continue
        notes.append(p)
    return notes


class ObsidianStrategy(Strategy):
    def __init__(
        self,
        vault: Path,
        search: Any | None,
        embeddings: TextEmbeddings | None,
        category: str = "obsidian",
    ) -> None:
        self.vault = vault
        self.search = search
        self.embeddings = embeddings
        self.category = category

    async def setup(self) -> None:
        if self.search:
            await self.search.ensure_index(multimodal=False)

    async def run(self) -> dict[str, Any]:
        notes = iter_vault_notes(self.vault)
        if not notes:
            logger.warning("No markdown notes found in vault: %s", self.vault)
            return {"notes": 0, "chunks": 0}

        vault_name = self.vault.name
        all_chunks: list[Chunk] = []
        n_notes = 0
        for path in notes:
            try:
                text = path.read_text(encoding="utf-8")
            except Exception:
                # iCloud-evicted or unreadable file; skip rather than fail the run.
                logger.exception("could not read note: %s", path)
                continue
            body, links, tags = parse_note(text)
            if not body.strip():
                continue
            rel = path.relative_to(self.vault).as_posix()
            note_id = hashlib.md5(rel.encode("utf-8")).hexdigest()
            deep_link = f"obsidian://open?vault={quote(vault_name)}&file={quote(rel[:-3])}"
            for ci, ctext in enumerate(split_text(body)):
                all_chunks.append(
                    Chunk(
                        id=f"obsidian-{note_id}-{ci}",
                        content=ctext,
                        source_file=rel,
                        source_page=None,
                        storage_url=deep_link,
                        category=self.category,
                        source_type="note",
                        acls=tags,
                    )
                )
            n_notes += 1
            if links:
                logger.debug("note %s links to: %s", rel, links)

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

        return {"notes": n_notes, "chunks": len(all_chunks)}

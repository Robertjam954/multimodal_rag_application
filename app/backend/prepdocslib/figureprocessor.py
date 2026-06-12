"""Figure processor: crop + describe + (optional) embed + upload to Blob."""
from __future__ import annotations

import logging
from typing import Any

from prepdocslib.embeddings import ImageEmbeddings
from prepdocslib.mediadescriber import describe
from prepdocslib.page import Figure

logger = logging.getLogger(__name__)


async def process_figure(figure: Figure, blob_manager: Any, source_file: str, multimodal: bool = False) -> Figure:
    figure.description = await describe(figure.image_bytes or b"", hint=figure.caption)
    if figure.image_bytes and blob_manager:
        figure.image_url = await blob_manager.upload(
            name=f"figures/{source_file}/{figure.id}.png",
            data=figure.image_bytes,
            content_type="image/png",
        )
    if multimodal and figure.image_bytes:
        try:
            emb = ImageEmbeddings()
            figure.embedding = await emb.embed(figure.image_bytes)
        except Exception:
            logger.exception("figure embedding failed; continuing without")
    return figure

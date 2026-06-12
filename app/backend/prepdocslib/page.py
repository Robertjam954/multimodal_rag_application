"""Data classes for the ingestion pipeline: Page, Figure, Chunk."""
from __future__ import annotations

import dataclasses
from typing import Any


@dataclasses.dataclass
class Figure:
    id: str
    page_number: int
    bounding_box: tuple[float, float, float, float] | None = None
    caption: str = ""
    description: str = ""
    image_bytes: bytes | None = None
    image_url: str = ""
    embedding: list[float] | None = None


@dataclasses.dataclass
class Page:
    page_number: int
    text: str
    figures: list[Figure] = dataclasses.field(default_factory=list)


@dataclasses.dataclass
class Chunk:
    id: str
    content: str
    source_file: str
    source_page: int | None = None
    source_timestamp_seconds: float | None = None
    storage_url: str = ""
    embedding: list[float] | None = None
    images: list[dict[str, Any]] = dataclasses.field(default_factory=list)
    category: str | None = None
    acls: list[str] = dataclasses.field(default_factory=list)

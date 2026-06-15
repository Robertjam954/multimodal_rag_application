"""Parser that fetches a YouTube transcript and emits one Page per segment.

Filename convention: `youtube://<video_id>`. The bytes parameter is unused by this
parser - the transcript comes from `youtube_transcript_api`. Each Page carries
the segment's start time in `Page.text`'s leading marker so downstream Chunk
records can compute a `source_timestamp_seconds` for deep-linking.
"""
from __future__ import annotations

import asyncio
import logging
import re
from typing import AsyncIterator

from prepdocslib.page import Page
from prepdocslib.parser import Parser

logger = logging.getLogger(__name__)

_YT_PREFIX = "youtube://"
_VIDEO_ID_RE = re.compile(r"^[A-Za-z0-9_-]{6,20}$")


def video_id_from_filename(filename: str) -> str:
    name = filename.strip()
    if name.startswith(_YT_PREFIX):
        name = name[len(_YT_PREFIX):]
    name = name.split("?")[0].split("&")[0]
    if not _VIDEO_ID_RE.match(name):
        raise ValueError(f"not a valid YouTube video id: {filename!r}")
    return name


class YouTubeTranscriptParser(Parser):
    """One Page per transcript segment. page_number is the segment index (1-based)."""

    def __init__(self, *, languages: tuple[str, ...] = ("en",), max_retries: int = 3) -> None:
        self.languages = languages
        self.max_retries = max_retries

    async def parse(self, content: bytes, filename: str) -> AsyncIterator[Page]:
        video_id = video_id_from_filename(filename)
        segments = await asyncio.to_thread(self._fetch, video_id)
        for idx, seg in enumerate(segments, start=1):
            start = float(seg.get("start", 0.0))
            duration = float(seg.get("duration", 0.0))
            # Prepend a timestamp marker so the splitter / search index can recover it.
            # `source_timestamp_seconds` is computed downstream when Chunks are built.
            marker = f"[t={start:.2f}s..{start + duration:.2f}s] "
            yield Page(page_number=idx, text=marker + str(seg.get("text", "")).strip())

    def _fetch(self, video_id: str) -> list[dict]:
        try:
            from youtube_transcript_api import YouTubeTranscriptApi
        except ImportError as exc:  # pragma: no cover
            raise RuntimeError(
                "youtube-transcript-api is not installed; add it to requirements.in"
            ) from exc

        last_err: Exception | None = None
        for attempt in range(self.max_retries):
            try:
                api = YouTubeTranscriptApi()
                fetched = api.fetch(video_id, languages=list(self.languages))
                return [
                    {"text": item.text, "start": item.start, "duration": item.duration}
                    for item in fetched
                ]
            except Exception as exc:  # noqa: BLE001
                last_err = exc
                logger.warning("YouTube transcript fetch %s attempt %d failed: %s", video_id, attempt + 1, exc)
        raise RuntimeError(f"failed to fetch transcript for {video_id} after {self.max_retries} attempts") from last_err

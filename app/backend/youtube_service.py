"""URL <-> video_id helpers and optional YouTube Data API metadata lookup.

The Data API call is gated on `YOUTUBE_API_KEY`; if unset, `fetch_metadata` returns
a stub built from the URL alone (still usable for ingestion - the transcript is
the actual payload).
"""
from __future__ import annotations

import logging
import os
import re
from dataclasses import dataclass
from urllib.parse import parse_qs, urlparse

logger = logging.getLogger(__name__)

_BARE_ID_RE = re.compile(r"^[A-Za-z0-9_-]{6,20}$")


@dataclass
class VideoMetadata:
    video_id: str
    video_url: str
    title: str
    description: str = ""
    channel_title: str = ""
    published_at: str = ""


def parse_video_id(url_or_id: str) -> str:
    """Accept a bare ID, a youtu.be short URL, or a youtube.com watch/embed URL."""
    s = url_or_id.strip()
    if _BARE_ID_RE.match(s):
        return s
    parsed = urlparse(s)
    host = (parsed.hostname or "").lower()
    if host.endswith("youtu.be"):
        return parsed.path.lstrip("/").split("/")[0]
    if "youtube.com" in host or "youtube-nocookie.com" in host:
        if parsed.path.startswith(("/embed/", "/v/", "/shorts/")):
            return parsed.path.split("/")[2]
        v = parse_qs(parsed.query).get("v")
        if v:
            return v[0]
    raise ValueError(f"could not parse YouTube video id from: {url_or_id!r}")


def video_url(video_id: str) -> str:
    return f"https://www.youtube.com/watch?v={video_id}"


async def fetch_metadata(video_id: str) -> VideoMetadata:
    """Optional Data API lookup. Falls back to a URL-only stub if no key is set."""
    api_key = os.getenv("YOUTUBE_API_KEY")
    if not api_key:
        return VideoMetadata(video_id=video_id, video_url=video_url(video_id), title=f"YouTube {video_id}")

    try:  # pragma: no cover - requires network + key
        import asyncio

        from googleapiclient.discovery import build  # type: ignore[import-untyped]

        def _call() -> VideoMetadata:
            client = build("youtube", "v3", developerKey=api_key, cache_discovery=False)
            response = client.videos().list(part="snippet", id=video_id).execute()
            items = response.get("items") or []
            if not items:
                return VideoMetadata(video_id=video_id, video_url=video_url(video_id), title=f"YouTube {video_id}")
            snippet = items[0]["snippet"]
            return VideoMetadata(
                video_id=video_id,
                video_url=video_url(video_id),
                title=snippet.get("title", f"YouTube {video_id}"),
                description=snippet.get("description", ""),
                channel_title=snippet.get("channelTitle", ""),
                published_at=snippet.get("publishedAt", ""),
            )

        return await asyncio.to_thread(_call)
    except Exception:
        logger.exception("YouTube Data API metadata lookup failed; returning stub")
        return VideoMetadata(video_id=video_id, video_url=video_url(video_id), title=f"YouTube {video_id}")

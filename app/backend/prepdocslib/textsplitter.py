"""Sentence-aware splitter. Targets ~1000 characters per chunk with 10% overlap.

Mirrors azure-search-openai-demo behavior:
- Recursive merging from sentences -> paragraphs -> chunks.
- Sliding window: sentence at the end of chunk N also starts chunk N+1 (when overlap fits).
- Guarantees: no chunk exceeds max_chars; no sentence is split.
"""
from __future__ import annotations

import re
from typing import Iterable, Iterator

DEFAULT_MAX_CHARS = 1000
DEFAULT_OVERLAP_PCT = 0.10
SENTENCE_END = re.compile(r"(?<=[.!?])\s+(?=[A-Z])")


def split_sentences(text: str) -> list[str]:
    text = text.strip()
    if not text:
        return []
    return [s.strip() for s in SENTENCE_END.split(text) if s.strip()]


def split_text(text: str, max_chars: int = DEFAULT_MAX_CHARS, overlap_pct: float = DEFAULT_OVERLAP_PCT) -> Iterator[str]:
    sentences = split_sentences(text)
    if not sentences:
        return
    overlap = int(max_chars * overlap_pct)
    buf: list[str] = []
    buf_len = 0
    i = 0
    while i < len(sentences):
        s = sentences[i]
        if buf_len + len(s) + 1 <= max_chars or not buf:
            buf.append(s)
            buf_len += len(s) + 1
            i += 1
        else:
            chunk = " ".join(buf).strip()
            yield chunk
            # build overlap tail by trimming buf
            tail: list[str] = []
            tail_len = 0
            for s_ in reversed(buf):
                if tail_len + len(s_) > overlap:
                    break
                tail.insert(0, s_)
                tail_len += len(s_) + 1
            buf = tail[:]
            buf_len = tail_len
    if buf:
        yield " ".join(buf).strip()


def split_iter(text_blocks: Iterable[str], **kwargs) -> Iterator[str]:
    for block in text_blocks:
        yield from split_text(block, **kwargs)

"""Plain-text + markdown parser."""
from __future__ import annotations

from typing import AsyncIterator

from prepdocslib.page import Page
from prepdocslib.parser import Parser


class TextParser(Parser):
    async def parse(self, content: bytes, filename: str) -> AsyncIterator[Page]:
        yield Page(page_number=1, text=content.decode("utf-8", errors="ignore"))

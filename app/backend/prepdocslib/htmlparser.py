"""HTML parser via BeautifulSoup."""
from __future__ import annotations

from typing import AsyncIterator

from prepdocslib.page import Page
from prepdocslib.parser import Parser


class HtmlParser(Parser):
    async def parse(self, content: bytes, filename: str) -> AsyncIterator[Page]:
        from bs4 import BeautifulSoup

        soup = BeautifulSoup(content.decode("utf-8", errors="ignore"), "html.parser")
        for s in soup(["script", "style"]):
            s.decompose()
        text = soup.get_text(separator="\n", strip=True)
        yield Page(page_number=1, text=text)

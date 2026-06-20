"""Parser for Microsoft Learn HTML pages.

Strips nav/breadcrumb/footer/feedback chrome and yields the article body
as a single Page. Title is taken from the first <h1>, used as the Page-1
header so retrieval surfaces it.
"""
from __future__ import annotations

from typing import AsyncIterator

from prepdocslib.page import Page
from prepdocslib.parser import Parser

_STRIP_SELECTORS = (
    "nav",
    "header",
    "footer",
    "aside",
    "script",
    "style",
    "noscript",
    "form",
    ".breadcrumb",
    ".feedback",
    ".feedback-vote",
    ".feedback-verbatim",
    ".page-metadata",
    ".disclaimer",
    ".alert",
    ".moniker-picker",
    ".lang-selector-container",
    ".header-holder",
    ".article-header",
    ".page-actions",
    ".article-metadata",
    "#user-feedback",
    "#article-header",
    "#ms--main-footer",
    "[data-bi-name='ratings']",
    "[data-bi-name='breadcrumbs']",
)


class LearnDocParser(Parser):
    async def parse(self, content: bytes, filename: str) -> AsyncIterator[Page]:
        from bs4 import BeautifulSoup

        soup = BeautifulSoup(content.decode("utf-8", errors="ignore"), "html.parser")

        for sel in _STRIP_SELECTORS:
            for el in soup.select(sel):
                el.decompose()

        article = soup.select_one("main#main") or soup.select_one("main") or soup.select_one("article") or soup
        title_el = article.find("h1")
        title = title_el.get_text(strip=True) if title_el else ""

        for code in article.select("pre code, pre"):
            code_text = code.get_text("\n", strip=False)
            code.replace_with(f"\n```\n{code_text}\n```\n")

        body = article.get_text(separator="\n", strip=True)
        text = f"# {title}\n\n{body}" if title else body
        yield Page(page_number=1, text=text)

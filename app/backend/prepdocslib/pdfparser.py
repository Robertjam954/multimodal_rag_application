"""PDF parser. Tries Azure Document Intelligence; falls back to PyPDF."""
from __future__ import annotations

import io
import logging
import os
from typing import AsyncIterator

from prepdocslib.page import Page
from prepdocslib.parser import Parser

logger = logging.getLogger(__name__)


class PdfParser(Parser):
    async def parse(self, content: bytes, filename: str) -> AsyncIterator[Page]:
        async for page in self._with_docintel(content, filename):
            yield page

    async def _with_docintel(self, content: bytes, filename: str) -> AsyncIterator[Page]:
        endpoint = os.getenv("AZURE_DOCUMENTINTELLIGENCE_ENDPOINT")
        if not endpoint:
            async for page in self._with_pypdf(content):
                yield page
            return
        try:
            from azure.ai.documentintelligence.aio import DocumentIntelligenceClient
            from azure.ai.documentintelligence.models import AnalyzeDocumentRequest
            from azure.core.credentials import AzureKeyCredential
        except Exception:
            logger.warning("docintel SDK missing; falling back to PyPDF")
            async for page in self._with_pypdf(content):
                yield page
            return

        key = os.getenv("AZURE_DOCUMENTINTELLIGENCE_KEY", "")
        client = DocumentIntelligenceClient(endpoint, AzureKeyCredential(key))
        poller = await client.begin_analyze_document(
            "prebuilt-layout",
            AnalyzeDocumentRequest(bytes_source=content),
        )
        result = await poller.result()
        for page in result.pages:
            text = " ".join((w.content or "") for w in (page.words or []))
            yield Page(page_number=page.page_number, text=text)

    async def _with_pypdf(self, content: bytes) -> AsyncIterator[Page]:
        try:
            from pypdf import PdfReader
        except Exception:
            logger.warning("pypdf missing; cannot parse PDF")
            return
        reader = PdfReader(io.BytesIO(content))
        for i, p in enumerate(reader.pages, start=1):
            yield Page(page_number=i, text=p.extract_text() or "")

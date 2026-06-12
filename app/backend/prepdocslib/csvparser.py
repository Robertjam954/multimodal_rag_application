"""CSV -> one row per chunk (joined as readable text)."""
from __future__ import annotations

import csv
import io
from typing import AsyncIterator

from prepdocslib.page import Page
from prepdocslib.parser import Parser


class CsvParser(Parser):
    async def parse(self, content: bytes, filename: str) -> AsyncIterator[Page]:
        reader = csv.reader(io.StringIO(content.decode("utf-8", errors="ignore")))
        rows = list(reader)
        if not rows:
            return
        header, *body = rows
        text = "\n".join(", ".join(f"{h}: {v}" for h, v in zip(header, row)) for row in body)
        yield Page(page_number=1, text=text)

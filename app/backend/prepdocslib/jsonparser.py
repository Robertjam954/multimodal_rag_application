"""JSON parser. Treats each top-level item as a chunk source."""
from __future__ import annotations

import json
from typing import AsyncIterator

from prepdocslib.page import Page
from prepdocslib.parser import Parser


class JsonParser(Parser):
    async def parse(self, content: bytes, filename: str) -> AsyncIterator[Page]:
        try:
            data = json.loads(content.decode("utf-8", errors="ignore"))
        except Exception:
            return
        if isinstance(data, list):
            for i, item in enumerate(data):
                yield Page(page_number=i + 1, text=json.dumps(item, ensure_ascii=False))
        else:
            yield Page(page_number=1, text=json.dumps(data, ensure_ascii=False))

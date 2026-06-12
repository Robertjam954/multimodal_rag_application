"""Base parser interface."""
from __future__ import annotations

import abc
from typing import AsyncIterator

from prepdocslib.page import Page


class Parser(abc.ABC):
    @abc.abstractmethod
    async def parse(self, content: bytes, filename: str) -> AsyncIterator[Page]: ...

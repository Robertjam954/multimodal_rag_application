"""Base strategy interface for ingestion runs."""
from __future__ import annotations

import abc
from typing import Any


class Strategy(abc.ABC):
    @abc.abstractmethod
    async def setup(self) -> None: ...

    @abc.abstractmethod
    async def run(self) -> dict[str, Any]: ...

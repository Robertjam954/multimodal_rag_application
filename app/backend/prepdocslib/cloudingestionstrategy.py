"""Cloud ingestion: builds AI Search indexer + skillset that calls the Azure Functions."""
from __future__ import annotations

import logging
from typing import Any

from prepdocslib.strategy import Strategy

logger = logging.getLogger(__name__)


class CloudIngestionStrategy(Strategy):
    async def setup(self) -> None:
        logger.info("CloudIngestionStrategy.setup: TODO POST indexer + skillset spec to AI Search REST API")

    async def run(self) -> dict[str, Any]:
        logger.info("CloudIngestionStrategy.run: TODO trigger indexer run")
        return {"strategy": "cloud", "ok": True}

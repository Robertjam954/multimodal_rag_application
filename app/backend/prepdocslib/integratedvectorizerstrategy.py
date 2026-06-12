"""Strategy that uses Azure AI Search built-in vectorizer (no local embedding pass)."""
from __future__ import annotations

import logging
from typing import Any

from prepdocslib.strategy import Strategy

logger = logging.getLogger(__name__)


class IntegratedVectorizerStrategy(Strategy):
    async def setup(self) -> None:
        logger.info("IntegratedVectorizerStrategy.setup: TODO wire AI Search vectorizer (see Bicep)")

    async def run(self) -> dict[str, Any]:
        logger.info("IntegratedVectorizerStrategy.run: TODO orchestrate indexer via SDK")
        return {"strategy": "integrated_vectorizer", "ok": True}

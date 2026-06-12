"""Constructs the Azure AI Search indexer + skillset used by cloud ingestion (Functions)."""
from __future__ import annotations

import asyncio
import json
import logging
import os
import sys

logger = logging.getLogger(__name__)

SKILLSET_TEMPLATE = {
    "name": "mmrag-skillset",
    "skills": [
        {
            "@odata.type": "#Microsoft.Skills.Custom.WebApiSkill",
            "name": "document_extractor",
            "uri": "${DOCUMENT_EXTRACTOR_URL}",
            "context": "/document",
            "inputs": [{"name": "blob_url", "source": "/document/metadata_storage_path"}],
            "outputs": [{"name": "markdown", "targetName": "markdown"}, {"name": "figures", "targetName": "figures"}],
        },
        {
            "@odata.type": "#Microsoft.Skills.Custom.WebApiSkill",
            "name": "figure_processor",
            "uri": "${FIGURE_PROCESSOR_URL}",
            "context": "/document/figures/*",
            "inputs": [{"name": "image_url", "source": "/document/figures/*/image_url"}],
            "outputs": [{"name": "description", "targetName": "description"}, {"name": "embedding", "targetName": "embedding"}],
        },
        {
            "@odata.type": "#Microsoft.Skills.Util.ShaperSkill",
            "name": "shaper",
            "context": "/document",
            "inputs": [{"name": "figures_enriched", "source": "/document/figures/*"}],
            "outputs": [{"name": "output", "targetName": "shaped"}],
        },
        {
            "@odata.type": "#Microsoft.Skills.Custom.WebApiSkill",
            "name": "text_processor",
            "uri": "${TEXT_PROCESSOR_URL}",
            "context": "/document",
            "inputs": [{"name": "markdown", "source": "/document/markdown"}, {"name": "shaped", "source": "/document/shaped"}],
            "outputs": [{"name": "chunks", "targetName": "chunks"}],
        },
    ],
}


async def main() -> int:
    logging.basicConfig(level=os.getenv("LOG_LEVEL", "INFO"))
    rendered = json.dumps(SKILLSET_TEMPLATE)
    for k in ("DOCUMENT_EXTRACTOR_URL", "FIGURE_PROCESSOR_URL", "TEXT_PROCESSOR_URL"):
        rendered = rendered.replace(f"${{{k}}}", os.getenv(k, ""))
    logger.info("Skillset rendered (POST this to AI Search):\n%s", rendered)
    return 0


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))

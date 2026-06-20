"""CLI entrypoint for local ingestion. Invoked by scripts/prepdocs.sh."""
from __future__ import annotations

import argparse
import asyncio
import logging
import os
import sys
from pathlib import Path
from typing import Any

from azure.identity.aio import AzureDeveloperCliCredential, DefaultAzureCredential

from prepdocslib.blobmanager import BlobManager
from prepdocslib.embeddings import TextEmbeddings
from prepdocslib.filestrategy import FileStrategy
from prepdocslib.learnstrategy import LearnStrategy
from prepdocslib.searchmanager import SearchManager

logger = logging.getLogger(__name__)


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser()
    p.add_argument("--source", choices=["files", "learn"], default="files")
    p.add_argument("--datadir", default=os.getenv("DATA_DIR", "data/papers"))
    p.add_argument("--learn-urls", default=os.getenv("LEARN_URLS", "data/learn/azure_ai_seed.txt"))
    p.add_argument("--learn-category", default=os.getenv("LEARN_CATEGORY", "learn-azure-ai"))
    p.add_argument("--learn-concurrency", type=int, default=int(os.getenv("LEARN_CONCURRENCY", "4")))
    p.add_argument("--category", default=None)
    p.add_argument("--removeall", action="store_true")
    p.add_argument("--remove", action="store_true")
    p.add_argument("--multimodal", action="store_true", default=os.getenv("USE_MULTIMODAL", "false").lower() == "true")
    return p.parse_args()


async def main() -> int:
    args = parse_args()
    logging.basicConfig(level=os.getenv("LOG_LEVEL", "INFO"))

    cred = AzureDeveloperCliCredential() if os.getenv("RUNNING_IN_PRODUCTION", "false").lower() != "true" else DefaultAzureCredential()
    blob = BlobManager(credential=cred, account=os.getenv("AZURE_STORAGE_ACCOUNT", ""), container=os.getenv("AZURE_STORAGE_CONTAINER", "content"))
    search = SearchManager(credential=cred)
    embeddings = TextEmbeddings()

    if args.removeall:
        await search.remove_all()
        logger.info("Removed search index")
        return 0

    if args.source == "learn":
        url_list = Path(args.learn_urls)
        if not url_list.exists():
            logger.error("learn url list not found: %s", url_list)
            return 2
        strat: Any = LearnStrategy(
            url_list=url_list,
            search=search,
            embeddings=embeddings,
            category=args.learn_category,
            concurrency=args.learn_concurrency,
        )
        await strat.setup()
        result = await strat.run()
        logger.info("prepdocs done (learn): %s", result)
        return 0

    data_dir = Path(args.datadir)
    if not data_dir.exists():
        logger.error("data dir not found: %s", data_dir)
        return 2

    strat = FileStrategy(
        data_dir=data_dir,
        blob_manager=blob,
        search=search,
        embeddings=embeddings,
        category=args.category,
        multimodal=args.multimodal,
    )
    await strat.setup()
    result = await strat.run()
    logger.info("prepdocs done: %s", result)
    return 0


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))

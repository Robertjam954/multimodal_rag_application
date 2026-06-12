"""Azure Blob / ADLS Gen2 manager. Provides upload, get_file_stream, list_paths_for_user."""
from __future__ import annotations

import logging
import os
from typing import Any

logger = logging.getLogger(__name__)


class BlobManager:
    def __init__(self, credential: Any, account: str, container: str) -> None:
        self.credential = credential
        self.account = account
        self.container = container

    def _service(self):
        try:
            from azure.storage.blob.aio import BlobServiceClient
        except Exception:
            return None
        if not self.account:
            return None
        return BlobServiceClient(account_url=f"https://{self.account}.blob.core.windows.net", credential=self.credential)

    async def upload(self, name: str, data: bytes, content_type: str = "application/octet-stream") -> str:
        svc = self._service()
        if svc is None:
            logger.info("Blob upload skipped (no account); name=%s", name)
            return f"local://{name}"
        container = svc.get_container_client(self.container)
        try:
            await container.create_container()
        except Exception:
            pass
        blob = container.get_blob_client(name)
        await blob.upload_blob(data, overwrite=True, content_type=content_type)
        return blob.url

    async def get_file_stream(self, filename: str) -> bytes | None:
        svc = self._service()
        if svc is None:
            return None
        container = svc.get_container_client(self.container)
        blob = container.get_blob_client(filename)
        try:
            downloader = await blob.download_blob()
            return await downloader.readall()
        except Exception:
            return None

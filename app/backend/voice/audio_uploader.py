"""Uploads finalized audio files to Blob with the same content-id used by the graph."""
from __future__ import annotations

import logging
from typing import Any

logger = logging.getLogger(__name__)


async def upload_audio(blob_manager: Any, recording_id: str, data: bytes, content_type: str = "audio/wav") -> str:
    """Returns the blob URL of the uploaded audio."""
    if blob_manager is None:
        return f"local://{recording_id}.wav"
    return await blob_manager.upload(name=f"recordings/{recording_id}.wav", data=data, content_type=content_type)

"""Generates text descriptions for figures using Azure OpenAI Vision."""
from __future__ import annotations

import base64
import logging
import os

logger = logging.getLogger(__name__)


async def describe(image_bytes: bytes, hint: str = "") -> str:
    if not (os.getenv("AZURE_OPENAI_SERVICE") or os.getenv("OPENAI_API_KEY")):
        return f"[no-vision] figure with hint: {hint}"
    from openai import AsyncAzureOpenAI, AsyncOpenAI

    if os.getenv("AZURE_OPENAI_SERVICE"):
        client = AsyncAzureOpenAI(
            azure_endpoint=f"https://{os.getenv('AZURE_OPENAI_SERVICE')}.openai.azure.com/",
            api_version=os.getenv("AZURE_OPENAI_API_VERSION", "2024-10-01-preview"),
            api_key=os.getenv("AZURE_OPENAI_API_KEY"),
        )
    else:
        client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    b64 = base64.b64encode(image_bytes).decode("ascii")
    resp = await client.chat.completions.create(
        model=os.getenv("AZURE_OPENAI_VISION_DEPLOYMENT", "gpt-4o-mini"),
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": f"Describe this figure in 1-2 sentences. {hint}".strip()},
                    {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{b64}"}},
                ],
            }
        ],
        temperature=0.2,
    )
    return resp.choices[0].message.content or ""

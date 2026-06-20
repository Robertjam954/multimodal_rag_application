"""Azure AI Speech **Voice Live API** bridge for live transcription (no RAG).

The browser cannot send the `api-key` header on a WebSocket handshake, so the
transcript flow is proxied server-side:

    browser  --(PCM16 binary frames)-->  /voice/stream  --(input_audio_buffer.append)-->  Voice Live

We run Voice Live in *transcription mode*: `create_response: false` so the model
never speaks, `modalities: ["text"]`, and Azure speech-to-text drives the
`conversation.item.input_audio_transcription.*` events that we relay back to the
browser as interim / final transcript JSON.

Protocol reference (events mirror the Azure OpenAI Realtime API):
https://learn.microsoft.com/azure/ai-services/speech-service/voice-live-how-to

Env:
- AZURE_VOICE_LIVE_ENDPOINT   e.g. https://<resource>.cognitiveservices.azure.com/
- AZURE_VOICE_LIVE_KEY        resource api-key
- AZURE_VOICE_LIVE_MODEL      deployed model driving the session (default gpt-4.1)
- AZURE_VOICE_LIVE_LANGUAGE   input language hint (default en)
"""
from __future__ import annotations

import asyncio
import base64
import json
import logging
import os
from typing import Any

logger = logging.getLogger(__name__)

API_VERSION = "2026-04-10"
# 24 kHz mono PCM16 is the Voice Live default and what the browser worklet emits.
SAMPLE_RATE = 24000


def is_configured() -> bool:
    return bool(os.getenv("AZURE_VOICE_LIVE_ENDPOINT") and os.getenv("AZURE_VOICE_LIVE_KEY"))


def _ws_url() -> str:
    endpoint = os.environ["AZURE_VOICE_LIVE_ENDPOINT"].rstrip("/")
    base = endpoint.replace("https://", "wss://", 1).replace("http://", "ws://", 1)
    model = os.getenv("AZURE_VOICE_LIVE_MODEL", "gpt-4.1")
    return f"{base}/voice-live/realtime?api-version={API_VERSION}&model={model}"


def _session_update() -> dict[str, Any]:
    """Transcription-only session: model stays silent, Azure STT emits transcripts."""
    return {
        "type": "session.update",
        "session": {
            "modalities": ["text"],
            "input_audio_format": "pcm16",
            "input_audio_sampling_rate": SAMPLE_RATE,
            "input_audio_transcription": {
                "model": "azure-speech",
                "language": os.getenv("AZURE_VOICE_LIVE_LANGUAGE", "en"),
            },
            "turn_detection": {
                "type": "azure_semantic_vad",
                "silence_duration_ms": 500,
                "create_response": False,
                "interrupt_response": False,
            },
        },
    }


def _relay_event(raw: str) -> dict[str, Any] | None:
    """Map a Voice Live server event to a browser-facing transcript message."""
    try:
        evt = json.loads(raw)
    except (ValueError, TypeError):
        return None
    etype = evt.get("type", "")
    if etype == "conversation.item.input_audio_transcription.delta":
        text = evt.get("delta", "")
        return {"type": "interim", "text": text} if text else None
    if etype == "conversation.item.input_audio_transcription.completed":
        return {"type": "final", "text": evt.get("transcript", "")}
    if etype == "error":
        err = evt.get("error", {})
        msg = err.get("message") if isinstance(err, dict) else str(err)
        logger.warning("Voice Live error event: %s", msg)
        return {"type": "error", "message": msg or "voice live error"}
    return None


async def run_bridge(client_ws: Any) -> None:
    """Pump audio from `client_ws` to Voice Live and transcripts back. Returns on disconnect."""
    if not is_configured():
        await client_ws.send(json.dumps({"type": "error", "message": "Voice Live is not configured"}))
        return

    import aiohttp

    headers = {"api-key": os.environ["AZURE_VOICE_LIVE_KEY"]}
    url = _ws_url()
    try:
        async with aiohttp.ClientSession() as session:
            async with session.ws_connect(url, headers=headers, heartbeat=30) as target:
                await target.send_str(json.dumps(_session_update()))

                async def client_to_voice() -> None:
                    while True:
                        data = await client_ws.receive()
                        if isinstance(data, (bytes, bytearray)):
                            b64 = base64.b64encode(bytes(data)).decode("ascii")
                            await target.send_str(json.dumps({"type": "input_audio_buffer.append", "audio": b64}))
                        elif isinstance(data, str):
                            # Control frames from the browser, e.g. {"type":"stop"}.
                            try:
                                if json.loads(data).get("type") == "stop":
                                    break
                            except (ValueError, TypeError):
                                pass

                async def voice_to_client() -> None:
                    async for msg in target:
                        if msg.type == aiohttp.WSMsgType.TEXT:
                            out = _relay_event(msg.data)
                            if out is not None:
                                await client_ws.send(json.dumps(out))
                        elif msg.type in (aiohttp.WSMsgType.CLOSE, aiohttp.WSMsgType.ERROR):
                            break

                tasks = [asyncio.create_task(client_to_voice()), asyncio.create_task(voice_to_client())]
                try:
                    await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)
                finally:
                    for t in tasks:
                        t.cancel()
                    await asyncio.gather(*tasks, return_exceptions=True)
    except asyncio.CancelledError:
        raise
    except Exception as e:  # noqa: BLE001 - surface any connect/transport failure to the client
        logger.exception("Voice Live bridge failed")
        try:
            await client_ws.send(json.dumps({"type": "error", "message": f"voice live bridge: {e}"}))
        except Exception:  # noqa: BLE001 - client already gone
            pass

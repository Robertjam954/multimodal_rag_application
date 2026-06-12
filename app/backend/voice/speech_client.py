"""Azure Speech-to-Text streaming client. Falls back to faster-whisper in MODE=local."""
from __future__ import annotations

import logging
import os
from typing import Any, AsyncIterator

logger = logging.getLogger(__name__)


class TranscriptEvent(dict):
    """Carries partial/final transcript events for SSE/WS."""


async def transcribe_stream(audio_chunks: AsyncIterator[bytes]) -> AsyncIterator[TranscriptEvent]:
    if os.getenv("MODE", "azure").lower() == "local":
        async for ev in _local_whisper(audio_chunks):
            yield ev
        return
    async for ev in _azure_speech(audio_chunks):
        yield ev


async def _azure_speech(audio_chunks: AsyncIterator[bytes]) -> AsyncIterator[TranscriptEvent]:
    """Streaming long-form transcription using Azure Cognitive Services Speech SDK.

    Simplified: collects all audio then sends to recognizer (replace with push-stream API in prod).
    """
    try:
        import azure.cognitiveservices.speech as speechsdk
    except Exception:
        logger.warning("azure speech sdk missing; emitting stub")
        yield TranscriptEvent(kind="final", utterance_id="u-stub", speaker="Speaker 1", start=0.0, end=1.0, text="stub transcript")
        return

    key = os.getenv("AZURE_SPEECH_KEY")
    region = os.getenv("AZURE_SPEECH_SERVICE_LOCATION")
    if not (key and region):
        yield TranscriptEvent(kind="final", utterance_id="u-stub", speaker="Speaker 1", start=0.0, end=1.0, text="stub transcript")
        return

    speech_config = speechsdk.SpeechConfig(subscription=key, region=region)
    speech_config.set_property(speechsdk.PropertyId.SpeechServiceConnection_LanguageIdMode, "Continuous")

    push_stream = speechsdk.audio.PushAudioInputStream()
    audio_config = speechsdk.audio.AudioConfig(stream=push_stream)
    transcriber = speechsdk.transcription.ConversationTranscriber(speech_config=speech_config, audio_config=audio_config)

    transcripts: list[TranscriptEvent] = []

    def _on_final(evt):
        transcripts.append(
            TranscriptEvent(
                kind="final",
                utterance_id=evt.result.result_id,
                speaker=getattr(evt.result, "speaker_id", "Unknown"),
                start=evt.result.offset / 10_000_000,
                end=(evt.result.offset + evt.result.duration) / 10_000_000,
                text=evt.result.text,
            )
        )

    transcriber.transcribed.connect(_on_final)
    transcriber.start_transcribing_async().get()
    async for chunk in audio_chunks:
        push_stream.write(chunk)
    push_stream.close()
    transcriber.stop_transcribing_async().get()

    for t in transcripts:
        yield t


async def _local_whisper(audio_chunks: AsyncIterator[bytes]) -> AsyncIterator[TranscriptEvent]:
    try:
        from faster_whisper import WhisperModel
    except Exception:
        yield TranscriptEvent(kind="final", utterance_id="u-stub", speaker="Speaker 1", start=0.0, end=1.0, text="local whisper missing")
        return
    import io
    import tempfile

    buf = io.BytesIO()
    async for chunk in audio_chunks:
        buf.write(chunk)
    buf.seek(0)
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
        tmp.write(buf.read())
        tmp.flush()
        model = WhisperModel(os.getenv("WHISPER_MODEL", "base.en"), device="cpu")
        segments, _ = model.transcribe(tmp.name, beam_size=1)
        for i, seg in enumerate(segments):
            yield TranscriptEvent(
                kind="final",
                utterance_id=f"u-{i}",
                speaker="Speaker 1",
                start=seg.start,
                end=seg.end,
                text=seg.text.strip(),
            )

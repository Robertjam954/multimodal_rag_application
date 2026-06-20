import { useEffect, useRef, useState } from "react";
import { Button } from "@fluentui/react-components";

// AudioWorklet that converts the mic's Float32 frames to 16-bit PCM and posts the
// raw bytes back to the main thread, which forwards them over the WebSocket.
const PCM_WORKLET = `
class PCMProcessor extends AudioWorkletProcessor {
  process(inputs) {
    const input = inputs[0];
    if (input && input[0]) {
      const ch = input[0];
      const buf = new Int16Array(ch.length);
      for (let i = 0; i < ch.length; i++) {
        const s = Math.max(-1, Math.min(1, ch[i]));
        buf[i] = s < 0 ? s * 0x8000 : s * 0x7fff;
      }
      this.port.postMessage(buf.buffer, [buf.buffer]);
    }
    return true;
  }
}
registerProcessor("pcm-processor", PCMProcessor);
`;

const SAMPLE_RATE = 24000;

export default function VoiceRecorder({ onTranscript }: { onTranscript: (text: string) => void }) {
    const [recording, setRecording] = useState(false);
    const [finalText, setFinalText] = useState("");
    const [interim, setInterim] = useState("");
    const [cleaned, setCleaned] = useState("");
    const [cleaning, setCleaning] = useState(false);
    const [error, setError] = useState("");

    const wsRef = useRef<WebSocket | null>(null);
    const ctxRef = useRef<AudioContext | null>(null);
    const streamRef = useRef<MediaStream | null>(null);
    const finalRef = useRef(""); // mirror of finalText for the stop handler

    useEffect(() => () => teardown(), []);

    function teardown() {
        try {
            ctxRef.current?.close();
        } catch {
            /* already closed */
        }
        streamRef.current?.getTracks().forEach(t => t.stop());
        wsRef.current?.close();
        ctxRef.current = null;
        streamRef.current = null;
        wsRef.current = null;
    }

    async function start() {
        setError("");
        setCleaned("");
        setFinalText("");
        setInterim("");
        finalRef.current = "";

        const stream = await navigator.mediaDevices.getUserMedia({ audio: { channelCount: 1, echoCancellation: true, noiseSuppression: true } });
        streamRef.current = stream;

        const ws = new WebSocket((location.protocol === "https:" ? "wss" : "ws") + "://" + location.host + "/voice/stream");
        ws.binaryType = "arraybuffer";
        wsRef.current = ws;
        ws.onmessage = ev => {
            let msg: { type: string; text?: string; message?: string };
            try {
                msg = JSON.parse(ev.data);
            } catch {
                return;
            }
            if (msg.type === "interim") {
                setInterim(msg.text ?? "");
            } else if (msg.type === "final") {
                setInterim("");
                const next = (finalRef.current + " " + (msg.text ?? "")).trim();
                finalRef.current = next;
                setFinalText(next);
                onTranscript(next);
            } else if (msg.type === "error") {
                setError(msg.message ?? "voice error");
            }
        };

        const ctx = new AudioContext({ sampleRate: SAMPLE_RATE });
        ctxRef.current = ctx;
        const blobUrl = URL.createObjectURL(new Blob([PCM_WORKLET], { type: "application/javascript" }));
        await ctx.audioWorklet.addModule(blobUrl);
        URL.revokeObjectURL(blobUrl);

        const source = ctx.createMediaStreamSource(stream);
        const node = new AudioWorkletNode(ctx, "pcm-processor");
        node.port.onmessage = e => {
            if (ws.readyState === WebSocket.OPEN) ws.send(e.data as ArrayBuffer);
        };
        source.connect(node);
        // Keep the graph alive without audible output.
        node.connect(ctx.destination);

        setRecording(true);
    }

    async function stop() {
        setRecording(false);
        try {
            wsRef.current?.send(JSON.stringify({ type: "stop" }));
        } catch {
            /* socket already closed */
        }
        teardown();

        const raw = finalRef.current.trim();
        if (!raw) return;
        setCleaning(true);
        try {
            const resp = await fetch("/voice/clean", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ text: raw })
            });
            if (resp.ok) {
                const data = await resp.json();
                setCleaned(data.cleaned ?? raw);
            } else {
                setCleaned(raw); // graceful fallback: cleaning unavailable
            }
        } catch {
            setCleaned(raw);
        } finally {
            setCleaning(false);
        }
    }

    const display = cleaned || (finalText + (interim ? " " + interim : "")).trim();

    async function copy() {
        try {
            await navigator.clipboard.writeText(display);
        } catch {
            setError("copy failed - clipboard not available");
        }
    }

    return (
        <div>
            <div style={{ display: "flex", gap: 8 }}>
                <Button appearance={recording ? "primary" : "outline"} onClick={recording ? stop : start} disabled={cleaning}>
                    {recording ? "Stop" : "Record"}
                </Button>
                <Button onClick={copy} disabled={!display}>
                    Copy
                </Button>
            </div>
            {error && <p style={{ color: "#b00", marginTop: 8 }}>{error}</p>}
            {cleaning && <p style={{ marginTop: 8 }}>Cleaning transcript...</p>}
            <div style={{ marginTop: 12, whiteSpace: "pre-wrap", minHeight: 48 }}>
                {finalText}
                {interim && <span style={{ opacity: 0.5 }}> {interim}</span>}
            </div>
            {cleaned && (
                <div style={{ marginTop: 12 }}>
                    <strong>Cleaned</strong>
                    <div style={{ whiteSpace: "pre-wrap", marginTop: 4 }}>{cleaned}</div>
                </div>
            )}
        </div>
    );
}

import { useEffect, useRef, useState } from "react";
import { Button } from "@fluentui/react-components";

interface Utterance {
    speaker: string;
    start: number;
    end: number;
    text: string;
    final?: boolean;
}

export default function VoiceRecorder({ onTranscript }: { onTranscript: (u: Utterance[]) => void }) {
    const [recording, setRecording] = useState(false);
    const [utterances, setUtterances] = useState<Utterance[]>([]);
    const wsRef = useRef<WebSocket | null>(null);
    const recRef = useRef<MediaRecorder | null>(null);

    useEffect(() => () => stop(), []);

    async function start() {
        const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
        const ws = new WebSocket((location.protocol === "https:" ? "wss" : "ws") + "://" + location.host + "/voice/stream");
        wsRef.current = ws;
        ws.binaryType = "arraybuffer";
        ws.onmessage = (ev) => {
            try {
                const u: Utterance = JSON.parse(ev.data);
                setUtterances((prev) => {
                    const next = [...prev, u];
                    onTranscript(next);
                    return next;
                });
            } catch {
                // ignore non-JSON keepalives
            }
        };
        const rec = new MediaRecorder(stream, { mimeType: "audio/webm;codecs=opus" });
        recRef.current = rec;
        rec.ondataavailable = (e) => {
            if (e.data.size > 0 && ws.readyState === 1) {
                e.data.arrayBuffer().then((b) => ws.send(b));
            }
        };
        rec.start(250);
        setRecording(true);
    }

    function stop() {
        recRef.current?.stop();
        wsRef.current?.close();
        setRecording(false);
    }

    return (
        <div>
            <Button appearance={recording ? "primary" : "outline"} onClick={recording ? stop : start}>
                {recording ? "Stop" : "Record"}
            </Button>
            <ul style={{ marginTop: 12 }}>
                {utterances.map((u, i) => (
                    <li key={i}>
                        <strong>{u.speaker}</strong> [{u.start.toFixed(1)}s]: {u.text}
                    </li>
                ))}
            </ul>
        </div>
    );
}

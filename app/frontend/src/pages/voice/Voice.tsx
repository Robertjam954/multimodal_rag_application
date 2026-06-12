import { useState } from "react";
import VoiceRecorder from "../../components/VoiceRecorder/VoiceRecorder";

interface Utt {
    speaker: string;
    start: number;
    end: number;
    text: string;
}

export default function Voice() {
    const [items, setItems] = useState<Utt[]>([]);
    return (
        <div>
            <h2>Voice transcription</h2>
            <p>Record audio - it's transcribed live, indexed into the same graph and vector store as PDFs, and queryable from the Chat tab.</p>
            <VoiceRecorder onTranscript={setItems} />
            <pre style={{ marginTop: 12, fontSize: 12 }}>{JSON.stringify(items.slice(-5), null, 2)}</pre>
        </div>
    );
}

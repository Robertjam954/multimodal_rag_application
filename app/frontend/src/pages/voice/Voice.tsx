import { useState } from "react";
import VoiceRecorder from "../../components/VoiceRecorder/VoiceRecorder";

export default function Voice() {
    const [, setText] = useState("");
    return (
        <div>
            <h2>Voice transcriber</h2>
            <p>Record audio - it's transcribed live with Azure Speech, then cleaned up by an LLM (filler words removed, errors fixed). Use Copy to grab the result.</p>
            <VoiceRecorder onTranscript={setText} />
        </div>
    );
}

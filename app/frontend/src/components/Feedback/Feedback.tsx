import { useState } from "react";
import { Button, Textarea } from "@fluentui/react-components";
import { sendFeedback } from "../../api/api";

export default function Feedback({ trace_id }: { trace_id?: string }) {
    const [vote, setVote] = useState<1 | -1 | null>(null);
    const [text, setText] = useState("");
    const [sent, setSent] = useState(false);

    async function submit() {
        await sendFeedback({ trace_id, vote, text, ts: Date.now() });
        setSent(true);
    }

    if (sent) return <em>Thanks for the feedback.</em>;
    return (
        <div style={{ display: "flex", flexDirection: "column", gap: 4, marginTop: 12 }}>
            <div style={{ display: "flex", gap: 6 }}>
                <Button appearance={vote === 1 ? "primary" : "outline"} onClick={() => setVote(1)}>
                    Up
                </Button>
                <Button appearance={vote === -1 ? "primary" : "outline"} onClick={() => setVote(-1)}>
                    Down
                </Button>
            </div>
            <Textarea placeholder="optional notes" value={text} onChange={(_, d) => setText(d.value)} />
            <Button onClick={submit} disabled={vote === null}>
                Submit
            </Button>
        </div>
    );
}

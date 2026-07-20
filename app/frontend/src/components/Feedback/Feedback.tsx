import { useState } from "react";
import { sendFeedback } from "../../api/api";

export default function Feedback({ trace_id }: { trace_id?: string }) {
    const [vote, setVote] = useState<1 | -1 | null>(null);
    const [text, setText] = useState("");
    const [sent, setSent] = useState(false);
    const [open, setOpen] = useState(false);

    function pick(v: 1 | -1) {
        setVote(v);
        setOpen(true);
    }

    async function submit() {
        await sendFeedback({ trace_id, vote, text, ts: Date.now() });
        setSent(true);
    }

    if (sent)
        return (
            <div style={{ marginTop: 14, fontSize: 13, color: "var(--muted)" }}>Thanks - your feedback helps improve answers.</div>
        );
    return (
        <div style={{ marginTop: 14, display: "flex", flexDirection: "column", gap: 8 }}>
            <div style={{ display: "flex", gap: 8, alignItems: "center" }}>
                <span style={{ fontSize: 13, color: "var(--muted)" }}>Was this helpful?</span>
                <button className={`btn-ghost${vote === 1 ? " selected" : ""}`} onClick={() => pick(1)} aria-label="Helpful">
                    👍
                </button>
                <button className={`btn-ghost${vote === -1 ? " selected" : ""}`} onClick={() => pick(-1)} aria-label="Not helpful">
                    👎
                </button>
            </div>
            {open ? (
                <div style={{ display: "flex", gap: 8 }}>
                    <input
                        style={{
                            flex: 1,
                            border: "1.5px solid var(--border)",
                            borderRadius: 10,
                            padding: "8px 12px",
                            background: "var(--bg)",
                            color: "var(--text)",
                            fontFamily: "var(--font-body)",
                            fontSize: 13.5,
                            outline: "none",
                        }}
                        placeholder="Optional: tell us more"
                        value={text}
                        onChange={(e) => setText(e.target.value)}
                    />
                    <button className="btn-primary" style={{ padding: "8px 16px" }} onClick={submit} disabled={vote === null}>
                        Send
                    </button>
                </div>
            ) : null}
        </div>
    );
}

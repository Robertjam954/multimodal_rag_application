import { useEffect, useRef, useState } from "react";
import { streamChat } from "../../api/stream";
import type { ChatAppRequestOverrides, ChatMessage, Citation, Claim } from "../../api/models";
import Answer from "../../components/Answer/Answer";
import Citations from "../../components/Citations/Citations";
import VerifierBadge from "../../components/VerifierBadge/VerifierBadge";
import FollowUps from "../../components/FollowUps/FollowUps";
import Settings from "../../components/Settings/Settings";
import ThoughtProcess from "../../components/ThoughtProcess/ThoughtProcess";
import SupportingContent from "../../components/SupportingContent/SupportingContent";
import GraphView from "../../components/GraphView/GraphView";
import Feedback from "../../components/Feedback/Feedback";
import { formatUSD } from "../../lib/cost";

const SAMPLES = [
    "What is transfer learning?",
    "How does fine-tuning differ from feature extraction?",
    "Summarize the key ideas in the indexed papers",
    "What skills does the AZ-204 exam measure?",
];

const TABS = ["Answer", "Thought process", "Supporting content", "Knowledge graph"] as const;
type TabName = (typeof TABS)[number];

export default function Chat() {
    const [input, setInput] = useState("");
    const [history, setHistory] = useState<ChatMessage[]>([]);
    const [answer, setAnswer] = useState("");
    const [claims, setClaims] = useState<Claim[]>([]);
    const [citations, setCitations] = useState<Citation[]>([]);
    const [verdict, setVerdict] = useState<{ unsupported_claims: number; retried: boolean } | null>(null);
    const [followups, setFollowups] = useState<string[]>([]);
    const [route, setRoute] = useState<string>("");
    const [cost, setCost] = useState<{ est_usd?: number } | null>(null);
    const [busy, setBusy] = useState(false);
    const [tab, setTab] = useState<TabName>("Answer");
    const [overrides, setOverrides] = useState<ChatAppRequestOverrides>({
        top: 5,
        use_verifier: true,
        use_graphrag: true,
        graph_hops: 2,
        reasoning_effort: "minimal",
        use_streaming: true,
    });
    const scrollRef = useRef<HTMLDivElement>(null);

    useEffect(() => {
        scrollRef.current?.scrollTo({ top: scrollRef.current.scrollHeight, behavior: "smooth" });
    }, [history, answer]);

    async function send(question?: string) {
        const q = (question ?? input).trim();
        if (!q || busy) return;
        const newHistory: ChatMessage[] = [...history, { role: "user", content: q }];
        setHistory(newHistory);
        setInput("");
        setAnswer("");
        setClaims([]);
        setCitations([]);
        setVerdict(null);
        setFollowups([]);
        setRoute("");
        setCost(null);
        setBusy(true);

        let acc = "";
        try {
            await streamChat({ messages: newHistory, context: { overrides }, stream: true }, (evt) => {
                switch (evt.event) {
                    case "route":
                        setRoute(String(evt.data));
                        break;
                    case "token":
                        acc += String(evt.data ?? "");
                        setAnswer(acc);
                        break;
                    case "citation":
                        setCitations((c) => [...c, evt.data as Citation]);
                        break;
                    case "claim":
                        setClaims((c) => [...c, evt.data as Claim]);
                        break;
                    case "verdict":
                        setVerdict(evt.data as { unsupported_claims: number; retried: boolean });
                        break;
                    case "followups":
                        setFollowups(evt.data as string[]);
                        break;
                    case "cost":
                        setCost(evt.data as { est_usd?: number });
                        break;
                }
            });
        } finally {
            setBusy(false);
            setHistory((h) => [...h, { role: "assistant", content: acc }]);
        }
    }

    // The latest assistant answer renders as the rich bubble (tabs, citations),
    // so drop it from the plain-bubble transcript to avoid showing it twice.
    const display = history.filter((m, i) => !(answer && i === history.length - 1 && m.role === "assistant"));
    const hasConversation = history.length > 0 || busy;

    return (
        <div className="page chat-layout">
            <aside className="card card-pad">
                <h3 className="section-title">Retrieval settings</h3>
                <Settings overrides={overrides} onChange={setOverrides} />
            </aside>

            <section className="card chat-panel">
                <div ref={scrollRef} className="transcript">
                    {!hasConversation ? (
                        <div className="empty-hero">
                            <h1>
                                What do you want to <span className="hl">learn</span> today?
                            </h1>
                            <p>
                                Ask about the indexed papers - answers are retrieved from a vector store, cited to the
                                page, and checked claim-by-claim by a verifier agent.
                            </p>
                            <div className="samples">
                                {SAMPLES.map((s) => (
                                    <button key={s} className="chip" onClick={() => send(s)}>
                                        {s}
                                    </button>
                                ))}
                            </div>
                        </div>
                    ) : (
                        <>
                            {display.map((m, i) =>
                                m.role === "user" ? (
                                    <div key={i} className="bubble-row user">
                                        <div className="bubble user">{m.content}</div>
                                    </div>
                                ) : (
                                    <div key={i} className="bubble-row">
                                        <div className="bubble assistant">
                                            <p style={{ whiteSpace: "pre-wrap", margin: 0 }}>{m.content}</p>
                                        </div>
                                    </div>
                                )
                            )}
                            {(answer || busy) && (
                                <div className="bubble-row">
                                    <div className="bubble assistant">
                                        <div style={{ display: "flex", flexWrap: "wrap", gap: 8, marginBottom: answer ? 10 : 0 }}>
                                            <VerifierBadge verdict={verdict} />
                                            {route ? <span className="pill info">route: {route}</span> : null}
                                            {cost?.est_usd != null ? <span className="pill info">est {formatUSD(cost.est_usd)}</span> : null}
                                        </div>
                                        {!answer && busy ? (
                                            <div className="typing">
                                                <span />
                                                <span />
                                                <span />
                                            </div>
                                        ) : (
                                            <>
                                                <div className="seg" style={{ marginBottom: 12 }}>
                                                    {TABS.map((t) => (
                                                        <button key={t} className={tab === t ? "active" : ""} onClick={() => setTab(t)}>
                                                            {t}
                                                        </button>
                                                    ))}
                                                </div>
                                                {tab === "Answer" && (
                                                    <>
                                                        <Answer text={answer} claims={claims} />
                                                        <Citations citations={citations} />
                                                        <FollowUps items={followups} onPick={(q) => send(q)} />
                                                        {!busy && <Feedback />}
                                                    </>
                                                )}
                                                {tab === "Thought process" && (
                                                    <ThoughtProcess
                                                        steps={[
                                                            { title: "route", description: route || "default" },
                                                            { title: "retrieval", description: `${citations.length} chunks retrieved` },
                                                            {
                                                                title: "verifier",
                                                                description: verdict
                                                                    ? `${verdict.unsupported_claims} unsupported claims`
                                                                    : "not run",
                                                            },
                                                        ]}
                                                    />
                                                )}
                                                {tab === "Supporting content" && <SupportingContent citations={citations} />}
                                                {tab === "Knowledge graph" && <GraphView data={{ nodes: [], edges: [] }} />}
                                            </>
                                        )}
                                    </div>
                                </div>
                            )}
                        </>
                    )}
                </div>

                <div className="composer">
                    <textarea
                        value={input}
                        rows={1}
                        onChange={(e) => setInput(e.target.value)}
                        placeholder="Ask anything about the indexed documents..."
                        onKeyDown={(e) => {
                            if (e.key === "Enter" && !e.shiftKey) {
                                e.preventDefault();
                                send();
                            }
                        }}
                    />
                    <button className="btn-primary" disabled={busy || !input.trim()} onClick={() => send()}>
                        {busy ? "Thinking..." : "Ask"}
                    </button>
                </div>
            </section>
        </div>
    );
}

import { useState } from "react";
import { Button, Textarea, Tab, TabList, TabValue, SelectTabData, SelectTabEvent } from "@fluentui/react-components";
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
    const [tab, setTab] = useState<TabValue>("answer");
    const [overrides, setOverrides] = useState<ChatAppRequestOverrides>({
        top: 5,
        use_verifier: true,
        use_graphrag: true,
        graph_hops: 2,
        reasoning_effort: "minimal",
        use_streaming: true,
    });

    async function send() {
        const q = input.trim();
        if (!q) return;
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

        try {
            await streamChat({ messages: newHistory, context: { overrides }, stream: true }, (evt) => {
                switch (evt.event) {
                    case "route":
                        setRoute(String(evt.data));
                        break;
                    case "token":
                        setAnswer((a) => a + String(evt.data ?? ""));
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
            setHistory((h) => [...h, { role: "assistant", content: answer }]);
        }
    }

    return (
        <div style={{ display: "grid", gridTemplateColumns: "260px 1fr", gap: 16 }}>
            <aside>
                <Settings overrides={overrides} onChange={setOverrides} />
            </aside>
            <section>
                <div style={{ display: "flex", gap: 8, marginBottom: 12 }}>
                    <VerifierBadge verdict={verdict} />
                    {route ? <span style={{ fontSize: 12, opacity: 0.7 }}>route: {route}</span> : null}
                    {cost?.est_usd != null ? <span style={{ fontSize: 12, opacity: 0.7 }}>est: {formatUSD(cost.est_usd)}</span> : null}
                </div>
                <TabList selectedValue={tab} onTabSelect={(_: SelectTabEvent, d: SelectTabData) => setTab(d.value)}>
                    <Tab value="answer">Answer</Tab>
                    <Tab value="thought">Thought process</Tab>
                    <Tab value="support">Supporting content</Tab>
                    <Tab value="graph">Knowledge graph</Tab>
                </TabList>
                <div style={{ marginTop: 12 }}>
                    {tab === "answer" && (
                        <>
                            <Answer text={answer} claims={claims} />
                            <Citations citations={citations} />
                            <FollowUps items={followups} onPick={setInput} />
                            <Feedback />
                        </>
                    )}
                    {tab === "thought" && (
                        <ThoughtProcess
                            steps={[
                                { title: "route", description: route },
                                { title: "retrieval", description: `${citations.length} chunks` },
                                { title: "verifier", description: verdict ? `${verdict.unsupported_claims} unsupported` : "n/a" },
                            ]}
                        />
                    )}
                    {tab === "support" && <SupportingContent citations={citations} />}
                    {tab === "graph" && <GraphView data={{ nodes: [], edges: [] }} />}
                </div>
                <div style={{ marginTop: 16, display: "flex", gap: 8 }}>
                    <Textarea
                        value={input}
                        onChange={(_, d) => setInput(d.value)}
                        placeholder="Ask about the indexed PDFs and recordings..."
                        style={{ flex: 1 }}
                        onKeyDown={(e) => {
                            if (e.key === "Enter" && !e.shiftKey) {
                                e.preventDefault();
                                send();
                            }
                        }}
                    />
                    <Button appearance="primary" disabled={busy} onClick={send}>
                        Send
                    </Button>
                </div>
            </section>
        </div>
    );
}

import type { AppConfig, ChatRequest, ChatResponse, SqlBundle } from "./models";

const BASE = "";

export async function getConfig(): Promise<AppConfig> {
    const r = await fetch(`${BASE}/config`);
    return r.json();
}

export async function chatNonstream(req: ChatRequest): Promise<ChatResponse> {
    const r = await fetch(`${BASE}/chat/nonstream`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(req),
    });
    if (!r.ok) throw new Error(`chat ${r.status}`);
    return r.json();
}

export async function sqlPlan(change_request: string): Promise<SqlBundle> {
    const r = await fetch(`${BASE}/sql/plan`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ change_request }),
    });
    return r.json();
}

export async function uploadPaper(file: File): Promise<{ uploaded: { filename: string; url: string; chunks: number }[] }> {
    const fd = new FormData();
    fd.append("file", file);
    const r = await fetch(`${BASE}/papers/upload`, { method: "POST", body: fd });
    return r.json();
}

export async function sendFeedback(payload: Record<string, unknown>): Promise<void> {
    await fetch(`${BASE}/feedback`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
    });
}

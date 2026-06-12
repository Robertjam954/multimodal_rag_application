import { fetchEventSource } from "@microsoft/fetch-event-source";
import type { ChatRequest } from "./models";

export type StreamEvent = {
    event: "token" | "citation" | "claim" | "verdict" | "followups" | "cost" | "route" | "sql" | "blocked" | "done";
    data?: unknown;
};

export async function streamChat(req: ChatRequest, onEvent: (e: StreamEvent) => void, signal?: AbortSignal): Promise<void> {
    await fetchEventSource("/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json", Accept: "text/event-stream" },
        body: JSON.stringify(req),
        signal,
        onmessage(ev) {
            try {
                const parsed = JSON.parse(ev.data || "{}");
                onEvent(parsed as StreamEvent);
            } catch {
                onEvent({ event: "token", data: ev.data } as StreamEvent);
            }
        },
        onerror(err) {
            throw err;
        },
    });
}

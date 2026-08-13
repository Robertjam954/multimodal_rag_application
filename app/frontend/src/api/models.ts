export interface ChatMessage {
    role: "user" | "assistant" | "system";
    content: string;
}

export interface ChatAppRequestOverrides {
    top?: number;
    use_verifier?: boolean;
    use_graphrag?: boolean;
    graph_hops?: number;
    reasoning_effort?: "minimal" | "low" | "medium" | "high";
    use_streaming?: boolean;
    verifier_retry?: boolean;
}

export interface ChatRequest {
    messages: ChatMessage[];
    context?: { overrides?: ChatAppRequestOverrides };
    stream?: boolean;
    session_state?: string | null;
}

export interface Citation {
    id: string;
    source_file: string;
    source_page?: string | null;
    source_timestamp_seconds?: number | null;
    score?: number | null;
    content_snippet?: string;
}

export interface Claim {
    sentence: string;
    citation_ids: string[];
    verdict: "supported" | "unsupported" | "skipped" | "unknown";
    verifier_reason?: string;
}

export interface ChatResponse {
    answer: string;
    claims: Claim[];
    citations: Citation[];
    verifier_verdict?: { unsupported_claims: number; retried: boolean } | null;
    followups?: string[];
    cost?: { input_tokens?: number; output_tokens?: number; est_usd?: number; model?: string };
    session_state?: string | null;
}

export interface DryRunStatement {
    layer: string;
    statement: string;
    ok: boolean;
    error?: string;
    skipped?: boolean;
}

export interface DryRunResult {
    ok: boolean;
    per_statement: DryRunStatement[];
}

export interface SqlBundle {
    request: string;
    parsed: Record<string, unknown>;
    impact: Record<string, unknown>;
    plan: Record<string, unknown>;
    sql: Record<string, unknown>;
    validation: { ok: boolean; issues: string[] };
    dry_run?: DryRunResult;
}

export interface AppConfig {
    streamingEnabled: boolean;
    verifierEnabled: boolean;
    graphragEnabled: boolean;
    multimodalEnabled: boolean;
    agenticKnowledgebaseEnabled: boolean;
    voiceDemoEnabled: boolean;
    sqlDemoEnabled: boolean;
    contentSafetyEnabled: boolean;
    feedbackEnabled: boolean;
    userUploadEnabled: boolean;
    chatHistoryBrowserEnabled: boolean;
    chatHistoryCosmosEnabled: boolean;
    speechInputEnabled: boolean;
    speechOutputAzureEnabled: boolean;
    speechOutputBrowserEnabled: boolean;
    speechVoice: string;
    reasoningEffortEnabled: boolean;
    reasoningEffortOptions: string[];
    vectorSearchEnabled: boolean;
    semanticRankerDeployed: boolean;
    authEnabled: boolean;
    languages: string[];
}

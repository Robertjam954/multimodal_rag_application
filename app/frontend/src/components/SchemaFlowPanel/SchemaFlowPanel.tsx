import { useState } from "react";
import type { SqlBundle, DryRunResult } from "../../api/models";
import "./SchemaFlowPanel.module.css";

export default function SchemaFlowPanel({ bundle }: { bundle: SqlBundle | null }) {
    const [expanded, setExpanded] = useState<Record<string, boolean>>({
        parsed: true,
        impact: false,
        plan: false,
        sql: false,
        validation: true,
        dryRun: false,
    });

    if (!bundle) return <em>Plan a SQL change to see the bundle.</em>;

    return (
        <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 12 }}>
            <Collapsible
                title="Parsed"
                expanded={expanded.parsed}
                onToggle={() => setExpanded((p) => ({ ...p, parsed: !p.parsed }))}
            >
                <JsonView data={bundle.parsed} />
            </Collapsible>

            <Collapsible
                title="Impact"
                expanded={expanded.impact}
                onToggle={() => setExpanded((p) => ({ ...p, impact: !p.impact }))}
            >
                <ImpactView impact={bundle.impact} />
            </Collapsible>

            <Collapsible
                title="Plan"
                expanded={expanded.plan}
                onToggle={() => setExpanded((p) => ({ ...p, plan: !p.plan }))}
            >
                <JsonView data={bundle.plan} />
            </Collapsible>

            <Collapsible
                title="SQL"
                expanded={expanded.sql}
                onToggle={() => setExpanded((p) => ({ ...p, sql: !p.sql }))}
            >
                <SqlView sql={bundle.sql} />
            </Collapsible>

            <Collapsible
                title={bundle.validation.ok ? "✓ Validation OK" : "✗ Validation Issues"}
                expanded={expanded.validation}
                onToggle={() => setExpanded((p) => ({ ...p, validation: !p.validation }))}
                status={bundle.validation.ok ? "success" : "error"}
            >
                {bundle.validation.issues.length > 0 ? (
                    <ul style={{ margin: 0, fontSize: 12 }}>
                        {bundle.validation.issues.map((issue, i) => (
                            <li key={i} style={{ marginBottom: 4 }}>
                                {issue}
                            </li>
                        ))}
                    </ul>
                ) : (
                    <em>No validation issues detected.</em>
                )}
            </Collapsible>

            {bundle.dry_run && (
                <Collapsible
                    title={bundle.dry_run.ok ? "✓ Dry-Run Passed" : "✗ Dry-Run Failed"}
                    expanded={expanded.dryRun}
                    onToggle={() => setExpanded((p) => ({ ...p, dryRun: !p.dryRun }))}
                    status={bundle.dry_run.ok ? "success" : "error"}
                >
                    <DryRunView dryRun={bundle.dry_run} />
                </Collapsible>
            )}
        </div>
    );
}

function Collapsible({
    title,
    expanded,
    onToggle,
    children,
    status,
}: {
    title: string;
    expanded: boolean;
    onToggle: () => void;
    children: React.ReactNode;
    status?: "success" | "error";
}) {
    const statusColor = status === "success" ? "#4ade80" : status === "error" ? "#f87171" : undefined;
    return (
        <section
            style={{
                border: `1px solid ${statusColor || "var(--colorNeutralStroke2)"}`,
                borderRadius: 6,
                padding: 8,
                backgroundColor: statusColor ? `${statusColor}08` : undefined,
            }}
        >
            <header
                onClick={onToggle}
                style={{
                    fontWeight: 600,
                    marginBottom: expanded ? 8 : 0,
                    cursor: "pointer",
                    display: "flex",
                    alignItems: "center",
                    gap: 6,
                    fontSize: 13,
                }}
            >
                <span style={{ fontSize: 10, color: statusColor }}>
                    {expanded ? "▼" : "▶"}
                </span>
                {title}
            </header>
            {expanded && <div>{children}</div>}
        </section>
    );
}

function JsonView({ data }: { data: Record<string, unknown> }) {
    return (
        <pre style={{ fontSize: 11, whiteSpace: "pre-wrap", margin: 0, fontFamily: "JetBrains Mono, monospace" }}>
            {JSON.stringify(data, null, 2)}
        </pre>
    );
}

function ImpactView({ impact }: { impact: Record<string, unknown> }) {
    const grounding = impact.grounding as any;
    return (
        <div>
            {grounding && (
                <div style={{ fontSize: 12, marginBottom: 8 }}>
                    <div style={{ fontWeight: 500, marginBottom: 4 }}>Grounding:</div>
                    {grounding.llm_confirmed && (
                        <div style={{ color: "#4ade80", marginBottom: 2 }}>
                            ✓ LLM Confirmed: {grounding.llm_confirmed.join(", ")}
                        </div>
                    )}
                    {grounding.llm_unsupported && grounding.llm_unsupported.length > 0 && (
                        <div style={{ color: "#f87171", marginBottom: 2 }}>
                            ✗ Unsupported: {grounding.llm_unsupported.join(", ")}
                        </div>
                    )}
                    {grounding.dependent_views && (
                        <div style={{ fontSize: 11, color: "var(--muted)" }}>
                            Dependent views: {grounding.dependent_views.join(", ")}
                        </div>
                    )}
                </div>
            )}
            <JsonView data={impact} />
        </div>
    );
}

function SqlView({ sql }: { sql: Record<string, unknown> }) {
    return (
        <div>
            {Object.entries(sql).map(([layer, statements]) => (
                <div key={layer} style={{ marginBottom: 8, fontSize: 11 }}>
                    <div style={{ fontWeight: 500, color: "var(--accent)", marginBottom: 2 }}>
                        {layer}:
                    </div>
                    {Array.isArray(statements) ? (
                        <div style={{ paddingLeft: 12 }}>
                            {statements.map((stmt, i) => (
                                <div key={i} style={{ fontFamily: "JetBrains Mono, monospace", fontSize: 10, marginBottom: 4 }}>
                                    <code style={{ whiteSpace: "pre-wrap" }}>{stmt}</code>
                                </div>
                            ))}
                        </div>
                    ) : (
                        <pre style={{ fontSize: 10, whiteSpace: "pre-wrap", margin: 0 }}>
                            {JSON.stringify(statements, null, 2)}
                        </pre>
                    )}
                </div>
            ))}
        </div>
    );
}

function DryRunView({ dryRun }: { dryRun: DryRunResult }) {
    return (
        <div style={{ fontSize: 11 }}>
            {dryRun.per_statement.map((stmt, i) => (
                <div
                    key={i}
                    style={{
                        marginBottom: 6,
                        padding: 6,
                        backgroundColor: stmt.ok ? "#4ade8008" : "#f8717108",
                        borderLeft: `3px solid ${stmt.ok ? "#4ade80" : "#f87171"}`,
                        borderRadius: 2,
                    }}
                >
                    <div style={{ fontWeight: 500, marginBottom: 2 }}>
                        <span style={{ color: stmt.ok ? "#4ade80" : "#f87171" }}>
                            {stmt.ok ? "✓" : "✗"}
                        </span>
                        {" "}
                        {stmt.layer}
                    </div>
                    {stmt.skipped && <div style={{ color: "var(--muted)", fontSize: 10 }}>Skipped</div>}
                    {stmt.statement && (
                        <code
                            style={{
                                display: "block",
                                whiteSpace: "pre-wrap",
                                fontFamily: "JetBrains Mono, monospace",
                                fontSize: 10,
                                marginBottom: stmt.error ? 4 : 0,
                            }}
                        >
                            {stmt.statement}
                        </code>
                    )}
                    {stmt.error && (
                        <div style={{ color: "#f87171", fontSize: 10, marginTop: 2 }}>
                            Error: {stmt.error}
                        </div>
                    )}
                </div>
            ))}
        </div>
    );
}

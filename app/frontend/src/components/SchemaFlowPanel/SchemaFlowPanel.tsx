import type { SqlBundle } from "../../api/models";

export default function SchemaFlowPanel({ bundle }: { bundle: SqlBundle | null }) {
    if (!bundle) return <em>Plan a SQL change to see the bundle.</em>;
    return (
        <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 12 }}>
            <Section title="Parsed">{JSON.stringify(bundle.parsed, null, 2)}</Section>
            <Section title="Impact">{JSON.stringify(bundle.impact, null, 2)}</Section>
            <Section title="Plan">{JSON.stringify(bundle.plan, null, 2)}</Section>
            <Section title="SQL">{JSON.stringify(bundle.sql, null, 2)}</Section>
            <Section title={bundle.validation.ok ? "Validation: OK" : "Validation: ISSUES"}>
                {bundle.validation.issues.join("\n") || "no issues"}
            </Section>
        </div>
    );
}

function Section({ title, children }: { title: string; children: React.ReactNode }) {
    return (
        <section style={{ border: "1px solid var(--colorNeutralStroke2)", borderRadius: 6, padding: 8 }}>
            <header style={{ fontWeight: 600, marginBottom: 4 }}>{title}</header>
            <pre style={{ fontSize: 12, whiteSpace: "pre-wrap", margin: 0 }}>{children}</pre>
        </section>
    );
}

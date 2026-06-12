import type { Citation } from "../../api/models";

export default function SupportingContent({ citations }: { citations: Citation[] }) {
    return (
        <div>
            {citations.map((c) => (
                <article key={c.id} style={{ marginBottom: 12, padding: 8, border: "1px solid var(--colorNeutralStroke2)", borderRadius: 6 }}>
                    <header style={{ fontWeight: 600 }}>
                        [{c.id}] {c.source_file}
                        {c.source_page ? ` p.${c.source_page}` : ""}
                        {c.source_timestamp_seconds != null ? ` t=${c.source_timestamp_seconds}s` : ""}
                    </header>
                    <p style={{ fontSize: 13, whiteSpace: "pre-wrap" }}>{c.content_snippet}</p>
                </article>
            ))}
        </div>
    );
}

import type { Citation } from "../../api/models";

export default function SupportingContent({ citations }: { citations: Citation[] }) {
    if (!citations.length) return <em>No supporting content for this answer.</em>;
    return (
        <div>
            {citations.map((c, i) => (
                <article key={c.id} className="snippet">
                    <header>
                        <span className="pill ok" style={{ fontSize: 11 }}>
                            {i + 1}
                        </span>
                        {c.source_file}
                        {c.source_page ? <span className="score">p.{c.source_page}</span> : null}
                        {c.source_timestamp_seconds != null ? <span className="score">t={c.source_timestamp_seconds}s</span> : null}
                    </header>
                    <p>{c.content_snippet}</p>
                </article>
            ))}
        </div>
    );
}

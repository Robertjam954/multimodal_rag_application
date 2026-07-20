import type { Citation } from "../../api/models";
import { citationHref, citationLabel } from "../../lib/deepLink";

export default function Citations({ citations }: { citations: Citation[] }) {
    if (!citations.length) return null;
    return (
        <div style={{ display: "flex", flexWrap: "wrap", gap: 8, marginTop: 14 }}>
            {citations.map((c, i) => (
                <a
                    key={c.id}
                    className="chip cite"
                    href={citationHref(c)}
                    target="_blank"
                    rel="noreferrer"
                    title={c.content_snippet || ""}
                >
                    <span style={{ fontWeight: 700 }}>{i + 1}</span>
                    {citationLabel(c)}
                    {c.score != null ? <span className="score">{c.score.toFixed(2)}</span> : null}
                </a>
            ))}
        </div>
    );
}

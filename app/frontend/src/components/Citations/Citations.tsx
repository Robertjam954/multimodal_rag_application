import { Badge } from "@fluentui/react-components";
import type { Citation } from "../../api/models";
import { citationHref, citationLabel } from "../../lib/deepLink";

export default function Citations({ citations }: { citations: Citation[] }) {
    if (!citations.length) return null;
    return (
        <div style={{ display: "flex", flexWrap: "wrap", gap: 6, marginTop: 12 }}>
            {citations.map((c) => (
                <a key={c.id} href={citationHref(c)} target="_blank" rel="noreferrer">
                    <Badge appearance="outline" title={c.content_snippet || ""}>
                        [{c.id}] {citationLabel(c)}
                        {c.score != null ? ` · ${c.score.toFixed(2)}` : ""}
                    </Badge>
                </a>
            ))}
        </div>
    );
}

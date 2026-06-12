import type { Claim } from "../../api/models";

/** Renders the accumulated answer text with sentence-level Verifier verdicts. */
export default function Answer({ text, claims }: { text: string; claims: Claim[] }) {
    if (!claims.length) {
        return <p style={{ whiteSpace: "pre-wrap" }}>{text}</p>;
    }
    return (
        <div style={{ lineHeight: 1.6 }}>
            {claims.map((c, i) => {
                const color =
                    c.verdict === "supported"
                        ? "inherit"
                        : c.verdict === "unsupported"
                          ? "var(--colorPaletteRedForeground1)"
                          : "var(--colorNeutralForeground3)";
                const td = c.verdict === "unsupported" ? "line-through" : "none";
                return (
                    <span
                        key={i}
                        title={c.verifier_reason || c.verdict}
                        style={{ color, textDecoration: td, marginRight: 4 }}
                    >
                        {c.sentence}{" "}
                    </span>
                );
            })}
        </div>
    );
}

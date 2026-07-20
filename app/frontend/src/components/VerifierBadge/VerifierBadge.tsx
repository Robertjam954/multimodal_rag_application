export default function VerifierBadge({ verdict }: { verdict?: { unsupported_claims: number; retried: boolean } | null }) {
    if (!verdict) return null;
    const ok = verdict.unsupported_claims === 0;
    return (
        <span className={`pill ${ok ? "ok" : "warn"}`}>
            {ok ? "✓ All claims supported" : `⚠ ${verdict.unsupported_claims} unsupported`}
            {verdict.retried ? " · retried" : ""}
        </span>
    );
}

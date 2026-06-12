import { Badge } from "@fluentui/react-components";

export default function VerifierBadge({ verdict }: { verdict?: { unsupported_claims: number; retried: boolean } | null }) {
    if (!verdict) return null;
    const appearance = verdict.unsupported_claims === 0 ? "filled" : "outline";
    const color = verdict.unsupported_claims === 0 ? "success" : "danger";
    return (
        <Badge appearance={appearance} color={color}>
            Verifier: {verdict.unsupported_claims === 0 ? "all supported" : `${verdict.unsupported_claims} unsupported`}
            {verdict.retried ? " · retried" : ""}
        </Badge>
    );
}

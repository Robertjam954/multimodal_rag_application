import { Button } from "@fluentui/react-components";

export default function FollowUps({ items, onPick }: { items: string[]; onPick: (q: string) => void }) {
    if (!items.length) return null;
    return (
        <div style={{ marginTop: 16, display: "flex", flexWrap: "wrap", gap: 6 }}>
            {items.map((q, i) => (
                <Button key={i} appearance="outline" size="small" onClick={() => onPick(q)}>
                    {q}
                </Button>
            ))}
        </div>
    );
}

export default function FollowUps({ items, onPick }: { items: string[]; onPick: (q: string) => void }) {
    if (!items.length) return null;
    return (
        <div style={{ marginTop: 16, display: "flex", flexWrap: "wrap", gap: 8 }}>
            {items.map((q, i) => (
                <button key={i} className="chip" onClick={() => onPick(q)}>
                    {q} →
                </button>
            ))}
        </div>
    );
}

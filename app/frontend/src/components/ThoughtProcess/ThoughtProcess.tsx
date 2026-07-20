interface Step {
    title: string;
    description?: string;
    props?: Record<string, unknown>;
}

export default function ThoughtProcess({ steps }: { steps: Step[] }) {
    if (!steps.length) return <em>No thought-process steps recorded.</em>;
    return (
        <ul className="timeline">
            {steps.map((s, i) => (
                <li key={i}>
                    <strong style={{ textTransform: "capitalize" }}>{s.title}</strong>
                    {s.description ? <div style={{ color: "var(--muted)", fontSize: 13.5 }}>{s.description}</div> : null}
                    {s.props ? <pre style={{ fontSize: 12, overflow: "auto" }}>{JSON.stringify(s.props, null, 2)}</pre> : null}
                </li>
            ))}
        </ul>
    );
}

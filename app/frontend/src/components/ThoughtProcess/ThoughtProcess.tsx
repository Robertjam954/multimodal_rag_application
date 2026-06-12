interface Step {
    title: string;
    description?: string;
    props?: Record<string, unknown>;
}

export default function ThoughtProcess({ steps }: { steps: Step[] }) {
    if (!steps.length) return <em>No thought-process steps recorded.</em>;
    return (
        <ol>
            {steps.map((s, i) => (
                <li key={i}>
                    <strong>{s.title}</strong>
                    {s.description ? `: ${s.description}` : ""}
                    {s.props ? <pre style={{ fontSize: 12 }}>{JSON.stringify(s.props, null, 2)}</pre> : null}
                </li>
            ))}
        </ol>
    );
}

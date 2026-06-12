import { Switch, Dropdown, Option, Input, Label } from "@fluentui/react-components";
import type { ChatAppRequestOverrides } from "../../api/models";

export default function Settings({
    overrides,
    onChange,
}: {
    overrides: ChatAppRequestOverrides;
    onChange: (next: ChatAppRequestOverrides) => void;
}) {
    function patch<K extends keyof ChatAppRequestOverrides>(k: K, v: ChatAppRequestOverrides[K]) {
        onChange({ ...overrides, [k]: v });
    }
    return (
        <div style={{ display: "flex", flexDirection: "column", gap: 12, padding: 12, minWidth: 240 }}>
            <Label>Top results</Label>
            <Input type="number" value={String(overrides.top ?? 5)} onChange={(_, d) => patch("top", Number(d.value))} />
            <Label>Graph hops</Label>
            <Input
                type="number"
                value={String(overrides.graph_hops ?? 2)}
                onChange={(_, d) => patch("graph_hops", Number(d.value))}
            />
            <Label>Reasoning effort</Label>
            <Dropdown
                value={overrides.reasoning_effort ?? "minimal"}
                onOptionSelect={(_, d) => patch("reasoning_effort", d.optionValue as ChatAppRequestOverrides["reasoning_effort"])}
            >
                {["minimal", "low", "medium", "high"].map((o) => (
                    <Option key={o} value={o}>
                        {o}
                    </Option>
                ))}
            </Dropdown>
            <Switch label="Verifier" checked={overrides.use_verifier ?? true} onChange={(_, d) => patch("use_verifier", d.checked)} />
            <Switch label="GraphRAG" checked={overrides.use_graphrag ?? true} onChange={(_, d) => patch("use_graphrag", d.checked)} />
            <Switch label="Streaming" checked={overrides.use_streaming ?? true} onChange={(_, d) => patch("use_streaming", d.checked)} />
        </div>
    );
}

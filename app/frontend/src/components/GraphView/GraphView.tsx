import { useEffect, useRef } from "react";

interface GraphData {
    nodes: { id: string; label?: string }[];
    edges: { source: string; target: string; label?: string }[];
}

export default function GraphView({ data }: { data: GraphData }) {
    const ref = useRef<HTMLDivElement>(null);
    useEffect(() => {
        if (!ref.current || !data?.nodes?.length) return;
        let cancelled = false;
        (async () => {
            const G6 = await import("@antv/g6");
            if (cancelled || !ref.current) return;
            ref.current.innerHTML = "";
            const graph = new G6.Graph({
                container: ref.current!,
                data,
                width: ref.current!.clientWidth,
                height: 320,
                node: { style: { labelText: (d: { id: string }) => d.id } },
                layout: { type: "force" },
            });
            graph.render();
        })();
        return () => {
            cancelled = true;
        };
    }, [data]);
    if (!data?.nodes?.length) return <em>No graph subgraph for this answer.</em>;
    return <div ref={ref} style={{ width: "100%", height: 320, border: "1px solid var(--colorNeutralStroke2)", borderRadius: 6 }} />;
}

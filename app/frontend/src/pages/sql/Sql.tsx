import { useState } from "react";
import { Button, Textarea } from "@fluentui/react-components";
import { sqlPlan } from "../../api/api";
import type { SqlBundle } from "../../api/models";
import SchemaFlowPanel from "../../components/SchemaFlowPanel/SchemaFlowPanel";

const SAMPLE =
    "Add MUTATION_STATUS VARCHAR(50) to the mutation fact table indicating pathogenic classification (benign, likely_benign, variant_of_uncertain_significance, likely_pathogenic, pathogenic). Backfill from clinical records. Propagate through staging, core, and mart layers.";

export default function Sql() {
    const [req, setReq] = useState(SAMPLE);
    const [bundle, setBundle] = useState<SqlBundle | null>(null);
    const [busy, setBusy] = useState(false);

    async function go() {
        setBusy(true);
        try {
            setBundle(await sqlPlan(req));
        } finally {
            setBusy(false);
        }
    }
    return (
        <div>
            <h2>SchemaFlow SQL planner</h2>
            <Textarea value={req} onChange={(_, d) => setReq(d.value)} style={{ width: "100%" }} rows={4} />
            <Button appearance="primary" onClick={go} disabled={busy} style={{ marginTop: 8 }}>
                Plan
            </Button>
            <div style={{ marginTop: 16 }}>
                <SchemaFlowPanel bundle={bundle} />
            </div>
        </div>
    );
}

import { useState } from "react";
import { Button } from "@fluentui/react-components";
import { uploadPaper } from "../../api/api";
import PDFViewer from "../../components/PDFViewer/PDFViewer";

export default function Papers() {
    const [uploaded, setUploaded] = useState<{ filename: string; url: string; chunks: number }[]>([]);
    const [busy, setBusy] = useState(false);
    const [selected, setSelected] = useState<string | null>(null);

    async function onFile(e: React.ChangeEvent<HTMLInputElement>) {
        if (!e.target.files?.length) return;
        setBusy(true);
        try {
            for (const f of Array.from(e.target.files)) {
                const r = await uploadPaper(f);
                setUploaded((prev) => [...prev, ...r.uploaded]);
                if (!selected && r.uploaded[0]) setSelected(r.uploaded[0].url);
            }
        } finally {
            setBusy(false);
        }
    }

    return (
        <div style={{ display: "grid", gridTemplateColumns: "280px 1fr", gap: 16 }}>
            <aside>
                <h3>Upload PDFs</h3>
                <input type="file" multiple accept="application/pdf" onChange={onFile} disabled={busy} />
                <ul style={{ marginTop: 12 }}>
                    {uploaded.map((u, i) => (
                        <li key={i}>
                            <Button appearance="subtle" onClick={() => setSelected(u.url)}>
                                {u.filename} ({u.chunks} chunks)
                            </Button>
                        </li>
                    ))}
                </ul>
            </aside>
            <section>{selected ? <PDFViewer url={selected} /> : <em>Select an uploaded PDF.</em>}</section>
        </div>
    );
}

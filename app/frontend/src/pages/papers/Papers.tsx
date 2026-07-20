import { useRef, useState } from "react";
import { uploadPaper } from "../../api/api";
import PDFViewer from "../../components/PDFViewer/PDFViewer";

export default function Papers() {
    const [uploaded, setUploaded] = useState<{ filename: string; url: string; chunks: number }[]>([]);
    const [busy, setBusy] = useState(false);
    const [drag, setDrag] = useState(false);
    const [selected, setSelected] = useState<string | null>(null);
    const fileInput = useRef<HTMLInputElement>(null);

    async function ingest(files: FileList | File[]) {
        setBusy(true);
        try {
            for (const f of Array.from(files)) {
                const r = await uploadPaper(f);
                setUploaded((prev) => [...prev, ...r.uploaded]);
                if (!selected && r.uploaded[0]) setSelected(r.uploaded[0].url);
            }
        } finally {
            setBusy(false);
        }
    }

    return (
        <div className="page chat-layout">
            <aside className="card card-pad">
                <h3 className="section-title">Upload PDFs</h3>
                <label
                    className={`dropzone${drag ? " drag" : ""}`}
                    onDragOver={(e) => {
                        e.preventDefault();
                        setDrag(true);
                    }}
                    onDragLeave={() => setDrag(false)}
                    onDrop={(e) => {
                        e.preventDefault();
                        setDrag(false);
                        if (e.dataTransfer.files.length) ingest(e.dataTransfer.files);
                    }}
                >
                    {busy ? (
                        <div>
                            <div className="typing" style={{ justifyContent: "center" }}>
                                <span />
                                <span />
                                <span />
                            </div>
                            <div style={{ marginTop: 8 }}>Parsing, embedding &amp; indexing...</div>
                        </div>
                    ) : (
                        <>
                            <div style={{ fontSize: 28, marginBottom: 6 }}>📄</div>
                            <strong>Drop a PDF here</strong>
                            <div style={{ fontSize: 12.5, marginTop: 4 }}>or click to browse - it becomes searchable in seconds</div>
                        </>
                    )}
                    <input
                        ref={fileInput}
                        type="file"
                        multiple
                        accept="application/pdf"
                        style={{ display: "none" }}
                        onChange={(e) => e.target.files?.length && ingest(e.target.files)}
                        disabled={busy}
                    />
                </label>
                {uploaded.length ? (
                    <div style={{ marginTop: 16, display: "flex", flexDirection: "column", gap: 4 }}>
                        {uploaded.map((u, i) => (
                            <div
                                key={i}
                                className={`file-row${selected === u.url ? " selected" : ""}`}
                                onClick={() => setSelected(u.url)}
                            >
                                <span>📄</span>
                                <div style={{ minWidth: 0 }}>
                                    <div style={{ overflow: "hidden", textOverflow: "ellipsis", whiteSpace: "nowrap" }}>{u.filename}</div>
                                    <div className="meta">{u.chunks} chunks indexed</div>
                                </div>
                            </div>
                        ))}
                    </div>
                ) : null}
            </aside>
            <section className="card card-pad" style={{ minHeight: 420 }}>
                {selected ? (
                    <PDFViewer url={selected} />
                ) : (
                    <div className="empty-hero">
                        <h1>
                            Teach it something <span className="hl">new</span>
                        </h1>
                        <p>Upload a PDF and it joins the tutor's knowledge - parsed, embedded, and ready to cite in chat.</p>
                    </div>
                )}
            </section>
        </div>
    );
}

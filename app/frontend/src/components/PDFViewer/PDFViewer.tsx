import { useState } from "react";
import { Document, Page, pdfjs } from "react-pdf";

pdfjs.GlobalWorkerOptions.workerSrc = `https://unpkg.com/pdfjs-dist@${pdfjs.version}/build/pdf.worker.min.mjs`;

export default function PDFViewer({ url, initialPage = 1 }: { url: string; initialPage?: number }) {
    const [pages, setPages] = useState(0);
    const [page, setPage] = useState(initialPage);
    if (!url) return <em>No PDF selected.</em>;
    return (
        <div>
            <div style={{ display: "flex", gap: 8, marginBottom: 6 }}>
                <button onClick={() => setPage((p) => Math.max(1, p - 1))}>{"<"}</button>
                <span>
                    p.{page} / {pages || "?"}
                </span>
                <button onClick={() => setPage((p) => Math.min(pages || p + 1, p + 1))}>{">"}</button>
            </div>
            <Document file={url} onLoadSuccess={({ numPages }) => setPages(numPages)}>
                <Page pageNumber={page} width={520} />
            </Document>
        </div>
    );
}

import type { Citation } from "../api/models";

/** Build a deep-link to the citation source. PDFs jump to page; audio seeks to timestamp. */
export function citationHref(c: Citation): string {
    const base = `/content/${encodeURIComponent(c.source_file)}`;
    if (c.source_page) return `${base}#page=${c.source_page}`;
    if (c.source_timestamp_seconds != null) return `${base}#t=${c.source_timestamp_seconds}`;
    return base;
}

export function citationLabel(c: Citation): string {
    if (c.source_page) return `${c.source_file} (p.${c.source_page})`;
    if (c.source_timestamp_seconds != null) return `${c.source_file} @${Math.round(c.source_timestamp_seconds)}s`;
    return c.source_file;
}

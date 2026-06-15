-- Schema for the AI-engineering blog notes library.
-- One row per ingested source (audio lecture, YouTube tutorial, PDF paper, blog post).

CREATE TABLE IF NOT EXISTS blog_notes (
    id                INTEGER PRIMARY KEY AUTOINCREMENT,
    content_topic     TEXT NOT NULL,
    hook_intro        TEXT,
    key_insights      TEXT,         -- JSON array of strings
    seo_keywords      TEXT,         -- JSON array of strings
    source_url        TEXT,
    source_type       TEXT NOT NULL CHECK (source_type IN ('audio', 'video', 'text')),
    transcript        TEXT,
    status            TEXT NOT NULL DEFAULT 'draft' CHECK (status IN ('draft', 'reviewed', 'published')),
    generated_content TEXT,
    created_at        TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE INDEX IF NOT EXISTS idx_blog_notes_source_type ON blog_notes(source_type);
CREATE INDEX IF NOT EXISTS idx_blog_notes_status      ON blog_notes(status);

CREATE TABLE IF NOT EXISTS tags (
    note_id INTEGER NOT NULL REFERENCES blog_notes(id) ON DELETE CASCADE,
    tag     TEXT    NOT NULL,
    PRIMARY KEY (note_id, tag)
);

CREATE INDEX IF NOT EXISTS idx_tags_tag ON tags(tag);

CREATE TABLE IF NOT EXISTS citations (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    note_id       INTEGER NOT NULL REFERENCES blog_notes(id) ON DELETE CASCADE,
    citation_text TEXT    NOT NULL,
    citation_url  TEXT,
    timestamp_s   REAL              -- seconds offset for video/audio sources
);

CREATE INDEX IF NOT EXISTS idx_citations_note_id ON citations(note_id);

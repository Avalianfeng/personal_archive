-- question_registry · v1 schema
PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS schema_version (
    version INTEGER PRIMARY KEY,
    applied_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS db_meta (
    key TEXT PRIMARY KEY,
    value TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS questions (
    uid TEXT PRIMARY KEY,
    id TEXT NOT NULL UNIQUE,
    question TEXT NOT NULL,
    category TEXT NOT NULL,
    subcategory TEXT NOT NULL,
    type TEXT NOT NULL,
    interaction TEXT,
    source TEXT,
    status TEXT NOT NULL DEFAULT 'active',
    depth TEXT,
    validation INTEGER NOT NULL DEFAULT 0,
    order_num INTEGER,
    deprecated_reason TEXT,
    superseded_by TEXT,
    notes TEXT,
    options_json TEXT,
    scale_note TEXT,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_questions_category ON questions(category);
CREATE INDEX IF NOT EXISTS idx_questions_status ON questions(status);
CREATE INDEX IF NOT EXISTS idx_questions_id ON questions(id);

CREATE TABLE IF NOT EXISTS question_tags (
    question_uid TEXT NOT NULL REFERENCES questions(uid) ON DELETE CASCADE,
    tag TEXT NOT NULL,
    PRIMARY KEY (question_uid, tag)
);

CREATE INDEX IF NOT EXISTS idx_question_tags_tag ON question_tags(tag);

CREATE TABLE IF NOT EXISTS question_prerequisites (
    question_uid TEXT NOT NULL REFERENCES questions(uid) ON DELETE CASCADE,
    prerequisite_id TEXT NOT NULL,
    PRIMARY KEY (question_uid, prerequisite_id)
);

CREATE TABLE IF NOT EXISTS question_relations (
    source_uid TEXT NOT NULL REFERENCES questions(uid) ON DELETE CASCADE,
    target_uid TEXT NOT NULL REFERENCES questions(uid) ON DELETE CASCADE,
    relation_type TEXT NOT NULL,
    PRIMARY KEY (source_uid, target_uid, relation_type)
);

CREATE INDEX IF NOT EXISTS idx_question_relations_target ON question_relations(target_uid);

-- FTS5 external content
CREATE VIRTUAL TABLE IF NOT EXISTS questions_fts USING fts5(
    question,
    content='questions',
    content_rowid='rowid'
);

CREATE TRIGGER IF NOT EXISTS questions_ai AFTER INSERT ON questions BEGIN
    INSERT INTO questions_fts(rowid, question) VALUES (new.rowid, new.question);
END;

CREATE TRIGGER IF NOT EXISTS questions_ad AFTER DELETE ON questions BEGIN
    INSERT INTO questions_fts(questions_fts, rowid, question) VALUES('delete', old.rowid, old.question);
END;

CREATE TRIGGER IF NOT EXISTS questions_au AFTER UPDATE ON questions BEGIN
    INSERT INTO questions_fts(questions_fts, rowid, question) VALUES('delete', old.rowid, old.question);
    INSERT INTO questions_fts(rowid, question) VALUES (new.rowid, new.question);
END;

INSERT OR IGNORE INTO schema_version (version, applied_at) VALUES (1, datetime('now'));

-- HemePath SQLite Database Schema
CREATE TABLE IF NOT EXISTS sources (
    id TEXT PRIMARY KEY,
    title TEXT NOT NULL,
    publisher TEXT,
    url_or_identifier TEXT,
    accessed_date TEXT,
    reviewer_status TEXT,
    description TEXT
);

CREATE TABLE IF NOT EXISTS topics (
    id TEXT PRIMARY KEY,
    title TEXT NOT NULL,
    description TEXT,
    order_index INTEGER
);

CREATE TABLE IF NOT EXISTS lessons (
    id INTEGER PRIMARY KEY,
    topic_id TEXT,
    title TEXT NOT NULL,
    short_desc TEXT,
    learning_objectives TEXT, -- JSON array
    key_definition TEXT,
    plain_explanation TEXT,
    mechanism_steps TEXT, -- JSON array
    key_terms TEXT, -- JSON array
    exam_takeaways TEXT, -- JSON array
    go_deeper TEXT,
    summary TEXT,
    estimated_minutes INTEGER,
    source_id TEXT,
    order_index INTEGER,
    diagram_id TEXT,
    diagram_caption TEXT,
    FOREIGN KEY(source_id) REFERENCES sources(id)
);

CREATE TABLE IF NOT EXISTS diagrams (
    id TEXT PRIMARY KEY,
    lesson_id INTEGER,
    title TEXT NOT NULL,
    diagram_type TEXT,
    diagram_data_or_url TEXT,
    alt_text TEXT,
    caption TEXT,
    FOREIGN KEY(lesson_id) REFERENCES lessons(id)
);

CREATE TABLE IF NOT EXISTS questions (
    id TEXT PRIMARY KEY,
    lesson_id INTEGER,
    type TEXT NOT NULL,
    stem TEXT NOT NULL,
    options_json TEXT, -- JSON array of strings or pairs/steps
    correct_answer TEXT,
    correct_index INTEGER,
    explanation TEXT,
    distractor_explanations TEXT, -- JSON object
    difficulty TEXT,
    review_status TEXT,
    source_id TEXT,
    FOREIGN KEY(lesson_id) REFERENCES lessons(id)
);

CREATE TABLE IF NOT EXISTS lesson_progress (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id TEXT NOT NULL,
    lesson_id INTEGER NOT NULL,
    status TEXT NOT NULL DEFAULT 'not_started', -- not_started, in_progress, completed
    last_opened_at TEXT,
    completed_at TEXT,
    UNIQUE(session_id, lesson_id)
);

CREATE TABLE IF NOT EXISTS quiz_attempts (
    id TEXT PRIMARY KEY,
    session_id TEXT NOT NULL,
    lesson_id INTEGER,
    started_at TEXT,
    completed_at TEXT,
    score REAL,
    total_questions INTEGER,
    difficulty TEXT,
    mode TEXT
);

CREATE TABLE IF NOT EXISTS quiz_responses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    attempt_id TEXT NOT NULL,
    question_id TEXT NOT NULL,
    selected_answer TEXT,
    is_correct INTEGER,
    FOREIGN KEY(attempt_id) REFERENCES quiz_attempts(id)
);

CREATE TABLE IF NOT EXISTS bookmarks_notes (
    id TEXT PRIMARY KEY,
    session_id TEXT NOT NULL,
    item_type TEXT NOT NULL, -- lesson, diagram, chat, textbook, note
    item_id TEXT,
    title TEXT,
    content_text TEXT,
    created_at TEXT
);

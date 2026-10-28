# database/db.py - SQLite storage and data access for HemePath
import sqlite3
import json
import os
from datetime import datetime

if os.environ.get("VERCEL"):
    DB_PATH = "/tmp/hemepath.db"
    bundled_db = os.path.join(os.path.dirname(__file__), "hemepath.db")
    if os.path.exists(bundled_db) and not os.path.exists(DB_PATH):
        try:
            import shutil
            shutil.copyfile(bundled_db, DB_PATH)
        except Exception:
            pass
else:
    DB_PATH = os.path.join(os.path.dirname(__file__), "hemepath.db")

SCHEMA_PATH = os.path.join(os.path.dirname(__file__), "schema.sql")
CONTENT_DIR = os.path.join(os.path.dirname(__file__), "..", "content")

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    with open(SCHEMA_PATH, "r", encoding="utf-8") as f:
        conn.executescript(f.read())
    conn.commit()
    seed_data(conn)
    conn.close()

def seed_data(conn):
    # Check if lessons already loaded
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM lessons")
    if cur.fetchone()[0] > 0:
        return

    # 1. Sources
    sources_file = os.path.join(CONTENT_DIR, "sources.json")
    if os.path.exists(sources_file):
        with open(sources_file, "r", encoding="utf-8") as f:
            sources = json.load(f)
            for s in sources:
                conn.execute(
                    "INSERT OR REPLACE INTO sources VALUES (?, ?, ?, ?, ?, ?, ?)",
                    (s["id"], s["title"], s.get("publisher"), s.get("url"), s.get("accessed_date"), s.get("reviewer_status"), s.get("description"))
                )

    # 2. Lessons
    lessons_file = os.path.join(CONTENT_DIR, "lessons.json")
    if os.path.exists(lessons_file):
        with open(lessons_file, "r", encoding="utf-8") as f:
            lessons = json.load(f)
            for l in lessons:
                conn.execute(
                    """INSERT OR REPLACE INTO lessons (
                        id, topic_id, title, short_desc, learning_objectives, key_definition,
                        plain_explanation, mechanism_steps, key_terms, exam_takeaways,
                        go_deeper, summary, estimated_minutes, source_id, order_index, diagram_id, diagram_caption
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                    (
                        l["id"], l.get("topic_id"), l["title"], l.get("short_desc"),
                        json.dumps(l.get("learning_objectives", [])),
                        l.get("key_definition"), l.get("plain_explanation"),
                        json.dumps(l.get("mechanism_steps", [])),
                        json.dumps(l.get("key_terms", [])),
                        json.dumps(l.get("exam_takeaways", [])),
                        l.get("go_deeper"), l.get("summary"),
                        l.get("estimated_minutes", 8),
                        l.get("source_id"), l.get("order_index", l["id"]),
                        l.get("diagram_id"), l.get("diagram_caption")
                    )
                )

    # 3. Questions
    questions_file = os.path.join(CONTENT_DIR, "questions_seed.json")
    if os.path.exists(questions_file):
        with open(questions_file, "r", encoding="utf-8") as f:
            questions = json.load(f)
            for q in questions:
                opts = q.get("options") or q.get("pairs") or q.get("steps") or []
                conn.execute(
                    """INSERT OR REPLACE INTO questions (
                        id, lesson_id, type, stem, options_json, correct_answer,
                        correct_index, explanation, distractor_explanations, difficulty,
                        review_status, source_id
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                    (
                        q["id"], q.get("lesson_id"), q["type"], q["stem"],
                        json.dumps(opts),
                        q.get("correct_answer", ""),
                        q.get("correct_index", 0),
                        q.get("explanation", ""),
                        json.dumps(q.get("distractor_explanations", {})),
                        q.get("difficulty", "Medium"),
                        q.get("review_status", "Reviewed"),
                        q.get("source_id", "src-robbins-pathology")
                    )
                )

    conn.commit()

# Progress and bookmark helpers
def get_user_progress(session_id):
    conn = get_db()
    rows = conn.execute("SELECT lesson_id, status, completed_at FROM lesson_progress WHERE session_id = ?", (session_id,)).fetchall()
    conn.close()
    return {r["lesson_id"]: {"status": r["status"], "completed_at": r["completed_at"]} for r in rows}

def update_lesson_status(session_id, lesson_id, status):
    conn = get_db()
    now = datetime.now().isoformat()
    completed_at = now if status == "completed" else None
    conn.execute(
        """INSERT INTO lesson_progress (session_id, lesson_id, status, last_opened_at, completed_at)
           VALUES (?, ?, ?, ?, ?)
           ON CONFLICT(session_id, lesson_id) DO UPDATE SET
           status=excluded.status, last_opened_at=excluded.last_opened_at,
           completed_at=COALESCE(excluded.completed_at, lesson_progress.completed_at)""",
        (session_id, lesson_id, status, now, completed_at)
    )
    conn.commit()
    conn.close()

def save_bookmark_or_note(session_id, item_id, item_type, title, content_text):
    conn = get_db()
    now = datetime.now().isoformat()
    note_id = f"note_{int(datetime.now().timestamp() * 1000)}"
    conn.execute(
        "INSERT INTO bookmarks_notes (id, session_id, item_type, item_id, title, content_text, created_at) VALUES (?, ?, ?, ?, ?, ?, ?)",
        (note_id, session_id, item_type, item_id, title, content_text, now)
    )
    conn.commit()
    conn.close()
    return note_id

def get_bookmarks_and_notes(session_id):
    conn = get_db()
    rows = conn.execute("SELECT * FROM bookmarks_notes WHERE session_id = ? ORDER BY created_at DESC", (session_id,)).fetchall()
    conn.close()
    return [dict(r) for r in rows]

def delete_bookmark_or_note(session_id, note_id):
    conn = get_db()
    conn.execute("DELETE FROM bookmarks_notes WHERE id = ? AND session_id = ?", (note_id, session_id))
    conn.commit()
    conn.close()

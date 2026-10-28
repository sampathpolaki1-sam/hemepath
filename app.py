# app.py - HemePath Flask Application
import os
import json
import uuid
from flask import Flask, render_template, request, jsonify, redirect, url_for, session
from flask_cors import CORS
from dotenv import load_dotenv

from database.db import (
    init_db, get_user_progress, update_lesson_status,
    save_bookmark_or_note, get_bookmarks_and_notes, delete_bookmark_or_note
)
from services.tutor_service import generate_tutor_response, SAFETY_DISCLAIMER
from services.image_explainer import validate_image_file, process_textbook_image
from services.quiz_service import get_filtered_quiz, evaluate_quiz_submission, load_all_questions

load_dotenv()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(BASE_DIR, "static")
TEMPLATE_DIR = os.path.join(BASE_DIR, "templates")

app = Flask(
    __name__,
    static_folder=STATIC_DIR,
    template_folder=TEMPLATE_DIR,
    static_url_path="/static"
)
app.secret_key = os.environ.get("SECRET_KEY", "hemepath-mbbs-secret-key-2026")
CORS(app)

# Ensure database is initialized on startup
with app.app_context():
    init_db()

def get_session_id():
    if "user_session_id" not in session:
        session["user_session_id"] = str(uuid.uuid4())
    return session["user_session_id"]

CONTENT_DIR = os.path.join(os.path.dirname(__file__), "content")

def load_json_file(filename):
    path = os.path.join(CONTENT_DIR, filename)
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

# ----------------- PAGE ROUTES -----------------

@app.route("/")
def index():
    session_id = get_session_id()
    lessons = load_json_file("lessons.json")
    progress = get_user_progress(session_id)
    
    completed_count = sum(1 for p in progress.values() if p.get("status") == "completed")
    in_progress_count = sum(1 for p in progress.values() if p.get("status") == "in_progress")
    pct_complete = round((completed_count / len(lessons) * 100) if lessons else 0)
    
    # Next recommended lesson
    next_lesson = None
    for l in lessons:
        status = progress.get(l["id"], {}).get("status", "not_started")
        if status != "completed":
            next_lesson = l
            break
    if not next_lesson and lessons:
        next_lesson = lessons[0]

    return render_template(
        "index.html",
        lessons=lessons,
        progress=progress,
        completed_count=completed_count,
        in_progress_count=in_progress_count,
        pct_complete=pct_complete,
        next_lesson=next_lesson
    )

@app.route("/roadmap")
def roadmap():
    session_id = get_session_id()
    lessons = load_json_file("lessons.json")
    progress = get_user_progress(session_id)
    return render_template("roadmap.html", lessons=lessons, progress=progress)

@app.route("/lesson/<int:lesson_id>")
def lesson_view(lesson_id):
    session_id = get_session_id()
    lessons = load_json_file("lessons.json")
    lesson = next((l for l in lessons if l["id"] == lesson_id), None)
    if not lesson:
        return redirect(url_for("roadmap"))
        
    # Mark in-progress if not started
    current_status = get_user_progress(session_id).get(lesson_id, {}).get("status")
    if current_status != "completed":
        update_lesson_status(session_id, lesson_id, "in_progress")
        
    prev_lesson = next((l for l in lessons if l["id"] == lesson_id - 1), None)
    next_lesson = next((l for l in lessons if l["id"] == lesson_id + 1), None)
    progress = get_user_progress(session_id)

    all_videos = load_json_file("video_classes.json")
    lesson_videos = [v for v in all_videos if v.get("lesson_id") == lesson_id]
    if not lesson_videos:
        lesson_videos = all_videos[:3]

    return render_template(
        "lesson.html",
        lesson=lesson,
        prev_lesson=prev_lesson,
        next_lesson=next_lesson,
        progress=progress.get(lesson_id, {}),
        all_lessons=lessons,
        lesson_videos=lesson_videos
    )

@app.route("/video-classes")
def video_classes():
    lang = request.args.get("lang", "all")
    topic = request.args.get("topic", "all")
    all_videos = load_json_file("video_classes.json")
    
    filtered = all_videos
    if lang != "all":
        filtered = [v for v in filtered if v.get("language_code") == lang or v.get("language", "").lower() == lang.lower()]
    if topic != "all":
        filtered = [v for v in filtered if topic.lower() in v.get("topic", "").lower()]
        
    return render_template(
        "video_classes.html",
        videos=filtered,
        all_videos=all_videos,
        selected_lang=lang,
        selected_topic=topic
    )

@app.route("/textbook-explainer")
def textbook_explainer():
    sample_textbooks = load_json_file("sample_textbooks.json")
    return render_template("upload_explainer.html", samples=sample_textbooks)

@app.route("/chat")
def chat():
    return render_template("chat.html")

@app.route("/quiz")
def quiz():
    lesson_id = request.args.get("lesson_id")
    difficulty = request.args.get("difficulty", "All")
    mode = request.args.get("mode", "mixed")
    count = int(request.args.get("count", 5))
    lessons = load_json_file("lessons.json")
    return render_template(
        "quiz.html",
        lesson_id=lesson_id,
        difficulty=difficulty,
        mode=mode,
        count=count,
        lessons=lessons
    )

@app.route("/results/<attempt_id>")
def results(attempt_id):
    return render_template("results.html", attempt_id=attempt_id)

@app.route("/flashcards")
def flashcards():
    cards = load_json_file("flashcards.json")
    return render_template("flashcards.html", cards=cards)

@app.route("/glossary")
def glossary():
    terms = load_json_file("glossary.json")
    return render_template("glossary.html", terms=terms)

@app.route("/bookmarks")
def bookmarks():
    session_id = get_session_id()
    items = get_bookmarks_and_notes(session_id)
    return render_template("bookmarks.html", bookmarks=items)

@app.route("/sources")
def sources():
    sources_list = load_json_file("sources.json")
    return render_template("sources.html", sources=sources_list)

# ----------------- REST API ENDPOINTS -----------------

@app.route("/api/health")
def api_health():
    return jsonify({
        "status": "healthy",
        "app": "HemePath — Anemia & Polycythemia Tutor",
        "target": "MBBS Medical Students",
        "lessons_count": 15,
        "mode": "Educational"
    })

@app.route("/api/lessons")
def api_lessons():
    return jsonify(load_json_file("lessons.json"))

@app.route("/api/lessons/<int:lesson_id>")
def api_lesson_detail(lesson_id):
    lessons = load_json_file("lessons.json")
    lesson = next((l for l in lessons if l["id"] == lesson_id), None)
    if not lesson:
        return jsonify({"error": "Lesson not found"}), 404
    return jsonify(lesson)

@app.route("/api/progress", methods=["GET"])
def api_get_progress():
    session_id = get_session_id()
    return jsonify(get_user_progress(session_id))

@app.route("/api/progress/update", methods=["POST"])
def api_update_progress():
    session_id = get_session_id()
    data = request.get_json() or {}
    lesson_id = data.get("lesson_id")
    status = data.get("status", "completed")
    if not lesson_id:
        return jsonify({"error": "Missing lesson_id"}), 400
    update_lesson_status(session_id, int(lesson_id), status)
    return jsonify({"success": True, "status": status})

@app.route("/api/chat", methods=["POST"])
def api_chat():
    data = request.get_json() or {}
    message = data.get("message", "").strip()
    mode = data.get("mode", "mbbs_exam")
    context = data.get("context")
    if not message:
        return jsonify({"error": "Message is required"}), 400
    resp = generate_tutor_response(message, mode, context)
    return jsonify(resp)

@app.route("/api/explain-image", methods=["POST"])
def api_explain_image():
    # Can accept multipart file or JSON with extracted_text / sample_preset
    if "image" in request.files:
        file = request.files["image"]
        valid, err_msg = validate_image_file(file)
        if not valid:
            return jsonify({"success": False, "error": err_msg}), 400
        image_bytes = file.read()
        res = process_textbook_image(image_bytes=image_bytes, filename=file.filename)
        return jsonify(res)
    
    # Or JSON payload
    data = request.get_json() or {}
    text = data.get("text")
    if text:
        res = process_textbook_image(extracted_text=text)
        return jsonify(res)
        
    return jsonify({"success": False, "error": "No image file or text provided"}), 400

@app.route("/api/quiz/generate", methods=["GET"])
def api_quiz_generate():
    lesson_id = request.args.get("lesson_id")
    difficulty = request.args.get("difficulty")
    count = int(request.args.get("count", 5))
    mode = request.args.get("mode", "mixed")
    quiz_data = get_filtered_quiz(lesson_id=lesson_id, difficulty=difficulty, count=count, mode=mode)
    return jsonify(quiz_data)

@app.route("/api/quiz/submit", methods=["POST"])
def api_quiz_submit():
    session_id = get_session_id()
    data = request.get_json() or {}
    attempt_id = data.get("attempt_id")
    responses = data.get("responses", [])
    if not attempt_id or not responses:
        return jsonify({"error": "Missing attempt_id or responses"}), 400
        
    evaluation = evaluate_quiz_submission(attempt_id, session_id, responses)
    return jsonify(evaluation)

@app.route("/api/bookmarks", methods=["GET", "POST"])
def api_bookmarks():
    session_id = get_session_id()
    if request.method == "POST":
        data = request.get_json() or {}
        item_id = data.get("item_id")
        item_type = data.get("item_type", "note")
        title = data.get("title", "Saved Item")
        content = data.get("content", "")
        note_id = save_bookmark_or_note(session_id, item_id, item_type, title, content)
        return jsonify({"success": True, "id": note_id})
    return jsonify(get_bookmarks_and_notes(session_id))

@app.route("/api/bookmarks/<note_id>", methods=["DELETE"])
def api_delete_bookmark(note_id):
    session_id = get_session_id()
    delete_bookmark_or_note(session_id, note_id)
    return jsonify({"success": True})

@app.route("/api/glossary")
def api_glossary():
    return jsonify(load_json_file("glossary.json"))

@app.route("/api/flashcards")
def api_flashcards():
    return jsonify(load_json_file("flashcards.json"))

@app.route("/api/videos")
def api_videos():
    lang = request.args.get("lang")
    lesson_id = request.args.get("lesson_id")
    videos = load_json_file("video_classes.json")
    if lang and lang != "all":
        videos = [v for v in videos if v.get("language_code") == lang or v.get("language", "").lower() == lang.lower()]
    if lesson_id:
        try:
            lid = int(lesson_id)
            videos = [v for v in videos if v.get("lesson_id") == lid]
        except (ValueError, TypeError):
            pass
    return jsonify(videos)

if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=5000)

# services/quiz_service.py - Question Bank Management, Scoring & Remediation Engine
import json
import os
import random
from datetime import datetime
from database.db import get_db

CONTENT_DIR = os.path.join(os.path.dirname(__file__), "..", "content")

def load_all_questions():
    q_file = os.path.join(CONTENT_DIR, "questions_seed.json")
    if os.path.exists(q_file):
        with open(q_file, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def get_filtered_quiz(lesson_id=None, topic_id=None, difficulty=None, count=5, mode="mixed"):
    all_qs = load_all_questions()
    
    filtered = all_qs
    if lesson_id:
        try:
            lid = int(lesson_id)
            filtered = [q for q in filtered if q.get("lesson_id") == lid]
        except (ValueError, TypeError):
            pass
            
    if difficulty and difficulty.lower() != "all":
        filtered = [q for q in filtered if q.get("difficulty", "").lower() == difficulty.lower()]
        
    if mode == "vignette":
        vignettes = [q for q in filtered if q.get("type") == "vignette"]
        if vignettes:
            filtered = vignettes
    elif mode == "matching":
        matching = [q for q in filtered if q.get("type") == "matching"]
        if matching:
            filtered = matching
    elif mode == "ordering":
        ordering = [q for q in filtered if q.get("type") == "ordering"]
        if ordering:
            filtered = ordering

    # If count requested is less than total, shuffle and pick
    if len(filtered) > count:
        selected = random.sample(filtered, count)
    else:
        selected = list(filtered)
        if not selected and all_qs:
            # Fallback to random sample of any questions if strict filter returned 0
            selected = random.sample(all_qs, min(count, len(all_qs)))

    # Generate a unique quiz session attempt ID
    attempt_id = f"attempt_{int(datetime.now().timestamp() * 1000)}"
    return {
        "attempt_id": attempt_id,
        "total": len(selected),
        "questions": selected
    }

def evaluate_quiz_submission(attempt_id, session_id, user_responses, questions_data=None):
    """
    Evaluates submitted user answers, computes score, analyzes mistakes,
    and returns rich distractor explanations and weak topic recommendations.
    """
    all_qs_map = {q["id"]: q for q in load_all_questions()}
    
    correct_count = 0
    total = len(user_responses)
    results = []
    subtopic_stats = {}
    weak_lessons = set()

    conn = get_db()
    now = datetime.now().isoformat()

    for item in user_responses:
        qid = item.get("question_id")
        user_choice = item.get("selected_answer")
        
        q_meta = all_qs_map.get(qid)
        if not q_meta:
            continue
            
        lid = q_meta.get("lesson_id", 1)
        subtopic_stats.setdefault(lid, {"correct": 0, "total": 0})
        subtopic_stats[lid]["total"] += 1
        
        q_type = q_meta.get("type", "mcq")
        is_correct = False
        
        if q_type in ["mcq", "vignette"]:
            # Check either index or string
            correct_idx = q_meta.get("correct_index")
            opts = q_meta.get("options", [])
            correct_str = q_meta.get("correct_answer")
            
            if str(user_choice) == str(correct_idx):
                is_correct = True
            elif user_choice == correct_str:
                is_correct = True
            elif isinstance(user_choice, int) and 0 <= user_choice < len(opts) and opts[user_choice] == correct_str:
                is_correct = True
                
        elif q_type == "true_false":
            correct_ans = str(q_meta.get("correct_answer", "")).lower()
            if str(user_choice).strip().lower() == correct_ans:
                is_correct = True
            elif str(user_choice) == str(q_meta.get("correct_index")):
                is_correct = True
                
        elif q_type == "matching":
            # If all pairs match
            is_correct = bool(item.get("is_correct", False))
            
        elif q_type == "ordering":
            # If sequence is correct
            is_correct = bool(item.get("is_correct", False))

        if is_correct:
            correct_count += 1
            subtopic_stats[lid]["correct"] += 1
        else:
            weak_lessons.add(lid)

        # Distractor analysis
        distractor_note = None
        if not is_correct and str(user_choice) in q_meta.get("distractor_explanations", {}):
            distractor_note = q_meta["distractor_explanations"][str(user_choice)]

        results.append({
            "question_id": qid,
            "lesson_id": lid,
            "stem": q_meta.get("stem"),
            "user_choice": user_choice,
            "correct_answer": q_meta.get("correct_answer"),
            "correct_index": q_meta.get("correct_index"),
            "is_correct": is_correct,
            "explanation": q_meta.get("explanation"),
            "distractor_note": distractor_note
        })

        # Save individual response to DB
        conn.execute(
            "INSERT INTO quiz_responses (attempt_id, question_id, selected_answer, is_correct) VALUES (?, ?, ?, ?)",
            (attempt_id, qid, str(user_choice), 1 if is_correct else 0)
        )

    score_pct = round((correct_count / total * 100) if total > 0 else 0, 1)

    # Save overall attempt to DB
    conn.execute(
        """INSERT OR REPLACE INTO quiz_attempts (id, session_id, lesson_id, started_at, completed_at, score, total_questions, difficulty, mode)
           VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
        (attempt_id, session_id, list(subtopic_stats.keys())[0] if subtopic_stats else 1, now, now, score_pct, total, "Mixed", "Standard")
    )
    conn.commit()
    conn.close()

    # Lesson titles map for weak topic remediation
    lesson_titles = {}
    lessons_file = os.path.join(CONTENT_DIR, "lessons.json")
    if os.path.exists(lessons_file):
        with open(lessons_file, "r", encoding="utf-8") as f:
            for l in json.load(f):
                lesson_titles[l["id"]] = l["title"]

    remediation = [
        {"lesson_id": lid, "title": lesson_titles.get(lid, f"Lesson {lid}")}
        for lid in weak_lessons
    ]

    return {
        "attempt_id": attempt_id,
        "score_pct": score_pct,
        "correct_count": correct_count,
        "total_questions": total,
        "passed": score_pct >= 70.0,
        "results": results,
        "weak_topics_to_revise": remediation
    }

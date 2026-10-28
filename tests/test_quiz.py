# tests/test_quiz.py - Unit tests for Quiz Engine and Scoring
import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app import app
from services.quiz_service import get_filtered_quiz, evaluate_quiz_submission

class TestQuizEngine(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        self.client = app.test_client()

    def test_quiz_generator(self):
        quiz = get_filtered_quiz(count=3)
        self.assertEqual(len(quiz['questions']), 3)
        self.assertTrue(quiz['attempt_id'].startswith('attempt_'))

    def test_quiz_filter_by_lesson(self):
        quiz = get_filtered_quiz(lesson_id=1, count=5)
        for q in quiz['questions']:
            self.assertEqual(q['lesson_id'], 1)

    def test_quiz_evaluation_scoring(self):
        responses = [
            {"question_id": "q1", "selected_answer": 1}, # Correct
            {"question_id": "q2", "selected_answer": 0}  # Incorrect
        ]
        result = evaluate_quiz_submission("test_att_1", "test_sess_1", responses)
        self.assertEqual(result['total_questions'], 2)
        self.assertEqual(result['correct_count'], 1)
        self.assertEqual(result['score_pct'], 50.0)
        self.assertFalse(result['passed'])
        self.assertTrue(len(result['weak_topics_to_revise']) > 0)

if __name__ == '__main__':
    unittest.main()

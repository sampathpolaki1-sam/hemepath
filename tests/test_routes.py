# tests/test_routes.py - Unit tests for Flask route handlers and core endpoints
import unittest
import sys
import os

# Add parent directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app import app

class TestHemePathRoutes(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        self.client = app.test_client()

    def test_health_check(self):
        response = self.client.get('/api/health')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data['status'], 'healthy')
        self.assertEqual(data['lessons_count'], 15)

    def test_homepage(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'HemePath', response.data)
        self.assertIn(b'Anemia &', response.data)

    def test_roadmap_page(self):
        response = self.client.get('/roadmap')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Course Roadmap', response.data)
        self.assertIn(b'Normal Red Blood Cells', response.data)

    def test_lesson_detail(self):
        response = self.client.get('/lesson/1')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Erythropoiesis', response.data)
        self.assertIn(b'Learning Objectives', response.data)

    def test_api_lessons(self):
        response = self.client.get('/api/lessons')
        self.assertEqual(response.status_code, 200)
        lessons = response.get_json()
        self.assertEqual(len(lessons), 15)

    def test_glossary_page(self):
        response = self.client.get('/glossary')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Hematology Glossary', response.data)

    def test_flashcards_page(self):
        response = self.client.get('/flashcards')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Active Recall Flashcards', response.data)

    def test_video_classes_page(self):
        # All videos
        response = self.client.get('/video-classes')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Top-Rated YouTube Medical Classes', response.data)
        self.assertIn(b'Ninja Nerd', response.data)
        self.assertIn(b'Telugu', response.data)
        self.assertIn(b'Hindi', response.data)

        # Telugu filter
        res_te = self.client.get('/video-classes?lang=te')
        self.assertEqual(res_te.status_code, 200)
        self.assertIn(b'Telugu Medicos', res_te.data)

        # Hindi filter
        res_hi = self.client.get('/video-classes?lang=hi')
        self.assertEqual(res_hi.status_code, 200)
        self.assertIn(b'Dr. Preeti Sharma', res_hi.data)

    def test_api_videos(self):
        response = self.client.get('/api/videos')
        self.assertEqual(response.status_code, 200)
        videos = response.get_json()
        self.assertGreaterEqual(len(videos), 15)
        for v in videos:
            self.assertIn('title', v)
            self.assertIn('youtube_id', v)
            self.assertIn('language', v)
            self.assertIn('channel', v)

        # Test language filter
        res_te = self.client.get('/api/videos?lang=te')
        te_vids = res_te.get_json()
        self.assertTrue(all(v['language_code'] == 'te' for v in te_vids))
        self.assertGreaterEqual(len(te_vids), 2)

if __name__ == '__main__':
    unittest.main()

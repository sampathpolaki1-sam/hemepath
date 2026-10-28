# tests/test_tutor.py - Unit tests for medical safety guardrails and chatbot scope
import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
os.environ["TESTING"] = "true"

from services.tutor_service import check_medical_safety, generate_tutor_response

class TestTutorService(unittest.TestCase):
    def test_personal_medical_request_rejected(self):
        query = "My hemoglobin is 8.5, what should I take to cure me?"
        safety = check_medical_safety(query)
        self.assertFalse(safety['safe'])
        self.assertEqual(safety['reason'], 'personal_medical_request')
        self.assertIn("Clinical Safety Warning", safety['message'])

    def test_out_of_scope_query_rejected(self):
        query = "How do you repair a broken lawn mower motor engine?"
        safety = check_medical_safety(query)
        self.assertFalse(safety['safe'])
        self.assertEqual(safety['reason'], 'out_of_scope')
        self.assertIn("Topic Boundary", safety['message'])

    def test_valid_hematology_query_accepted(self):
        query = "Explain why 2,3-BPG causes a right shift in anemia"
        safety = check_medical_safety(query)
        self.assertTrue(safety['safe'])

    def test_tutor_modes_generation(self):
        modes = ["explain_simply", "compare", "mbbs_exam", "diagram"]
        for mode in modes:
            resp = generate_tutor_response("Compare iron deficiency with anemia of chronic disease", mode=mode)
            self.assertIn("reply", resp)
            self.assertIn("disclaimer", resp)
            self.assertTrue(len(resp['citations']) > 0)

if __name__ == '__main__':
    unittest.main()

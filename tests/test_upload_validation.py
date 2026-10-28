# tests/test_upload_validation.py - Unit tests for image validation and OCR handling
import unittest
import io
import sys
import os
from PIL import Image

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
os.environ["TESTING"] = "true"

from services.image_explainer import process_textbook_image, synthesize_textbook_structure

class TestUploadValidation(unittest.TestCase):
    def test_blurred_low_resolution_image_flagging(self):
        # Create a tiny 50x50 image (<200px threshold)
        img = Image.new('RGB', (50, 50), color='white')
        buf = io.BytesIO()
        img.save(buf, format='JPEG')
        image_bytes = buf.getvalue()

        result = process_textbook_image(image_bytes=image_bytes)
        self.assertFalse(result['success'])
        self.assertIn('resolution is too low', result['uncertainty_warning'])

    def test_textbook_synthesis_7_parts(self):
        sample_text = (
            "Iron deficiency is the most common cause of anemia worldwide. "
            "Depletion of storage ferritin leads to impaired heme synthesis and microcytic hypochromic red blood cells. "
            "Total iron binding capacity rises."
        )
        result = synthesize_textbook_structure(sample_text)
        
        # Verify all 7 required components from PDF section 5
        self.assertIn("page_summary", result)
        self.assertIn("simple_explanation", result)
        self.assertIn("mechanism_steps", result)
        self.assertIn("key_terms", result)
        self.assertIn("exam_takeaway", result)
        self.assertIn("recall_questions", result)
        self.assertIn("text_flowchart", result)
        self.assertIn("uncertainty_notes", result)
        self.assertEqual(len(result['recall_questions']), 3)

if __name__ == '__main__':
    unittest.main()

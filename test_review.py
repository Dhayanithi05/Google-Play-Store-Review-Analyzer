import os
import unittest
from review import analyze_sentiment, categorize_reviews, extract_app_id, generate_report


class TestReviewAnalyzer(unittest.TestCase):
    def test_extract_app_id(self):
        self.assertEqual(
            extract_app_id("https://play.google.com/store/apps/details?id=com.example.app"),
            "com.example.app"
        )
        self.assertEqual(
            extract_app_id("https://play.google.com/store/apps/details?id=com.example.app&hl=en"),
            "com.example.app"
        )
        self.assertEqual(extract_app_id("com.example.app"), "com.example.app")

    def test_analyze_sentiment(self):
        self.assertGreater(analyze_sentiment("Great app, love it!"), 0)
        self.assertLess(analyze_sentiment("Terrible app, hate it!"), 0)

    def test_categorize_reviews(self):
        reviews = [
            {"content": "Great app!"},
            {"content": "Terrible app!"},
            {"content": "Meh."}
        ]
        res = categorize_reviews(reviews)
        self.assertEqual(len(res["Positive"]), 1)
        self.assertEqual(len(res["Negative"]), 1)
        self.assertEqual(len(res["Neutral"]), 1)

    def test_generate_report(self):
        reviews = [{"content": "Good app"}]
        test_app_id = "test_app_id_unittest"
        pdf_filename = f"{test_app_id}_review_report.pdf"

        try:
            generate_report(test_app_id, reviews)
            self.assertTrue(os.path.exists(pdf_filename))
        finally:
            if os.path.exists(pdf_filename):
                os.remove(pdf_filename)


if __name__ == "__main__":
    unittest.main()

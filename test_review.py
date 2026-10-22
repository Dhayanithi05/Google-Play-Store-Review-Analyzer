import os
import unittest
from review import (
    extract_app_id,
    analyze_sentiment,
    categorize_reviews,
    create_pie_chart,
    generate_report,
)


class TestReviewAnalyzer(unittest.TestCase):

    def test_extract_app_id(self):
        url = "https://play.google.com/store/apps/details?id=com.example.app&hl=en"
        self.assertEqual(extract_app_id(url), "com.example.app")

        raw_id = "com.example.app"
        self.assertEqual(extract_app_id(raw_id), "com.example.app")

    def test_analyze_sentiment(self):
        pos_score = analyze_sentiment("Great app! Loved it.")
        neg_score = analyze_sentiment("Horrible experience, crashes always.")
        self.assertGreater(pos_score, 0)
        self.assertLess(neg_score, 0)

    def test_categorize_reviews(self):
        reviews_data = [
            {"content": "Awesome application!"},
            {"content": "This application was downloaded on Tuesday."},
            {"content": "Terrible bug, terrible software."},
        ]
        categorized = categorize_reviews(reviews_data)
        self.assertIn("Positive", categorized)
        self.assertIn("Neutral", categorized)
        self.assertIn("Negative", categorized)
        self.assertEqual(len(categorized["Positive"]), 1)
        self.assertEqual(len(categorized["Neutral"]), 1)
        self.assertEqual(len(categorized["Negative"]), 1)

    def test_create_pie_chart(self):
        filename = "test_sentiment_chart.png"
        sentiment_counts = {"Positive": 10, "Neutral": 5, "Negative": 2}
        try:
            create_pie_chart(sentiment_counts, filename=filename)
            self.assertTrue(os.path.exists(filename))
        finally:
            if os.path.exists(filename):
                os.remove(filename)

    def test_generate_report(self):
        app_id = "com.test.app"
        pdf_filename = f"{app_id}_review_report.pdf"
        reviews_data = [
            {"content": "Very good app!"},
            {"content": "Bad app."},
        ]
        try:
            generate_report(app_id, reviews_data)
            self.assertTrue(os.path.exists(pdf_filename))
        finally:
            if os.path.exists(pdf_filename):
                os.remove(pdf_filename)


if __name__ == "__main__":
    unittest.main()

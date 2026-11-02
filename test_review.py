import os
import unittest
from unittest.mock import patch

from review import (
    analyze_sentiment,
    categorize_reviews,
    create_pie_chart,
    extract_app_id,
    generate_report,
)


class TestReviewAnalyzer(unittest.TestCase):
    def test_extract_app_id_url(self):
        url = "https://play.google.com/store/apps/details?id=com.example.app&hl=en"
        self.assertEqual(extract_app_id(url), "com.example.app")

    def test_extract_app_id_plain(self):
        app_id = "com.example.app"
        self.assertEqual(extract_app_id(app_id), "com.example.app")

    def test_analyze_sentiment(self):
        positive_text = "This application is wonderful and amazing!"
        negative_text = "This application is terrible and awful."
        self.assertGreater(analyze_sentiment(positive_text), 0.1)
        self.assertLess(analyze_sentiment(negative_text), -0.1)

    def test_categorize_reviews(self):
        reviews_data = [
            {"content": "I love this app, works great!"},
            {"content": "Worst app ever, completely unusable and broken."},
            {"content": "It is an app."},
        ]
        categorized = categorize_reviews(reviews_data)
        self.assertIn("Positive", categorized)
        self.assertIn("Neutral", categorized)
        self.assertIn("Negative", categorized)
        self.assertEqual(len(categorized["Positive"]), 1)
        self.assertEqual(len(categorized["Negative"]), 1)
        self.assertEqual(len(categorized["Neutral"]), 1)

    def test_create_pie_chart(self):
        test_filename = "test_chart.png"
        sentiment_counts = {"Positive": 10, "Neutral": 5, "Negative": 2}
        try:
            create_pie_chart(sentiment_counts, test_filename)
            self.assertTrue(os.path.exists(test_filename))
            self.assertGreater(os.path.getsize(test_filename), 0)
        finally:
            if os.path.exists(test_filename):
                os.remove(test_filename)

    def test_generate_report(self):
        app_id = "test_app_id"
        pdf_filename = f"{app_id}_review_report.pdf"
        reviews_data = [
            {"content": "Great experience!"},
            {"content": "Bad experience."},
        ]
        try:
            with patch("builtins.print"):
                generate_report(app_id, reviews_data)
            self.assertTrue(os.path.exists(pdf_filename))
            self.assertGreater(os.path.getsize(pdf_filename), 0)
            # Ensure temporary sentiment chart file was cleaned up
            self.assertFalse(os.path.exists("sentiment_chart.png"))
        finally:
            if os.path.exists(pdf_filename):
                os.remove(pdf_filename)


if __name__ == "__main__":
    unittest.main()

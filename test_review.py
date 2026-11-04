import os
import unittest
from unittest.mock import patch

from review import (
    analyze_sentiment,
    categorize_reviews,
    create_pie_chart,
    extract_app_id,
    fetch_reviews,
    generate_report,
)


class TestReviewAnalyzer(unittest.TestCase):
    def test_extract_app_id_from_url(self):
        url = "https://play.google.com/store/apps/details?id=com.spotify.music&hl=en"
        self.assertEqual(extract_app_id(url), "com.spotify.music")

    def test_extract_app_id_plain_id(self):
        app_id = "com.spotify.music"
        self.assertEqual(extract_app_id(app_id), "com.spotify.music")

    def test_analyze_sentiment_positive(self):
        text = "This app is absolutely amazing, wonderful, and fantastic!"
        polarity = analyze_sentiment(text)
        self.assertGreater(polarity, 0.1)

    def test_analyze_sentiment_negative(self):
        text = "This app is terrible, horrible, worst ever, completely broken!"
        polarity = analyze_sentiment(text)
        self.assertLess(polarity, -0.1)

    def test_categorize_reviews(self):
        reviews_data = [
            {"content": "This is amazing, excellent, great!"},
            {"content": "This is terrible, horrible, worst app ever!"},
            {"content": "This is an app with basic neutral statements."},
        ]
        categorized = categorize_reviews(reviews_data)
        self.assertIn("Positive", categorized)
        self.assertIn("Neutral", categorized)
        self.assertIn("Negative", categorized)
        self.assertEqual(len(categorized["Positive"]), 1)
        self.assertEqual(len(categorized["Negative"]), 1)
        self.assertEqual(len(categorized["Neutral"]), 1)

    def test_create_pie_chart(self):
        test_filename = "test_chart_output.png"
        try:
            counts = {"Positive": 10, "Neutral": 5, "Negative": 2}
            create_pie_chart(counts, filename=test_filename)
            self.assertTrue(os.path.exists(test_filename))
            self.assertGreater(os.path.getsize(test_filename), 0)
        finally:
            if os.path.exists(test_filename):
                os.remove(test_filename)

    def test_generate_report(self):
        app_id = "com.test.app"
        expected_pdf = f"{app_id}_review_report.pdf"
        try:
            reviews_data = [
                {"content": "Great experience, loved using it!"},
                {"content": "Awful and crashy."},
            ]
            generate_report(app_id, reviews_data)
            self.assertTrue(os.path.exists(expected_pdf))
            self.assertGreater(os.path.getsize(expected_pdf), 0)
            self.assertFalse(os.path.exists("sentiment_chart.png"))
        finally:
            if os.path.exists(expected_pdf):
                os.remove(expected_pdf)

    @patch("review.reviews")
    def test_fetch_reviews(self, mock_reviews):
        mock_reviews.return_value = ([{"content": "Great!"}], None)
        result = fetch_reviews("com.test.app", num_reviews=1)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["content"], "Great!")


if __name__ == "__main__":
    unittest.main()

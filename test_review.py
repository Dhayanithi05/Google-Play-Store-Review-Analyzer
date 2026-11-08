import io
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


class TestReview(unittest.TestCase):
    def test_extract_app_id_url(self):
        url = "https://play.google.com/store/apps/details?id=com.spotify.music&hl=en"
        self.assertEqual(extract_app_id(url), "com.spotify.music")

    def test_extract_app_id_direct(self):
        app_id = "com.spotify.music"
        self.assertEqual(extract_app_id(app_id), "com.spotify.music")

    def test_analyze_sentiment_positive_and_caching(self):
        text = "This app is absolutely amazing and wonderful!"
        score1 = analyze_sentiment(text)
        self.assertGreater(score1, 0.1)

        # Verify caching works by inspecting cache_info
        info_before = analyze_sentiment.cache_info()
        score2 = analyze_sentiment(text)
        info_after = analyze_sentiment.cache_info()
        self.assertEqual(score1, score2)
        self.assertEqual(info_after.hits, info_before.hits + 1)

    def test_analyze_sentiment_negative(self):
        text = "This app is terrible, horrible, and completely broken."
        score = analyze_sentiment(text)
        self.assertLess(score, -0.1)

    def test_categorize_reviews(self):
        sample_reviews = [
            {"content": "Love this app, it is great!"},
            {"content": "Awful and worst app ever."},
            {"content": "It is an application."},
        ]
        categorized = categorize_reviews(sample_reviews)
        self.assertIn("Love this app, it is great!", categorized["Positive"])
        self.assertIn("Awful and worst app ever.", categorized["Negative"])
        self.assertIn("It is an application.", categorized["Neutral"])

    def test_create_pie_chart_in_memory(self):
        sentiment_counts = {"Positive": 10, "Neutral": 5, "Negative": 2}
        buf = create_pie_chart(sentiment_counts)
        self.assertIsInstance(buf, io.BytesIO)
        content = buf.getvalue()
        self.assertGreater(len(content), 0)
        # PNG signature check: \x89PNG\r\n\x1a\n
        self.assertTrue(content.startswith(b"\x89PNG\r\n\x1a\n"))

    def test_create_pie_chart_to_file(self):
        filename = "test_sentiment_chart.png"
        try:
            sentiment_counts = {"Positive": 5, "Neutral": 3, "Negative": 1}
            res = create_pie_chart(sentiment_counts, target=filename)
            self.assertEqual(res, filename)
            self.assertTrue(os.path.exists(filename))
            self.assertGreater(os.path.getsize(filename), 0)
        finally:
            if os.path.exists(filename):
                os.remove(filename)

    def test_generate_report(self):
        app_id = "com.test.app"
        expected_pdf = f"{app_id}_review_report.pdf"
        sample_reviews = [
            {"content": "Very helpful and clean design."},
            {"content": "Crashes on startup, unusable."},
        ]
        try:
            generate_report(app_id, sample_reviews)
            self.assertTrue(os.path.exists(expected_pdf))
            self.assertGreater(os.path.getsize(expected_pdf), 0)
        finally:
            if os.path.exists(expected_pdf):
                os.remove(expected_pdf)

    @patch("review.reviews")
    def test_fetch_reviews(self, mock_reviews):
        mock_reviews.return_value = ([{"content": "Good"}], None)
        result = fetch_reviews("com.test.app", num_reviews=10)
        self.assertEqual(result, [{"content": "Good"}])
        mock_reviews.assert_called_once()


if __name__ == "__main__":
    unittest.main()

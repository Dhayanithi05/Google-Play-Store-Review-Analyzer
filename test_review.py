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
    def setUp(self):
        # Clear LRU cache before each test to guarantee fresh state
        analyze_sentiment.cache_clear()

    def test_extract_app_id_from_url(self):
        url = "https://play.google.com/store/apps/details?id=com.spotify.music&hl=en"
        self.assertEqual(extract_app_id(url), "com.spotify.music")

    def test_extract_app_id_plain_id(self):
        app_id = "com.spotify.music"
        self.assertEqual(extract_app_id(app_id), "com.spotify.music")

    def test_analyze_sentiment_polarity(self):
        pos_score = analyze_sentiment("This app is absolutely wonderful and great!")
        neg_score = analyze_sentiment("This app is terrible, horrible, and keeps crashing.")
        neu_score = analyze_sentiment("This is an application.")

        self.assertGreater(pos_score, 0.1)
        self.assertLess(neg_score, -0.1)
        self.assertAlmostEqual(neu_score, 0.0, places=1)

    def test_analyze_sentiment_lru_cache(self):
        text = "Fast and intuitive user interface!"
        # First call: cache miss
        analyze_sentiment(text)
        info_after_first = analyze_sentiment.cache_info()
        self.assertEqual(info_after_first.hits, 0)
        self.assertEqual(info_after_first.misses, 1)

        # Second call: cache hit
        analyze_sentiment(text)
        info_after_second = analyze_sentiment.cache_info()
        self.assertEqual(info_after_second.hits, 1)
        self.assertEqual(info_after_second.misses, 1)

    def test_categorize_reviews(self):
        sample_data = [
            {"content": "Amazing product, totally love it!"},
            {"content": "Awful and useless, complete garbage."},
            {"content": "It is an app on Android."},
            {"content": "Amazing product, totally love it!"},  # Duplicate to trigger cache
        ]
        categorized = categorize_reviews(sample_data)
        self.assertEqual(len(categorized["Positive"]), 2)
        self.assertEqual(len(categorized["Negative"]), 1)
        self.assertEqual(len(categorized["Neutral"]), 1)

    def test_create_pie_chart(self):
        chart_filename = "test_sentiment_chart.png"
        try:
            counts = {"Positive": 10, "Neutral": 5, "Negative": 2}
            create_pie_chart(counts, chart_filename)
            self.assertTrue(os.path.exists(chart_filename))
            self.assertGreater(os.path.getsize(chart_filename), 0)
        finally:
            if os.path.exists(chart_filename):
                os.remove(chart_filename)

    def test_generate_report(self):
        app_id = "test.unit.app"
        report_filename = f"{app_id}_review_report.pdf"
        chart_filename = "sentiment_chart.png"
        sample_data = [
            {"content": "Great tool, very fast!"},
            {"content": "Too many ads and bad design."},
            {"content": "Just okay."},
        ]
        try:
            generate_report(app_id, sample_data)
            self.assertTrue(os.path.exists(report_filename))
            self.assertGreater(os.path.getsize(report_filename), 0)
            # Ensure temporary chart is cleaned up
            self.assertFalse(os.path.exists(chart_filename))
        finally:
            if os.path.exists(report_filename):
                os.remove(report_filename)

    @patch("review.reviews")
    def test_fetch_reviews(self, mock_reviews):
        mock_reviews.return_value = ([{"content": "Review 1"}], None)
        result = fetch_reviews("com.dummy.app", num_reviews=5)
        self.assertEqual(result, [{"content": "Review 1"}])
        mock_reviews.assert_called_once()


if __name__ == "__main__":
    unittest.main()

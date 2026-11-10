import os
import unittest

from review import (
    analyze_sentiment,
    categorize_reviews,
    extract_app_id,
    generate_report,
)


class TestReviewAnalyzer(unittest.TestCase):
    def test_extract_app_id(self):
        url = "https://play.google.com/store/apps/details?id=com.spotify.music&hl=en"
        self.assertEqual(extract_app_id(url), "com.spotify.music")
        self.assertEqual(extract_app_id("com.spotify.music"), "com.spotify.music")

    def test_analyze_sentiment_polarity(self):
        positive = analyze_sentiment("This app is amazing and absolutely wonderful!")
        negative = analyze_sentiment("This app is terrible and horrible.")
        neutral = analyze_sentiment("This is a mobile application.")

        self.assertGreater(positive, 0.1)
        self.assertLess(negative, -0.1)
        self.assertAlmostEqual(neutral, 0.0, places=1)

    def test_categorize_reviews(self):
        reviews_data = [
            {"content": "This app is amazing and great!"},
            {"content": "This app is terrible and bad!"},
            {"content": "This is an app."},
        ]
        categorized = categorize_reviews(reviews_data)
        self.assertIn("This app is amazing and great!", categorized["Positive"])
        self.assertIn("This app is terrible and bad!", categorized["Negative"])
        self.assertIn("This is an app.", categorized["Neutral"])
        self.assertEqual(len(categorized["Positive"]), 1)
        self.assertEqual(len(categorized["Negative"]), 1)
        self.assertEqual(len(categorized["Neutral"]), 1)

    def test_generate_report(self):
        app_id = "test_app_unit"
        reviews_data = [
            {"content": "Great app, highly recommend!"},
            {"content": "Awful experience."},
        ]
        pdf_filename = f"{app_id}_review_report.pdf"
        chart_filename = "sentiment_chart.png"
        try:
            generate_report(app_id, reviews_data)
            self.assertTrue(os.path.exists(pdf_filename))
            # Chart should be cleaned up
            self.assertFalse(os.path.exists(chart_filename))
        finally:
            if os.path.exists(pdf_filename):
                os.remove(pdf_filename)
            if os.path.exists(chart_filename):
                os.remove(chart_filename)


if __name__ == "__main__":
    unittest.main()

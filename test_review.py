import os
import unittest

from review import (
    analyze_sentiment,
    categorize_reviews,
    create_pie_chart,
    extract_app_id,
    generate_report,
)


class TestReviewAnalyzer(unittest.TestCase):
    def test_extract_app_id(self):
        url = "https://play.google.com/store/apps/details?id=com.example.app&hl=en"
        self.assertEqual(extract_app_id(url), "com.example.app")

        plain_id = "com.example.app"
        self.assertEqual(extract_app_id(plain_id), "com.example.app")

    def test_analyze_sentiment(self):
        positive_text = "This app is absolutely amazing, great job!"
        negative_text = "Terrible app, crashes constantly and horrible support."
        neutral_text = "This is an app on the Google Play Store."

        self.assertGreater(analyze_sentiment(positive_text), 0.1)
        self.assertLess(analyze_sentiment(negative_text), -0.1)
        self.assertTrue(-0.1 <= analyze_sentiment(neutral_text) <= 0.1)

    def test_categorize_reviews(self):
        reviews_data = [
            {"content": "This app is wonderful and very helpful!"},
            {"content": "Awful experience, totally broken and useless."},
            {"content": "It opens and closes."},
        ]
        categorized = categorize_reviews(reviews_data)
        self.assertIn("Positive", categorized)
        self.assertIn("Negative", categorized)
        self.assertIn("Neutral", categorized)
        self.assertEqual(len(categorized["Positive"]), 1)
        self.assertEqual(len(categorized["Negative"]), 1)
        self.assertEqual(len(categorized["Neutral"]), 1)

    def test_create_pie_chart(self):
        chart_file = "test_chart_output.png"
        try:
            sentiment_counts = {"Positive": 10, "Neutral": 5, "Negative": 2}
            create_pie_chart(sentiment_counts, chart_file)
            self.assertTrue(os.path.exists(chart_file))
            self.assertGreater(os.path.getsize(chart_file), 0)
        finally:
            if os.path.exists(chart_file):
                os.remove(chart_file)

    def test_generate_report(self):
        app_id = "com.test.unit"
        report_pdf = f"{app_id}_review_report.pdf"
        chart_file = "sentiment_chart.png"
        sample_reviews = [
            {"content": "Superb application! Loved it."},
            {"content": "Horrible, ruined my phone."},
            {"content": "Average app with neutral feedback."},
        ]

        try:
            generate_report(app_id, sample_reviews)
            self.assertTrue(os.path.exists(report_pdf))
            self.assertGreater(os.path.getsize(report_pdf), 0)
            # The temporary chart file should have been cleaned up
            self.assertFalse(os.path.exists(chart_file))
        finally:
            if os.path.exists(report_pdf):
                os.remove(report_pdf)
            if os.path.exists(chart_file):
                os.remove(chart_file)


if __name__ == "__main__":
    unittest.main()

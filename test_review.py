import io
import os
import unittest

from review import (
    analyze_sentiment,
    categorize_reviews,
    create_pie_chart,
    extract_app_id,
    generate_report,
)


class TestReview(unittest.TestCase):
    def test_extract_app_id_from_url(self):
        url = "https://play.google.com/store/apps/details?id=com.example.app&hl=en"
        self.assertEqual(extract_app_id(url), "com.example.app")

    def test_extract_app_id_from_plain_id(self):
        app_id = "com.example.app"
        self.assertEqual(extract_app_id(app_id), "com.example.app")

    def test_analyze_sentiment_positive(self):
        positive_text = "This application is absolutely amazing and wonderful!"
        self.assertGreater(analyze_sentiment(positive_text), 0.1)

    def test_analyze_sentiment_negative(self):
        negative_text = "This application is terrible, horribly broken and crashes."
        self.assertLess(analyze_sentiment(negative_text), -0.1)

    def test_categorize_reviews(self):
        reviews_data = [
            {"content": "This application is absolutely wonderful and great!"},
            {"content": "Terrible app, completely broken and useless."},
            {"content": "It is an app with basic functionality."},
        ]
        categorized = categorize_reviews(reviews_data)
        self.assertEqual(len(categorized["Positive"]), 1)
        self.assertEqual(len(categorized["Negative"]), 1)
        self.assertEqual(len(categorized["Neutral"]), 1)

    def test_create_pie_chart_in_memory(self):
        sentiment_counts = {"Positive": 10, "Neutral": 5, "Negative": 2}
        buf = create_pie_chart(sentiment_counts)
        self.assertIsInstance(buf, io.BytesIO)
        content = buf.getvalue()
        # Verify PNG header
        self.assertTrue(content.startswith(b"\x89PNG\r\n\x1a\n"))

    def test_create_pie_chart_to_file(self):
        sentiment_counts = {"Positive": 10, "Neutral": 5, "Negative": 2}
        test_filename = "test_chart_output.png"
        try:
            create_pie_chart(sentiment_counts, target=test_filename)
            self.assertTrue(os.path.exists(test_filename))
            self.assertGreater(os.path.getsize(test_filename), 0)
        finally:
            if os.path.exists(test_filename):
                os.remove(test_filename)

    def test_generate_report_no_temp_disk_artifacts(self):
        app_id = "test_app_id"
        expected_pdf = f"{app_id}_review_report.pdf"
        reviews_data = [
            {"content": "Amazing application!"},
            {"content": "Terrible application!"},
            {"content": "Average application."},
        ]
        try:
            generate_report(app_id, reviews_data)
            self.assertTrue(os.path.exists(expected_pdf))
            # Verify no intermediate chart file was created on disk
            self.assertFalse(os.path.exists("sentiment_chart.png"))
        finally:
            if os.path.exists(expected_pdf):
                os.remove(expected_pdf)


if __name__ == "__main__":
    unittest.main()

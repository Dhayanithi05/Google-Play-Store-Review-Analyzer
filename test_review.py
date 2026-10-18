import unittest
import os
import review
from reportlab.graphics.shapes import Drawing

class TestReviewAnalyzer(unittest.TestCase):
    def test_extract_app_id(self):
        url = "https://play.google.com/store/apps/details?id=com.example.app"
        self.assertEqual(review.extract_app_id(url), "com.example.app")
        self.assertEqual(review.extract_app_id("com.example.app"), "com.example.app")

    def test_analyze_sentiment(self):
        self.assertGreater(review.analyze_sentiment("Great app! Love it."), 0)
        self.assertLess(review.analyze_sentiment("Terrible app! Hate it."), 0)

    def test_categorize_reviews(self):
        reviews_data = [
            {"content": "Great app! Love it."},
            {"content": "This is an app."},
            {"content": "Terrible app! Hate it."}
        ]
        categorized = review.categorize_reviews(reviews_data)
        self.assertIn("Great app! Love it.", categorized["Positive"])
        self.assertIn("This is an app.", categorized["Neutral"])
        self.assertIn("Terrible app! Hate it.", categorized["Negative"])

    def test_create_pie_chart(self):
        sentiment_counts = {"Positive": 10, "Neutral": 5, "Negative": 2}
        chart = review.create_pie_chart(sentiment_counts)
        self.assertIsInstance(chart, Drawing)

    def test_generate_report(self):
        app_id = "com.test.app"
        filename = f"{app_id}_review_report.pdf"
        if os.path.exists(filename):
            os.remove(filename)

        mock_reviews = [
            {"content": "Great app! Love it."},
            {"content": "This is an app."},
            {"content": "Terrible app! Hate it."}
        ]

        review.generate_report(app_id, mock_reviews)
        self.assertTrue(os.path.exists(filename))

        # Cleanup
        if os.path.exists(filename):
            os.remove(filename)

if __name__ == '__main__':
    unittest.main()

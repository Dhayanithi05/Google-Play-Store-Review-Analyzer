import os
import unittest
from review import analyze_sentiment, categorize_reviews, create_pie_chart, generate_report

class TestReviewAnalyzer(unittest.TestCase):

    def test_analyze_sentiment(self):
        positive_score = analyze_sentiment("This app is amazing and wonderful!")
        negative_score = analyze_sentiment("This app is terrible and horrible!")
        neutral_score = analyze_sentiment("This is an app.")

        self.assertGreater(positive_score, 0.1)
        self.assertLess(negative_score, -0.1)
        self.assertAlmostEqual(neutral_score, 0.0, places=1)

    def test_categorize_reviews(self):
        reviews_data = [
            {"content": "Great app, love it!"},
            {"content": "Awful experience, hates it."},
            {"content": "It is an application."}
        ]
        categorized = categorize_reviews(reviews_data)
        self.assertIn("Great app, love it!", categorized["Positive"])
        self.assertIn("Awful experience, hates it.", categorized["Negative"])
        self.assertIn("It is an application.", categorized["Neutral"])

    def test_create_pie_chart(self):
        chart_filename = "test_chart.png"
        sentiment_counts = {"Positive": 10, "Neutral": 5, "Negative": 2}
        try:
            create_pie_chart(sentiment_counts, chart_filename)
            self.assertTrue(os.path.exists(chart_filename))
        finally:
            if os.path.exists(chart_filename):
                os.remove(chart_filename)

    def test_generate_report(self):
        app_id = "com.test.app"
        report_filename = f"{app_id}_review_report.pdf"
        reviews_data = [
            {"content": "Super app!"},
            {"content": "Bad app!"}
        ]
        try:
            generate_report(app_id, reviews_data)
            self.assertTrue(os.path.exists(report_filename))
        finally:
            if os.path.exists(report_filename):
                os.remove(report_filename)

if __name__ == "__main__":
    unittest.main()

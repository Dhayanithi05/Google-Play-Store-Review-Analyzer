import os
import unittest
from review import extract_app_id, analyze_sentiment, categorize_reviews, create_pie_chart, generate_report

class TestReviewAnalyzer(unittest.TestCase):

    def test_extract_app_id(self):
        url = "https://play.google.com/store/apps/details?id=com.spotify.music&hl=en"
        self.assertEqual(extract_app_id(url), "com.spotify.music")

        direct_id = "com.spotify.music"
        self.assertEqual(extract_app_id(direct_id), "com.spotify.music")

    def test_analyze_sentiment(self):
        positive = analyze_sentiment("This app is amazing and wonderful!")
        negative = analyze_sentiment("This app is terrible and useless.")
        self.assertGreater(positive, 0.1)
        self.assertLess(negative, -0.1)

    def test_analyze_sentiment_caching(self):
        # Clear cache before test
        analyze_sentiment.cache_clear()

        text = "Great user experience and fast performance."
        val1 = analyze_sentiment(text)
        val2 = analyze_sentiment(text)

        info = analyze_sentiment.cache_info()
        self.assertEqual(val1, val2)
        self.assertEqual(info.hits, 1)

    def test_categorize_reviews(self):
        reviews = [
            {"content": "I love this app, it is amazing!"},
            {"content": "The app updated on Monday."},
            {"content": "Worst app ever, constantly crashes."}
        ]
        categorized = categorize_reviews(reviews)
        self.assertEqual(len(categorized["Positive"]), 1)
        self.assertEqual(len(categorized["Neutral"]), 1)
        self.assertEqual(len(categorized["Negative"]), 1)

    def test_create_pie_chart(self):
        chart_file = "test_chart.png"
        if os.path.exists(chart_file):
            os.remove(chart_file)

        create_pie_chart({"Positive": 10, "Neutral": 5, "Negative": 2}, filename=chart_file)
        self.assertTrue(os.path.exists(chart_file))
        os.remove(chart_file)

    def test_generate_report(self):
        app_id = "com.example.testapp"
        report_file = f"{app_id}_review_report.pdf"
        if os.path.exists(report_file):
            os.remove(report_file)

        reviews = [
            {"content": "Fantastic app!"},
            {"content": "It works as expected."},
            {"content": "Terrible experience."}
        ]
        generate_report(app_id, reviews)
        self.assertTrue(os.path.exists(report_file))
        os.remove(report_file)

if __name__ == "__main__":
    unittest.main()

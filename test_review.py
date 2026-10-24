import unittest
import os
from review import analyze_sentiment, categorize_reviews, create_pie_chart, generate_report, extract_app_id

class TestReviewAnalyzer(unittest.TestCase):

    def test_analyze_sentiment(self):
        positive_score = analyze_sentiment("This app is amazing and wonderful!")
        negative_score = analyze_sentiment("This app is awful, terrible, and useless.")

        self.assertGreater(positive_score, 0)
        self.assertLess(negative_score, 0)

    def test_analyze_sentiment_caching(self):
        # Clear cache prior to test
        analyze_sentiment.cache_clear()

        text = "Caching performance test review string."

        # First call: cache miss
        _ = analyze_sentiment(text)
        info1 = analyze_sentiment.cache_info()
        self.assertEqual(info1.hits, 0)
        self.assertEqual(info1.misses, 1)

        # Second call: cache hit
        _ = analyze_sentiment(text)
        info2 = analyze_sentiment.cache_info()
        self.assertEqual(info2.hits, 1)
        self.assertEqual(info2.misses, 1)

    def test_categorize_reviews(self):
        reviews_data = [
            {'content': 'Super fast and helpful app!'},
            {'content': 'It is an app.'},
            {'content': 'Horrible crash issue, very bad!'}
        ]

        categorized = categorize_reviews(reviews_data)
        self.assertIn('Positive', categorized)
        self.assertIn('Neutral', categorized)
        self.assertIn('Negative', categorized)
        self.assertEqual(len(categorized['Positive']), 1)
        self.assertEqual(len(categorized['Neutral']), 1)
        self.assertEqual(len(categorized['Negative']), 1)

    def test_extract_app_id(self):
        url = "https://play.google.com/store/apps/details?id=com.example.app&hl=en"
        self.assertEqual(extract_app_id(url), "com.example.app")

        plain_id = "com.example.app"
        self.assertEqual(extract_app_id(plain_id), "com.example.app")

    def test_create_pie_chart_and_generate_report(self):
        app_id = "com.test.sample"
        report_filename = f"{app_id}_review_report.pdf"

        if os.path.exists(report_filename):
            os.remove(report_filename)

        mock_reviews = [
            {'content': 'Great product!'},
            {'content': 'Bad experience.'}
        ]

        generate_report(app_id, mock_reviews)
        self.assertTrue(os.path.exists(report_filename))

        # Clean up generated PDF
        if os.path.exists(report_filename):
            os.remove(report_filename)

if __name__ == '__main__':
    unittest.main()

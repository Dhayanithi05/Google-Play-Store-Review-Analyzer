import unittest
import os
from review import analyze_sentiment, categorize_reviews, generate_report, extract_app_id

class TestReviewAnalyzer(unittest.TestCase):

    def setUp(self):
        analyze_sentiment.cache_clear()

    def test_extract_app_id(self):
        url = "https://play.google.com/store/apps/details?id=com.example.app&hl=en"
        self.assertEqual(extract_app_id(url), "com.example.app")
        self.assertEqual(extract_app_id("com.example.app"), "com.example.app")

    def test_analyze_sentiment_and_caching(self):
        text = "This application is absolutely amazing and wonderful!"

        # Initial call
        score1 = analyze_sentiment(text)
        self.assertGreater(score1, 0.1)
        cache_info1 = analyze_sentiment.cache_info()
        self.assertEqual(cache_info1.hits, 0)
        self.assertEqual(cache_info1.misses, 1)

        # Second call with same input should hit cache
        score2 = analyze_sentiment(text)
        self.assertEqual(score1, score2)
        cache_info2 = analyze_sentiment.cache_info()
        self.assertEqual(cache_info2.hits, 1)
        self.assertEqual(cache_info2.misses, 1)

    def test_categorize_reviews(self):
        sample_reviews = [
            {'content': 'Awesome app, highly recommended!'},
            {'content': 'Worst app ever, keeps crashing and deleting my data.'},
            {'content': 'Meh'}
        ]
        categorized = categorize_reviews(sample_reviews)
        self.assertEqual(len(categorized['Positive']), 1)
        self.assertEqual(len(categorized['Negative']), 1)
        self.assertEqual(len(categorized['Neutral']), 1)

    def test_generate_report(self):
        app_id = "com.test.app"
        sample_reviews = [
            {'content': 'Great app!'},
            {'content': 'Terrible experience.'}
        ]
        pdf_filename = f"{app_id}_review_report.pdf"
        try:
            generate_report(app_id, sample_reviews)
            self.assertTrue(os.path.exists(pdf_filename))
        finally:
            if os.path.exists(pdf_filename):
                os.remove(pdf_filename)

if __name__ == '__main__':
    unittest.main()

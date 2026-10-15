import unittest
from review import analyze_sentiment, categorize_reviews, extract_app_id

class TestReviewAnalysis(unittest.TestCase):
    def setUp(self):
        analyze_sentiment.cache_clear()

    def test_extract_app_id(self):
        url = "https://play.google.com/store/apps/details?id=com.example.app&hl=en"
        self.assertEqual(extract_app_id(url), "com.example.app")
        self.assertEqual(extract_app_id("com.example.app"), "com.example.app")

    def test_analyze_sentiment(self):
        pos_score = analyze_sentiment("Great app! Loved it.")
        neg_score = analyze_sentiment("Horrible app, crashes every time.")
        self.assertGreater(pos_score, 0)
        self.assertLess(neg_score, 0)

    def test_sentiment_caching(self):
        # Initial call cache info
        info_before = analyze_sentiment.cache_info()
        analyze_sentiment("Excellent user interface!")
        info_after_first = analyze_sentiment.cache_info()
        self.assertEqual(info_after_first.hits, info_before.hits)
        self.assertEqual(info_after_first.misses, info_before.misses + 1)

        # Call with identical string
        analyze_sentiment("Excellent user interface!")
        info_after_second = analyze_sentiment.cache_info()
        self.assertEqual(info_after_second.hits, info_before.hits + 1)

    def test_categorize_reviews(self):
        sample_reviews = [
            {'content': 'Great app! Loved it.'},
            {'content': 'Horrible app, crashes every time.'},
            {'content': 'nothing'}
        ]
        categorized = categorize_reviews(sample_reviews)
        self.assertIn('Great app! Loved it.', categorized['Positive'])
        self.assertIn('Horrible app, crashes every time.', categorized['Negative'])
        self.assertIn('nothing', categorized['Neutral'])

if __name__ == '__main__':
    unittest.main()

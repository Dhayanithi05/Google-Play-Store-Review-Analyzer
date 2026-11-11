import unittest
from review import analyze_sentiment, categorize_reviews


class TestReviewAnalysis(unittest.TestCase):
    def setUp(self):
        # Clear lru_cache between test runs to ensure test isolation
        analyze_sentiment.cache_clear()

    def test_analyze_sentiment_positive(self):
        polarity = analyze_sentiment("This app is amazing and very useful!")
        self.assertGreater(polarity, 0.1)

    def test_analyze_sentiment_negative(self):
        polarity = analyze_sentiment("Terrible app, crashes constantly and doesn't work.")
        self.assertLess(polarity, -0.1)

    def test_analyze_sentiment_neutral(self):
        polarity = analyze_sentiment("The application is an app.")
        self.assertAlmostEqual(polarity, 0.0, places=2)

    def test_analyze_sentiment_empty_and_whitespace(self):
        self.assertEqual(analyze_sentiment(""), 0.0)
        self.assertEqual(analyze_sentiment("   \n\t  "), 0.0)

    def test_analyze_sentiment_caching(self):
        # Initial call should be a cache miss
        info_before = analyze_sentiment.cache_info()
        analyze_sentiment("Great product!")
        info_after_miss = analyze_sentiment.cache_info()
        self.assertEqual(info_after_miss.misses, info_before.misses + 1)

        # Repeating call should be a cache hit
        analyze_sentiment("Great product!")
        info_after_hit = analyze_sentiment.cache_info()
        self.assertEqual(info_after_hit.hits, info_before.hits + 1)

    def test_categorize_reviews(self):
        reviews_data = [
            {"content": "Awesome application, highly recommended!"},
            {"content": "Horrible bug-ridden mess."},
            {"content": "It is an app."},
            {"content": ""},
        ]
        categorized = categorize_reviews(reviews_data)

        self.assertIn("Positive", categorized)
        self.assertIn("Neutral", categorized)
        self.assertIn("Negative", categorized)

        self.assertIn("Awesome application, highly recommended!", categorized["Positive"])
        self.assertIn("Horrible bug-ridden mess.", categorized["Negative"])
        self.assertIn("It is an app.", categorized["Neutral"])
        self.assertIn("", categorized["Neutral"])


if __name__ == "__main__":
    unittest.main()

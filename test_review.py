import unittest
from review import analyze_sentiment, categorize_reviews, extract_app_id

class TestReviewAnalyzer(unittest.TestCase):
    def test_extract_app_id(self):
        url = "https://play.google.com/store/apps/details?id=com.example.app&hl=en"
        self.assertEqual(extract_app_id(url), "com.example.app")
        self.assertEqual(extract_app_id("com.example.app"), "com.example.app")

    def test_analyze_sentiment(self):
        self.assertGreater(analyze_sentiment("Great app, love it!"), 0)
        self.assertLess(analyze_sentiment("Terrible app, hate it!"), 0)

    def test_sentiment_caching(self):
        # Reset cache info if present
        if hasattr(analyze_sentiment, "cache_clear"):
            analyze_sentiment.cache_clear()

        # Initial call - cache miss
        _ = analyze_sentiment("Great app, love it!")
        info1 = analyze_sentiment.cache_info()
        self.assertEqual(info1.hits, 0)
        self.assertEqual(info1.misses, 1)

        # Subsequent call - cache hit
        _ = analyze_sentiment("Great app, love it!")
        info2 = analyze_sentiment.cache_info()
        self.assertEqual(info2.hits, 1)
        self.assertEqual(info2.misses, 1)

    def test_categorize_reviews(self):
        reviews_data = [
            {"content": "Great app, love it!"},
            {"content": "Terrible app, hate it!"},
            {"content": "the product is standard"}
        ]
        categorized = categorize_reviews(reviews_data)
        self.assertEqual(len(categorized["Positive"]), 1)
        self.assertEqual(len(categorized["Negative"]), 1)
        self.assertEqual(len(categorized["Neutral"]), 1)

if __name__ == "__main__":
    unittest.main()

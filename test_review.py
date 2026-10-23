import unittest
from review import analyze_sentiment, categorize_reviews, extract_app_id

class TestReviewAnalysis(unittest.TestCase):

    def setUp(self):
        # Clear lru_cache info before each test if available
        if hasattr(analyze_sentiment, "cache_clear"):
            analyze_sentiment.cache_clear()

    def test_analyze_sentiment_polarity(self):
        pos_score = analyze_sentiment("Great and wonderful app!")
        neg_score = analyze_sentiment("Terrible and awful experience.")
        self.assertGreater(pos_score, 0)
        self.assertLess(neg_score, 0)

    def test_analyze_sentiment_caching(self):
        text = "This is a repeated review text for testing caching."

        # Initial call - cache miss
        score1 = analyze_sentiment(text)

        # Second call - cache hit
        score2 = analyze_sentiment(text)

        self.assertEqual(score1, score2)
        cache_info = analyze_sentiment.cache_info()
        self.assertGreaterEqual(cache_info.hits, 1)

    def test_categorize_reviews(self):
        mock_reviews = [
            {"content": "Awesome application!"},
            {"content": "This is a review."},
            {"content": "Horrible app, crashes constantly."}
        ]
        categorized = categorize_reviews(mock_reviews)
        self.assertEqual(len(categorized["Positive"]), 1)
        self.assertEqual(len(categorized["Neutral"]), 1)
        self.assertEqual(len(categorized["Negative"]), 1)

    def test_extract_app_id(self):
        url = "https://play.google.com/store/apps/details?id=com.example.app&hl=en"
        app_id = extract_app_id(url)
        self.assertEqual(app_id, "com.example.app")

        plain_id = "com.example.app"
        self.assertEqual(extract_app_id(plain_id), "com.example.app")

if __name__ == "__main__":
    unittest.main()

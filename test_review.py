import unittest
from review import analyze_sentiment, categorize_reviews

class TestReview(unittest.TestCase):
    def setUp(self):
        # Clear cache before each test
        analyze_sentiment.cache_clear()

    def test_analyze_sentiment_polarity(self):
        pos_score = analyze_sentiment("Great amazing app!")
        neg_score = analyze_sentiment("Terrible horrible crash app!")
        self.assertGreater(pos_score, 0)
        self.assertLess(neg_score, 0)

    def test_analyze_sentiment_caching(self):
        text = "This is a neutral feedback statement."

        # Initial call - cache miss
        _ = analyze_sentiment(text)
        info1 = analyze_sentiment.cache_info()
        self.assertEqual(info1.hits, 0)
        self.assertEqual(info1.misses, 1)

        # Second call - cache hit
        _ = analyze_sentiment(text)
        info2 = analyze_sentiment.cache_info()
        self.assertEqual(info2.hits, 1)

    def test_categorize_reviews(self):
        reviews_data = [
            {"content": "Great app, highly recommend!"},
            {"content": "Terrible app, crashes instantly."},
            {"content": "It is an app."}
        ]
        categorized = categorize_reviews(reviews_data)
        self.assertIn("Great app, highly recommend!", categorized["Positive"])
        self.assertIn("Terrible app, crashes instantly.", categorized["Negative"])
        self.assertIn("It is an app.", categorized["Neutral"])

if __name__ == "__main__":
    unittest.main()

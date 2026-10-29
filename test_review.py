import unittest
from review import analyze_sentiment, categorize_reviews

class TestReviewAnalysis(unittest.TestCase):
    def setUp(self):
        # Clear cache before tests
        analyze_sentiment.cache_clear()

    def test_analyze_sentiment_positive(self):
        polarity = analyze_sentiment("Great app, I love it!")
        self.assertGreater(polarity, 0.1)

    def test_analyze_sentiment_negative(self):
        polarity = analyze_sentiment("Terrible experience, constant crashes.")
        self.assertLess(polarity, -0.1)

    def test_analyze_sentiment_neutral(self):
        polarity = analyze_sentiment("This is a phone application.")
        self.assertTrue(-0.1 <= polarity <= 0.1)

    def test_analyze_sentiment_caching(self):
        text = "Awesome design and fast interface!"
        # First call (cache miss)
        res1 = analyze_sentiment(text)
        info1 = analyze_sentiment.cache_info()

        # Second call (cache hit)
        res2 = analyze_sentiment(text)
        info2 = analyze_sentiment.cache_info()

        self.assertEqual(res1, res2)
        self.assertEqual(info2.hits, info1.hits + 1)

    def test_categorize_reviews(self):
        reviews_data = [
            {"content": "Awesome app!"},
            {"content": "Horrible app."},
            {"content": "It is an app."}
        ]
        categorized = categorize_reviews(reviews_data)
        self.assertEqual(len(categorized["Positive"]), 1)
        self.assertEqual(len(categorized["Negative"]), 1)
        self.assertEqual(len(categorized["Neutral"]), 1)

if __name__ == "__main__":
    unittest.main()

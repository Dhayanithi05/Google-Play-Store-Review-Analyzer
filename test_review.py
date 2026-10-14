import unittest
from review import analyze_sentiment, categorize_reviews, extract_app_id

class TestReviewAnalysis(unittest.TestCase):
    def test_extract_app_id_url(self):
        url = "https://play.google.com/store/apps/details?id=com.spotify.music&hl=en"
        self.assertEqual(extract_app_id(url), "com.spotify.music")

    def test_extract_app_id_plain(self):
        self.assertEqual(extract_app_id("com.spotify.music"), "com.spotify.music")

    def test_analyze_sentiment_positive(self):
        polarity = analyze_sentiment("This app is amazing! I love it so much.")
        self.assertGreater(polarity, 0.1)

    def test_analyze_sentiment_negative(self):
        polarity = analyze_sentiment("This app is terrible and keeps crashing.")
        self.assertLess(polarity, -0.1)

    def test_analyze_sentiment_caching(self):
        # Clear cache info before test
        analyze_sentiment.cache_clear()

        text = "Awesome application, works great!"
        # First call: miss
        res1 = analyze_sentiment(text)
        info1 = analyze_sentiment.cache_info()
        self.assertEqual(info1.misses, 1)
        self.assertEqual(info1.hits, 0)

        # Second call: hit
        res2 = analyze_sentiment(text)
        info2 = analyze_sentiment.cache_info()
        self.assertEqual(res1, res2)
        self.assertEqual(info2.hits, 1)

    def test_categorize_reviews(self):
        reviews_data = [
            {'content': 'This app is wonderful and fantastic!'},
            {'content': 'It is a phone application.'},
            {'content': 'Horrible app, completely broken!'}
        ]
        categorized = categorize_reviews(reviews_data)
        self.assertEqual(len(categorized["Positive"]), 1)
        self.assertEqual(len(categorized["Neutral"]), 1)
        self.assertEqual(len(categorized["Negative"]), 1)

if __name__ == "__main__":
    unittest.main()

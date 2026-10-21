import unittest
from review import analyze_sentiment, categorize_reviews, extract_app_id

class TestReview(unittest.TestCase):

    def setUp(self):
        analyze_sentiment.cache_clear()

    def test_extract_app_id(self):
        url = "https://play.google.com/store/apps/details?id=com.example.app&hl=en"
        self.assertEqual(extract_app_id(url), "com.example.app")

        plain_id = "com.example.app"
        self.assertEqual(extract_app_id(plain_id), "com.example.app")

    def test_analyze_sentiment(self):
        positive_score = analyze_sentiment("Great app! Highly recommended.")
        self.assertGreater(positive_score, 0.1)

        negative_score = analyze_sentiment("Terrible app, crashes constantly.")
        self.assertLess(negative_score, -0.1)

        neutral_score = analyze_sentiment("The app is installed.")
        self.assertLessEqual(abs(neutral_score), 0.1)

    def test_analyze_sentiment_caching(self):
        text = "Awesome application!"
        analyze_sentiment.cache_clear()

        score1 = analyze_sentiment(text)
        score2 = analyze_sentiment(text)

        self.assertEqual(score1, score2)
        cache_info = analyze_sentiment.cache_info()
        self.assertEqual(cache_info.hits, 1)
        self.assertEqual(cache_info.misses, 1)

    def test_categorize_reviews(self):
        reviews_data = [
            {'content': 'Great app!'},
            {'content': 'Horrible app, hate it!'},
            {'content': 'The app is installed.'}
        ]
        categorized = categorize_reviews(reviews_data)
        self.assertIn('Great app!', categorized['Positive'])
        self.assertIn('Horrible app, hate it!', categorized['Negative'])
        self.assertIn('The app is installed.', categorized['Neutral'])

if __name__ == '__main__':
    unittest.main()

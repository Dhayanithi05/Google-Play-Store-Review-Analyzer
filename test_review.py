import unittest
from review import analyze_sentiment, categorize_reviews, extract_app_id

class TestReviewAnalyzer(unittest.TestCase):
    def test_extract_app_id_full_url(self):
        url = "https://play.google.com/store/apps/details?id=com.example.app&hl=en"
        self.assertEqual(extract_app_id(url), "com.example.app")

    def test_extract_app_id_plain_id(self):
        app_id = "com.example.app"
        self.assertEqual(extract_app_id(app_id), "com.example.app")

    def test_analyze_sentiment_positive(self):
        text = "This app is absolutely wonderful and amazing!"
        self.assertGreater(analyze_sentiment(text), 0.1)

    def test_analyze_sentiment_negative(self):
        text = "This app is terrible, awful, and completely broken."
        self.assertLess(analyze_sentiment(text), -0.1)

    def test_categorize_reviews(self):
        reviews_data = [
            {'content': 'Great app!'},
            {'content': 'Worst app ever.'},
            {'content': 'None'}
        ]
        categorized = categorize_reviews(reviews_data)
        self.assertIn('Positive', categorized)
        self.assertIn('Negative', categorized)
        self.assertIn('Neutral', categorized)
        self.assertEqual(len(categorized['Positive']), 1)
        self.assertEqual(len(categorized['Negative']), 1)
        self.assertEqual(len(categorized['Neutral']), 1)

if __name__ == '__main__':
    unittest.main()

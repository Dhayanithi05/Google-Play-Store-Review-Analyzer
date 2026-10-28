import unittest
from review import extract_app_id, categorize_reviews, analyze_sentiment

class TestReviewAnalyzer(unittest.TestCase):
    def test_extract_app_id(self):
        url = "https://play.google.com/store/apps/details?id=com.example.app"
        self.assertEqual(extract_app_id(url), "com.example.app")
        url_with_param = "https://play.google.com/store/apps/details?id=com.example.app&hl=en"
        self.assertEqual(extract_app_id(url_with_param), "com.example.app")
        self.assertEqual(extract_app_id("com.example.app"), "com.example.app")

    def test_analyze_sentiment(self):
        pos = analyze_sentiment("Great app!")
        neg = analyze_sentiment("Terrible app!")
        self.assertGreater(pos, 0)
        self.assertLess(neg, 0)

    def test_categorize_reviews(self):
        mock_reviews = [
            {'content': 'Great app! Really loved it.'},
            {'content': 'Terrible app! Keeps crashing.'},
            {'content': 'This is an app.'}
        ]
        categorized = categorize_reviews(mock_reviews)
        self.assertEqual(len(categorized['Positive']), 1)
        self.assertEqual(len(categorized['Negative']), 1)
        self.assertEqual(len(categorized['Neutral']), 1)

if __name__ == '__main__':
    unittest.main()

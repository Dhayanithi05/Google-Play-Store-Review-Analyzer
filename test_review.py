import unittest
import review

class TestReviewAnalyzer(unittest.TestCase):
    def test_extract_app_id(self):
        url = 'https://play.google.com/store/apps/details?id=com.example.app&hl=en'
        self.assertEqual(review.extract_app_id(url), 'com.example.app')
        self.assertEqual(review.extract_app_id('com.example.app'), 'com.example.app')

    def test_analyze_sentiment(self):
        pos_score = review.analyze_sentiment('Great app, amazing features!')
        neg_score = review.analyze_sentiment('Horrible app, crashes constantly.')
        self.assertGreater(pos_score, 0)
        self.assertLess(neg_score, 0)

    def test_categorize_reviews(self):
        reviews_data = [
            {'content': 'Great app, amazing features!'},
            {'content': 'Horrible app, crashes constantly.'},
            {'content': 'It is an app.'}
        ]
        categorized = review.categorize_reviews(reviews_data)
        self.assertIn('Great app, amazing features!', categorized['Positive'])
        self.assertIn('Horrible app, crashes constantly.', categorized['Negative'])
        self.assertIn('It is an app.', categorized['Neutral'])

if __name__ == '__main__':
    unittest.main()

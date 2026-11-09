import unittest

from review import analyze_sentiment, categorize_reviews


class TestReviewAnalysis(unittest.TestCase):
    def test_analyze_sentiment_positive(self):
        polarity = analyze_sentiment("This app is amazing and very helpful!")
        self.assertGreater(polarity, 0.1)

    def test_analyze_sentiment_negative(self):
        polarity = analyze_sentiment("This app is terrible and constantly crashes.")
        self.assertLess(polarity, -0.1)

    def test_analyze_sentiment_neutral(self):
        polarity = analyze_sentiment("This is an app on a mobile device.")
        self.assertGreaterEqual(polarity, -0.1)
        self.assertLessEqual(polarity, 0.1)

    def test_categorize_reviews(self):
        reviews_data = [
            {"content": "I love this app, it is amazing!"},
            {"content": "Worst app ever, hate it."},
            {"content": "The application installed on my phone."},
        ]
        categorized = categorize_reviews(reviews_data)
        self.assertEqual(len(categorized["Positive"]), 1)
        self.assertEqual(len(categorized["Negative"]), 1)
        self.assertEqual(len(categorized["Neutral"]), 1)
        self.assertEqual(categorized["Positive"][0], "I love this app, it is amazing!")
        self.assertEqual(categorized["Negative"][0], "Worst app ever, hate it.")
        self.assertEqual(categorized["Neutral"][0], "The application installed on my phone.")


if __name__ == "__main__":
    unittest.main()

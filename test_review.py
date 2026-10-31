import unittest
from review import analyze_sentiment, categorize_reviews, extract_app_id
from textblob import TextBlob

class TestReview(unittest.TestCase):
    def test_analyze_sentiment_polarity(self):
        # Positive
        pos_text = "This app is absolutely amazing, fast, and delightful!"
        self.assertGreater(analyze_sentiment(pos_text), 0.1)

        # Negative
        neg_text = "This app is terrible, horrible, keeps crashing and freezing!"
        self.assertLess(analyze_sentiment(neg_text), -0.1)

        # Neutral
        neutral_text = "The application was updated on Tuesday."
        self.assertAlmostEqual(analyze_sentiment(neutral_text), 0.0, places=1)

    def test_analyze_sentiment_matches_textblob(self):
        sample_texts = [
            "",
            "Hello world",
            "Great work, really love it!",
            "Worst update ever, broke everything.",
            "Normal interface with standard buttons."
        ]
        for text in sample_texts:
            expected = TextBlob(text).sentiment.polarity
            actual = analyze_sentiment(text)
            self.assertEqual(actual, expected)

    def test_categorize_reviews(self):
        reviews_data = [
            {"content": "I absolutely love this app, works wonderfully!"},
            {"content": "Worst app ever, completely broken and unusable."},
            {"content": "The app opened and displayed text."}
        ]
        categorized = categorize_reviews(reviews_data)
        self.assertEqual(len(categorized["Positive"]), 1)
        self.assertEqual(len(categorized["Negative"]), 1)
        self.assertEqual(len(categorized["Neutral"]), 1)
        self.assertIn("love this app", categorized["Positive"][0])
        self.assertIn("Worst app", categorized["Negative"][0])
        self.assertIn("displayed text", categorized["Neutral"][0])

    def test_extract_app_id(self):
        url = "https://play.google.com/store/apps/details?id=com.spotify.music&hl=en"
        self.assertEqual(extract_app_id(url), "com.spotify.music")
        raw_id = "com.spotify.music"
        self.assertEqual(extract_app_id(raw_id), "com.spotify.music")

if __name__ == "__main__":
    unittest.main()

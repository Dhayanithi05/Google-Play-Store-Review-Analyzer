import unittest
import time
from review import analyze_sentiment, categorize_reviews, extract_app_id

class TestReviewAnalysis(unittest.TestCase):

    def test_extract_app_id(self):
        url = "https://play.google.com/store/apps/details?id=com.spotify.music&hl=en"
        self.assertEqual(extract_app_id(url), "com.spotify.music")
        self.assertEqual(extract_app_id("com.spotify.music"), "com.spotify.music")

    def test_analyze_sentiment(self):
        pos = analyze_sentiment("Great app, I love it!")
        neg = analyze_sentiment("Terrible, crashes all the time and unusable.")
        neu = analyze_sentiment("It is an app.")
        self.assertGreater(pos, 0.1)
        self.assertLess(neg, -0.1)
        self.assertAlmostEqual(neu, 0.0, delta=0.1)

    def test_categorize_reviews(self):
        reviews_data = [
            {'content': "Great app, I love it!"},
            {'content': "Terrible, crashes all the time and unusable."},
            {'content': "It is an app."},
            {'content': "Great app, I love it!"} # Repeated review
        ]
        categorized = categorize_reviews(reviews_data)
        self.assertEqual(len(categorized["Positive"]), 2)
        self.assertEqual(len(categorized["Negative"]), 1)
        self.assertEqual(len(categorized["Neutral"]), 1)

    def test_benchmark_categorize_reviews(self):
        # Generate 1000 reviews with repetition (typical for app reviews)
        templates = [
            "Great app, I love it!",
            "Terrible, crashes all the time and unusable.",
            "It is okay, nothing special.",
            "Awesome features and very smooth UI.",
            "Bad update, ruined everything."
        ]
        reviews_data = [{'content': templates[i % len(templates)]} for i in range(1000)]

        start_time = time.perf_counter()
        categorized = categorize_reviews(reviews_data)
        elapsed_time = time.perf_counter() - start_time

        total_categorized = sum(len(v) for v in categorized.values())
        self.assertEqual(total_categorized, 1000)
        print(f"\nCategorized 1000 reviews in {elapsed_time:.4f} seconds")

if __name__ == '__main__':
    unittest.main()

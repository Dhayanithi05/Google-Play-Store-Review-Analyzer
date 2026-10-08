import unittest
import os
import review

class TestReviewAnalyzer(unittest.TestCase):

    def test_extract_app_id(self):
        url = "https://play.google.com/store/apps/details?id=com.example.app&hl=en"
        self.assertEqual(review.extract_app_id(url), "com.example.app")

        plain_id = "com.example.app"
        self.assertEqual(review.extract_app_id(plain_id), "com.example.app")

    def test_analyze_sentiment(self):
        positive_text = "This app is wonderful, fantastic, and super easy to use!"
        negative_text = "This app is horrible, terrible, and useless."

        self.assertGreater(review.analyze_sentiment(positive_text), 0.1)
        self.assertLess(review.analyze_sentiment(negative_text), -0.1)

    def test_categorize_reviews(self):
        sample_reviews = [
            {'content': "Great app, highly recommend!"},
            {'content': "This is a statement."},
            {'content': "Horrible app, completely broken."}
        ]
        categorized = review.categorize_reviews(sample_reviews)
        self.assertIn("Positive", categorized)
        self.assertIn("Neutral", categorized)
        self.assertIn("Negative", categorized)
        self.assertEqual(len(categorized["Positive"]), 1)
        self.assertEqual(len(categorized["Neutral"]), 1)
        self.assertEqual(len(categorized["Negative"]), 1)

    def test_create_pie_chart(self):
        filename = "test_sentiment_chart.png"
        counts = {"Positive": 10, "Neutral": 5, "Negative": 2}
        try:
            review.create_pie_chart(counts, filename=filename)
            self.assertTrue(os.path.exists(filename))
        finally:
            if os.path.exists(filename):
                os.remove(filename)

    def test_generate_report(self):
        app_id = "test_app_id"
        pdf_filename = f"{app_id}_review_report.pdf"
        sample_reviews = [
            {'content': "Awesome application!"},
            {'content': "Bad update."}
        ]
        try:
            review.generate_report(app_id, sample_reviews)
            self.assertTrue(os.path.exists(pdf_filename))
        finally:
            if os.path.exists(pdf_filename):
                os.remove(pdf_filename)

if __name__ == '__main__':
    unittest.main()

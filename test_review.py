import os
import unittest
import review

class TestReviewAnalyzer(unittest.TestCase):

    def test_extract_app_id(self):
        url1 = "https://play.google.com/store/apps/details?id=com.example.app&hl=en"
        url2 = "com.example.app"
        self.assertEqual(review.extract_app_id(url1), "com.example.app")
        self.assertEqual(review.extract_app_id(url2), "com.example.app")

    def test_analyze_sentiment(self):
        positive_score = review.analyze_sentiment("Great application, very helpful!")
        negative_score = review.analyze_sentiment("Terrible app, crashes and fails completely.")
        self.assertGreater(positive_score, 0)
        self.assertLess(negative_score, 0)

    def test_analyze_sentiment_caching(self):
        review.analyze_sentiment.cache_clear()
        info_before = review.analyze_sentiment.cache_info()
        self.assertEqual(info_before.hits, 0)

        text = "Awesome product, works seamlessly!"
        score1 = review.analyze_sentiment(text)
        score2 = review.analyze_sentiment(text)

        info_after = review.analyze_sentiment.cache_info()
        self.assertEqual(score1, score2)
        self.assertEqual(info_after.hits, 1)

    def test_categorize_reviews(self):
        mock_reviews = [
            {'content': 'Great application, love it!'},
            {'content': 'Horrible app, completely broken.'},
            {'content': 'This is a neutral review text.'}
        ]
        categorized = review.categorize_reviews(mock_reviews)
        self.assertIn('Great application, love it!', categorized['Positive'])
        self.assertIn('Horrible app, completely broken.', categorized['Negative'])

    def test_create_pie_chart(self):
        chart_file = "test_chart.png"
        sentiment_counts = {"Positive": 10, "Neutral": 5, "Negative": 2}
        try:
            review.create_pie_chart(sentiment_counts, filename=chart_file)
            self.assertTrue(os.path.exists(chart_file))
        finally:
            if os.path.exists(chart_file):
                os.remove(chart_file)

    def test_generate_report(self):
        app_id = "test.app.id"
        pdf_file = f"{app_id}_review_report.pdf"
        mock_reviews = [
            {'content': 'Excellent service and design.'},
            {'content': 'Worst experience ever.'}
        ]
        try:
            review.generate_report(app_id, mock_reviews)
            self.assertTrue(os.path.exists(pdf_file))
        finally:
            if os.path.exists(pdf_file):
                os.remove(pdf_file)

if __name__ == '__main__':
    unittest.main()

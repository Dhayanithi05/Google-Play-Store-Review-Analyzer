import unittest
import os
import review

class TestReviewAnalyzer(unittest.TestCase):

    def test_analyze_sentiment(self):
        """Test sentiment analysis output and caching."""
        pos = review.analyze_sentiment("This app is amazing and wonderful!")
        neg = review.analyze_sentiment("This app is terrible and useless.")
        neu = review.analyze_sentiment("The app is updated.")

        self.assertGreater(pos, 0.1)
        self.assertLess(neg, -0.1)
        self.assertTrue(-0.1 <= neu <= 0.1)

        # Test cache info
        info_before = review.analyze_sentiment.cache_info()
        review.analyze_sentiment("This app is amazing and wonderful!")
        info_after = review.analyze_sentiment.cache_info()
        self.assertGreater(info_after.hits, info_before.hits)

    def test_categorize_reviews(self):
        """Test categorization of reviews."""
        mock_data = [
            {'content': 'Great app!'},
            {'content': 'Terrible app!'},
            {'content': 'The app is updated.'}
        ]
        categorized = review.categorize_reviews(mock_data)
        self.assertIn('Great app!', categorized['Positive'])
        self.assertIn('Terrible app!', categorized['Negative'])
        self.assertIn('The app is updated.', categorized['Neutral'])

    def test_extract_app_id(self):
        """Test extracting app ID from URL or raw string."""
        url = "https://play.google.com/store/apps/details?id=com.example.app&hl=en"
        self.assertEqual(review.extract_app_id(url), "com.example.app")
        self.assertEqual(review.extract_app_id("com.example.app"), "com.example.app")

    def test_generate_report(self):
        """Test PDF report generation."""
        app_id = "test.app.id"
        pdf_file = f"{app_id}_review_report.pdf"
        mock_reviews = [{'content': 'Love it!'} for _ in range(5)]

        if os.path.exists(pdf_file):
            os.remove(pdf_file)

        review.generate_report(app_id, mock_reviews)

        self.assertTrue(os.path.exists(pdf_file))
        self.assertGreater(os.path.getsize(pdf_file), 0)

        # Clean up generated PDF file
        if os.path.exists(pdf_file):
            os.remove(pdf_file)

if __name__ == "__main__":
    unittest.main()

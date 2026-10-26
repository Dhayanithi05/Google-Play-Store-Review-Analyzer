import unittest
import os
import review

class TestReviewAnalyzer(unittest.TestCase):

    def test_extract_app_id(self):
        url = "https://play.google.com/store/apps/details?id=com.example.app&hl=en"
        self.assertEqual(review.extract_app_id(url), "com.example.app")
        self.assertEqual(review.extract_app_id("com.example.app"), "com.example.app")

    def test_analyze_sentiment(self):
        pos_score = review.analyze_sentiment("This is wonderful and amazing!")
        neg_score = review.analyze_sentiment("This is horrible and terrible!")
        self.assertGreater(pos_score, 0)
        self.assertLess(neg_score, 0)

    def test_categorize_reviews(self):
        mock_reviews = [
            {'content': "This is wonderful and amazing!"},
            {'content': "This is horrible and terrible!"},
            {'content': "This is a book."}
        ]
        categorized = review.categorize_reviews(mock_reviews)
        self.assertEqual(len(categorized["Positive"]), 1)
        self.assertEqual(len(categorized["Negative"]), 1)
        self.assertEqual(len(categorized["Neutral"]), 1)

    def test_create_pie_chart(self):
        chart_filename = "test_chart.png"
        try:
            review.create_pie_chart({"Positive": 10, "Neutral": 5, "Negative": 2}, chart_filename)
            self.assertTrue(os.path.exists(chart_filename))
        finally:
            if os.path.exists(chart_filename):
                os.remove(chart_filename)

    def test_generate_report(self):
        mock_reviews = [
            {'content': "Great app!"},
            {'content': "Bad app!"}
        ]
        app_id = "test_app"
        pdf_filename = f"{app_id}_review_report.pdf"
        try:
            review.generate_report(app_id, mock_reviews)
            self.assertTrue(os.path.exists(pdf_filename))
        finally:
            if os.path.exists(pdf_filename):
                os.remove(pdf_filename)

if __name__ == "__main__":
    unittest.main()

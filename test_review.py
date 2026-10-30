import unittest
import os
import review

class TestReviewAnalyzer(unittest.TestCase):
    def test_analyze_sentiment(self):
        positive_score = review.analyze_sentiment("This app is amazing and awesome!")
        negative_score = review.analyze_sentiment("This app is terrible and horrible!")
        self.assertGreater(positive_score, 0)
        self.assertLess(negative_score, 0)

    def test_categorize_reviews(self):
        reviews_data = [
            {'content': 'This app is awesome!'},
            {'content': 'This app is terrible!'},
            {'content': 'It is an app.'}
        ]
        categorized = review.categorize_reviews(reviews_data)
        self.assertIn('Positive', categorized)
        self.assertIn('Negative', categorized)
        self.assertIn('Neutral', categorized)
        self.assertEqual(len(categorized['Positive']), 1)
        self.assertEqual(len(categorized['Negative']), 1)
        self.assertEqual(len(categorized['Neutral']), 1)

    def test_create_pie_chart(self):
        filename = "test_chart.png"
        review.create_pie_chart({'Positive': 10, 'Neutral': 5, 'Negative': 2}, filename=filename)
        self.assertTrue(os.path.exists(filename))
        if os.path.exists(filename):
            os.remove(filename)

    def test_generate_report(self):
        app_id = "test_app_id"
        reviews_data = [
            {'content': 'Great app!'},
            {'content': 'Bad app!'}
        ]
        pdf_filename = f"{app_id}_review_report.pdf"
        review.generate_report(app_id, reviews_data)
        self.assertTrue(os.path.exists(pdf_filename))
        if os.path.exists(pdf_filename):
            os.remove(pdf_filename)

if __name__ == "__main__":
    unittest.main()

import unittest
import os
from review import analyze_sentiment, categorize_reviews, extract_app_id, generate_report, create_pie_chart

class TestReviewAnalyzer(unittest.TestCase):

    def test_extract_app_id(self):
        url = "https://play.google.com/store/apps/details?id=com.example.app&hl=en"
        self.assertEqual(extract_app_id(url), "com.example.app")

        plain_id = "com.example.app"
        self.assertEqual(extract_app_id(plain_id), "com.example.app")

    def test_analyze_sentiment(self):
        pos_score = analyze_sentiment("This app is amazing and wonderful!")
        neg_score = analyze_sentiment("This app is terrible and horrible.")
        self.assertGreater(pos_score, 0)
        self.assertLess(neg_score, 0)

    def test_categorize_reviews(self):
        reviews_data = [
            {'content': 'Love this app, it is great!'},
            {'content': 'This app opens a blue screen with a menu.'},
            {'content': 'Worst experience ever, terrible app.'}
        ]
        categorized = categorize_reviews(reviews_data)
        self.assertIn('Love this app, it is great!', categorized['Positive'])
        self.assertIn('This app opens a blue screen with a menu.', categorized['Neutral'])
        self.assertIn('Worst experience ever, terrible app.', categorized['Negative'])

    def test_generate_report(self):
        app_id = "test_app"
        reviews_data = [
            {'content': 'Great app!'},
            {'content': 'Bad experience.'}
        ]
        pdf_filename = f"{app_id}_review_report.pdf"

        if os.path.exists(pdf_filename):
            os.remove(pdf_filename)

        generate_report(app_id, reviews_data)
        self.assertTrue(os.path.exists(pdf_filename))

        # Cleanup generated test artifact
        if os.path.exists(pdf_filename):
            os.remove(pdf_filename)

if __name__ == "__main__":
    unittest.main()

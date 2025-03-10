from google_play_scraper import reviews, Sort
from textblob import TextBlob
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, Image
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
import matplotlib.pyplot as plt
import os

def fetch_reviews(app_id, num_reviews=100):
    """Fetch reviews from Google Play Store."""
    result, _ = reviews(
        app_id,
        lang='en',
        country='us',
        count=num_reviews,
        sort=Sort.MOST_RELEVANT
    )
    return result

def analyze_sentiment(review_text):
    """Analyze sentiment of a review using TextBlob."""
    analysis = TextBlob(review_text)
    return analysis.sentiment.polarity

def categorize_reviews(reviews_data):
    """Categorize reviews based on sentiment."""
    categorized = {"Positive": [], "Neutral": [], "Negative": []}

    for review in reviews_data:
        sentiment = analyze_sentiment(review['content'])
        if sentiment > 0.1:
            categorized["Positive"].append(review['content'])
        elif sentiment < -0.1:
            categorized["Negative"].append(review['content'])
        else:
            categorized["Neutral"].append(review['content'])

    return categorized

def create_pie_chart(sentiment_counts, filename="sentiment_chart.png"):
    """Generate a pie chart of sentiment distribution."""
    labels = sentiment_counts.keys()
    sizes = sentiment_counts.values()
    colors = ['green', 'grey', 'red']
    explode = (0.1, 0, 0)  # Emphasize positive sentiment

    plt.figure(figsize=(6, 6))
    plt.pie(sizes, labels=labels, autopct='%1.1f%%', colors=colors, startangle=140, explode=explode, shadow=True)
    plt.title("Sentiment Distribution")
    plt.savefig(filename)
    plt.close()

def generate_report(app_id, reviews_data):
    """Generate a structured PDF report with extracted reviews and analysis."""
    filename = f"{app_id}_review_report.pdf"
    doc = SimpleDocTemplate(filename, pagesize=letter)
    styles = getSampleStyleSheet()
    elements = []

    # Title
    elements.append(Paragraph(f"App Review Analysis: {app_id}", styles['Title']))
    elements.append(Spacer(1, 12))

    # Categorize reviews
    categorized_reviews = categorize_reviews(reviews_data)
    sentiment_counts = {key: len(value) for key, value in categorized_reviews.items()}
    total_reviews = sum(sentiment_counts.values())

    # Generate and add pie chart
    chart_filename = "sentiment_chart.png"
    create_pie_chart(sentiment_counts, chart_filename)
    elements.append(Image(chart_filename, width=400, height=300))
    elements.append(Spacer(1, 12))

    # Summary Section
    elements.append(Paragraph("Summary of Sentiment Analysis:", styles['Heading2']))
    summary_data = [["Sentiment", "Count", "Percentage"]]

    for sentiment, count in sentiment_counts.items():
        percentage = (count / total_reviews) * 100 if total_reviews > 0 else 0
        summary_data.append([sentiment, count, f"{percentage:.2f}%"])

    summary_table = Table(summary_data, colWidths=[150, 100, 100])
    summary_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))
    elements.append(summary_table)
    elements.append(Spacer(1, 12))

    # Detailed Reviews by Category
    for sentiment, review_list in categorized_reviews.items():
        elements.append(Paragraph(f"{sentiment} Reviews:", styles['Heading2']))
        elements.append(Spacer(1, 6))

        data = [["Review"]]
        for review in review_list:
            data.append([Paragraph(review, styles['BodyText'])])

        table = Table(data, colWidths=[500])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ]))
        elements.append(table)
        elements.append(Spacer(1, 12))

    # Final Verdict
    overall_sentiment = "Positive" if sentiment_counts["Positive"] > sentiment_counts["Negative"] else "Negative" if sentiment_counts["Negative"] > sentiment_counts["Positive"] else "Neutral"
    final_verdict = f"<b>Overall Sentiment:</b> {overall_sentiment}"
    elements.append(Paragraph(final_verdict, styles['Heading2']))

    doc.build(elements)
    print(f"Report saved as {filename}")

    # Cleanup chart file
    if os.path.exists(chart_filename):
        os.remove(chart_filename)

def extract_app_id(url):
    """Extracts the app ID from a Google Play Store URL."""
    if "id=" in url:
        return url.split("id=")[1].split("&")[0]
    return url

def main():
    app_url = input("Enter the Google Play App URL or App ID: ")
    app_id = extract_app_id(app_url)
    reviews_data = fetch_reviews(app_id)
    generate_report(app_id, reviews_data)

if __name__ == "__main__":
    main()

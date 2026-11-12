import io

import matplotlib.pyplot as plt
from google_play_scraper import Sort, reviews
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import (
    Image,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)
from textblob import TextBlob


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


def create_pie_chart(sentiment_counts, target=None):
    """Generate a pie chart of sentiment distribution.

    Performance optimization: saves directly to an in-memory BytesIO buffer
    when target is None or a buffer, eliminating disk write/read and cleanup overhead.
    """
    labels = sentiment_counts.keys()
    sizes = sentiment_counts.values()
    colors_list = ['green', 'grey', 'red']
    explode = (0.1, 0, 0)  # Emphasize positive sentiment

    fig, ax = plt.subplots(figsize=(6, 6))
    ax.pie(sizes, labels=labels, autopct='%1.1f%%', colors=colors_list, startangle=140, explode=explode, shadow=True)
    ax.set_title("Sentiment Distribution")

    # If no target specified, render into an in-memory BytesIO buffer
    return_buffer = False
    if target is None:
        target = io.BytesIO()
        return_buffer = True

    fig.savefig(target, format='png')
    plt.close(fig)

    if return_buffer:
        target.seek(0)
        return target
    elif hasattr(target, 'seek'):
        target.seek(0)
    return target


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

    # Generate and add pie chart in-memory (bypasses disk I/O)
    chart_buffer = create_pie_chart(sentiment_counts)
    elements.append(Image(chart_buffer, width=400, height=300))
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

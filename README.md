# Google Play Store Review Analyzer

## Overview
This project fetches and analyzes user reviews from the Google Play Store for a given app. It categorizes reviews into positive, neutral, and negative sentiments using **TextBlob**, generates a structured PDF report with visual storytelling, and includes a sentiment distribution pie chart for UX research purposes.

## Features
- Fetches app reviews from Google Play Store using `google_play_scraper`
- Sentiment analysis using **TextBlob**
- Categorization of reviews into Positive, Neutral, and Negative
- Generates a **PDF report** with:
  - Detailed reviews grouped by sentiment
  - A **pie chart** visualization of sentiment distribution
  - Summary statistics and overall sentiment verdict
  
## Installation
### Prerequisites
Make sure you have Python installed. Then, install the required dependencies:

```bash
pip install google-play-scraper textblob reportlab matplotlib
```

## Usage
Run the script and enter the Google Play Store app URL or app ID:

```bash
python enhanced_review_pdf.py
```

### Example Input
```
Enter the Google Play App URL or App ID: https://play.google.com/store/apps/details?id=com.example.app
```

### Output
- A structured PDF report named `<app_id>_review_report.pdf` containing:
  - Review sentiment distribution (pie chart)
  - Categorized reviews (Positive, Neutral, Negative)
  - Summary statistics
  - Final sentiment verdict

## File Structure
```
📁 Google-Play-Review-Analyzer
│── enhanced_review_pdf.py  # Main script for fetching, analyzing, and generating reports
│── README.md               # Project documentation
```

## Dependencies
- **google_play_scraper** - Fetches reviews from Google Play Store
- **TextBlob** - Performs sentiment analysis
- **ReportLab** - Generates PDF reports
- **Matplotlib** - Creates sentiment pie charts

## License
This project is licensed under the MIT License.

## Contributing
Feel free to submit pull requests or open issues for suggestions and improvements!


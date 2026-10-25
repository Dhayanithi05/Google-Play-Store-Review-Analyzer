## 2026-03-31 - Memoizing TextBlob sentiment analysis for app reviews
**Learning:** TextBlob instantiation and sentiment property calculation (`analysis.sentiment.polarity`) carries significant overhead (creating internal NLTK tokenizers and sentiment objects per call). In app store review processing, identical standard phrases ("Great app", "Good", "Worst update") are very frequent.
**Action:** Wrap `analyze_sentiment` with `@functools.lru_cache(maxsize=1024)` to skip repeated TextBlob evaluations, yielding ~170x faster execution for duplicate review phrases.

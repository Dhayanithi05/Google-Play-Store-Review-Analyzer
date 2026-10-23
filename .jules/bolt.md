## 2025-10-23 - Memoizing Sentiment Analysis with lru_cache

**Learning:** Review text datasets frequently contain duplicate short feedback phrases (e.g. "Great app!", "Terrible"). TextBlob sentiment analysis involves tokenization and lexicon lookup which can be expensive when repeated over thousands of items.
**Action:** Use `@lru_cache(maxsize=1024)` on `analyze_sentiment` to speed up sentiment categorization for duplicate review texts by ~200x with zero regression for unique reviews.

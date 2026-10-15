## 2025-10-15 - Memoizing TextBlob sentiment analysis with lru_cache
**Learning:** `TextBlob(text).sentiment.polarity` performs full NLP tokenization and parsing on every invocation. For datasets with repetitive strings, wrapping `analyze_sentiment` with `@functools.lru_cache(maxsize=1024)` avoids redundant NLP computation and speeds up sentiment analysis significantly (~400x for duplicate review texts).
**Action:** When analyzing repeated text strings in Python NLP pipelines, use `functools.lru_cache` to memoize deterministic sentiment analysis results.

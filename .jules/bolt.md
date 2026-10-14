## 2026-03-31 - Memoize TextBlob Sentiment Analysis
**Learning:** TextBlob sentiment analysis performs expensive NLP parsing and tokenization per invocation. Caching sentiment scores for duplicate text using `@functools.lru_cache(maxsize=1024)` avoids redundant computation when analyzing reviews with repeated phrases.
**Action:** Always consider memoization with `lru_cache` for pure, repetitive NLP / sentiment analysis functions.

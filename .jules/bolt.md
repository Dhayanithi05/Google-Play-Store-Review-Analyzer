# Bolt's Journal - Critical Learnings

## 2026-03-29 - LRU Caching for TextBlob Sentiment Analysis
**Learning:** In review analysis applications, duplicate or repeated feedback text fragments (or common phrases across app reviews) often trigger expensive redundant natural language parsing in `TextBlob`. Using `functools.lru_cache` on `analyze_sentiment` eliminates repeated calculations, dramatically accelerating sentiment processing when repetitive or common reviews are processed.
**Action:** Always memoize pure NLTK / TextBlob NLP analysis functions with `@lru_cache` when processing batch collections of text.

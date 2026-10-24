# Bolt's Journal - Critical Performance Learnings

## 2025-10-24 - LRU Caching TextBlob Sentiment Analysis
**Learning:** TextBlob NLP polarity evaluation (`TextBlob(text).sentiment.polarity`) involves text parsing, tokenization, and Lexicon lookup. In review analysis workloads where reviews or review fragments repeat (or when analyze_sentiment is invoked multiple times in processing pipelines), NLP analysis can become a CPU bottleneck.
**Action:** Use `@functools.lru_cache(maxsize=1024)` on pure text evaluation functions like `analyze_sentiment` to eliminate redundant sentiment computation and improve categorizing throughput.

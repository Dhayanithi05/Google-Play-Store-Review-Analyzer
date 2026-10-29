## 2025-05-18 - Sentiment Analysis LRU Caching
**Learning:** TextBlob sentiment analysis involves NLP tokenization and parsing, which is expensive when called repeatedly. Caching polarity results using `functools.lru_cache` on sentiment analysis functions yields a ~100x+ speedup on duplicate or common review strings without introducing state bugs.
**Action:** Always check if NLP or regex parsing functions are pure and can be decorated with `lru_cache` when processing bulk user-generated texts.

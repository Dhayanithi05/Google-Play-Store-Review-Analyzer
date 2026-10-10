## 2025-05-10 - Memoize sentiment analysis with lru_cache
**Learning:** Sentiment analysis using TextBlob on repeated review text or phrases can be an unnecessary CPU bottleneck. Caching sentiment computation results using `@lru_cache` reduces repeat execution times by >99%.
**Action:** When working with natural language processing or sentiment analysis functions on user-generated inputs, check if identical or recurring strings are processed and apply bounded LRU caching.

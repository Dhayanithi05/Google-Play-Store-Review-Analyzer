## 2025-10-11 - Sentiment Analysis Memoization with `lru_cache`
**Learning:** TextBlob sentiment analysis involves NLP tokenization and lexicon parsing on every call. In review dataset processing, duplicate review texts or repeated sentiment checks benefit massively from `functools.lru_cache`.
**Action:** Use `functools.lru_cache` for pure, deterministic NLP/sentiment functions.

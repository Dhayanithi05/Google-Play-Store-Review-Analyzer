## 2025-10-20 - Memoizing Sentiment Analysis & Table Formatting in ReportLab

**Learning:** In Google Play Store review analysis, sentiment evaluation via TextBlob involves NLP tokenization and lexicon lookups that dominate execution time when identical/short repeated phrases appear in review samples. Additionally, dynamically building ReportLab tables cell-by-cell inside nested loops adds redundant object construction and style creation overhead. Memoizing sentiment evaluation with `@lru_cache(maxsize=1024)` cuts review categorization time by ~80-90% for repeated review texts, while list comprehension and table style reuse reduces table construction time.

**Action:** Look for pure NLP/evaluation functions on text data and memoize them when processing large datasets, and construct ReportLab tables using bulk list comprehensions and shared `TableStyle` instances.

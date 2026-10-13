## 2026-10-13 - Caching NLP Sentiment Analysis and Headless Matplotlib Rendering

**Learning:** In text analysis pipelines like Google Play store review categorization, user reviews frequently contain repetitive sentiment phrases ("Great app", "Love it", "Terrible update"). Using `functools.lru_cache` on sentiment evaluation functions eliminates redundant TextBlob NLP parsing, cutting sentiment categorization time by ~50% on repetitive datasets. Additionally, explicitly setting `matplotlib.use('Agg')` before importing `pyplot` avoids overhead associated with GUI backend selection in headless environments.

**Action:** Always memoize pure NLP scoring functions when processing repetitive user content and ensure Matplotlib uses non-interactive backends in backend/CLI utilities.

## 2026-10-22 - Deferred Heavy Imports and Sentiment Caching

**Learning:** Heavy visualization packages like `matplotlib` impose significant top-level import overhead (~600ms) even when chart generation is not immediately needed. Additionally, review datasets frequently contain repeated short phrases or duplicate text; running raw TextBlob sentiment analysis on every item incurs redundant NLP parsing costs.
**Action:** Defer heavy visualization imports inside functions where they are actually called and configure headless backends (`matplotlib.use('Agg')`). Use `@functools.lru_cache` for pure text processing functions like sentiment analysis.

## 2026-10-08 - Lazy Loading Heavy Plotting Libraries & Sentiment Analysis Caching
**Learning:** Top-level imports of `matplotlib.pyplot` add ~0.5s+ overhead on module initialization in CLI apps. Deferred importing combined with `matplotlib.use('Agg')` avoids headless GUI initialization delays. In sentiment categorization, `@lru_cache` yields ~77% faster review batch processing when text contains duplicate phrases.
**Action:** Defer heavy visualization imports to functions that generate figures and cache text classification endpoints.

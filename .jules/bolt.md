## 2025-02-23 - In-Memory Buffer for ReportLab Images & Sentiment LRU Cache

**Learning:** ReportLab's `Image` flowable supports file-like objects such as `io.BytesIO`. Writing matplotlib charts to disk and reading them back for PDF generation causes unnecessary disk I/O latency (~15-20% overhead in chart/PDF pipeline) and file cleanup overhead. Furthermore, sentiment analysis on repetitive review text benefits significantly from `@functools.lru_cache`, avoiding repeated NLP parsing overhead.

**Action:** Render matplotlib figures into `io.BytesIO()` streams when constructing ReportLab elements rather than persisting temporary image files to the filesystem. Use LRU caching on pure sentiment scoring functions.

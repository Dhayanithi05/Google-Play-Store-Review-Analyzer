# Bolt's Journal

Critical learnings only.

## 2025-05-14 - TextBlob wrapper overhead in high-throughput sentiment analysis
**Learning:** Wrapping strings in `TextBlob(text).sentiment.polarity` introduces significant overhead due to full object initialization, property descriptors, and dynamic `namedtuple` construction inside `PatternAnalyzer.analyze()` (`Sentiment = namedtuple(...)` executed on every call). Calling `textblob.en.sentiments.pattern_sentiment(text)[0]` directly returns the identical polarity tuple `(polarity, subjectivity)` in a fraction of the time without any wrapper allocations.
**Action:** When performing batched or high-volume sentiment analysis using TextBlob, import and invoke `pattern_sentiment` directly instead of instantiating `TextBlob` instances per item.

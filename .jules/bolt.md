## 2025-02-23 - In-memory Matplotlib Figures with ReportLab

**Learning:** Using Matplotlib's stateful `pyplot` interface (`plt.figure()`, `plt.savefig('file.png')`, `plt.close()`) introduces noticeable overhead from global figure manager tracking and disk I/O when embedding charts into ReportLab PDFs. ReportLab's `Image` flowable natively accepts `io.BytesIO` streams, and Matplotlib's object-oriented `matplotlib.figure.Figure` avoids pyplot's state machine overhead entirely. Combining `Figure` with `io.BytesIO` speeds up chart rendering and embedding by ~25% (from ~93ms to ~70ms per chart) while avoiding unnecessary disk writes and cleanup overhead.

**Action:** When rendering dynamic charts into ReportLab PDFs, use `matplotlib.figure.Figure` directly and stream the PNG image into ReportLab via `io.BytesIO` instead of writing temporary files to disk.

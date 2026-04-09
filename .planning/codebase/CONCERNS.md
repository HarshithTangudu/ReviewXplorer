# Codebase Concerns

## 1. Brittleness of Scrapers
- **Amazon/Flipkart Web Scraping:** Scraping eCommerce sites directly via Playwright makes the app extremely brittle. Small UI changes by Amazon or Flipkart will break the extraction logic.

## 2. Resource Intensiveness
- **ML Model Initialization:** Loading three separate `transformers` pipelines (`BERT` models) at startup takes significant time and consumes large amounts of RAM/VRAM. This makes the FastAPI server slow to boot and expensive to host.
- **Concurrency Bottlenecks:** ML analysis is CPU/GPU bound. Fast API routes are async, but pipeline inference is synchronous and could block the event loop under load unless offloaded to separate threads or workers.

## 3. Lack of Automated Testing
- The complete absence of unit tests means that regressions in scraping logic or UI components must be caught manually.

## 4. Error Handling and Logging
- The backend relies mainly on `print()` for internal logging. A structured logging library (like Python's built-in `logging` module or `loguru`) would provide better observability.
- The `AnalyzerService` wraps model loading in broad `try/except` blocks that can silently swallow severe model-loading issues.

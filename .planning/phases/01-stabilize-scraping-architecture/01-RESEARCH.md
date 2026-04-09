# Phase 1 Research: Stabilize Scraping Architecture

## Domain Patterns & Discoveries

1. **Anti-Bot Defenses**:
   Amazon and Flipkart have highly sophisticated anti-bot mechanisms. The current codebase uses standard synchronous `requests` within a thread execution pool, employing simple header swapping (Mobile User Agents). This is easily detected resulting in "Robot Check" captures by the sites.
2. **Current vs Intended Implementation**:
   The `requirements.txt` and `README.md` already document and instruct installing `playwright`. However, the current implementations of `amazon.py` and `flipkart.py` completely bypass playwright for synchronous `BeautifulSoup` parsing.
3. **Playwright Solution**:
   Playwright allows headless browser execution natively capable of executing JavaScript, rendering DOM content implicitly, and avoiding HTTP-layer bot trapping. We must wrap the scrapers using `playwright.async_api` effectively.

## Pitfalls & Recommendations

- **Timeout Issues**: Playwright navigation might timeout due to bot captchas blocking the requested nodes indefinitely. Ensure graceful `TimeoutError` catching so collected data is safely returned rather than crashing.
- **Selector Retention**: The CSS selectors inside the existing beautifulsoup parsers are still valid and should just be converted to `page.locator().all_inner_texts()`.

## Requirements Addressed
- SCRP-01: Fix Amazon scraper extraction
- SCRP-02: Fix Flipkart scraper extraction
- SCRP-03: Handle blocks explicitly and gracefully using built-in timeout catching

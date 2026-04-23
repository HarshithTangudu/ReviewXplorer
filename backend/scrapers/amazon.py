import asyncio
import random
import re
from typing import List
from urllib.parse import urlparse, parse_qs, urlunparse
from playwright.async_api import async_playwright, TimeoutError
from playwright_stealth import Stealth
from .base import BaseScraper

class AmazonScraper(BaseScraper):
    def is_match(self, url: str) -> bool:
        return "amazon" in url.lower()

    def _extract_asin(self, url: str) -> str:
        asin_match = re.search(r"/(?:dp|gp/product|product-reviews|aw/d|gp/aw/d)/([A-Z0-9]{10})", url)
        if asin_match:
            return asin_match.group(1)
        parsed = urlparse(url)
        params = parse_qs(parsed.query)
        if 'asin' in params:
            return params['asin'][0]
        return None

    async def scrape(self, url: str, max_pages: int = 20) -> List[str]:
        asin = self._extract_asin(url)
        if not asin:
            print(f"❌ [Amazon] Could not find ASIN in URL: {url}")
            return []

        parsed_url = urlparse(url)
        domain = parsed_url.netloc if parsed_url.netloc else "www.amazon.in"
        all_texts = []

        print(f"\n🚀 [Amazon] LAUNCHING BROWSER for ASIN: {asin}")
        
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True) 
            context = await browser.new_context(
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
                viewport={'width': 1920, 'height': 1080}
            )
            page = await context.new_page()
            try: await Stealth().apply_stealth_async(page)
            except: pass

            # FALLBACK 1: Try product page directly (often has top reviews)
            try:
                print(f"📦 [Amazon] Checking product page for reviews...")
                await page.goto(f"https://{domain}/dp/{asin}/", wait_until="load")
                await asyncio.sleep(3)
                await page.evaluate("window.scrollTo(0, document.body.scrollHeight / 2)")
                await asyncio.sleep(2)
                
                # Try extraction from product page
                found = await self._extract_from_page(page, all_texts)
                print(f"✨ [Amazon] Product page: Found {found} reviews.")
            except: pass

            # If we need more reviews, try the review pages
            if len(all_texts) < 5:
                for page_num in range(1, max_pages + 1):
                    target = f"https://{domain}/product-reviews/{asin}/?reviewerType=all_reviews&pageNumber={page_num}&sortBy=recent"
                    print(f"📄 [Amazon] Scraping Review Page {page_num}...")
                    
                    try:
                        await page.goto(target, wait_until="load", timeout=60000)
                        await asyncio.sleep(random.uniform(3, 5))
                        
                        if "Sign-In" in await page.title():
                            print(f"⚠️  [Amazon] Blocked by Sign-In on page {page_num}.")
                            # Try mobile version as last resort
                            if page_num == 1:
                                await page.goto(f"https://{domain}/gp/aw/reviews/{asin}/", wait_until="load")
                                await asyncio.sleep(3)
                            else: break
                            
                        found = await self._extract_from_page(page, all_texts)
                        print(f"✨ [Amazon] Page {page_num}: Found {found} new reviews.")
                        
                        if found == 0: break
                        
                        next_button = page.locator("li.a-last:not(.a-disabled) a")
                        if await next_button.count() == 0: break
                    except: break
            
            await browser.close()
            
        return list(set(all_texts))

    async def _extract_from_page(self, page, all_texts) -> int:
        selectors = [
            "[data-hook='review-body']",
            ".review-text-content",
            ".review-text",
            "span[class*='default_cursor_cs_']",
            "div[class*='review-text-content']"
        ]
        
        count = 0
        for selector in selectors:
            try:
                locators = await page.locator(selector).all()
                for loc in locators:
                    text = await loc.inner_text()
                    text = text.replace("Read more", "").replace("Read less", "").strip()
                    if len(text) > 30 and text not in all_texts:
                        if not any(x in text.lower() for x in ["one person found this helpful", "helpful", "report"]):
                            all_texts.append(text)
                            count += 1
            except: continue
        return count

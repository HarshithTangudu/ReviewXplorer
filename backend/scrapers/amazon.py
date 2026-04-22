import asyncio
import random
from typing import List
import re
from urllib.parse import urlparse
from playwright.async_api import async_playwright, TimeoutError
from playwright_stealth import Stealth
from .base import BaseScraper

class AmazonScraper(BaseScraper):
    def is_match(self, url: str) -> bool:
        return "amazon" in url.lower()

    async def scrape(self, url: str, max_pages: int = 5) -> List[str]:
        parsed_url = urlparse(url)
        domain = parsed_url.netloc if parsed_url.netloc else "www.amazon.in"
        asin_match = re.search(r"/(?:dp|gp/product|product-reviews)/([A-Z0-9]{10})", url)
        
        if not asin_match: return []
        asin = asin_match.group(1)
        
        all_texts = []
        # Modern User Agent
        user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"

        print(f"Scraping Amazon reviews locally using Stealth Playwright for ASIN: {asin}")
        async with async_playwright() as p:
            # We use channel='chrome' or 'msedge' if available for better stealth, 
            # otherwise default chromium is fine with stealth plugin
            browser = await p.chromium.launch(headless=True) 
            
            # Use a realistic viewport
            context = await browser.new_context(
                user_agent=user_agent,
                viewport={'width': 1920, 'height': 1080}
            )
            
            page = await context.new_page()
            
            # Apply Stealth
            await Stealth().apply_stealth_async(page)

            for page_num in range(1, max_pages + 1):
                print(f"Page {page_num}...")
                target = f"https://{domain}/product-reviews/{asin}/?reviewerType=all_reviews&pageNumber={page_num}&sortBy=recent"
                
                try:
                    # Random delay before navigation
                    await asyncio.sleep(random.uniform(2, 4))
                    
                    await page.goto(target, wait_until="domcontentloaded", timeout=60000)
                    
                    # Human-like scroll
                    await page.evaluate("window.scrollTo(0, document.body.scrollHeight / 2)")
                    await asyncio.sleep(random.uniform(1, 2))
                    await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
                    
                    # Wait for reviews to appear
                    try:
                        await page.wait_for_selector("[data-hook='review-body'], .review-text-content, .review-text", timeout=15000)
                    except TimeoutError:
                        # Check for Robot Check
                        content = await page.content()
                        if "Robot Check" in content or "api-services-support@amazon.com" in content:
                            print("Amazon blocked the request with a Captcha. Stopping.")
                            break
                        else:
                            print(f"No reviews found on page {page_num}. Ending.")
                            break
                    
                    locators = await page.locator("[data-hook='review-body'], .review-text-content, .review-text").all()
                    texts = [await loc.inner_text() for loc in locators]
                    
                    added = 0
                    for t in texts:
                        clean_text = t.strip()
                        # Remove 'Read more' text if present in extraction
                        if clean_text.endswith("Read more"):
                            clean_text = clean_text[:-9].strip()
                            
                        if len(clean_text) > 20:
                            all_texts.append(clean_text)
                            added += 1
                            
                    print(f"Extracted {added} reviews from page {page_num}.")
                    
                    if added == 0:
                        break

                except Exception as e:
                    print(f"Exception scraping page {page_num}: {e}")
                    break
            
            await browser.close()

        print(f"Total reviews collected for free: {len(all_texts)}")
        return list(set(all_texts))

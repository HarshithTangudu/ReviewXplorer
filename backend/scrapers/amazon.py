import asyncio
import random
from typing import List
import re
from urllib.parse import urlparse
from playwright.async_api import async_playwright, TimeoutError
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
        user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"

        print(f"Scraping Amazon reviews for ASIN: {asin}")
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            context = await browser.new_context(user_agent=user_agent)
            page = await context.new_page()

            for page_num in range(1, max_pages + 1):
                print(f"Page {page_num}...")
                target = f"https://{domain}/product-reviews/{asin}/?reviewerType=all_reviews&pageNumber={page_num}"
                
                try:
                    await page.goto(target, wait_until="domcontentloaded")
                    await page.wait_for_selector("[data-hook='review-body'], .review-text-content, .review-text", timeout=15000)
                    
                    locators = await page.locator("[data-hook='review-body'], .review-text-content, .review-text").all()
                    texts = [await loc.inner_text() for loc in locators]
                    
                    added = 0
                    for t in texts:
                        clean_text = t.strip()
                        if len(clean_text) > 20:
                            all_texts.append(clean_text)
                            added += 1
                            
                    if added == 0 and page_num == 1:
                        print("Trying product page fallback...")
                        target = f"https://{domain}/dp/{asin}"
                        await page.goto(target, wait_until="domcontentloaded")
                        await page.wait_for_selector("[data-hook='review-body'], .review-text-content, .review-text", timeout=15000)
                        locators = await page.locator("[data-hook='review-body'], .review-text-content, .review-text").all()
                        texts = [await loc.inner_text() for loc in locators]
                        for t in texts:
                            clean_text = t.strip()
                            if len(clean_text) > 20:
                                all_texts.append(clean_text)
                                added += 1
                    
                    if added == 0:
                        break  # No more reviews found

                    await asyncio.sleep(random.uniform(1.5, 3.5))
                except TimeoutError:
                    print("Captcha or bot block encountered on Amazon. Halting scrape and returning gathered reviews.")
                    break
                except Exception as e:
                    print(f"Exception scraping page {page_num}: {e}")
                    break
            
            await browser.close()

        print(f"Final Count: {len(all_texts)}")
        return list(set(all_texts))

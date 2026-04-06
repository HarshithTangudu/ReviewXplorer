import asyncio
from playwright.async_api import async_playwright
from .base import BaseScraper
from typing import List

class FlipkartScraper(BaseScraper):
    def is_match(self, url: str) -> bool:
        return "flipkart" in url.lower()

    async def scrape(self, url: str, max_pages: int = 3) -> List[str]:
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            context = await browser.new_context(
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
            )
            page = await context.new_page()
            
            # Navigate to product page first to find "All Reviews" link if not already on it
            await page.goto(url, wait_until="domcontentloaded")
            
            # Extract review URL from product page or construct it
            reviews_url = url
            if "/p/" in url:
                # Try to find reviews link or just append /product-reviews/
                reviews_url = url.replace("/p/", "/product-reviews/")
            
            all_texts = []
            for page_num in range(1, max_pages + 1):
                print(f"Scraping Flipkart page {page_num}...")
                current_url = f"{reviews_url}&page={page_num}" if "?" in reviews_url else f"{reviews_url}?page={page_num}"
                
                try:
                    await page.goto(current_url, wait_until="domcontentloaded", timeout=30000)
                    await asyncio.sleep(1) # Extra wait for Flipkart's dynamic content
                    
                    reviews = await page.query_selector_all(".ZmyHeS")
                    if not reviews:
                        reviews = await page.query_selector_all("div.t-ZTKy")
                        
                    page_texts = []
                    for review in reviews:
                        text = await review.inner_text()
                        text = text.replace("READ MORE", "").strip()
                        if text:
                            page_texts.append(text)
                    
                    if not page_texts:
                        break
                    
                    all_texts.extend(page_texts)
                    await asyncio.sleep(1)
                except Exception as e:
                    print(f"Error on page {page_num}: {e}")
                    break
            
            await browser.close()
            return all_texts

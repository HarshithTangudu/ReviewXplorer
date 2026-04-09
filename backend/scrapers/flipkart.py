import asyncio
import random
from typing import List
from urllib.parse import urlparse
from playwright.async_api import async_playwright, TimeoutError
from .base import BaseScraper

class FlipkartScraper(BaseScraper):
    def is_match(self, url: str) -> bool:
        return "flipkart" in url.lower()

    async def scrape(self, url: str, max_pages: int = 5) -> List[str]:
        pid = ""
        if "/p/" in url:
            pid = url.split("/p/")[1].split("?")[0]
        elif "/product-reviews/" in url:
            pid = url.split("/product-reviews/")[1].split("?")[0]
            
        if not pid: return []
        
        parsed_url = urlparse(url)
        base_domain = f"https://{parsed_url.netloc}" if parsed_url.netloc else "https://www.flipkart.com"
        
        all_texts = []
        user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"

        print(f"Scraping Flipkart reviews for PID: {pid}")
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            context = await browser.new_context(user_agent=user_agent)
            page = await context.new_page()

            for page_num in range(1, max_pages + 1):
                print(f"Page {page_num}...")
                target = f"{base_domain}/product-reviews/{pid}?page={page_num}"
                
                try:
                    await page.goto(target, wait_until="domcontentloaded")
                    await page.wait_for_selector("div.t-ZTKy, .ZmyHeS, ._6NES6J, ._17N_6P", timeout=15000)
                    
                    locators = await page.locator("div.t-ZTKy, .ZmyHeS, ._6NES6J, ._17N_6P").all()
                    texts = [await loc.inner_text() for loc in locators]
                    
                    added = 0
                    for t in texts:
                        clean = t.replace("READ MORE", "").strip()
                        if len(clean) > 20:
                            all_texts.append(clean)
                            added += 1
                            
                    if added == 0:
                        break # No more reviews found

                    await asyncio.sleep(random.uniform(1.0, 2.5))
                except TimeoutError:
                    print("Captcha or bot block encountered on Flipkart. Halting scrape and returning gathered reviews.")
                    break
                except Exception as e:
                    print(f"Exception scraping page {page_num}: {e}")
                    break
            
            await browser.close()
            
        print(f"Final Count: {len(all_texts)}")
        return list(set(all_texts))

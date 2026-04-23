import asyncio
import random
import re
import os
from typing import List
from urllib.parse import urlparse, parse_qs
from playwright.async_api import async_playwright, TimeoutError
from playwright_stealth import Stealth
from .base import BaseScraper

class FlipkartScraper(BaseScraper):
    def is_match(self, url: str) -> bool:
        return "flipkart" in url.lower()

    def _extract_pid(self, url: str) -> str:
        parsed = urlparse(url)
        params = parse_qs(parsed.query)
        return params.get('pid', [None])[0]

    async def scrape(self, url: str, max_pages: int = 20) -> List[str]:
        all_texts = []
        pid = self._extract_pid(url)
        consecutive_empty_pages = 0
        max_empty_pages = 3
        
        # Prepare base URL
        base_url = url
        if "/p/" in base_url:
            base_url = base_url.replace("/p/", "/product-reviews/")
        
        # Strip existing page or other pagination markers
        base_url = re.sub(r'[?&]page=\d+', '', base_url)

        print(f"\n🚀 [Flipkart] LAUNCHING BROWSER for URL: {base_url}")
        
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True) 
            context = await browser.new_context(
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
                viewport={'width': 1920, 'height': 1080}
            )
            page = await context.new_page()
            
            try:
                await Stealth().apply_stealth_async(page)
            except: pass

            for page_num in range(1, max_pages + 1):
                # Construct target URL for this page
                sep = "&" if "?" in base_url else "?"
                target = f"{base_url}{sep}page={page_num}"
                
                print(f"📄 [Flipkart] Scraping Page {page_num}...")
                
                try:
                    # Use networkidle to wait for dynamic content
                    await page.goto(target, wait_until="networkidle", timeout=60000)
                    
                    # Extra wait for safety
                    await asyncio.sleep(random.uniform(2, 4))
                    
                    # Expand reviews ("READ MORE")
                    # On some pages it's "READ MORE", on others it's just "more"
                    try:
                        read_mores = await page.locator('span:has-text("READ MORE"), span:has-text("more")').all()
                        for rm in read_mores:
                            if await rm.is_visible(): 
                                try: await rm.click(timeout=1000)
                                except: pass
                    except: pass

                    # Multiple selector fallbacks for review text
                    selectors = [
                        'div.t-ZTKy', 
                        'div.ZmyHeS', 
                        'div._27M-N_', 
                        'div.t-y77z',
                        'div[class*="EPC_7+"]',
                        'div[dir="auto"].css-146c3p1', # New layout text blocks
                        'div.X7978B' # Another potential container
                    ]
                    
                    page_added = 0
                    
                    # Try specific selectors first
                    for selector in selectors:
                        try:
                            locators = await page.locator(selector).all()
                            for loc in locators:
                                text = await loc.inner_text()
                                text = text.replace("READ MORE", "").replace("more", "").strip()
                                # Heuristic to avoid names and small meta info
                                if len(text) > 25 and text not in all_texts:
                                    # Basic check to avoid common footer/header text
                                    if not any(x in text.lower() for x in ["copyright", "all rights reserved", "contact us"]):
                                        all_texts.append(text)
                                        page_added += 1
                        except: continue

                    # If still nothing, try a very broad approach
                    if page_added == 0:
                        # Find divs with a lot of text that aren't scripts or styles
                        potential_reviews = await page.evaluate("""
                            () => {
                                const divs = Array.from(document.querySelectorAll('div[dir="auto"]'));
                                return divs
                                    .filter(d => d.innerText.length > 40)
                                    .map(d => d.innerText);
                            }
                        """)
                        for text in potential_reviews:
                            text = text.replace("READ MORE", "").replace("more", "").strip()
                            if len(text) > 40 and text not in all_texts:
                                if not any(x in text.lower() for x in ["privacy policy", "terms of use"]):
                                    all_texts.append(text)
                                    page_added += 1
                            
                    print(f"✨ [Flipkart] Page {page_num}: Found {page_added} new reviews.")
                    
                    if page_added == 0:
                        consecutive_empty_pages += 1
                        if consecutive_empty_pages >= max_empty_pages:
                            break
                    else:
                        consecutive_empty_pages = 0

                    # Check for "Next" button
                    next_button = page.locator('a:has-text("Next"), span:has-text("Next")')
                    if await next_button.count() == 0 and page_added == 0:
                        break

                    await asyncio.sleep(random.uniform(1, 3))
                    
                except Exception as e:
                    print(f"❌ [Flipkart] Error on page {page_num}: {e}")
                    break
            
            await browser.close()
            
        return list(set(all_texts))
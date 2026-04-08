import asyncio
import random
import requests
from bs4 import BeautifulSoup
from .base import BaseScraper
from typing import List
import re
from urllib.parse import urlparse

class AmazonScraper(BaseScraper):
    def is_match(self, url: str) -> bool:
        return "amazon" in url.lower()

    async def scrape(self, url: str, max_pages: int = 5) -> List[str]:
        # A list of real-world mobile user agents which are often less blocked
        mobile_uas = [
            "Mozilla/5.0 (iPhone; CPU iPhone OS 17_4_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4.1 Mobile/15E148 Safari/604.1",
            "Mozilla/5.0 (Linux; Android 14; Pixel Pro) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.6312.80 Mobile Safari/537.36"
        ]
        
        parsed_url = urlparse(url)
        domain = parsed_url.netloc if parsed_url.netloc else "www.amazon.in"
        asin_match = re.search(r"/(?:dp|gp/product|product-reviews)/([A-Z0-9]{10})", url)
        
        if not asin_match: return []
        asin = asin_match.group(1)
        
        all_texts = []
        
        def fetch_worker(page_num):
            # Specialized headers to mimic a real mobile browser
            headers = {
                "User-Agent": random.choice(mobile_uas),
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
                "Accept-Language": "en-US,en;q=0.5",
                "Accept-Encoding": "gzip, deflate, br",
                "Connection": "keep-alive",
                "Upgrade-Insecure-Requests": "1"
            }
            
            # Review page URL
            target = f"https://{domain}/product-reviews/{asin}/?reviewerType=all_reviews&pageNumber={page_num}"
            if page_num == 0: # Signal for product page fallback
                target = f"https://{domain}/dp/{asin}"

            try:
                response = requests.get(target, headers=headers, timeout=20)
                
                # If blocked, try one more time with a different UA
                if "Robot Check" in response.text or response.status_code != 200:
                    headers["User-Agent"] = random.choice(mobile_uas)
                    response = requests.get(target, headers=headers, timeout=20)
                
                soup = BeautifulSoup(response.content, 'html.parser')
                # Amazon's review selectors (Desktop and Mobile)
                reviews = soup.select("[data-hook='review-body'], .review-text-content, .review-text")
                
                return [r.get_text(strip=True) for r in reviews if len(r.get_text(strip=True)) > 20]
            except:
                return []

        print(f"Scraping Amazon reviews for ASIN: {asin}")
        for p in range(1, max_pages + 1):
            print(f"Page {p}...")
            # Use threads for synchronous requests
            page_data = await asyncio.to_thread(fetch_worker, p)
            if not page_data: 
                if p == 1:
                    print("Trying product page fallback...")
                    page_data = await asyncio.to_thread(lambda: fetch_worker(0))
                
                if not page_data:
                    break
            
            all_texts.extend(page_data)
            await asyncio.sleep(random.uniform(1.5, 3.5))
            
        print(f"Final Count: {len(all_texts)}")
        return list(set(all_texts))

import asyncio
import random
import requests
from bs4 import BeautifulSoup
from .base import BaseScraper
from typing import List
import re
from urllib.parse import urlparse

class FlipkartScraper(BaseScraper):
    def is_match(self, url: str) -> bool:
        return "flipkart" in url.lower()

    async def scrape(self, url: str, max_pages: int = 5) -> List[str]:
        # Flipkart often allows mobile requests more freely than automated browsers
        mobile_uas = [
            "Mozilla/5.0 (iPhone; CPU iPhone OS 17_4_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4.1 Mobile/15E148 Safari/604.1",
            "Mozilla/5.0 (Linux; Android 14; Pixel 8 Pro) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.6312.80 Mobile Safari/537.36"
        ]
        
        # Smart extraction of Product ID from Flipkart URL
        # Format: .../product-reviews/itm... or .../p/itm...
        pid = ""
        if "/p/" in url:
            pid = url.split("/p/")[1].split("?")[0]
        elif "/product-reviews/" in url:
            pid = url.split("/product-reviews/")[1].split("?")[0]
            
        if not pid: return []
        
        parsed_url = urlparse(url)
        base_domain = f"https://{parsed_url.netloc}" if parsed_url.netloc else "https://www.flipkart.com"
        
        all_texts = []
        
        def fetch_worker(page_num):
            headers = {
                "User-Agent": random.choice(mobile_uas),
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
                "Accept-Language": "en-US,en;q=0.5",
                "Accept-Encoding": "gzip, deflate, br",
                "Connection": "keep-alive"
            }
            
            # Reconstruct direct reviews URL
            target = f"{base_domain}/product-reviews/{pid}?page={page_num}"
            
            try:
                response = requests.get(target, headers=headers, timeout=20)
                if response.status_code != 200:
                    return []
                
                soup = BeautifulSoup(response.content, 'html.parser')
                # Flipkart's review selectors
                # Desktop uses .t-ZTKy, Mobile uses ._17N_6P or similar
                reviews = soup.select("div.t-ZTKy, .ZmyHeS, ._6NES6J, ._17N_6P")
                
                texts = []
                for r in reviews:
                    t = r.get_text(strip=True).replace("READ MORE", "").strip()
                    if len(t) > 20:
                        texts.append(t)
                return texts
            except:
                return []

        print(f"Scraping Flipkart reviews for PID: {pid}")
        for p in range(1, max_pages + 1):
            print(f"Page {p}...")
            page_data = await asyncio.to_thread(fetch_worker, p)
            if not page_data:
                break
            
            all_texts.extend(page_data)
            await asyncio.sleep(random.uniform(1.0, 2.5))
            
        print(f"Final Count: {len(all_texts)}")
        return list(set(all_texts))

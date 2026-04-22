from typing import List, Optional
from .base import BaseScraper
from .amazon import AmazonScraper
from .apify_amazon import ApifyAmazonScraper
from .flipkart import FlipkartScraper
from .youtube import YouTubeScraper
from .reddit import RedditScraper

class ScraperManager:
    def __init__(self):
        self.scrapers: List[BaseScraper] = [
            ApifyAmazonScraper(),
            AmazonScraper(),
            FlipkartScraper(),
            YouTubeScraper(),
            RedditScraper()
        ]

    async def scrape(self, url: str) -> List[str]:
        for scraper in self.scrapers:
            if scraper.is_match(url):
                print(f"Trying scraper: {scraper.__class__.__name__}")
                results = await scraper.scrape(url)
                if results:
                    return results
        return []

    def get_platform(self, url: str) -> str:
        if "amazon" in url.lower(): return "Amazon"
        if "flipkart" in url.lower(): return "Flipkart"
        if "youtube" in url.lower() or "youtu.be" in url.lower(): return "YouTube"
        if "reddit" in url.lower(): return "Reddit"
        return "Unknown"

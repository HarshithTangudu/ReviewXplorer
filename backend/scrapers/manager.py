from typing import List, Optional
from .base import BaseScraper
from .amazon import AmazonScraper
from .flipkart import FlipkartScraper
from .youtube import YouTubeScraper
from .reddit import RedditScraper

class ScraperManager:
    def __init__(self):
        self.scrapers: List[BaseScraper] = [
            AmazonScraper(),
            FlipkartScraper(),
            YouTubeScraper(),
            RedditScraper()
        ]

    async def scrape(self, url: str) -> List[str]:
        for scraper in self.scrapers:
            if scraper.is_match(url):
                return await scraper.scrape(url)
        return []

    def get_platform(self, url: str) -> str:
        if "amazon" in url.lower(): return "Amazon"
        if "flipkart" in url.lower(): return "Flipkart"
        if "youtube" in url.lower() or "youtu.be" in url.lower(): return "YouTube"
        if "reddit" in url.lower(): return "Reddit"
        return "Unknown"

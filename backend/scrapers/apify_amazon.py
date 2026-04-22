import os
import asyncio
import re
from typing import List
from urllib.parse import urlparse
from apify_client import ApifyClientAsync
from .base import BaseScraper
from dotenv import load_dotenv

load_dotenv()

class ApifyAmazonScraper(BaseScraper):
    def __init__(self):
        self.api_token = os.getenv("APIFY_API_TOKEN")
        if self.api_token:
            self.client = ApifyClientAsync(self.api_token)
        else:
            self.client = None

    def is_match(self, url: str) -> bool:
        return "amazon" in url.lower() and self.api_token is not None

    async def scrape(self, url: str) -> List[str]:
        if not self.client:
            print("Apify API token not configured. Skipping ApifyAmazonScraper.")
            return []

        print(f"Scraping Amazon reviews via Apify for URL: {url}")
        
        try:
            # Prepare the Actor input for junglee/amazon-reviews-scraper
            run_input = {
                "productUrls": [{"url": url}],
            }

            # Run the Actor and wait for it to finish
            run = await self.client.actor("junglee/amazon-reviews-scraper").call(run_input=run_input)

            # Fetch and print Actor results from the run's dataset
            comments = []
            async for item in self.client.dataset(run["defaultDatasetId"]).iterate_items():
                # Check for error in item (e.g. 404)
                if item.get("error"):
                    print(f"Apify item error: {item.get('error')}")
                    continue

                review_text = item.get("reviewDescription") or item.get("reviewText") or item.get("text")
                if review_text:
                    comments.append(review_text)

            print(f"Apify found {len(comments)} reviews.")
            return comments

        except Exception as e:
            print(f"Error scraping with Apify: {e}")
            return []

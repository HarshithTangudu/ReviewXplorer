import os
import asyncio
import re
from typing import List
from apify_client import ApifyClientAsync
from .base import BaseScraper
from dotenv import load_dotenv

load_dotenv()

class ApifyFlipkartScraper(BaseScraper):
    def __init__(self):
        self.api_token = os.getenv("APIFY_API_TOKEN")
        if self.api_token:
            self.client = ApifyClientAsync(self.api_token)
        else:
            self.client = None

    def is_match(self, url: str) -> bool:
        return "flipkart" in url.lower() and self.api_token is not None

    async def scrape(self, url: str) -> List[str]:
        if not self.client:
            print("Apify API token not configured. Skipping ApifyFlipkartScraper.")
            return []

        # Force a review page URL format which easyapi prefers
        review_url = url
        if "/p/" in review_url:
            review_url = review_url.replace("/p/", "/product-reviews/")
        elif "/product-reviews/" not in review_url:
            # Example logic: add it after the product name segment
            # But let's try the URL as provided first, most actors are smart
            pass

        print(f"Scraping Flipkart reviews via Apify (easyapi) for URL: {review_url}")
        
        try:
            # easyapi/flipkart-review-scraper input schema
            run_input = {
                "reviewUrls": [review_url],
                "maxItems": 50,
                # NO explicit proxy configuration - let the actor use its own defaults
            }

            # Run the Actor
            run = await self.client.actor("easyapi/flipkart-review-scraper").call(run_input=run_input)

            # Fetch results
            comments = []
            async for item in self.client.dataset(run["defaultDatasetId"]).iterate_items():
                review_text = item.get("reviewText") or item.get("review_text") or item.get("text")
                if review_text:
                    comments.append(review_text)

            print(f"Apify (easyapi) found {len(comments)} Flipkart reviews.")
            return comments

        except Exception as e:
            print(f"Error scraping Flipkart with Apify (easyapi): {e}")
            return []

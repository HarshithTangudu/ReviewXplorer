import asyncio
import sys
import os

# Add current directory to path so we can import scrapers
sys.path.append(os.getcwd())

from scrapers.amazon import AmazonScraper
from scrapers.flipkart import FlipkartScraper
from scrapers.youtube import YouTubeScraper
from scrapers.reddit import RedditScraper

async def test_scraper(name, scraper, url):
    print(f"\n--- Testing {name} ---")
    print(f"URL: {url}")
    try:
        results = await scraper.scrape(url, max_pages=1)
        print(f"Result: Found {len(results)} reviews.")
        if results:
            print(f"Sample: {results[0][:100]}...")
        return len(results) > 0
    except Exception as e:
        print(f"Error testing {name}: {e}")
        return False

async def main():
    scrapers = [
        ("Amazon", AmazonScraper(), "https://www.amazon.in/dp/B0CX92S95S"),
        ("Flipkart", FlipkartScraper(), "https://www.flipkart.com/urban-jungle-zest-daypack-18-3-l-laptop-backpack/p/itm46b7a0fb55821"),
        ("YouTube", YouTubeScraper(), "https://www.youtube.com/watch?v=dQw4w9WgXcQ"),
        ("Reddit", RedditScraper(), "https://www.reddit.com/r/technology/comments/17rm6n0/is_it_just_me_or_is_the_internet_getting_worse/")
    ]
    
    success_count = 0
    for name, scraper, url in scrapers:
        if await test_scraper(name, scraper, url):
            success_count += 1
            
    print(f"\nSummary: {success_count}/{len(scrapers)} scrapers returned data.")

if __name__ == "__main__":
    asyncio.run(main())

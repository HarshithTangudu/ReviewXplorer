import asyncio
from scrapers.amazon import AmazonScraper

async def test():
    scraper = AmazonScraper()
    # Replace with a real Amazon URL if you have one, 
    # otherwise this tests the logic with a sample.
    test_url = "https://www.amazon.in/dp/B0CX92S95S" 
    print(f"Testing scraper with URL: {test_url}")
    
    reviews = await scraper.scrape(test_url, max_pages=1)
    print(f"\nFinal Result: Found {len(reviews)} reviews.")

if __name__ == "__main__":
    asyncio.run(test())

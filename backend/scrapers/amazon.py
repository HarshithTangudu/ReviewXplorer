import asyncio
from playwright.async_api import async_playwright
from .base import BaseScraper
from typing import List

class AmazonScraper(BaseScraper):
    def is_match(self, url: str) -> bool:
        return "amazon" in url.lower()

    async def scrape(self, url: str, max_pages: int = 3) -> List[str]:
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            context = await browser.new_context(
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
                viewport={'width': 1920, 'height': 1080}
            )
            page = await context.new_page()
            
            # Base reviews URL
            reviews_url = ""
            if "/dp/" in url or "/gp/product/" in url:
                asin = ""
                domain = "amazon.in" # Default
                if "amazon.com" in url: domain = "amazon.com"
                elif "amazon.co.uk" in url: domain = "amazon.co.uk"
                
                try:
                    if "/dp/" in url:
                        asin = url.split("/dp/")[1].split("/")[0].split("?")[0]
                    elif "/gp/product/" in url:
                        asin = url.split("/gp/product/")[1].split("/")[0].split("?")[0]
                    reviews_url = f"https://{domain}/product-reviews/{asin}/ref=cm_cr_arp_d_paging_btm_next_2?ie=UTF8&reviewerType=all_reviews&pageNumber="
                except Exception as e:
                    print(f"Error parsing ASIN: {e}")
                    reviews_url = url + "&pageNumber=" if "?" in url else url + "?pageNumber="
            else:
                reviews_url = url + "&pageNumber=" if "?" in url else url + "?pageNumber="

            print(f"Constructed reviews URL: {reviews_url}")
            all_texts = []
            for page_num in range(1, max_pages + 1):
                current_url = f"{reviews_url}{page_num}"
                print(f"Navigating to Amazon page {page_num}: {current_url}")
                try:
                    await page.goto(current_url, wait_until="networkidle", timeout=60000)
                    
                    # Wait for either review body or a message that no reviews were found
                    try:
                        await page.wait_for_selector("[data-hook='review-body']", timeout=15000)
                    except:
                        print(f"No more review bodies found on page {page_num}.")
                        break
                    
                    reviews = await page.query_selector_all("[data-hook='review-body']")
                    print(f"Found {len(reviews)} reviews on page {page_num}.")
                    
                    page_texts = []
                    for review in reviews:
                        text = await review.inner_text()
                        if text.strip():
                            page_texts.append(text.strip())
                    
                    if not page_texts:
                        print("Page texts empty, stopping.")
                        break
                    
                    all_texts.extend(page_texts)
                    await asyncio.sleep(2) # Anti-bot delay
                except Exception as e:
                    print(f"Exception on Amazon page {page_num}: {e}")
                    break
            
            print(f"Scraping complete. Total Amazon reviews found: {len(all_texts)}")
            await browser.close()
            return all_texts

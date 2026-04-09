# Integrations

The system interfaces with multiple external platforms primarily for data ingestion (scraping).

## 1. Amazon
- **Integration Type:** Web Scraping
- **Tool:** Playwright and BeautifulSoup
- **Purpose:** Scraping product reviews and comments.

## 2. Flipkart
- **Integration Type:** Web Scraping
- **Tool:** Playwright
- **Purpose:** Scraping product reviews.

## 3. YouTube
- **Integration Type:** External Library API
- **Tool:** youtube-comment-downloader
- **Purpose:** Extracting comments from YouTube videos given a video URL.

## 4. Reddit
- **Integration Type:** Direct API (OAuth via script)
- **Tool:** PRAW (Python Reddit API Wrapper)
- **Authentication:** `REDDIT_CLIENT_ID` and `REDDIT_CLIENT_SECRET` in `.env`
- **Purpose:** Fetching discussion comments from a Reddit thread.

## 5. Hugging Face Model Hub
- **Integration Type:** Pre-trained Models downloading / Loading
- **Tool:** Transformers pipeline
- **Purpose:** Downloading zero-shot/finetuned classification models for NLP processing. Model caching happens locally.

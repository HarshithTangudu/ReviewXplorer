import praw
import os
from dotenv import load_dotenv
from .base import BaseScraper
from typing import List

load_dotenv()

class RedditScraper(BaseScraper):
    def __init__(self):
        self.reddit = None
        client_id = os.getenv("REDDIT_CLIENT_ID")
        client_secret = os.getenv("REDDIT_CLIENT_SECRET")
        user_agent = os.getenv("REDDIT_USER_AGENT", "ReviewXplorer/1.0")
        
        if client_id and client_secret:
            self.reddit = praw.Reddit(
                client_id=client_id,
                client_secret=client_secret,
                user_agent=user_agent
            )

    def is_match(self, url: str) -> bool:
        return "reddit.com" in url.lower()

    async def scrape(self, url: str) -> List[str]:
        if not self.reddit:
            return ["Reddit credentials not configured. Please add REDDIT_CLIENT_ID and REDDIT_CLIENT_SECRET to .env"]
        
        try:
            submission = self.reddit.submission(url=url)
            submission.comments.replace_more(limit=0) # Get top level comments
            texts = []
            for comment in submission.comments.list()[:100]:
                if hasattr(comment, 'body'):
                    texts.append(comment.body)
            return texts
        except Exception as e:
            return [f"Error scraping Reddit: {str(e)}"]

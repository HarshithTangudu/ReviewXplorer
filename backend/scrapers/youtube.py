from .base import BaseScraper
from youtube_comment_downloader import YoutubeCommentDownloader, SORT_BY_RECENT
from typing import List
import itertools

class YouTubeScraper(BaseScraper):
    def is_match(self, url: str) -> bool:
        return "youtube.com" in url.lower() or "youtu.be" in url.lower()

    async def scrape(self, url: str, max_pages: int = 1) -> List[str]:
        downloader = YoutubeCommentDownloader()
        # Increase comment count based on max_pages (e.g. 100 per page)
        limit = max_pages * 100
        comments = downloader.get_comments_from_url(url, sort_by=SORT_BY_RECENT)
        
        texts = []
        for comment in itertools.islice(comments, limit):
            if 'text' in comment:
                texts.append(comment['text'])
        
        return texts

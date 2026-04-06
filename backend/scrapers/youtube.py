from .base import BaseScraper
from youtube_comment_downloader import YoutubeCommentDownloader, SORT_BY_RECENT
from typing import List
import itertools

class YouTubeScraper(BaseScraper):
    def is_match(self, url: str) -> bool:
        return "youtube.com" in url.lower() or "youtu.be" in url.lower()

    async def scrape(self, url: str) -> List[str]:
        downloader = YoutubeCommentDownloader()
        # Limit to 100 comments for performance
        comments = downloader.get_comments_from_url(url, sort_by=SORT_BY_RECENT)
        
        texts = []
        for comment in itertools.islice(comments, 100):
            if 'text' in comment:
                texts.append(comment['text'])
        
        return texts

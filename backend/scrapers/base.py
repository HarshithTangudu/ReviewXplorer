from abc import ABC, abstractmethod
from typing import List

class BaseScraper(ABC):
    @abstractmethod
    def scrape(self, url: str) -> List[str]:
        """
        Scrape comments from the given URL and return a list of strings.
        """
        pass

    @abstractmethod
    def is_match(self, url: str) -> bool:
        """
        Check if the scraper can handle the given URL.
        """
        pass

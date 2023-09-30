from typing import List

import requests
from googlesearch import search

from crawlall.models.search.search_result import SearchResult
from crawlall.shared.utils.logger import Logger


class Searcher:
    def __init__(self):
        self.logger = Logger()

    def search(self, query: str) -> List[SearchResult]:
        self.logger.info(f"Searching for '{query}'...")
        urls = search(query, num_results=3, sleep_interval=3)
        search_results = []
        for url in urls:
            self.logger.info(f"Gathering: {url}")
            html = self.get_html(url)
            search_results.append(SearchResult(url=url, html=html))
        return search_results

    @staticmethod
    def get_html(url: str) -> str:
        r = requests.get(url)
        return r.text

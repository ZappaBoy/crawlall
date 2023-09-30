from typing import List

import requests
from googlesearch import search

from crawlall.models.search.search_result import SearchResult
from crawlall.shared.utils.common import get_requests_session
from crawlall.shared.utils.constants import DEFAULT_LIMIT, DEFAULT_MAX_RETRIES, DEFAULT_TIMEOUT, DEFAULT_DELAY
from crawlall.shared.utils.logger import Logger


class Searcher:
    def __init__(self):
        self.logger = Logger()

    def search(self, query: str, limit: int = DEFAULT_LIMIT, delay: int = DEFAULT_DELAY, timeout: int = DEFAULT_TIMEOUT,
               max_retries: int = DEFAULT_MAX_RETRIES) \
            -> List[SearchResult]:
        self.logger.info(f"Searching for '{query}'...")
        urls = search(query, num_results=limit, sleep_interval=delay)
        search_results = []
        session = get_requests_session(timeout=timeout, max_retries=max_retries)
        for url in urls:
            self.logger.info(f"Gathering: {url}")
            try:
                html = self.get_html(session, url)
                search_results.append(SearchResult(url=url, html=html))
            except requests.exceptions.RequestException as e:
                self.logger.error(f"Failed to gather: {url} ({e})")
        return search_results

    @staticmethod
    def get_html(session, url: str) -> str:
        r = session.get(url)
        return r.text

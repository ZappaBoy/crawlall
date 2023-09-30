from typing import List

import requests
from googlesearch import search

from crawlall.models.search.search_result import SearchResult
from crawlall.services.user_agent_rotator import UserAgentRotator
from crawlall.shared.utils.common import get_requests_session
from crawlall.shared.utils.constants import DEFAULT_LIMIT, DEFAULT_MAX_RETRIES, DEFAULT_TIMEOUT, DEFAULT_DELAY
from crawlall.shared.utils.logger import Logger


class Searcher:
    def __init__(self):
        self.logger = Logger()
        self.user_agent_rotator = UserAgentRotator()

    def search(self, query: str, limit: int = DEFAULT_LIMIT, delay: int = DEFAULT_DELAY, timeout: int = DEFAULT_TIMEOUT,
               max_retries: int = DEFAULT_MAX_RETRIES, rotate_user_agents: bool = False) \
            -> List[SearchResult]:
        self.logger.info(f"Searching for '{query}'...")
        urls = search(query, num_results=limit, sleep_interval=delay)
        search_results = []
        session = get_requests_session(timeout=timeout, max_retries=max_retries)
        headers = {}
        for url in urls:
            self.logger.info(f"Gathering: {url}")
            try:
                if rotate_user_agents:
                    headers["User-Agent"] = self.user_agent_rotator.get_random_user_agent()
                html = self.get_html(session, url, headers=headers)
                search_results.append(SearchResult(url=url, html=html))
            except requests.exceptions.RequestException as e:
                self.logger.error(f"Failed to gather: {url} ({e})")
        return search_results

    @staticmethod
    def get_html(session, url: str, headers: dict = {}) -> str:
        r = session.get(url, headers=headers)
        return r.text

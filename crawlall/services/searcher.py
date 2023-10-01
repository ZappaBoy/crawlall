import threading
from queue import Queue
from typing import List

import requests
from duckduckgo_search import DDGS
from googlesearch import search as google_search

from crawlall.models.search.search_result import SearchResult
from crawlall.services.ip_rotator import IpRotator
from crawlall.services.user_agent_rotator import UserAgentRotator
from crawlall.shared.utils.common import get_requests_session
from crawlall.shared.utils.constants import DEFAULT_LIMIT, DEFAULT_MAX_RETRIES, DEFAULT_TIMEOUT, DEFAULT_DELAY, \
    DEFAULT_IP_ROTATOR_COUNTRIES, DEFAULT_SEARCH_ENGINE, SEARCH_ENGINES, GOOGLE_SEARCH_ENGINE, DUCKDUCKGO_SEARCH_ENGINE
from crawlall.shared.utils.logger import Logger


class Searcher:
    def __init__(self):
        self.logger = Logger()
        self.ip_rotator = IpRotator()
        self.user_agent_rotator = UserAgentRotator()
        self.thread_finished = threading.Event()

    def search(self, query: str, limit: int = DEFAULT_LIMIT, delay: int = DEFAULT_DELAY, timeout: int = DEFAULT_TIMEOUT,
               max_retries: int = DEFAULT_MAX_RETRIES, rotate_user_agents: bool = False, rotate_search_ip: bool = False,
               rotate_connection_ip: bool = False, rotate_ip_countries: List[str] = DEFAULT_IP_ROTATOR_COUNTRIES,
               search_engine: str = DEFAULT_SEARCH_ENGINE) \
            -> List[SearchResult]:
        self.logger.info(f"Searching for '{query}'...")
        search_results = []
        headers = None
        proxies = None
        fastest_proxy = None
        if rotate_search_ip:
            proxies = self.ip_rotator.get_random_proxy_list(countries=rotate_ip_countries)
            fastest_proxy = self.get_fastest_proxy(proxies)
        urls = self.search_on_web(query, limit=limit, delay=delay, proxy=fastest_proxy, search_engine=search_engine)
        session = get_requests_session(timeout=timeout, max_retries=max_retries)
        for url in urls:
            self.logger.info(f"Gathering: {url}")
            try:
                if rotate_user_agents:
                    user_agent = self.user_agent_rotator.get_random_user_agent()
                    headers = {'User-Agent': user_agent}
                if rotate_connection_ip and proxies is not None:
                    html = self.request_with_proxies(url, session=session, proxies=proxies, headers=headers)
                else:
                    html = self.get_html(session, url, headers=headers)
                search_results.append(SearchResult(url=url, html=html))
            except requests.exceptions.RequestException as e:
                self.logger.error(f"Failed to gather: {url} ({e})")
        return search_results

    def search_on_web(self, query: str, limit: int = DEFAULT_LIMIT, delay: int = DEFAULT_DELAY, proxy: str = None,
                      search_engine: str = DEFAULT_SEARCH_ENGINE) -> List[str]:
        if not self.search_engine_exists(search_engine):
            raise ValueError(f"Search engine '{search_engine}' does not exist")
        if search_engine == GOOGLE_SEARCH_ENGINE:
            urls = google_search(query, num_results=limit, proxy=proxy, sleep_interval=delay)
        elif search_engine == DUCKDUCKGO_SEARCH_ENGINE:
            urls = []
            with DDGS(proxies=proxy) as ddgs:
                for r in ddgs.text(query, max_results=limit):
                    urls.append(r['href'])
        else:
            raise NotImplementedError(f"Search engine '{search_engine}' is not implemented")
        return urls

    @staticmethod
    def get_html(session: requests.Session(), url: str, headers: dict = None) -> str:
        r = session.get(url, headers=headers)
        return r.text

    def get_fastest_proxy(self, proxies: List[str]) -> str:
        self.logger.info(f"Checking proxies...")
        session = get_requests_session(timeout=DEFAULT_TIMEOUT, max_retries=0)
        fastest_proxy = self.request_with_proxies('https://wikipedia.org/', session=session, proxies=proxies,
                                                  return_fastest_proxy=True)
        self.logger.info(f"Fastest proxy is {fastest_proxy}")
        fastest_proxy = f"http://{fastest_proxy}"
        return fastest_proxy

    def request_with_proxies(self, url: str, session: requests.Session(), proxies: List[str], headers: dict = None,
                             return_fastest_proxy: bool = False) -> str:
        queue = Queue()
        self.thread_finished = threading.Event()
        args = (queue, session, url, headers)
        threads = [
            threading.Thread(target=self.execute_queue_request, args=args + (proxies[i],) + (return_fastest_proxy,))
            for i in range(len(proxies))]
        for thread in threads:
            thread.daemon = True
            thread.start()

        self.thread_finished.wait()
        response = queue.get()
        queue.task_done()
        return response.text if not return_fastest_proxy else response

    def execute_queue_request(self, queue: Queue, session: requests.Session, url: str, headers: dict, proxy: str,
                              return_fastest_proxy: bool = False) -> None:
        proxy_map = {"http": proxy, "https": proxy}
        try:
            response = session.get(url, headers=headers, proxies=proxy_map)
            if return_fastest_proxy:
                if response.ok:
                    queue.put(proxy)
            else:
                queue.put(response)
            self.thread_finished.set()
        except Exception as e:
            self.logger.debug(f"Error proxying request: {e}")

    @staticmethod
    def search_engine_exists(search_engine: str) -> bool:
        return search_engine in SEARCH_ENGINES

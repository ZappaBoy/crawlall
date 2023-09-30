import functools
import operator
from typing import List

import requests
from requests.adapters import HTTPAdapter
from urllib3 import Retry

from crawlall.models.match.search_match import SearchMatch
from crawlall.shared.utils.constants import DEFAULT_TIMEOUT, DEFAULT_MAX_RETRIES


def get_only_matches(search_matches: List[SearchMatch]) -> List[str]:
    values = [match.matches for match in search_matches]
    values = functools.reduce(operator.iconcat, values, [])
    return values


def get_requests_session(timeout: int = DEFAULT_TIMEOUT, max_retries: int = DEFAULT_MAX_RETRIES) -> requests.Session():
    session = requests.Session()
    session.request = functools.partial(session.request, timeout=timeout)
    retries = Retry(total=max_retries, backoff_factor=1, status_forcelist=[500, 502, 503, 504])
    adapter = HTTPAdapter(max_retries=retries)
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    return session

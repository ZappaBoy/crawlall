import re
from typing import List

from crawlall.models.match.search_match import SearchMatch
from crawlall.models.search.search_result import SearchResult
from crawlall.shared.exceptions.invalid_regex import InvalidRegexError
from crawlall.shared.exceptions.pattern_not_found import PatternNotFoundError
from crawlall.shared.utils.logger import Logger

patterns = {
    "email": r"[\w\.-]+@[\w\.-]+",
    "phone": r"\d{3}-\d{3}-\d{4}",
}


class PatternMatcher:
    def __init__(self):
        self.logger = Logger()

    def match(self, search_results: List[SearchResult], regex: str) -> List[SearchMatch]:
        self.logger.info(f"Matching results...")
        if not self.is_valid_regex(regex):
            raise InvalidRegexError(regex)
        matches = []
        for search_result in search_results:
            regex_match = re.findall(regex, search_result.html)
            matches.append(SearchMatch(url=search_result.url, matches=regex_match))
        return matches

    @staticmethod
    def get_pattern_regex(pattern: str) -> str:
        if not PatternMatcher.pattern_exists(pattern):
            raise PatternNotFoundError(pattern)
        regex = patterns[pattern]
        return regex

    @staticmethod
    def pattern_exists(pattern: str) -> bool:
        return pattern in patterns.keys()

    @staticmethod
    def is_valid_regex(regex: str) -> bool:
        try:
            re.compile(regex)
            return True
        except re.error:
            return False

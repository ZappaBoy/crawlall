import argparse
import importlib.metadata as metadata
from argparse import Namespace

from crawlall.models.log_level import LogLevel
from crawlall.services.pattern_matcher import PatternMatcher
from crawlall.services.searcher import Searcher
from crawlall.shared.utils.logger import Logger

__version__ = metadata.version(__package__ or __name__)


class Crawlall:
    def __init__(self):
        self.logger = Logger()
        self.searcher = Searcher()
        self.pattern_matcher = PatternMatcher()
        self.args = self.parse_args()
        self.set_verbosity()

    def run(self):
        self.check_args()
        self.logger.info(f"Running...")
        self.print_args_info()
        search_results = self.searcher.search(self.args.search)
        regex = self.args.regex
        if regex is None and self.args.pattern is not None:
            regex = self.pattern_matcher.get_pattern_regex(self.args.pattern)
        matched_results = self.pattern_matcher.match(search_results, regex=regex)
        self.logger.info(f"Found {len(matched_results)} results:")
        for result in matched_results:
            self.logger.info(f"{result}")

    @staticmethod
    def parse_args() -> Namespace:
        parser = argparse.ArgumentParser(
            description="Crawlall (craw-all) is a simple crawler tool that uses google search engine supported "
                        "features to find and collect required patterns.")

        parser.add_argument('--verbose', '-v', action='count', default=1,
                            help='Increase verbosity. Use more than once to increase verbosity level (e.g. -vvv).')
        parser.add_argument('--debug', '-d', action='store_true', default=False,
                            help='Enable debug mode.')
        parser.add_argument('--quiet', '-q', action=argparse.BooleanOptionalAction, default=False, required=False,
                            help='Do not print any output/log')
        parser.add_argument('--version', action='version', version=f'%(prog)s {__version__}',
                            help='Show version and exit.')

        parser.add_argument('--search', '-s', required=True, type=str,
                            help='Define search query (e.g. "Just Another SRL").')

        parser.add_argument('--regex', '-r', required=False, type=str, default=None,
                            help='Define regex pattern to match (e.g. "Just([A-Z]{7})").')

        parser.add_argument('--pattern', '-p', required=False, type=str, default=None,
                            help='Define pre-defined pattern to match (e.g. "email").')

        return parser.parse_args()

    def check_args(self) -> None:
        error_message = None
        if not self.args.regex and not self.args.pattern:
            error_message = "Neither regex nor pattern are defined. Please use one of them."
        if self.args.regex and self.args.pattern:
            error_message = "Both regex and pattern are defined. Please use only one of them."
        if self.args.pattern and not self.pattern_matcher.pattern_exists(self.args.pattern):
            error_message = f"Pattern '{self.args.pattern}' does not exist."
        if error_message:
            self.logger.error(error_message)
            exit(1)

    def print_args_info(self) -> None:
        self.logger.info(f"Search query: {self.args.search}")
        if self.args.regex:
            self.logger.info(f"Match Regex: {self.args.regex}")
        if self.args.pattern:
            self.logger.info(f"Match pattern: {self.args.pattern}")

    def set_verbosity(self) -> None:
        if self.args.quiet:
            verbosity_level = LogLevel.DISABLED
        else:
            if self.args.debug or self.args.verbose > LogLevel.DEBUG.value:
                verbosity_level = LogLevel.DEBUG
            else:
                verbosity_level = self.args.verbose
        self.logger.set_log_level(verbosity_level)

import argparse
import importlib.metadata as metadata
from argparse import Namespace

from crawlall.models.log_level import LogLevel
from crawlall.shared.utils.logger import Logger

__version__ = metadata.version(__package__ or __name__)


class Crawlall:
    def __init__(self):
        self.logger = Logger()
        self.args = self.parse_args()
        self.set_verbosity()

    def run(self):
        self.logger.info(f"Running...")


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

        return parser.parse_args()

    def set_verbosity(self) -> None:
        if self.args.quiet:
            verbosity_level = LogLevel.DISABLED
        else:
            if self.args.debug or self.args.verbose > LogLevel.DEBUG.value:
                verbosity_level = LogLevel.DEBUG
            else:
                verbosity_level = self.args.verbose
        self.logger.set_log_level(verbosity_level)

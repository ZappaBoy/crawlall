# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
    ['crawlall',
     'crawlall.models',
     'crawlall.models.match',
     'crawlall.models.search',
     'crawlall.services',
     'crawlall.shared',
     'crawlall.shared.exceptions',
     'crawlall.shared.utils']

package_data = \
    {'': ['*']}

install_requires = \
    ['free-proxy>=1.1.1,<2.0.0',
     'googlesearch-python>=1.2.3,<2.0.0',
     'pandas>=2.1.1,<3.0.0',
     'pydantic>=2.4.2,<3.0.0',
     'random-user-agent>=1.0.1,<2.0.0']

entry_points = \
    {'console_scripts': ['crawlall = crawlall:main', 'test = pytest:main']}

setup_kwargs = {
    'name': 'crawlall',
    'version': '0.1.0',
    'description': 'Crawlall (craw-all) is a simple crawler tool that uses google search engine supported features to find and collect required patterns.',
    'long_description': '# crawlall\n\nCrawlall (craw-all) is a simple crawler tool that uses google search engine supported features to find and collect\nrequired patterns.\n\n## Installation\n\nCrawlall uses [poetry](https://python-poetry.org/) to manage dependencies and packaging. To install all the dependencies\nsimply run:\n\n``` shell\npoetry install\n```\n\n## Usage\n\nYou can run the tool using poetry:\n\n``` shell\npoetry run crawlall --help\n```\n\nOr you can run the tool using python:\n\n``` shell\npython -m crawlall --help\n```\n\nOr you can run the tool directly from the directory or add it to your path:\n\n``` shell\ncrawlall --help\n```\n\n```shell\nusage: crawlall [-h] [--verbose] [--debug] [--quiet | --no-quiet | -q] [--version] --search SEARCH [--regex REGEX] [--pattern PATTERN] [--csv CSV] [--only-matches | --no-only-matches | -o] [--limit LIMIT] [--delay DELAY] [--timeout TIMEOUT]\n                [--retries RETRIES] [--rotate-user-agents | --no-rotate-user-agents | -g]\n\nCrawlall (craw-all) is a simple crawler tool that uses google search engine supported features to find and collect required patterns.\n\noptions:\n  -h, --help            show this help message and exit\n  --verbose, -v         Increase verbosity. Use more than once to increase verbosity level (e.g. -vvv).\n  --debug               Enable debug mode.\n  --quiet, --no-quiet, -q\n                        Do not print any output/log\n  --version             Show version and exit.\n  --search SEARCH, -s SEARCH\n                        Define search query (e.g. "Just Another SRL").\n  --regex REGEX, -r REGEX\n                        Define regex pattern to match (e.g. "Just([A-Z]{7})").\n  --pattern PATTERN, -p PATTERN\n                        Use pre-defined pattern to match (e.g. "email").\n  --csv CSV, -c CSV     Save results to CSV file.\n  --only-matches, --no-only-matches, -o\n                        Export only matches.\n  --limit LIMIT, -l LIMIT\n                        Limit number of site to crawl. Default: 10\n  --delay DELAY, -d DELAY\n                        Delay between each request. Default: 3\n  --timeout TIMEOUT, -t TIMEOUT\n                        Timeout for each request. Default: 3\n  --retries RETRIES, -m RETRIES\n                        Max retries for each request. Default: 3\n  --rotate-user-agents, --no-rotate-user-agents, -g\n                        Rotate user agents to avoid bans. Default: False\n```\n\n## Examples\n\n### Crawl mails\n\n``` shell\ncrawlall --search "Just Another" --pattern email\n```\n\n### Crawl mails and save results to CSV file\n\n``` shell\ncrawlall --search "Just Another" --pattern email --csv results.csv\n```\n\n### Crawl mails and save only matches to CSV file\n\n``` shell\ncrawlall --search "Just Another" --pattern email --csv results.csv --only-matches\n```\n\n### Crawl user defined pattern\n\n``` shell\ncrawlall --search "Just Another" --regex "[A-Z]{7}"\n```\n\n## Supported patterns\n\n```shell\nemail: "[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\\.[a-zA-Z0-9-.]+"\nurl: "https?://(?:[-\\w.]|(?:%[\\da-fA-F]{2}))+"\nphone: "\\d{3}-\\d{3}-\\d{4}"\ninternational_phone: "\\+\\d{1,3}\\s?\\(?\\d{1,4}\\)?[-.\\s]?\\d{1,9}"\ndate: "\\d{2}/\\d{2}/\\d{4}"\nip_address: "\\d{1,3}\\.\\d{1,3}\\.\\d{1,3}\\.\\d{1,3}"\nhashtag: "#\\w+"\nmention: "@\\w+"\neuro_prices: "\\€\\d+(\\.\\d{2})?"\ndollar_price: "\\$\\d+(\\.\\d{2})?"\n```\n\n## Searching using Google Search Engine features\n\nYou can use Google Dorks to search for specific patterns. For example, to search for emails in a specific domain you can\nuse the following query:\n\n```shell\ncrawlall --search "site:justanother.cloud" --pattern email\n```\n\nOr a more complex query:\n\n```shell\ncrawlall --search "site:justanother.cloud inurl:about" --pattern email\n```\n',
    'author': 'ZappaBoy',
    'author_email': 'federico.zappone@justanother.cloud',
    'maintainer': 'ZappaBoy',
    'maintainer_email': 'federico.zappone@justanother.cloud',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.11,<3.12',
}

setup(**setup_kwargs)

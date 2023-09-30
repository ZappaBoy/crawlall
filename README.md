# crawlall

Crawlall (craw-all) is a simple crawler tool that uses google search engine supported features to find and collect
required patterns.

## Installation

Crawlall uses [poetry](https://python-poetry.org/) to manage dependencies and packaging. To install all the dependencies
simply run:

``` shell
poetry install
```

## Usage

You can run the tool using poetry:

``` shell
poetry run crawlall --help
```

Or you can run the tool using python:

``` shell
python -m crawlall --help
```

Or you can run the tool directly from the directory or add it to your path:

``` shell
crawlall --help
```

```shell
usage: crawlall [-h] [--verbose] [--debug] [--quiet | --no-quiet | -q] [--version] --search SEARCH [--regex REGEX] [--pattern PATTERN] [--csv CSV] [--only-matches | --no-only-matches | -o] [--limit LIMIT] [--delay DELAY] [--timeout TIMEOUT]
                [--retries RETRIES] [--rotate-user-agents | --no-rotate-user-agents | -g]

Crawlall (craw-all) is a simple crawler tool that uses google search engine supported features to find and collect required patterns.

options:
  -h, --help            show this help message and exit
  --verbose, -v         Increase verbosity. Use more than once to increase verbosity level (e.g. -vvv).
  --debug               Enable debug mode.
  --quiet, --no-quiet, -q
                        Do not print any output/log
  --version             Show version and exit.
  --search SEARCH, -s SEARCH
                        Define search query (e.g. "Just Another SRL").
  --regex REGEX, -r REGEX
                        Define regex pattern to match (e.g. "Just([A-Z]{7})").
  --pattern PATTERN, -p PATTERN
                        Use pre-defined pattern to match (e.g. "email").
  --csv CSV, -c CSV     Save results to CSV file.
  --only-matches, --no-only-matches, -o
                        Export only matches.
  --limit LIMIT, -l LIMIT
                        Limit number of site to crawl. Default: 10
  --delay DELAY, -d DELAY
                        Delay between each request. Default: 3
  --timeout TIMEOUT, -t TIMEOUT
                        Timeout for each request. Default: 3
  --retries RETRIES, -m RETRIES
                        Max retries for each request. Default: 3
  --rotate-user-agents, --no-rotate-user-agents, -g
                        Rotate user agents to avoid bans. Default: False
```

## Examples

### Crawl mails

``` shell
crawlall --search "Just Another" --pattern email
```

### Crawl mails and save results to CSV file

``` shell
crawlall --search "Just Another" --pattern email --csv results.csv
```

### Crawl mails and save only matches to CSV file

``` shell
crawlall --search "Just Another" --pattern email --csv results.csv --only-matches
```

### Crawl user defined pattern

``` shell
crawlall --search "Just Another" --regex "[A-Z]{7}"
```

## Supported patterns

```shell
email: "[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+"
url: "https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+"
phone: "\d{3}-\d{3}-\d{4}"
international_phone: "\+\d{1,3}\s?\(?\d{1,4}\)?[-.\s]?\d{1,9}"
date: "\d{2}/\d{2}/\d{4}"
ip_address: "\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}"
hashtag: "#\w+"
mention: "@\w+"
euro_prices: "\€\d+(\.\d{2})?"
dollar_price: "\$\d+(\.\d{2})?"
```

## Searching using Google Search Engine features

You can use Google Dorks to search for specific patterns. For example, to search for emails in a specific domain you can
use the following query:

```shell
crawlall --search "site:justanother.cloud" --pattern email
```

Or a more complex query:

```shell
crawlall --search "site:justanother.cloud inurl:about" --pattern email
```

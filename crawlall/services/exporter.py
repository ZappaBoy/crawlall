from typing import List

import pandas as pd

from crawlall.shared.utils.logger import Logger


class Exporter:
    def __init__(self):
        self.logger = Logger()

    @staticmethod
    def to_csv(values: List, filepath: str, ignore_header: bool = False) -> None:
        df = pd.DataFrame(values)
        df.drop_duplicates(inplace=True)
        df.to_csv(filepath, index=False, header=not ignore_header)

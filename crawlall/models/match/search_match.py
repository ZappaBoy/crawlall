from typing import List

from crawlall.models.custom_base_model import CustomBaseModel


class SearchMatch(CustomBaseModel):
    url: str
    matches: List[str]

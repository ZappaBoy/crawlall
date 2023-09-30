from crawlall.models.custom_base_model import CustomBaseModel


class SearchResult(CustomBaseModel):
    url: str
    html: str

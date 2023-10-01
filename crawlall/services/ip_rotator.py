from typing import List

from fp.fp import FreeProxy

from crawlall.shared.utils.constants import DEFAULT_IP_ROTATOR_COUNTRIES
from crawlall.shared.utils.logger import Logger


class IpRotator:

    def __init__(self):
        self.logger = Logger()

    @staticmethod
    def get_random_proxy_list(countries: List[str] = None) -> List[str]:
        if countries is None or len(countries) == 0:
            countries = DEFAULT_IP_ROTATOR_COUNTRIES
        return FreeProxy(country_id=countries, rand=True, https=True).get_proxy_list(repeat=True)

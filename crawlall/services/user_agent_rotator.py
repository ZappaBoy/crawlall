from random_user_agent.params import SoftwareName, OperatingSystem, Popularity
from random_user_agent.user_agent import UserAgent

from crawlall.shared.utils.logger import Logger


class UserAgentRotator:

    def __init__(self):
        self.logger = Logger()
        software_names = [SoftwareName.CHROME.value, SoftwareName.FIREFOX.value, SoftwareName.EDGE.value]
        operating_systems = [OperatingSystem.WINDOWS.value, OperatingSystem.LINUX.value, OperatingSystem.MAC_OS_X.value]
        popularities = [Popularity.POPULAR.value, Popularity.COMMON.value]
        self.user_agent_rotator = UserAgent(software_names=software_names, operating_systems=operating_systems,
                                            popularity=popularities)

    def get_random_user_agent(self) -> str:
        return self.user_agent_rotator.get_random_user_agent()

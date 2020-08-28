from typing import List, Dict

import yaml
from mastodon import Mastodon
import vk

from .types import Publication

class VKPage:
    "это откуда мы тыбзим"
    screen_name: str
    api: vk.API

    def __init__(self, config: Dict):
        screen_name = config.get("screen_name")
        token = config.get("token")
        if not all(screen_name, token):
            raise ValueError("Invalid source definition")
        self.screen_name = screen_name
        self.api = vk.API(vk.Session(access_token=token), v=5.95)

    def get_new(self, last_post_time: int, count: int) -> List[Publication]:
        pass


class MastodonAccount:
    "это куда мы постим"
    api: Mastodon

    def __init__(self, config: Dict):
        node_domain = config.get("domain")
        token = config.get("token")
        if not all(node_domain, token):
            raise ValueError("Invalid destination definition")
        self.api = Mastodon(access_token=token, api_base_url=node_domain)

    def publish(self, post: Publication):
        pass


class Bridge:
    "связываем место тыбзинга и место постинга"
    source: VKPage
    destination: MastodonAccount
    last_post_time: int
    period: int
    count: int


class Config:
    "сюда буим парсить короче"
    sources: Dict[str, VKPage] = {}
    destinations: Dict[str, MastodonAccount] = {}
    raw_bridges = List[Dict] = []

    def __init__(self, file_name: str):
        with open(file_name) as file:
            config_dict: dict = yaml.safe_load(file)

        if "sources" in config_dict:
            for name, source in config_dict["sources"].items():
                self.sources[name] = VKPage(source, self.vk_token)

        if "destinations" in config_dict:
            for name, destination in config_dict["destinations"].items():
                self.destinations[name] = MastodonAccount(destination)

        if "bridges" in config_dict:
            self.raw_bridges = config_dict["bridges"]

    def make_bridges(self) -> List[Bridge]:
        "нельзя создавать мосты до того,"
        "как все конфиги будут считаны"
        "к тому же класс конфига будет не нужен"
        pass

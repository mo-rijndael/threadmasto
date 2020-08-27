from typing import List, Dict, Optional

import yaml


class VKPage:
    "это откуда мы тыбзим"
    domain: str
    token: str

    def __init__(self, config: Dict):
        pass


class MastodonAccount:
    "это куда мы постим"
    token: str
    node_domain: str

    def __init__(self, config: Dict):
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
        if "global" in config_dict:
            self.vk_token = config_dict["global"].get("vk_token", None)

        if "sources" in config_dict:
            for name, source in config_dict["sources"].items():
                self.sources[name] = VKPage(source, self.vk_token)

        if "destinations" in config_dict:
            for name, destination in config_dict["destinations"]:
                self.destinations[name] = MastodonAccount(destination)

        if "bridges" in config_dict:
            self.raw_bridges = config_dict["bridges"]

    def make_bridges(self) -> List[Bridge]:
        "нельзя создавать мосты до того,"
        "как все конфиги будут считаны"
        "к тому же класс конфига будет не нужен"
        pass

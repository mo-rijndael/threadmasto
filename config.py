import time
from typing import List, Dict

import yaml

from exceptions import InvalidConfig
from modules.destinations.base_dest import Destination
from modules.sources.base_source import Source


class Bridge:
    """связываем место тыбзинга и место постинга"""
    source: Source
    destination: Destination
    last_post_time: float
    last_activation: float
    period: int

    def __init__(self,
                 source: Source,
                 destination: Destination,
                 period: int):
        self.source = source
        self.destination = destination
        self.last_post_time = time.time()
        self.last_activation = time.time()
        self.period = period

    def time_to_activation(self) -> float:
        now = time.time()
        activation = self.last_activation + self.period
        return activation - now

    def activate(self):
        now = time.time()
        self.last_activation = now
        posts = self.source.get(self.last_post_time)
        for p in posts:
            self.destination.publish(p)

    def ready(self) -> bool:
        return self.time_to_activation() <= 0


class Config:
    "сюда буим парсить короче"
    sources: Dict[str, Source] = {}
    destinations: Dict[str, Destination] = {}
    raw_bridges: List[Dict] = []

    def __init__(self, file_name: str):
        with open(file_name) as file:
            config_dict: dict = yaml.safe_load(file)

        if "sources" in config_dict:
            for name, source in config_dict["sources"].items():
                try:
                    self.sources[name] = VKPage(source)
                except InvalidConfig as e:
                    e.file = f"{file_name}/sources/{name}"
                    raise e

        if "destinations" in config_dict:
            for name, destination in config_dict["destinations"].items():
                try:
                    self.destinations[name] = MastodonAccount(destination)
                except InvalidConfig as e:
                    e.file = f"{file_name}/destinations/{name}"
                    raise e

        if "bridges" in config_dict:
            self.raw_bridges = config_dict["bridges"]

    def make_bridges(self) -> List[Bridge]:
        "нельзя создавать мосты до того,"
        "как все конфиги будут считаны"
        "к тому же класс конфига будет не нужен"
        pass

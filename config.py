from typing import List, Dict

import yaml


class Config:
    "сюда буим парсить короче"
    def __init__(self, file_name: str):
        pass


class VKPage:
    "это откуда мы тыбзим"
    domain: str
    token: str


class MastodonAccount:
    "это куда мы постим"
    token: str
    node_domain: str


class Bridge:
    "связываем место тыбзинга и место постинга"
    source: VKPage
    destination: MastodonAccount
    last_post_time: int
    period: int
    count: int

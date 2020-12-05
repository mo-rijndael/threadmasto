from typing import Dict
from types import ModuleType
import importlib
import os

from modules.sources.base_source import Source
from modules.destinations.base_dest import Destination


def load_all_folder(path: str) -> Dict[str, ModuleType]:
    files = os.listdir(path)
    modules = dict()

    for module in filter(lambda s: s.endswith(".py"), files):
        name = module[:-3]



def load_sources(path: str) -> Dict[str, Source]:
    ...


def load_destinations(path: str) -> Dict[str, Destination]:
    ...

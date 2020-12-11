from typing import Dict
from types import ModuleType
import importlib.util
import os

from modules.sources.base_source import Source
from modules.destinations.base_dest import Destination


def _can_be_module(name: str):
    return name.endswith(".py") and not name.startswith("_")


def _load_from_modules(subpackage: str) -> Dict[str, ModuleType]:
    modules = dict()
    files = os.listdir(f"./modules/{subpackage}")
    for module in filter(_can_be_module, files):
        name = module[:-3]
        try:
            mod = importlib.import_module(f"modules.{subpackage}.{name}")
        except ModuleNotFoundError:
            continue
        modules[name] = mod
    return modules


def load_sources(path: str) -> Dict[str, Source]:
    unfiltered = _load_from_modules("sources")
    for name, mod in unfiltered:
        



def load_destinations(path: str) -> Dict[str, Destination]:
    ...

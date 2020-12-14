from abc import ABC, abstractmethod
from typing import List, Dict, Any
import os
from importlib import import_module
import logging

from publication import Publication


sources: Dict[str, 'Source'] = dict()
destinations: Dict[str, 'Destination'] = dict()


class Destination(ABC):
    @abstractmethod
    def __init__(self, config: Dict[str, Any]):
        pass

    @abstractmethod
    def publish(self, publication: Publication):
        pass

    @staticmethod
    def register(name: str):
        def decorator(dest):
            if not isinstance(dest, Destination.__class__):
                raise ValueError("must inherit from Destination class")
            destinations[name] = dest
        return decorator


class Source(ABC):
    @abstractmethod
    def __init__(self, config: Dict[str, Any]):
        pass

    @abstractmethod
    def get(self, after_timestamp: float) -> List[Publication]:
        pass

    @staticmethod
    def register(name: str):
        def decorator(source):
            if not isinstance(source, Source.__class__):
                raise ValueError("must inherit from Source class")
            sources[name] = source
        return decorator


def _is_module_name(name: str):
    return name.endswith(".py") and not name.startswith("_")


for m in filter(_is_module_name, os.listdir('modules')):
    name = m[:-3]
    try:
        import_module("modules."+name)
    except ImportError as e:
        logging.error(f"module {name} possible missing depency "
                      f"{e.name}. Loading skipped")

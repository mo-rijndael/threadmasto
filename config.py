import time
import logging
from typing import List, Dict
import traceback

import yaml

from exceptions import InvalidConfig
import modules


class Bridge:
    source: modules.Source
    destination: modules.Destination
    last_activation: float
    interval: int

    def __init__(self,
                 source: modules.Source,
                 destination: modules.Destination,
                 period: int):
        print(source, destination, period)
        self.source = source
        self.destination = destination
        self.last_activation = time.time()
        self.interval = period

    def time_to_activation(self) -> float:
        now = time.time()
        activation = self.last_activation + self.interval
        return activation - now

    def activate(self):
        now = time.time()
        try:
            posts = self.source.get(self.last_activation)
        except Exception as e:
            logging.error(f"Bridge {self}."
                          f" Source throws an error: {e}")
            logging.debug(traceback.format_exc())
            return
        finally:
            self.last_activation = now
        for p in posts:
            try:
                self.destination.publish(p)
            except Exception as e:
                logging.error(f"Bridge {self}."
                              f" Destination throws an error: {e}")
                logging.debug(traceback.format_exc())

    def ready(self) -> bool:
        return self.time_to_activation() <= 0

    def __repr__(self):
        return f"{self.source} -> {self.destination}"


class BridgeConfig:
    sources: Dict[str, modules.Source] = {}
    destinations: Dict[str, modules.Destination] = {}
    raw_bridges: List[Dict] = []

    def __init__(self, file_name: str):
        with open(file_name) as file:
            config_dict: dict = yaml.safe_load(file)

        if "sources" in config_dict:
            print(config_dict)
            for name, source in config_dict["sources"].items():
                path = f"{file_name}/sources/{name}"
                try:
                    type = source["type"]
                    self.sources[name] = modules.sources[type](source)
                except InvalidConfig as e:
                    e.file = e.file or path
                    raise e
                except KeyError:
                    raise InvalidConfig("No 'type' field.", path)
                except Exception as e:
                    raise InvalidConfig(f"Unexpected exception in constructor: {e}", path)

        if "destinations" in config_dict:
            for name, destination in config_dict["destinations"].items():
                path = f"{file_name}/destinations/{name}"
                try:
                    type = destination["type"]
                    self.destinations[name] = \
                        modules.destinations[type](destination)
                except InvalidConfig as e:
                    e.file = e.file or path
                    raise e
                except KeyError:
                    raise InvalidConfig("No 'type' field.", path)
                except Exception as e:
                    raise InvalidConfig(f"Unexpected exception in constructor: {e}", path)

        if "bridges" in config_dict:
            self.raw_bridges = config_dict["bridges"]

    def make_bridges(self) -> List[Bridge]:
        bridges = []
        for b in self.raw_bridges:
            try:
                source = self.sources[b['source']]
                destination = self.destinations[b['destination']]
                interval = b['interval']
            except KeyError as e:
                logging.fatal(f"Invalid bridge definition. "
                              f"Missing field {e.args[0]}")
                raise InvalidConfig("Bad bridge")
            bridges.append(Bridge(source, destination, interval))
        return bridges

    def update(self, other: 'BridgeConfig'):
        self.sources.update(other.sources)
        self.destinations.update(other.destinations)
        self.raw_bridges.extend(other.raw_bridges)
        return self

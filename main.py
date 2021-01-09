import time
import logging
import sys
import os
from getpass import getuser
from functools import reduce

from config import BridgeConfig, Bridge
from exceptions import InvalidConfig


def load_configuration(config_dir: str) -> BridgeConfig:
    if not config_dir.endswith('/'):
        config_dir += '/'
    if os.path.exists(config_dir) and os.path.isdir(config_dir):
        configs = os.listdir(config_dir)
        if not configs:
            raise InvalidConfig("No configs!")
        configs.sort()
        parsed = []
        for c in configs:
            if c.endswith('.yaml') or c.endswith('.yml'):
                parsed.append(BridgeConfig(config_dir + c))

        return reduce(BridgeConfig.update, parsed)
    else:
        raise InvalidConfig("config directory not exists", config_dir)


def main():
    user = getuser()
    if user == "root":
        logging.warning("running under root is VERY DANGEROUS.")

    try:
        config = load_configuration("path.d/")
        bridges = config.make_bridges()
    except InvalidConfig as e:
        sys.exit(e)

    while True:
        for bridge in filter(Bridge.ready, bridges):
            bridge.activate()

        nearest = min(bridges, key=Bridge.time_to_activation)
        time_to_nearest = nearest.time_to_activation()
        if time_to_nearest > 0:
            time.sleep(time_to_nearest)


if __name__ == "__main__":
    main()

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
            raise ValueError
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
        time.sleep(nearest.time_to_activation())


if __name__ == "__main__":
    main()
# план значит:
# 1) если мы запущены от рута, сообщаем автору, что у него атрофирован мозг
#    при этом продолжаем работать
# 2) загружаем конфиги
# 3) собираем по ним мосты
# если конфиг где то падла такая кинул InvalidConfig
# ловим это и говорим юзеру "ты долб#еб, sys.exit(бл#ть)"
# 4) если какой то жадный пид#рас поставил слишком частое обновление,
#    доходчиво объясняем ему, что он упрётся в пять тысяч запросов,
#    мать их в сарае через лисью трещину. Но раз так хочется стрелять в ногу..
# 5) начинаем мейн луп из семи зал#уп
#   1 зал#па будет сортировать мосты по тому, как скоро они активируются
#   2 зал#па будет ждать время до активации самого раннего моста
#   3 зал#па будет выбирать мосты, которые уже надо активировать
#   4 зал#па будет каждый из них пинать, и возвращать управление 3 залупе
#   5 зал#па будет заниматься логгированием
#   6 зал#па будет внутри моста вызывать адаптеры
#   7 зал#па будет просто чтобы было число 7
# 6) если адаптер выкинул исключение, то
#    мы его ловим но покрываем автора матом, ибо нех#й
# 7) наверное можно ловить сигналы и перезагружать конфиг, но....
#    кому это нах#й надо? Серьезно, проще перезапустить

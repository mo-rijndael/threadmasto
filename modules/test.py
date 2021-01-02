from datetime import datetime

from . import Source, Destination
from publication import Publication


@Source.register("test")
class TestSrc(Source):
    def __init__(self, config):
        pass

    def get(self, after: float):
        print(f"getting after {datetime.fromtimestamp(after)} ({after})")
        return [Publication(datetime.fromtimestamp(after).isoformat())]


@Destination.register("test")
class TestDest(Destination):
    def __init__(self, _):
        pass

    def publish(self, post: Publication):
        print(post)

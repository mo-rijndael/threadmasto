from . import Source, Destination
from publication import Publication


@Source.register("test")
class TestSrc(Source):
    def __init__(self, config):
        pass

    def get(self, _):
        print("getting...")
        return [Publication()]


@Destination.register("test")
class TestDest(Destination):
    def __init__(self, _):
        pass

    def publish(self, post: Publication):
        print(post)

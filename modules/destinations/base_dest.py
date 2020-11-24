from abc import ABC, abstractmethod

from publication import Publication


class Destination(ABC):
    @abstractmethod
    def publish(self, publication: Publication):
        pass

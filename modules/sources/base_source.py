from typing import List
from abc import ABC, abstractmethod

from publication import Publication


class Source(ABC):
    @abstractmethod
    def get(self, after_timestamp: float) -> List[Publication]:
        pass

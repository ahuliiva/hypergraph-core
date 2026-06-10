from abc import ABC, abstractmethod
from pathlib import Path

from kgcore.hypergraph import Hypergraph


class DatasetAdapter(ABC):
    @abstractmethod
    def load(self, path: Path) -> Hypergraph:
        raise NotImplementedError
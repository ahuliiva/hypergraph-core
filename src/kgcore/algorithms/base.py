from abc import ABC, abstractmethod

from kgcore.hypergraph import Hypergraph
from kgcore.types import CoreParams, CoreResult


class CoreAlgorithm(ABC):
    @abstractmethod
    def run(self, hypergraph: Hypergraph, params: CoreParams) -> CoreResult:
        raise NotImplementedError
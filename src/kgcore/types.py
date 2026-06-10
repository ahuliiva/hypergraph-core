from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class CoreParams:
    k: int
    g: int | None = None
    p: float | None = None


@dataclass
class CoreResult:
    remaining_vertices: set[str]
    remaining_edges: set[str]
    metadata: dict[str, Any] = field(default_factory=dict)
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Callable


@dataclass(frozen=True)
class AlgorithmSpec:
    name: str
    function: Callable
    inplace: bool
    use_instrumented_list: bool = False
    kwargs: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class DatasetSpec:
    name: str
    generator: Callable
    kwargs: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class RunSpec:
    algorithm: AlgorithmSpec
    dataset: DatasetSpec
    size: int
    seed: int
    repetition: int
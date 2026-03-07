from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

# ts class tracks the numbers of comparisons array writes, partitions and recursion depth, in an algorithm test run, basis for benchmarking
@dataclass
class RunCounters:
    comparisons: int = 0
    writes: int = 0
    partition_calls: int = 0
    max_recursion_depth: int = 0


_ACTIVE_COUNTERS: Optional[RunCounters] = None 


class CounterContext:
    def __init__(self) -> None:
        self.counters = RunCounters()

    def __enter__(self) -> RunCounters:
        global _ACTIVE_COUNTERS
        _ACTIVE_COUNTERS = self.counters
        return self.counters

    def __exit__(self, exc_type, exc, tb) -> None:
        global _ACTIVE_COUNTERS
        _ACTIVE_COUNTERS = None


def active_counters() -> Optional[RunCounters]:
    return _ACTIVE_COUNTERS
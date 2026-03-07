from __future__ import annotations

from sorting_benchmark.instrumentation.counters import active_counters

# this is my own list, which tracks the number of writes to the list for benchmarking purposes
class InstrumentedList(list):
    def __setitem__(self, key, value) -> None:
        counters = active_counters()
        if counters is not None:
            if isinstance(key, slice):
                try:
                    counters.writes += len(value)
                except TypeError:
                    counters.writes += 1
            else:
                counters.writes += 1
        super().__setitem__(key, value)
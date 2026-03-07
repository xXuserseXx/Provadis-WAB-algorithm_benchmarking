from __future__ import annotations

from sorting_benchmark.instrumentation.counters import active_counters


def mergesort(data, depth: int = 1):
    counters = active_counters()
    if counters is not None:
        counters.max_recursion_depth = max(counters.max_recursion_depth, depth)

    if len(data) <= 1:
        return list(data)

    mid = len(data) // 2
    left = mergesort(data[:mid], depth + 1)
    right = mergesort(data[mid:], depth + 1)
    return _merge(left, right)


def _merge(left, right):
    counters = active_counters()
    result = []
    i = 0
    j = 0

    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            if counters is not None:
                counters.writes += 1
            i += 1
        else:
            result.append(right[j])
            if counters is not None:
                counters.writes += 1
            j += 1

    while i < len(left):
        result.append(left[i])
        if counters is not None:
            counters.writes += 1
        i += 1

    while j < len(right):
        result.append(right[j])
        if counters is not None:
            counters.writes += 1
        j += 1

    return result
from __future__ import annotations

from sorting_benchmark.instrumentation.counters import active_counters


def _median_of_three_index(data, lo: int, hi: int) -> int:
    mid = (lo + hi) // 2

    a = data[lo]
    b = data[mid]
    c = data[hi]

    if a <= b:
        if b <= c:
            return mid
        if a <= c:
            return hi
        return lo
    else:
        if a <= c:
            return lo
        if b <= c:
            return hi
        return mid


def _move_pivot_to_end(data, lo: int, hi: int) -> None:
    pivot_idx = _median_of_three_index(data, lo, hi)
    tmp = data[pivot_idx]
    data[pivot_idx] = data[hi]
    data[hi] = tmp

# 2 splits, pivot in the middle, good for random data, bad for many duplicates or presorted data, crashes on duplicates, nots stable
# will not be used for the benchmarks, but I will keep it here for testing purposes and because I didnt want to delete my work
def quicksort_2way_inplace(data, lo: int = 0, hi: int | None = None, depth: int = 1):
    if hi is None:
        hi = len(data) - 1

    counters = active_counters()
    if counters is not None:
        counters.partition_calls += 1
        counters.max_recursion_depth = max(counters.max_recursion_depth, depth)

    if lo >= hi:
        return data

    _move_pivot_to_end(data, lo, hi)
    p = _partition_2way(data, lo, hi)

    quicksort_2way_inplace(data, lo, p - 1, depth + 1)
    quicksort_2way_inplace(data, p + 1, hi, depth + 1)
    return data

# Helper function for quicksort_2way_inplace, partitions the array and returns the index of the pivot after partitioning
def _partition_2way(data, lo: int, hi: int) -> int:
    pivot = data[hi]
    i = lo

    for j in range(lo, hi):
        if data[j] <= pivot:
            tmp = data[i]
            data[i] = data[j]
            data[j] = tmp
            i += 1

    tmp = data[i]
    data[i] = data[hi]
    data[hi] = tmp
    return i


def quicksort_3way_inplace(data, lo: int = 0, hi: int | None = None, depth: int = 1):
    if hi is None:
        hi = len(data) - 1

    counters = active_counters()
    if counters is not None:
        counters.partition_calls += 1
        counters.max_recursion_depth = max(counters.max_recursion_depth, depth)

    if lo >= hi:
        return data

    _move_pivot_to_end(data, lo, hi)
    pivot = data[hi]

    lt = lo
    i = lo
    gt = hi

    while i <= gt:
        if data[i] < pivot:
            tmp = data[lt]
            data[lt] = data[i]
            data[i] = tmp
            lt += 1
            i += 1
        elif data[i] > pivot:
            tmp = data[i]
            data[i] = data[gt]
            data[gt] = tmp
            gt -= 1
        else:
            i += 1

    quicksort_3way_inplace(data, lo, lt - 1, depth + 1)
    quicksort_3way_inplace(data, gt + 1, hi, depth + 1)
    return data
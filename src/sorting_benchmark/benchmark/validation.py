from __future__ import annotations


def unwrap_values(data) -> list:
    result = []
    for item in data:
        result.append(getattr(item, "value", item))
    return result


def is_sorted_non_decreasing(data) -> bool:
    return all(data[i] <= data[i + 1] for i in range(len(data) - 1))


def same_elements(a, b) -> bool:
    return sorted(a) == sorted(b)
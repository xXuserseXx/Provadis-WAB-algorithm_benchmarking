from __future__ import annotations

import csv
import os

# resuls are logged in csv for easy analysis of data in excel. I dont want to bother with pandas right now
FIELDNAMES = [
    "algorithm",
    "dataset",
    "size",
    "seed",
    "repetition",
    "runtime_ns",
    "comparisons",
    "writes",
    "partition_calls",
    "max_recursion_depth",
    "peak_mem_bytes",
    "correct",
    "error",
]


def ensure_csv_exists(path: str) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    if os.path.exists(path):
        return

    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
        writer.writeheader()


def append_row(path: str, row: dict) -> None:
    with open(path, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
        writer.writerow(row)
from __future__ import annotations

from sorting_benchmark.algorithms.builtin import builtin_sorted
from sorting_benchmark.algorithms.insertion import insertion_sort_inplace
from sorting_benchmark.algorithms.merge import mergesort
from sorting_benchmark.algorithms.quicksort import (
    quicksort_2way_inplace,
    quicksort_3way_inplace,
)
from sorting_benchmark.benchmark.specs import AlgorithmSpec, DatasetSpec, RunSpec
from sorting_benchmark.data.generators import (
    gen_duplicates,
    gen_presorted_with_swaps,
    gen_random_permutation,
    gen_reverse_sorted,
)


def default_algorithms() -> list[AlgorithmSpec]:
    return [
        AlgorithmSpec("builtin_sorted", builtin_sorted, inplace=False),
        AlgorithmSpec("mergesort", mergesort, inplace=False),
        AlgorithmSpec("quicksort_3way", quicksort_3way_inplace, inplace=True, use_instrumented_list=True),
        AlgorithmSpec("insertion_sort", insertion_sort_inplace, inplace=True, use_instrumented_list=True),
        ]


def default_datasets() -> list[DatasetSpec]:
    return [
        DatasetSpec("random", gen_random_permutation),
        DatasetSpec("reverse", gen_reverse_sorted),
        DatasetSpec("presorted_10pct_swaps", gen_presorted_with_swaps, {"swap_fraction": 0.10}),
        DatasetSpec("presorted_25pct_swaps", gen_presorted_with_swaps, {"swap_fraction": 0.25}),
        DatasetSpec("duplicates_10", gen_duplicates, {"unique_values": 10}),
    ]


def default_run_specs(
    algorithms: list[AlgorithmSpec],
    datasets: list[DatasetSpec],
    sizes: list[int],
    seeds: list[int],
    repetitions: int,
) -> list[RunSpec]:
    specs = []
    for algorithm in algorithms:
        for dataset in datasets:
            for size in sizes:
                for seed in seeds:
                    for repetition in range(repetitions):
                        specs.append(
                            RunSpec(
                                algorithm=algorithm,
                                dataset=dataset,
                                size=size,
                                seed=seed,
                                repetition=repetition,
                            )
                        )
    return specs
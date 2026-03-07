from __future__ import annotations

import gc
import time
import tracemalloc

from sorting_benchmark.benchmark.csv_logger import append_row, ensure_csv_exists
from sorting_benchmark.benchmark.validation import (
    is_sorted_non_decreasing,
    same_elements,
    unwrap_values,
)
from sorting_benchmark.instrumentation.counters import CounterContext
from sorting_benchmark.instrumentation.lists import InstrumentedList
from sorting_benchmark.instrumentation.values import InstrumentedValue


def _prepare_input(raw_data: list[int], use_instrumented_list: bool):
    wrapped = [InstrumentedValue(x) for x in raw_data]
    if use_instrumented_list:
        return InstrumentedList(wrapped)
    return wrapped


def _execute_algorithm(algorithm_spec, prepared_input):
    if algorithm_spec.inplace:
        return algorithm_spec.function(prepared_input, **algorithm_spec.kwargs)
    return algorithm_spec.function(prepared_input, **algorithm_spec.kwargs)


def run_single_benchmark(run_spec, warmup: int = 1, measure_memory: bool = True) -> dict:
    raw_data = run_spec.dataset.generator(
        run_spec.size,
        run_spec.seed,
        **run_spec.dataset.kwargs,
    )

    # warmup runs to mitigate startup overhead, will not be used, due to hardware limitations and insertion sort being really slow on large inputs, which makes the warmup runs take a very long time, and they are not really necessary for the insights I want to gain from the benchmarks
    for _ in range(warmup):
        with CounterContext():
            warmup_input = _prepare_input(raw_data, run_spec.algorithm.use_instrumented_list)
            _execute_algorithm(run_spec.algorithm, warmup_input)

    if measure_memory:
        tracemalloc.start()

    gc_enabled = gc.isenabled()
    if gc_enabled:
        gc.disable()

    result = {
        "algorithm": run_spec.algorithm.name,
        "dataset": run_spec.dataset.name,
        "size": run_spec.size,
        "seed": run_spec.seed,
        "repetition": run_spec.repetition,
        "runtime_ns": None,
        "comparisons": None,
        "writes": None,
        "partition_calls": None,
        "max_recursion_depth": None,
        "peak_mem_bytes": None,
        "correct": False,
        "error": "",
    }

    try:
        with CounterContext() as counters:
            prepared_input = _prepare_input(raw_data, run_spec.algorithm.use_instrumented_list)

            start = time.perf_counter_ns()
            output = _execute_algorithm(run_spec.algorithm, prepared_input)
            end = time.perf_counter_ns()

            final_data = output if output is not None else prepared_input
            final_values = unwrap_values(final_data)

            result["runtime_ns"] = end - start
            result["comparisons"] = counters.comparisons
            result["writes"] = counters.writes
            result["partition_calls"] = counters.partition_calls
            result["max_recursion_depth"] = counters.max_recursion_depth
            result["correct"] = (
                is_sorted_non_decreasing(final_values)
                and same_elements(raw_data, final_values)
            )
            if not result["correct"]:
                result["error"] = "validation_failed"

    except Exception as exc:
        result["error"] = type(exc).__name__

    finally:
        if gc_enabled:
            gc.enable()

        if measure_memory:
            _, peak = tracemalloc.get_traced_memory()
            result["peak_mem_bytes"] = peak
            tracemalloc.stop()

    return result


def run_benchmarks(run_specs: list, output_csv: str, warmup: int = 1, measure_memory: bool = True) -> None:
    ensure_csv_exists(output_csv)

    for run_spec in run_specs:
        row = run_single_benchmark(
            run_spec=run_spec,
            warmup=warmup,
            measure_memory=measure_memory,
        )
        append_row(output_csv, row)
        print(
            f"{row['algorithm']} | {row['dataset']} | n={row['size']} | "
            f"seed={row['seed']} | rep={row['repetition']} | ok={row['correct']}"
        )
from sorting_benchmark.benchmark.runner import run_benchmarks
from sorting_benchmark.experiments.defaults import (
    default_algorithms,
    default_datasets,
    default_run_specs,
)

if __name__ == "__main__":
    run_specs = default_run_specs(
        algorithms=default_algorithms(),
        datasets=default_datasets(),
        sizes=[50000],
        seeds=list(range(1,100)),
        repetitions=1,
    )
    run_benchmarks(
        run_specs=run_specs,
        output_csv="results/runs.csv",
        warmup=0, # warmup runs are a functionality, but disabled due to insertion sort fucking me over
        measure_memory=True,
    )
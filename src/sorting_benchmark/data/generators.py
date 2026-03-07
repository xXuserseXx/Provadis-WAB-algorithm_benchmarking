from __future__ import annotations

import math
import random

# I dont think ts needs explaining
def gen_random_permutation(n: int, seed: int) -> list[int]:
    rng = random.Random(seed)
    data = list(range(n))
    rng.shuffle(data)
    return data

# literally just a reverse sorted list
def gen_reverse_sorted(n: int, seed: int) -> list[int]:
    return list(range(n - 1, -1, -1))

# generating the presorted data (meaning partially swapped) by randomly swapping a fraction of the elements in an sorted list
def gen_presorted_with_swaps(n: int, seed: int, swap_fraction: float = 0.01) -> list[int]:
    rng = random.Random(seed)
    data = list(range(n))
    swaps = math.ceil(n * swap_fraction)
    for _ in range(swaps):
        i = rng.randrange(n)
        j = rng.randrange(n)
        data[i], data[j] = data[j], data[i]
    return data

# many duplicates due to limited number of unqiue values
def gen_duplicates(n: int, seed: int, unique_values: int = 10) -> list[int]:
    rng = random.Random(seed)
    return [rng.randrange(unique_values) for _ in range(n)]
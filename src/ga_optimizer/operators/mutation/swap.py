# Implementuje mutację zamiany

from __future__ import annotations
import random
from typing import Any


def mutation_swap(
    chromosomes: list[list[int]],
    config_dict: dict[str, Any],
) -> list[list[int]]:

    p = config_dict["mutation_swap_p"]
    rng = config_dict["rng"]

    mutated = []

    for chromosome in chromosomes:

        new_chromosome = chromosome.copy()

        if rng.random() < p and len(new_chromosome) >= 2:

            i, j = rng.sample(range(len(new_chromosome)), 2)

            new_chromosome[i], new_chromosome[j] = (
                new_chromosome[j],
                new_chromosome[i],
            )

        mutated.append(new_chromosome)

    return mutated
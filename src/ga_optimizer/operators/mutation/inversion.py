# Implementuje mutację inwersji

from __future__ import annotations
import random
from typing import Any


def mutation_inversion(
    chromosomes: list[list[int]],
    config_dict: dict[str, Any],
) -> list[list[int]]:

    p = config_dict["mutation_inversion_p"]

    mutated = []

    for chromosome in chromosomes:

        new_chromosome = chromosome.copy()

        if random.random() < p and len(new_chromosome) >= 3:

            i, j = sorted(random.sample(range(len(new_chromosome)), 2))

            new_chromosome[i:j] = reversed(new_chromosome[i:j])

        mutated.append(new_chromosome)

    return mutated
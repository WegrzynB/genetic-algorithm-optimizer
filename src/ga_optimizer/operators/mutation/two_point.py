# Implementuje mutację dwupunktową

from __future__ import annotations
import random
from typing import Any


def mutation_two_point(
    chromosomes: list[list[int]],
    config_dict: dict[str, Any],
) -> list[list[int]]:

    p = config_dict["mutation_two_point_p"]
    rng = config_dict["rng"]

    mutated = []

    for chromosome in chromosomes:

        new_chromosome = chromosome.copy()

        if rng.random() < p and len(new_chromosome) >= 2:

            i, j = rng.sample(range(len(new_chromosome)), 2)

            new_chromosome[i] = 1 - new_chromosome[i]
            new_chromosome[j] = 1 - new_chromosome[j]

        mutated.append(new_chromosome)

    return mutated
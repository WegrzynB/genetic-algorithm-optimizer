# Implementuje mutację tasowania

from __future__ import annotations
import random
from typing import Any


def mutation_scramble(
    chromosomes: list[list[int]],
    config_dict: dict[str, Any],
) -> list[list[int]]:

    p = config_dict["mutation_scramble_p"]
    rng = config_dict["rng"]

    mutated = []

    for chromosome in chromosomes:

        new_chromosome = chromosome.copy()

        if rng.random() < p and len(new_chromosome) >= 3:

            i, j = sorted(rng.sample(range(len(new_chromosome)), 2))

            segment = new_chromosome[i:j]
            rng.shuffle(segment)

            new_chromosome[i:j] = segment

        mutated.append(new_chromosome)

    return mutated
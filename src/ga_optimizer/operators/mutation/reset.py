# Implementuje mutację resetowania

from __future__ import annotations
import random
from typing import Any


def mutation_reset(
    chromosomes: list[list[int]],
    config_dict: dict[str, Any],
) -> list[list[int]]:

    p = config_dict["mutation_reset_p"]
    rng = config_dict["rng"]

    mutated = []

    for chromosome in chromosomes:

        new_chromosome = chromosome.copy()

        if rng.random() < p:

            idx = rng.randrange(len(new_chromosome))
            new_chromosome[idx] = rng.choice([0, 1])

        mutated.append(new_chromosome)

    return mutated
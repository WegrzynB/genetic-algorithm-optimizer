# Implementuje mutację resetowania

from __future__ import annotations
import random
from typing import Any


def mutation_reset(
    chromosomes: list[list[int]],
    config_dict: dict[str, Any],
) -> list[list[int]]:

    p = config_dict["mutation_reset_p"]

    mutated = []

    for chromosome in chromosomes:

        new_chromosome = chromosome.copy()

        if random.random() < p:

            idx = random.randrange(len(new_chromosome))
            new_chromosome[idx] = random.choice([0, 1])

        mutated.append(new_chromosome)

    return mutated
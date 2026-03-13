# Implementuje mutację bitową

from __future__ import annotations
import random
from typing import Any


def mutation_bit_flip(
    chromosomes: list[list[int]],
    config_dict: dict[str, Any],
) -> list[list[int]]:

    p = config_dict["mutation_bit_flip_p"]

    mutated = []

    for chromosome in chromosomes:

        new_chromosome = chromosome.copy()

        for i in range(len(new_chromosome)):
            if random.random() < p:
                new_chromosome[i] = 1 - new_chromosome[i]

        mutated.append(new_chromosome)

    return mutated
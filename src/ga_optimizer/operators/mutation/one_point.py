# Implementuje mutację jednopunktową

from __future__ import annotations
import random
from typing import Any


def mutation_one_point(
    chromosomes: list[list[int]],
    config_dict: dict[str, Any],
) -> list[list[int]]:

    p = config_dict["mutation_one_point_p"]
    rng = config_dict["rng"]

    mutated = []

    for chromosome in chromosomes:

        new_chromosome = chromosome.copy()

        if rng.random() < p:
            index = rng.randrange(len(new_chromosome))
            new_chromosome[index] = 1 - new_chromosome[index]

        mutated.append(new_chromosome)

    return mutated
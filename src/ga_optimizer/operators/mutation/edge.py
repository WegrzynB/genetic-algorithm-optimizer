# Implementuje mutację skrajnych bitów/genów

from __future__ import annotations
import random
from typing import Any


def mutation_edge(
    chromosomes: list[list[int]],
    config_dict: dict[str, Any],
) -> list[list[int]]:

    p = config_dict["mutation_edge_p"]
    mode = config_dict["mutation_edge_mode"]
    rng = config_dict["rng"]

    mutated = []

    for chromosome in chromosomes:

        new_chromosome = chromosome.copy()

        if rng.random() < p and len(new_chromosome) >= 2:

            first = 0
            last = len(new_chromosome) - 1

            if mode == "Ends":
                idx = rng.choice([first, last])
                new_chromosome[idx] = 1 - new_chromosome[idx]

            elif mode == "First_last":
                new_chromosome[first] = 1 - new_chromosome[first]

            elif mode == "Both":
                new_chromosome[first] = 1 - new_chromosome[first]
                new_chromosome[last] = 1 - new_chromosome[last]

        mutated.append(new_chromosome)

    return mutated
# Implementuje operator inwersji fragmentu chromosomu

from __future__ import annotations
import random
from typing import Any
from ga_optimizer.utils.helpers import debug_print


def inversion(
    chromosomes: list[list[int]],
    config_dict: dict[str, Any],
) -> list[list[int]]:

    inversion_enabled = config_dict["inversion_enabled"]
    verbose = bool(config_dict.get("verbose", False))
    rng = config_dict["rng"]

    if not inversion_enabled:
        return chromosomes

    inverted = []

    debug_print(verbose, "\n"f"INVERSION")
    for i, chromosome in enumerate(chromosomes):
        if len(chromosome) < 2:
            inverted.append(chromosome)
            continue

        new_chromosome = list(chromosome)

        point1 = rng.randint(0, len(new_chromosome) - 2)
        point2 = rng.randint(point1 + 1, len(new_chromosome) - 1)

        debug_print(verbose, f"\nChromosome {i}")
        debug_print(verbose, "Before:", new_chromosome)
        debug_print(verbose, f"Inversion points: {point1}, {point2}")

        fragment = new_chromosome[point1:point2+1]

        new_chromosome[point1:point2+1] = fragment[::-1]

        debug_print(verbose, "After:", new_chromosome)

        inverted.append(new_chromosome)

    return inverted



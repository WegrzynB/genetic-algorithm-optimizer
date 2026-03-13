# Implementuje operator inwersji fragmentu chromosomu

from __future__ import annotations
import random
from typing import Any


def inversion(
    chromosomes: list[list[int]],
    config_dict: dict[str, Any],
) -> list[list[int]]:

    inversion_enabled = config_dict["inversion_enabled"]

    if not inversion_enabled:
        return chromosomes

    inverted = []

    print("\n"f"INVERSION")
    for i, chromosome in enumerate(chromosomes):
        if len(chromosome) < 2:
            inverted.append(chromosome)
            continue

        new_chromosome = list(chromosome)

        point1 = random.randint(0, len(new_chromosome) - 2)
        point2 = random.randint(point1 + 1, len(new_chromosome) - 1)

        print(f"\nChromosome {i}")
        print("Before:", new_chromosome)
        print(f"Inversion points: {point1}, {point2}")

        fragment = new_chromosome[point1:point2+1]

        new_chromosome[point1:point2+1] = fragment[::-1]

        print("After:", new_chromosome)

        inverted.append(new_chromosome)

    return inverted



# krzyżowanie dwupunktowe

from __future__ import annotations

import random
from typing import Any


def two_point_crossover(
    chromosomes: list[list[int]],
    config_dict: dict[str, Any],
) -> list[list[int]]:

    p = config_dict["crossover_two_point_p"]
    rng = config_dict["rng"]

    new_population = chromosomes.copy()

    for i in range(0, len(chromosomes) - 1, 2):

        parent1 = chromosomes[i]
        parent2 = chromosomes[i + 1]

        if rng.random() > p:
            continue

        length = len(parent1)

        point1 = rng.randint(1, length - 2)
        point2 = rng.randint(point1 + 1, length - 1)

        child1 = (
            parent1[:point1]
            + parent2[point1:point2]
            + parent1[point2:]
        )

        child2 = (
            parent2[:point1]
            + parent1[point1:point2]
            + parent2[point2:]
        )

        new_population[i] = child1
        new_population[i + 1] = child2

    return new_population
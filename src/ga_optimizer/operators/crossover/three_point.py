#Krzyżowanie trzypunktowe

from __future__ import annotations

import random
from typing import Any


def three_point_crossover(
    chromosomes: list[list[int]],
    config_dict: dict[str, Any],
) -> list[list[int]]:

    p = config_dict["crossover_three_point_p"]
    rng = config_dict["rng"]

    new_population = [c[:] for c in chromosomes]

    for i in range(0, len(chromosomes) - 1, 2):

        parent1 = chromosomes[i]
        parent2 = chromosomes[i + 1]

        if rng.random() > p:
            continue

        length = len(parent1)

        points = sorted(rng.sample(range(1, length), 3))

        p1, p2, p3 = points

        child1 = (
            parent1[:p1]
            + parent2[p1:p2]
            + parent1[p2:p3]
            + parent2[p3:]
        )

        child2 = (
            parent2[:p1]
            + parent1[p1:p2]
            + parent2[p2:p3]
            + parent1[p3:]
        )

        new_population[i] = child1
        new_population[i + 1] = child2

    return new_population
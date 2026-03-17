# Krzyżowanie zredukowane

from __future__ import annotations

import random
from typing import Any


def reduced_surro_crossover(
    chromosomes: list[list[int]],
    config_dict: dict[str, Any],
) -> list[list[int]]:

    p = config_dict["crossover_reduced_surro_p"]
    rng = config_dict["rng"]

    new_population = [c[:] for c in chromosomes]

    for i in range(0, len(chromosomes) - 1, 2):

        parent1 = chromosomes[i]
        parent2 = chromosomes[i + 1]

        if rng.random() > p:
            continue

        length = len(parent1)

        candidate_points = [
            j for j in range(1, length)
            if parent1[j] != parent2[j]
        ]
        if not candidate_points:
            continue

        point = rng.choice(candidate_points)

        child1 = parent1[:point] + parent2[point:]
        child2 = parent2[:point] + parent1[point:]

        new_population[i] = child1
        new_population[i + 1] = child2

    return new_population
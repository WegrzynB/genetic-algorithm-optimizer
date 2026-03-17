# krzyżowanie ziarniste

from __future__ import annotations

import random
from typing import Any


def granular_crossover(
    chromosomes: list[list[int]],
    config_dict: dict[str, Any],
) -> list[list[int]]:

    p = config_dict["crossover_granular_p"]
    granularity = config_dict["crossover_granular_granularity"]
    rng = config_dict["rng"]

    new_population = [c[:] for c in chromosomes]

    for i in range(0, len(chromosomes) - 1, 2):

        parent1 = chromosomes[i]
        parent2 = chromosomes[i + 1]

        # czy w ogóle robimy crossover
        if rng.random() > p:
            continue

        length = len(parent1)

        child1 = parent1[:]
        child2 = parent2[:]

        # przechodzimy blokami genów
        for g in range(0, length, granularity):

            a = rng.random()

            end = min(g + granularity, length)

            if a <= 0.5:
                child1[g:end] = parent1[g:end]
                child2[g:end] = parent2[g:end]
            else:
                child1[g:end] = parent2[g:end]
                child2[g:end] = parent1[g:end]

        new_population[i] = child1
        new_population[i + 1] = child2

    return new_population
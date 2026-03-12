# Krzyżowanie równomierne

from __future__ import annotations

import random
from typing import Any


def uniform_crossover(
    chromosomes: list[list[int]],
    config_dict: dict[str, Any],
) -> list[list[int]]:

    p = config_dict["crossover_uniform_p"]

    new_population = [c[:] for c in chromosomes]

    for i in range(0, len(chromosomes) - 1, 2):

        parent1 = chromosomes[i]
        parent2 = chromosomes[i + 1]

        child1 = parent1[:]
        child2 = parent2[:]

        for g in range(len(parent1)):

            alpha = random.random()

            if alpha < p:
                child1[g] = parent2[g]
                child2[g] = parent1[g]

        new_population[i] = child1
        new_population[i + 1] = child2

    return new_population
# Krzyżowanie niszczące

from __future__ import annotations

import random
from typing import Any


def disruptive_crossover(
    chromosomes: list[list[int]],
    config_dict: dict[str, Any],
) -> list[list[int]]:

    p = config_dict["crossover_disruptive_p"]

    new_population = [c[:] for c in chromosomes]

    for i in range(0, len(chromosomes) - 1, 2):

        parent1 = chromosomes[i]
        parent2 = chromosomes[i + 1]

        if random.random() > p:
            continue

        child1 = parent1[:]
        child2 = parent2[:]

        diff_positions = [
            j for j in range(len(parent1))
            if parent1[j] != parent2[j]
        ]

        diff = len(diff_positions)

        if diff == 0:
            continue

        swaps = diff // 2

        chosen_positions = random.sample(diff_positions, swaps)

        for pos in chosen_positions:

            child1[pos], child2[pos] = child2[pos], child1[pos]

        new_population[i] = child1
        new_population[i + 1] = child2

    return new_population
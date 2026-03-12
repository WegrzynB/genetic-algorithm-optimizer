# Krzyżowanie jednopunktowe

from __future__ import annotations

import random
from typing import Any


def one_point_crossover(
    chromosomes: list[list[int]],
    config_dict: dict[str, Any],
) -> list[list[int]]:

    p = config_dict["crossover_one_point_p"]

    new_population = chromosomes.copy()

    for i in range(0, len(chromosomes) - 1, 2):

        parent1 = chromosomes[i]
        parent2 = chromosomes[i + 1]

        # ZABEZPIECZENIE
        if len(parent1) < 2:
            continue

        if random.random() <= p:

            length = len(parent1)

            # losujemy punkt przecięcia
            point = random.randint(1, length - 1)

            child1 = parent1[:point] + parent2[point:]
            child2 = parent2[:point] + parent1[point:]

            new_population[i] = child1
            new_population[i + 1] = child2

    return new_population
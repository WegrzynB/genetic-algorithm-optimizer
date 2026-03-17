#Krzyżowanie wielopunktowe

from __future__ import annotations

import random
from typing import Any


def multi_point_crossover(
    chromosomes: list[list[int]],
    config_dict: dict[str, Any],
) -> list[list[int]]:

    p = config_dict["crossover_multi_point_p"]
    k = config_dict["crossover_multi_point_k"]
    rng = config_dict["rng"]

    new_population = [c[:] for c in chromosomes]

    for i in range(0, len(chromosomes) - 1, 2):

        parent1 = chromosomes[i]
        parent2 = chromosomes[i + 1]

        if rng.random() > p:
            continue

        length = len(parent1)

        k = min(k, length - 1)

        points = sorted(rng.sample(range(1, length), k))
        points = [0] + points + [length]

        child1 = []
        child2 = []

        swap = False

        for j in range(len(points) - 1):

            start = points[j]
            end = points[j + 1]

            if not swap:
                child1 += parent1[start:end]
                child2 += parent2[start:end]
            else:
                child1 += parent2[start:end]
                child2 += parent1[start:end]

            swap = not swap

        new_population[i] = child1
        new_population[i + 1] = child2

    return new_population
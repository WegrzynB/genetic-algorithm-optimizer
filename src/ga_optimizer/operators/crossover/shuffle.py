#Krzyżowanie tasujące

from __future__ import annotations

import random
from typing import Any

def shuffle_crossover(
    chromosomes: list[list[int]],
    config_dict: dict[str, Any],
) -> list[list[int]]:

    p = config_dict["crossover_shuffle_p"]

    new_population = [c[:] for c in chromosomes]

    for i in range(0, len(chromosomes) - 1, 2):

        parent1 = chromosomes[i]
        parent2 = chromosomes[i + 1]

        if random.random() > p:
            continue

        length = len(parent1)

        perm = list(range(length))
        random.shuffle(perm)

        shuffled1 = [parent1[j] for j in perm]
        shuffled2 = [parent2[j] for j in perm]

        point = random.randint(1, length - 1)

        child1 = shuffled1[:point] + shuffled2[point:]
        child2 = shuffled2[:point] + shuffled1[point:]

        unshuffled1 = [0] * length
        unshuffled2 = [0] * length

        for j, pj in enumerate(perm):
            unshuffled1[pj] = child1[j]
            unshuffled2[pj] = child2[j]

        new_population[i] = unshuffled1
        new_population[i + 1] = unshuffled2

    return new_population
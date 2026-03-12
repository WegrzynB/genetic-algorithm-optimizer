#Krzyżowanie większościowe

from __future__ import annotations

import random
from typing import Any


def majority_crossover(
    chromosomes: list[list[int]],
    config_dict: dict[str, Any],
) -> list[list[int]]:

    p = config_dict["crossover_majority_p"]

    new_population = [c[:] for c in chromosomes]

    for i in range(0, len(chromosomes) - 1, 2):

        parent1 = chromosomes[i]
        parent2 = chromosomes[i + 1]

        if random.random() > p:
            continue

        length = len(parent1)

        child1 = []
        child2 = []

        for g in range(length):

            if parent1[g] == parent2[g]:

                child1.append(parent1[g])
                child2.append(parent2[g])

            else:

                gene = random.choice([parent1[g], parent2[g]])

                child1.append(gene)
                child2.append(1 - gene)

        new_population[i] = child1
        new_population[i + 1] = child2

    return new_population
# Implementuje zachowanie najlepszych osobników między epokami

from __future__ import annotations
from typing import Any


def elitism(
    chromosomes: list[list[int]],
    fitness_values: list[float],
    previous_chromosomes: list[list[int]],
    previous_fitness: list[float],
    config_dict: dict,
) -> list[list[int]]:

    elitism_enabled = config_dict["elitism_enabled"]

    if not elitism_enabled:
        return chromosomes

    print("ELITISM")
    print("Previous fitness:", previous_fitness)
    print("New fitness:", fitness_values)

    # najlepszy z poprzedniej populacji
    best_index = previous_fitness.index(min(previous_fitness))
    best_chromosome = list(previous_chromosomes[best_index])

    # najgorszy z nowej populacji
    worst_index = fitness_values.index(max(fitness_values))

    print("Best from previous:", best_chromosome)
    print("Replacing chromosome index:", worst_index)
    print("\n")

    new_population = chromosomes.copy()
    new_population[worst_index] = best_chromosome

    return new_population
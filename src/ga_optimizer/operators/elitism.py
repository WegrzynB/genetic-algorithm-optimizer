# elitism.py
# Implementuje zachowanie najlepszego osobnika między epokami

from __future__ import annotations
from typing import Any


def elitism(
    chromosomes: list[list[int]],
    fitness_values: list[float],
    previous_chromosomes: list[list[int]],
    previous_fitness: list[float],
    config_dict: dict[str, Any],
) -> list[list[int]]:

    elitism_enabled = config_dict.get("elitism_enabled", False)
    objective_mode = config_dict.get("objective_mode", "min")

    if not elitism_enabled:
        return chromosomes

    if not chromosomes or not previous_chromosomes:
        return chromosomes

    print("ELITISM")
    print("Previous fitness:", previous_fitness)
    print("New fitness:", fitness_values)

    # wybór najlepszego z poprzedniej populacji
    if objective_mode == "max":
        best_index = previous_fitness.index(max(previous_fitness))
        worst_index = fitness_values.index(min(fitness_values))
    else:
        best_index = previous_fitness.index(min(previous_fitness))
        worst_index = fitness_values.index(max(fitness_values))

    best_chromosome = previous_chromosomes[best_index].copy()

    print("Best from previous:", best_chromosome)
    print("Replacing chromosome index:", worst_index)
    print()

    new_population = [c.copy() for c in chromosomes]
    new_population[worst_index] = best_chromosome

    return new_population

# elitism.py
# Implementuje zachowanie najlepszego osobnika między epokami

from __future__ import annotations
from typing import Any
from ga_optimizer.utils.helpers import debug_print


def elitism(
    chromosomes: list[list[int]],
    fitness_values: list[float],
    previous_chromosomes: list[list[int]],
    previous_fitness: list[float],
    config_dict: dict[str, Any],
) -> list[list[int]]:

    elitism_enabled = config_dict.get("elitism_enabled", False)
    objective_mode = config_dict.get("objective_mode", "min")
    verbose = bool(config_dict.get("verbose", False))

    if not elitism_enabled:
        return chromosomes

    if not chromosomes or not previous_chromosomes:
        return chromosomes

    debug_print(verbose, "ELITISM")
    debug_print(verbose, "Previous fitness:", previous_fitness)
    debug_print(verbose, "New fitness:", fitness_values)

    # wybór najlepszego z poprzedniej populacji
    if objective_mode == "max":
        best_index = previous_fitness.index(max(previous_fitness))
        worst_index = fitness_values.index(min(fitness_values))
    else:
        best_index = previous_fitness.index(min(previous_fitness))
        worst_index = fitness_values.index(max(fitness_values))

    best_chromosome = previous_chromosomes[best_index].copy()

    debug_print(verbose, "Best from previous:", best_chromosome)
    debug_print(verbose, "Replacing chromosome index:", worst_index)
    debug_print(verbose)

    new_population = [c.copy() for c in chromosomes]
    new_population[worst_index] = best_chromosome

    return new_population

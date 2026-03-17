# ga_optimizer/operators/selection/sus.py

from __future__ import annotations

import random
from typing import Any, TYPE_CHECKING

if TYPE_CHECKING:
    from ga_optimizer.core.population import Population


def select_sus(population: "Population", num_parents: int, config_dict: dict[str, Any]) -> list[list[int]]:
    eps = config_dict.get("selection_sus_eps", 1e-9)
    rng = config_dict["rng"]
    
    total_fitness = sum((f or 0.0) + eps for f in population.fitness_values)
    distance = total_fitness / num_parents
    start_point = rng.uniform(0.0, distance)
    pointers = [start_point + i * distance for i in range(num_parents)]
    selected_chromosomes: list[list[int]] = []

    idx = 0
    current_sum = (population.fitness_values[idx] or 0.0) + eps

    for pointer in pointers:
        while current_sum < pointer and idx < len(population) - 1:
            idx += 1
            current_sum += (population.fitness_values[idx] or 0.0) + eps

        selected_chromosomes.append(population.chromosomes[idx].copy())

    return selected_chromosomes
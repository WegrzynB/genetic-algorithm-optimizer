# ga_optimizer/operators/selection/roulette.py

from __future__ import annotations

import random
from typing import Any, TYPE_CHECKING

if TYPE_CHECKING:
    from ga_optimizer.core.population import Population


def select_roulette(
    population: "Population",
    num_parents: int,
    config_dict: dict[str, Any],
    is_copy: bool = False,
) -> list[list[int]]:
    eps_key = "selection_roulette_copy_eps" if is_copy else "selection_roulette_eps"
    rng = config_dict["rng"]
    eps = config_dict.get(eps_key, 1e-9)

    selected_chromosomes: list[list[int]] = []

    # Przeliczamy całkowity fitness populacji uwzględniając epsilon
    total_fitness = sum((f or 0.0) + eps for f in population.fitness_values)

    for _ in range(num_parents):
        spin = rng.uniform(0.0, total_fitness)
        current_sum = 0.0

        for idx, fitness in enumerate(population.fitness_values):
            current_sum += (fitness or 0.0) + eps
            if current_sum >= spin:
                selected_chromosomes.append(population.chromosomes[idx].copy())
                break

    return selected_chromosomes
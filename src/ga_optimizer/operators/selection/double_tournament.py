# ga_optimizer/operators/selection/double_tournament.py

from __future__ import annotations

import random
from typing import Any, TYPE_CHECKING

if TYPE_CHECKING:
    from ga_optimizer.core.population import Population


def select_double_tournament(population: "Population", num_parents: int, config_dict: dict[str, Any]) -> list[list[int]]:
    k1 = config_dict.get("selection_double_tournament_k1", 3)
    k2 = config_dict.get("selection_double_tournament_k2", 3)
    rng = config_dict["rng"]

    pop_size = len(population)
    k1 = max(1, min(k1, pop_size))
    k2 = max(1, min(k2, pop_size))

    selected_chromosomes: list[list[int]] = []
    indices = list(range(pop_size))

    for _ in range(num_parents):
        finalists = []

        for _ in range(k2):
            participants = rng.choices(indices, k=k1)
            winner = max(
                participants,
                key=lambda i: population.fitness_values[i] if population.fitness_values[i] is not None else float("-inf"),
            )
            finalists.append(winner)

        grand_winner = max(
            finalists,
            key=lambda i: population.fitness_values[i] if population.fitness_values[i] is not None else float("-inf"),
        )
        selected_chromosomes.append(population.chromosomes[grand_winner].copy())

    return selected_chromosomes
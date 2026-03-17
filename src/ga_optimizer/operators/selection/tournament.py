# ga_optimizer/operators/selection/tournament.py

from __future__ import annotations

import random
from typing import Any, TYPE_CHECKING

if TYPE_CHECKING:
    from ga_optimizer.core.population import Population


def select_tournament(population: "Population", num_parents: int, config_dict: dict[str, Any]) -> list[list[int]]:
    k = config_dict.get("selection_tournament_k", 3)
    k = max(1, min(k, len(population)))
    rng = config_dict["rng"]

    selected_chromosomes: list[list[int]] = []
    indices = list(range(len(population)))

    for _ in range(num_parents):
        # Losujemy K indeksów uczestników turnieju
        participants_indices = rng.choices(indices, k=k)

        # Wybieramy indeks zwycięzcy z największym fitness
        winner_idx = max(
            participants_indices,
            key=lambda i: population.fitness_values[i] if population.fitness_values[i] is not None else float("-inf"),
        )
        selected_chromosomes.append(population.chromosomes[winner_idx].copy())

    return selected_chromosomes
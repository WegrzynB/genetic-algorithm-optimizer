# ga_optimizer/operators/selection/unbiased.py

from __future__ import annotations

import random
from typing import Any, TYPE_CHECKING

if TYPE_CHECKING:
    from ga_optimizer.core.population import Population


def select_unbiased(population: "Population", num_parents: int, config_dict: dict[str, Any]) -> list[list[int]]:
    rng = config_dict["rng"]
    selected_chromosomes: list[list[int]] = []
    indices = list(range(len(population)))

    for _ in range(num_parents):
        # rng.choice wybiera jeden element z równym prawdopodobieństwem
        chosen_idx = rng.choice(indices)
        selected_chromosomes.append(population.chromosomes[chosen_idx].copy())

    return selected_chromosomes
# ga_optimizer/operators/selection/unbiased.py

import random
from typing import Any
from ga_optimizer.core.population import Population

def select_unbiased(population: Population, num_parents: int, config_dict: dict[str, Any]) -> list[list[int]]:
    selected_chromosomes: list[list[int]] = []
    indices = list(range(len(population)))
    
    for _ in range(num_parents):
        # random.choice wybiera jeden element z równym prawdopodobieństwem
        chosen_idx = random.choice(indices)
        selected_chromosomes.append(population.chromosomes[chosen_idx].copy())
        
    return selected_chromosomes
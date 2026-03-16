# ga_optimizer/operators/selection/worst.py

from typing import Any
from ga_optimizer.core.population import Population

def select_worst(population: Population, num_parents: int, config_dict: dict[str, Any]) -> list[list[int]]:
    k = config_dict.get("selection_worst_k", 2)
    k = max(1, min(k, len(population)))
    
    # Sortujemy rosnąco (najgorszy na początku)
    sorted_indices = sorted(
        range(len(population)), 
        key=lambda i: population.fitness_values[i] if population.fitness_values[i] is not None else float('inf')
    )
    
    worst_k_indices = sorted_indices[:k]
    selected_chromosomes: list[list[int]] = []
    
    for i in range(num_parents):
        chosen_idx = worst_k_indices[i % len(worst_k_indices)]
        selected_chromosomes.append(population.chromosomes[chosen_idx].copy())
        
    return selected_chromosomes
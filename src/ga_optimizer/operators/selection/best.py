# ga_optimizer/operators/selection/best.py

from typing import Any
from ga_optimizer.core.population import Population

def select_best(population: Population, num_parents: int, config_dict: dict[str, Any]) -> list[list[int]]:
    k = config_dict.get("selection_best_k", 2)
    k = max(1, min(k, len(population)))
    
    # Tworzymy listę indeksów od 0 do N i sortujemy ją malejąco po wartości fitness
    sorted_indices = sorted(
        range(len(population)), 
        key=lambda i: population.fitness_values[i] if population.fitness_values[i] is not None else float('-inf'),
        reverse=True
    )
    
    # Wybieramy indeksy K najlepszych osobników
    best_k_indices = sorted_indices[:k]
    
    selected_chromosomes: list[list[int]] = []
    
    # Kopiujemy geny najlepszych osobników (z rotacją, aby wypełnić pulę rodziców)
    for i in range(num_parents):
        chosen_idx = best_k_indices[i % len(best_k_indices)]
        selected_chromosomes.append(population.chromosomes[chosen_idx].copy())
        
    return selected_chromosomes
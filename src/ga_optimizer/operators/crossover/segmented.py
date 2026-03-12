
#Krzyżowanie segmentowe

from __future__ import annotations
from typing import Any

def segmented_crossover(chromosomes: list[list[int]], config_dict: dict[str, Any]) -> list[list[int]]:
    segment_length = config_dict.get("crossover_segment_length", 3)
    new_chromosomes = []

    for i in range(0, len(chromosomes), 2):
        parent1 = chromosomes[i]
        parent2 = chromosomes[i+1] if i+1 < len(chromosomes) else chromosomes[i]
        child1, child2 = parent1.copy(), parent2.copy()
        
        for start in range(0, len(parent1), segment_length*2):
            end = min(start + segment_length, len(parent1))
            # Zamiana segmentów
            child1[start:end], child2[start:end] = child2[start:end], child1[start:end]
        
        new_chromosomes.extend([child1, child2])

    return new_chromosomes
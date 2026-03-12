#Krzyżowanie arytmetyczne

from __future__ import annotations
from typing import Any

def arithmetic_crossover(chromosomes: list[list[int]], config_dict: dict[str, Any]) -> list[list[int]]:
    alpha = config_dict.get("crossover_arithmetic_alpha", 0.5)
    new_chromosomes = []

    for i in range(0, len(chromosomes), 2):
        parent1 = chromosomes[i]
        parent2 = chromosomes[i+1] if i+1 < len(chromosomes) else chromosomes[i]
        child1 = [int(alpha*p1 + (1-alpha)*p2) for p1, p2 in zip(parent1, parent2)]
        child2 = [int(alpha*p2 + (1-alpha)*p1) for p1, p2 in zip(parent1, parent2)]
        new_chromosomes.extend([child1, child2])
    
    return new_chromosomes
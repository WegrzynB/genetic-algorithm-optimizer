# ga_optimizer/operators/selection/dispatch_selection.py

from __future__ import annotations
from typing import Any

from ga_optimizer.core.population import Population

from ga_optimizer.operators.selection.best import select_best
from ga_optimizer.operators.selection.roulette import select_roulette
from ga_optimizer.operators.selection.tournament import select_tournament


def dispatch_selection(
    population: Population,
    config_dict: dict[str, Any],
) -> list[list[int]]:
    
    method_name = config_dict.get("selection_method", "roulette")
    num_parents = len(population)
    
    match method_name:
        case "best":
            selected_chromosomes = select_best(population, num_parents, config_dict)
            
        case "roulette":
            selected_chromosomes = select_roulette(population, num_parents, config_dict, is_copy=False)
            
        case "roulette copy":
            selected_chromosomes = select_roulette(population, num_parents, config_dict, is_copy=True)

        case "tournament":
            selected_chromosomes = select_tournament(population, num_parents, config_dict)

        case _:
            print(f"[Ostrzeżenie] Nieznana metoda selekcji: {method_name}. Przepisuję populację 1:1.")
            selected_chromosomes = [chrom.copy() for chrom in population.chromosomes]

    return selected_chromosomes
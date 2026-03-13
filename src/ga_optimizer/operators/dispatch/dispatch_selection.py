# ga_optimizer/operators/dispatch/dispatch_selection.py

from __future__ import annotations
from typing import Any

from ga_optimizer.core.population import Population

from ga_optimizer.operators.selection.best import select_best
from ga_optimizer.operators.selection.roulette import select_roulette
from ga_optimizer.operators.selection.tournament import select_tournament
from ga_optimizer.operators.selection.worst import select_worst
from ga_optimizer.operators.selection.unbiased import select_unbiased
from ga_optimizer.operators.selection.double_tournament import select_double_tournament
from ga_optimizer.operators.selection.sus import select_sus


def dispatch_selection(
    chromosomes: list[list[int]],
    config_dict: dict[str, Any],
) -> list[list[int]]:
    temp_pop = Population(config_dict=config_dict)
    temp_pop.set_chromosomes(chromosomes)
    method_name = config_dict.get("selection_method", "roulette")
    num_parents = len(chromosomes)
    
    match method_name:
        case "best":
            selected_chromosomes = select_best(temp_pop, num_parents, config_dict)
            
        case "worst":
            selected_chromosomes = select_worst(temp_pop, num_parents, config_dict)
            
        case "unbiased":
            selected_chromosomes = select_unbiased(temp_pop, num_parents, config_dict)
            
        case "roulette":
            selected_chromosomes = select_roulette(temp_pop, num_parents, config_dict, is_copy=False)
            
        case "roulette copy":
            selected_chromosomes = select_roulette(temp_pop, num_parents, config_dict, is_copy=True)
            
        case "sus":
            selected_chromosomes = select_sus(temp_pop, num_parents, config_dict)

        case "tournament":
            selected_chromosomes = select_tournament(temp_pop, num_parents, config_dict)
            
        case "double_tournament":
            selected_chromosomes = select_double_tournament(temp_pop, num_parents, config_dict)

        case _:
            print(f"[Ostrzeżenie] Nieznana metoda selekcji: {method_name}. Przepisuję populację 1:1.")
            selected_chromosomes = [chrom.copy() for chrom in chromosomes]

    return selected_chromosomes
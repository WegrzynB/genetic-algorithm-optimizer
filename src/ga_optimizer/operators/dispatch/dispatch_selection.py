# ga_optimizer/operators/dispatch/dispatch_selection.py

from __future__ import annotations
from typing import Any

from ga_optimizer.core.population import Population

from ga_optimizer.operators.selection.best import select_best
from ga_optimizer.operators.selection.roulette import select_roulette
from ga_optimizer.operators.selection.tournament import select_tournament


def dispatch_selection(
    chromosomes: list[list[int]],
    config_dict: dict[str, Any],
) -> list[list[int]]:
    
    temp_pop = Population(config_dict=config_dict)
    
    # Wrzucenie genów automatycznie uruchamia ewaluację (liczy fitness)
    temp_pop.set_chromosomes(chromosomes)
    # ------------------------------------

    method_name = config_dict.get("selection_method", "roulette")
    num_parents = len(chromosomes)
    
    match method_name:
        case "best":
            # Przekazujemy naszą tymczasową (ale w pełni przeliczoną) populację
            selected_chromosomes = select_best(temp_pop, num_parents, config_dict)
            
        case "roulette":
            selected_chromosomes = select_roulette(temp_pop, num_parents, config_dict, is_copy=False)
            
        case "roulette copy":
            selected_chromosomes = select_roulette(temp_pop, num_parents, config_dict, is_copy=True)

        case "tournament":
            selected_chromosomes = select_tournament(temp_pop, num_parents, config_dict)

        case _:
            print(f"[Ostrzeżenie] Nieznana metoda selekcji: {method_name}. Przepisuję populację 1:1.")
            selected_chromosomes = [chrom.copy() for chrom in chromosomes]

    return selected_chromosomes
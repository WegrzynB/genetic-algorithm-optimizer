# dispatch_selection.py
# Dispatcher metod selekcji.

from __future__ import annotations

from typing import Any, TYPE_CHECKING

from ga_optimizer.operators.selection.best import select_best
from ga_optimizer.operators.selection.double_tournament import select_double_tournament
from ga_optimizer.operators.selection.roulette import select_roulette
from ga_optimizer.operators.selection.sus import select_sus
from ga_optimizer.operators.selection.tournament import select_tournament
from ga_optimizer.operators.selection.unbiased import select_unbiased
from ga_optimizer.operators.selection.worst import select_worst
from ga_optimizer.utils.helpers import debug_print

if TYPE_CHECKING:
    from ga_optimizer.core.population import Population


def dispatch_selection(
    population: "Population",
    config_dict: dict[str, Any],
) -> list[list[int]]:
    method_name = config_dict.get("selection_method", "roulette")
    num_parents = len(population)
    verbose = bool(config_dict.get("verbose", False))

    match method_name:
        case "best":
            selected_chromosomes = select_best(population, num_parents, config_dict)

        case "worst":
            selected_chromosomes = select_worst(population, num_parents, config_dict)

        case "unbiased":
            selected_chromosomes = select_unbiased(population, num_parents, config_dict)

        case "roulette":
            selected_chromosomes = select_roulette(population, num_parents, config_dict, is_copy=False)

        case "sus":
            selected_chromosomes = select_sus(population, num_parents, config_dict)

        case "tournament":
            selected_chromosomes = select_tournament(population, num_parents, config_dict)

        case "double_tournament":
            selected_chromosomes = select_double_tournament(population, num_parents, config_dict)

        case _:
            debug_print(verbose, f"[Ostrzeżenie] Nieznana metoda selekcji: {method_name}. Przepisuję populację 1:1.")
            selected_chromosomes = [chrom.copy() for chrom in population.chromosomes]

    debug_print(verbose, f"\n[Selection] Chromosomy dla metody: {method_name}")
    for index, chromosome in enumerate(selected_chromosomes):
        debug_print(verbose, f"{index}: {chromosome}")
    debug_print(verbose, "\n")

    return selected_chromosomes
# dispatch_mutation.py
# Dispatcher metod mutacji.

from __future__ import annotations

from typing import Any

from ga_optimizer.operators.mutation.bit_flip import mutation_bit_flip
from ga_optimizer.operators.mutation.edge import mutation_edge
from ga_optimizer.operators.mutation.one_point import mutation_one_point
from ga_optimizer.operators.mutation.reset import mutation_reset
from ga_optimizer.operators.mutation.scramble import mutation_scramble
from ga_optimizer.operators.mutation.swap import mutation_swap
from ga_optimizer.operators.mutation.two_point import mutation_two_point
from ga_optimizer.utils.helpers import debug_print


def dispatch_mutation(
    chromosomes: list[list[int]],
    config_dict: dict[str, Any],
) -> list[list[int]]:
    method_name = config_dict["mutation_method"]
    verbose = bool(config_dict.get("verbose", False))
    mutated_chromosomes = [chromosome.copy() for chromosome in chromosomes]

    match method_name:
        case "one_point":
            mutated_chromosomes = mutation_one_point(chromosomes, config_dict)

        case "two_point":
            mutated_chromosomes = mutation_two_point(chromosomes, config_dict)

        case "edge":
            mutated_chromosomes = mutation_edge(chromosomes, config_dict)

        case "bit_flip":
            mutated_chromosomes = mutation_bit_flip(chromosomes, config_dict)

        case "swap":
            mutated_chromosomes = mutation_swap(chromosomes, config_dict)

        case "scramble":
            mutated_chromosomes = mutation_scramble(chromosomes, config_dict)

        case "reset":
            mutated_chromosomes = mutation_reset(chromosomes, config_dict)

        case _:
            debug_print(verbose, f"[Ostrzeżenie] Nieznana metoda mutacji: {method_name}. Zostawiam chromosomy bez zmian.")

    debug_print(verbose, f"[Mutation] Chromosomy dla metody: {method_name}")
    for index, chromosome in enumerate(mutated_chromosomes):
        debug_print(verbose, f"{index}: {chromosome}")
    debug_print(verbose, "\n")

    return mutated_chromosomes
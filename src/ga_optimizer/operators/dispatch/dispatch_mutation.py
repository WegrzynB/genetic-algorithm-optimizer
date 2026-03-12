# dispatch_mutation.py
# Dispatcher metod mutacji.
# Na razie zwraca chromosomy bez zmian.

from __future__ import annotations

from typing import Any


def dispatch_mutation(
    chromosomes: list[list[int]],
    config_dict: dict[str, Any],
) -> list[list[int]]:
    
    method_name = config_dict["mutation_method"]
    mutated_chromosomes = chromosomes.copy()

    # Tu kod

    print(f"[Mutation] Chromosomy dla metody: {method_name}")
    for index, chromosome in enumerate(mutated_chromosomes):
        print(f"{index}: {chromosome}")
    print("\n")

    return mutated_chromosomes
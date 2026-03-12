# dispatch_crossover.py
# Dispatcher metod krzyżowania.
# Na razie zwraca chromosomy bez zmian.

from __future__ import annotations

from typing import Any


def dispatch_crossover(
    chromosomes: list[list[int]],
    config_dict: dict[str, Any],
) -> list[list[int]]:
    
    method_name = config_dict["crossover_method"]
    crossovered_chromosomes = chromosomes.copy()

    # Tu kod

    print(f"[Crossover] Chromosomy dla metody: {method_name}")
    for index, chromosome in enumerate(crossovered_chromosomes):
        print(f"{index}: {chromosome}")
    print("\n")

    return crossovered_chromosomes
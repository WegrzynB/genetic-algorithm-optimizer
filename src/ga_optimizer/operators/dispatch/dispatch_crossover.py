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
    # Przykład chromosomu:
    # [[0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0], [0, 0, 1, 0, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1], 
    # [0, 0, 1, 0, 1, 1, 1, 0, 1, 0, 1, 0, 1, 1], [0, 0, 0, 0, 1, 0, 0, 0, 1, 1, 1, 1, 0, 1]]
    match method_name:
        case "one_point":
            pass

        case "two_point":
            pass
        
        case _:
            print("Nieznana metoda")

    print(f"[Crossover] Chromosomy dla metody: {method_name}")
    for index, chromosome in enumerate(crossovered_chromosomes):
        print(f"{index}: {chromosome}")
    print("\n")

    return crossovered_chromosomes
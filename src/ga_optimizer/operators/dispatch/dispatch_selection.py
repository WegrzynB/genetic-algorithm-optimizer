# dispatch_selection.py
# Dispatcher metod selekcji.
# Na razie zwraca chromosomy bez zmian.

from __future__ import annotations

from typing import Any


def dispatch_selection(
    chromosomes: list[list[int]],
    config_dict: dict[str, Any],
) -> list[list[int]]:
    
    method_name = config_dict["selection_method"]
    selected_chromosomes = chromosomes.copy()

    # Tu kod
    # Przykład chromosomu:
    # [[0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0], [0, 0, 1, 0, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1], 
    # [0, 0, 1, 0, 1, 1, 1, 0, 1, 0, 1, 0, 1, 1], [0, 0, 0, 0, 1, 0, 0, 0, 1, 1, 1, 1, 0, 1]]
    match method_name:
        case "roulette":
            pass

        case "tournament":
            pass

        case _:
            print("Nieznana metoda")

    print(f"[Selection] Chromosomy dla metody: {method_name}")
    for index, chromosome in enumerate(selected_chromosomes):
        print(f"{index}: {chromosome}")
    print("\n")

    return selected_chromosomes
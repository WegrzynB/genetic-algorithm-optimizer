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

    print(f"[Selection] Placeholder dispatch dla metody: {method_name}")
    for index, chromosome in enumerate(chromosomes):
        print(f"{index}: {chromosome}")
    print("\n")

    return [chromosome.copy() for chromosome in chromosomes]
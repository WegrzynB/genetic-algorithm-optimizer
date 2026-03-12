# dispatch_elitism.py
# Dispatcher operatora elitaryzmu.
# Na razie zwraca chromosomy bez zmian.

from __future__ import annotations

from typing import Any


def dispatch_elitism(
    chromosomes: list[list[int]],
    previous_chromosomes: list[list[int]],
    config_dict: dict[str, Any],
) -> list[list[int]]:
    
    elitism_enabled = config_dict.get("elitism_enabled", False)
    elited_chromosomes = chromosomes.copy()

    if elitism_enabled:
        # Tu kod
        print("Elitaryzm włączony")

    print(f"[Elitism] Chromosomy, aktywne: {elitism_enabled}")
    for index, chromosome in enumerate(elited_chromosomes):
        print(f"{index}: {chromosome}")
    print("\n")

    return elited_chromosomes
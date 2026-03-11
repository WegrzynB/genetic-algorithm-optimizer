# dispatch_inversion.py
# Dispatcher operatora inwersji.
# Na razie zwraca chromosomy bez zmian.

from __future__ import annotations

from typing import Any


def dispatch_inversion(
    chromosomes: list[list[int]],
    config_dict: dict[str, Any],
) -> list[list[int]]:
    
    inversion_enabled = config_dict.get("inversion_enabled", False)

    print(f"[Inversion] Placeholder dispatch, aktywne: {inversion_enabled}")
    for index, chromosome in enumerate(chromosomes):
        print(f"{index}: {chromosome}")
    print("\n")

    return [chromosome.copy() for chromosome in chromosomes]
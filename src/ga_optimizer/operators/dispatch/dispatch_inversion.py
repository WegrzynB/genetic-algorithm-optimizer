# dispatch_inversion.py
# Dispatcher operatora inwersji.
# Na razie zwraca chromosomy bez zmian.

from __future__ import annotations
from ga_optimizer.operators.inversion import inversion
from typing import Any


def dispatch_inversion(
    chromosomes: list[list[int]],
    config_dict: dict[str, Any],
) -> list[list[int]]:

    inversion_enabled = config_dict["inversion_enabled"]

    if inversion_enabled:
        chromosomes = inversion(chromosomes, config_dict)

    print("\n")
    print(f"[Inversion] Chromosomy, aktywne: {inversion_enabled}")
    for index, chromosome in enumerate(chromosomes):
        print(f"{index}: {chromosome}")
    print("\n")

    return chromosomes



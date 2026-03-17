# dispatch_inversion.py
# Dispatcher operatora inwersji.

from __future__ import annotations

from typing import Any

from ga_optimizer.operators.inversion import inversion
from ga_optimizer.utils.helpers import debug_print


def dispatch_inversion(
    chromosomes: list[list[int]],
    config_dict: dict[str, Any],
) -> list[list[int]]:
    inversion_enabled = config_dict["inversion_enabled"]
    verbose = bool(config_dict.get("verbose", False))

    if inversion_enabled:
        chromosomes = inversion(chromosomes, config_dict)

    debug_print(verbose, "\n")
    debug_print(verbose, f"[Inversion] Chromosomy, aktywne: {inversion_enabled}")
    for index, chromosome in enumerate(chromosomes):
        debug_print(verbose, f"{index}: {chromosome}")
    debug_print(verbose, "\n")

    return chromosomes
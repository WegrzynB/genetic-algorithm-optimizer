# dispatch_elitism.py
# Dispatcher operatora elitaryzmu.
# Na razie zwraca chromosomy bez zmian.

# Dispatcher operatora elitaryzmu – działa także bez fitness_values.

from __future__ import annotations
from typing import Any
from ga_optimizer.operators.elitism import elitism


def dispatch_elitism(
    chromosomes: list[list[int]],
    previous_chromosomes: list[list[int]],
    config_dict: dict[str, Any],
    fitness_values: list[float] | None = None,
    previous_fitness: list[float] | None = None,
) -> list[list[int]]:
    """
    Dispatcher operatora elitaryzmu.
    Zastępuje najgorszy chromosom w nowej populacji najlepszym
    chromosomem z poprzedniej populacji (jeśli elitism_enabled=True).
    Jeśli nie podano fitness_values lub previous_fitness, używa heurystyki:
    sumy wartości chromosomu (mniejsze = lepsze).
    """
    elitism_enabled = config_dict.get("elitism_enabled", False)

    # Jeśli brak fitnessów, wyliczamy proste heurystyczne wartości
    if fitness_values is None:
        fitness_values = [sum(chromo) for chromo in chromosomes]
    if previous_fitness is None:
        previous_fitness = [sum(chromo) for chromo in previous_chromosomes]

    chromosomes = elitism(
        chromosomes=chromosomes,
        fitness_values=fitness_values,
        previous_chromosomes=previous_chromosomes,
        previous_fitness=previous_fitness,
        config_dict=config_dict,
    )
    print("[Elitism] Chromosomes after elitism, aktywne:", elitism_enabled)
    for index, chromosome in enumerate(chromosomes):
        print(f"{index}: {chromosome}")
    print("\n")

    return chromosomes



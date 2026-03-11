# lifecycle.py
# Jedna epoka algorytmu genetycznego:
# ewaluacja bieżącej populacji + wywołanie operatorów + aktualizacja populacji.

from __future__ import annotations

from typing import Any

from ga_optimizer.core.population import Population
from ga_optimizer.operators.dispatch.dispatch_crossover import dispatch_crossover
from ga_optimizer.operators.dispatch.dispatch_elitism import dispatch_elitism
from ga_optimizer.operators.dispatch.dispatch_inversion import dispatch_inversion
from ga_optimizer.operators.dispatch.dispatch_mutation import dispatch_mutation
from ga_optimizer.operators.dispatch.dispatch_selection import dispatch_selection


def run_lifecycle(
    config_dict: dict[str, Any],
    population: Population,
    epoch_index: int,
) -> dict[str, Any]:
    # Najpierw oceniamy bieżącą populację.
    population.evaluate_population()
    summary = population.get_summary()

    # Zachowujemy poprzednią populację pod ewentualny elitaryzm.
    previous_chromosomes = [chromosome.copy() for chromosome in population.chromosomes]

    # Selekcja wybiera materiał do dalszych operacji.
    selected_chromosomes = dispatch_selection(
        chromosomes=population.chromosomes,
        config_dict=config_dict,
    )

    # Krzyżowanie tworzy nowe chromosomy.
    crossed_chromosomes = dispatch_crossover(
        chromosomes=selected_chromosomes,
        config_dict=config_dict,
    )

    # Mutacja modyfikuje chromosomy po krzyżowaniu.
    mutated_chromosomes = dispatch_mutation(
        chromosomes=crossed_chromosomes,
        config_dict=config_dict,
    )

    # Inwersja jest dodatkowym operatorem zmiany chromosomu
    # i naturalnie działa po mutacji.
    inverted_chromosomes = dispatch_inversion(
        chromosomes=mutated_chromosomes,
        config_dict=config_dict,
    )

    # Elitaryzm powinien być na końcu, bo może podmienić końcową populację
    # najlepszymi osobnikami z poprzedniego pokolenia.
    final_chromosomes = dispatch_elitism(
        chromosomes=inverted_chromosomes,
        previous_chromosomes=previous_chromosomes,
        config_dict=config_dict,
    )

    # Podmieniamy chromosomy i aktualizujemy wszystko,
    # co od nich zależy.
    population.set_chromosomes(final_chromosomes)

    return {
        "epoch_index": epoch_index,
        "summary": summary,
    }
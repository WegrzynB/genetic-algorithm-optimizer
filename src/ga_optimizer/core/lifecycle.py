# ga_optimizer/core/lifecycle.py

from typing import Any

from ga_optimizer.core.population import Population
from ga_optimizer.operators.dispatch.dispatch_selection import dispatch_selection

def run_lifecycle(
    config_dict: dict[str, Any],
    population: Population,
    epoch_index: int,
) -> dict[str, Any]:
    
    # 1. EWALUACJA (na wszelki wypadek, choć dzieje się też na koniec set_chromosomes)
    population.evaluate_population()
    summary = population.get_summary()

    # 2. SELEKCJA
    selected_chromosomes = dispatch_selection(
        population=population,
        config_dict=config_dict,
    )

    # 3. KRZYŻOWANIE (wkrótce)
    crossed_chromosomes = selected_chromosomes

    # 4. MUTACJA (wkrótce)
    mutated_chromosomes = crossed_chromosomes

    # 5. AKTUALIZACJA POPULACJI
    # Twoja klasa Population już ma gotową metodę do tego!
    population.set_chromosomes(mutated_chromosomes)

    return {
        "epoch_index": epoch_index,
        "summary": summary,
    }
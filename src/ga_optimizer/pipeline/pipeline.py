# pipeline.py
# Warstwa orkiestracji pojedynczego uruchomienia aplikacji.
# Na razie:
# - pobiera problem na podstawie configu,
# - składa jeden duży słownik wejściowy,
# - wypisuje go w konsoli,
# - wywołuje placeholder engine,
# - zwraca ustandaryzowany wynik do GUI.

from typing import Any

from ga_optimizer.config.schema import GAConfig
from ga_optimizer.core.engine import run_engine
from ga_optimizer.problems.function_catalog import get_problem_definition


def build_pipeline_input_dict(config: GAConfig) -> dict[str, Any]:
    # Składa wszystkie wartości z configu do jednego dużego słownika.
    # Parametry metod są spłaszczane do poziomu głównego.
    data = {
        "problem_name": config.problem_name,
        "n_vars": config.n_vars,
        "range_start": config.range_start,
        "range_end": config.range_end,
        "population": config.population,
        "epochs": config.epochs,
        "epsilon": config.epsilon,
        "seed": config.seed,
        "precision_mode": config.precision_mode,
        "precision_numeric": config.precision_numeric,
        "precision_bits": config.precision_bits,
        "selection_method": config.selection_method,
        "crossover_method": config.crossover_method,
        "mutation_method": config.mutation_method,
        "inversion_enabled": config.inversion_enabled,
        "elitism_enabled": config.elitism_enabled,
    }

    # Dorzuca aktywne parametry metod jako zwykłe pola słownika.
    data.update(config.method_params)

    return data


def run_pipeline(config: GAConfig) -> dict[str, Any]:
    # Główny punkt wejścia pojedynczego uruchomienia z GUI.
    # Docelowo tutaj będzie pełna orkiestracja kolejnych etapów.
    problem = get_problem_definition(config.problem_name)
    input_dict = build_pipeline_input_dict(config)

    print("\n=== PIPELINE INPUT ===")
    for key, value in input_dict.items():
        print(f"{key}: {value}")
    print("======================\n")

    # Placeholder wywołania silnika.
    engine_result = run_engine(config=config, problem=problem)

    return {
        "status": "ok",
        "message": "Pipeline wykonany poprawnie.",
        "problem_name": problem.display_name,
        "input_dict": input_dict,
        "engine_result": engine_result,
    }
# pipeline.py
# Warstwa orkiestracji pojedynczego uruchomienia aplikacji.

from typing import Any

from ga_optimizer.config.schema import GAConfig
from ga_optimizer.core.engine import run_engine


def run_pipeline(config: GAConfig) -> dict[str, Any]:
    # Składa config do prostego słownika wejściowego dla engine.
    input_dict = {
        "problem_name": config.problem_name,
        "n_vars": config.n_vars,
        "objective_mode": config.objective_mode,
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

    input_dict.update(config.method_params)

    print("\n=== PIPELINE INPUT ===")
    for key, value in input_dict.items():
        print(f"{key}: {value}")
    print("======================\n")

    engine_result = run_engine(config_dict=input_dict)

    return {
        "status": "ok",
        "message": "Pipeline wykonany poprawnie.",
        "problem_name": input_dict["problem_name"],
        "input_dict": input_dict,
        "engine_result": engine_result,
    }
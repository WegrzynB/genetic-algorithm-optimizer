# pipeline.py
# Warstwa orkiestracji pojedynczego uruchomienia aplikacji.

from __future__ import annotations

import random
from typing import Any, Callable

from ga_optimizer.config.schema import GAConfig
from ga_optimizer.core.engine import run_engine
from ga_optimizer.utils.helpers import debug_print


def run_pipeline(
    config: GAConfig,
    progress_callback: Callable[[int, int], None] | None = None,
    verbose: bool = True,
) -> dict[str, Any]:
    # Składa config do prostego słownika wejściowego dla engine.
    input_dict = {
        "problem_name": config.problem_name,
        "n_vars": config.n_vars,
        "objective_mode": config.objective_mode,
        "range_start": config.range_start,
        "range_end": config.range_end,
        "population": config.population,
        "epochs": config.epochs,
        "run_count": config.run_count,
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

    if input_dict["seed"] in (None, ""):
        input_dict["seed"] = random.randint(0, 2_147_483_647)

    # True żeby wypisywać debug_print
    input_dict["verbose"] = bool(verbose)

    debug_print(input_dict["verbose"], "\n=== PIPELINE INPUT ===")
    for key, value in input_dict.items():
        debug_print(input_dict["verbose"], f"{key}: {value}")
    debug_print(input_dict["verbose"], "======================\n")


    engine_result = run_engine(
        config_dict=input_dict,
        progress_callback=progress_callback,
    )

    return {
        "status": "ok",
        "message": "Algorytm ukończył działanie.",
        "problem_name": input_dict["problem_name"],
        "input_dict": input_dict,
        "engine_result": engine_result,
    }
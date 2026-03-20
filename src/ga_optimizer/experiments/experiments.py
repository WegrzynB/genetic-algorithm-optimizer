# experiments.py
from __future__ import annotations

from ga_optimizer.experiments.test_all_functions_global import run_all_functions_global_operator_search
from ga_optimizer.experiments.test_random_functions import run_random_functions_test
from ga_optimizer.experiments.test_single_function_operator_search import run_single_function_operator_search


def run_experiment_by_name(
    name: str,
    preset_name: str,
    preset: dict,
) -> dict:
    if name == "random_functions":
        return run_random_functions_test(preset_name, preset)

    if name == "all_functions_global_operator_search":
        return run_all_functions_global_operator_search(preset_name, preset)

    if name == "single_function_operator_search":
        return run_single_function_operator_search(preset_name, preset)

    raise ValueError(f"Nieobsługiwany test_name: {name}")
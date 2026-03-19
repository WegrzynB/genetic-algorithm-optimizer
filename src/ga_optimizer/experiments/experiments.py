from __future__ import annotations

from typing import Any

from ga_optimizer.experiments.test_ablation import run_ablation_test
from ga_optimizer.experiments.test_all_functions_global import run_all_functions_global_operator_search
from ga_optimizer.experiments.test_random_functions import run_random_functions_test
from ga_optimizer.experiments.test_sensitivity import run_sensitivity_test
from ga_optimizer.experiments.test_single_function_operator_search import run_single_function_operator_search


def run_experiment_by_name(
    name: str,
    preset_name: str,
    preset: dict[str, Any],
) -> dict[str, Any]:
    normalized = str(name).strip()

    if normalized == "random_functions":
        return run_random_functions_test(preset_name=preset_name, preset=preset)

    if normalized == "all_functions_global_operator_search":
        return run_all_functions_global_operator_search(preset_name=preset_name, preset=preset)

    if normalized == "single_function_operator_search":
        return run_single_function_operator_search(preset_name=preset_name, preset=preset)

    if normalized == "sensitivity_test":
        return run_sensitivity_test(preset_name=preset_name, preset=preset)

    if normalized == "ablation_test":
        return run_ablation_test(preset_name=preset_name, preset=preset)

    raise ValueError(f"Nieobsługiwana nazwa testu: {name}")
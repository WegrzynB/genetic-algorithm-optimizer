# defaults.py
# Domyślne wartości configu oraz funkcje budujące startowy config aplikacji.

from copy import deepcopy

from ga_optimizer.config.schema import (
    CROSSOVER_METHOD_PARAM_SPECS,
    GAConfig,
    GA_MAIN_FIELD_SPECS,
    MUTATION_METHOD_PARAM_SPECS,
    OPERATOR_FIELD_SPECS,
    PRECISION_FIELD_SPECS,
    SELECTION_METHOD_PARAM_SPECS,
)
from ga_optimizer.problems.function_catalog import (
    get_default_problem_name,
    get_problem_definition,
)


DEFAULT_GA_VALUES = {
    "population": GA_MAIN_FIELD_SPECS["population"]["default"],
    "objective_mode": GA_MAIN_FIELD_SPECS["objective_mode"]["default"],
    "epochs": GA_MAIN_FIELD_SPECS["epochs"]["default"],
    "run_count": GA_MAIN_FIELD_SPECS["run_count"]["default"],
    "seed": GA_MAIN_FIELD_SPECS["seed"]["default"],
}

DEFAULT_PRECISION_VALUES = {
    "precision_mode": PRECISION_FIELD_SPECS["precision_mode"]["default"],
    "precision_numeric": PRECISION_FIELD_SPECS["precision_numeric"]["default"],
    "precision_bits": PRECISION_FIELD_SPECS["precision_bits"]["default"],
}

DEFAULT_OPERATOR_VALUES = {
    "selection_method": OPERATOR_FIELD_SPECS["selection_method"]["default"],
    "crossover_method": OPERATOR_FIELD_SPECS["crossover_method"]["default"],
    "mutation_method": OPERATOR_FIELD_SPECS["mutation_method"]["default"],
    "inversion_enabled": OPERATOR_FIELD_SPECS["inversion_enabled"]["default"],
    "elitism_enabled": OPERATOR_FIELD_SPECS["elitism_enabled"]["default"],
}


def _build_default_method_params(
    selection_method: str,
    crossover_method: str,
    mutation_method: str,
) -> dict:
    # Buduje domyślne parametry tylko dla aktualnie aktywnych metod.
    params: dict = {}

    for spec in SELECTION_METHOD_PARAM_SPECS.get(selection_method, []):
        params[spec["key"]] = deepcopy(spec.get("default"))

    for spec in CROSSOVER_METHOD_PARAM_SPECS.get(crossover_method, []):
        params[spec["key"]] = deepcopy(spec.get("default"))

    for spec in MUTATION_METHOD_PARAM_SPECS.get(mutation_method, []):
        params[spec["key"]] = deepcopy(spec.get("default"))

    return params


def build_default_config(problem_name: str | None = None) -> GAConfig:
    # Tworzy domyślny config na podstawie domyślnej lub wskazanej funkcji.
    selected_problem_name = problem_name or get_default_problem_name()
    problem = get_problem_definition(selected_problem_name)

    return GAConfig(
        problem_name=problem.key,
        objective_mode=DEFAULT_GA_VALUES["objective_mode"],
        n_vars=problem.default_n_vars,
        range_start=problem.suggested_range[0],
        range_end=problem.suggested_range[1],
        population=DEFAULT_GA_VALUES["population"],
        epochs=DEFAULT_GA_VALUES["epochs"],
        run_count=DEFAULT_GA_VALUES["run_count"],
        seed=DEFAULT_GA_VALUES["seed"],
        precision_mode=DEFAULT_PRECISION_VALUES["precision_mode"],
        precision_numeric=DEFAULT_PRECISION_VALUES["precision_numeric"],
        precision_bits=DEFAULT_PRECISION_VALUES["precision_bits"],
        selection_method=DEFAULT_OPERATOR_VALUES["selection_method"],
        crossover_method=DEFAULT_OPERATOR_VALUES["crossover_method"],
        mutation_method=DEFAULT_OPERATOR_VALUES["mutation_method"],
        inversion_enabled=DEFAULT_OPERATOR_VALUES["inversion_enabled"],
        elitism_enabled=DEFAULT_OPERATOR_VALUES["elitism_enabled"],
        method_params=_build_default_method_params(
            selection_method=DEFAULT_OPERATOR_VALUES["selection_method"],
            crossover_method=DEFAULT_OPERATOR_VALUES["crossover_method"],
            mutation_method=DEFAULT_OPERATOR_VALUES["mutation_method"],
        ),
    )
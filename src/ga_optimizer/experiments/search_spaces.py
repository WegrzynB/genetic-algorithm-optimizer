from __future__ import annotations

import random
from typing import Any

from ga_optimizer.config.method_crossover import CROSSOVER_METHOD_PARAM_SPECS
from ga_optimizer.config.method_mutation import MUTATION_METHOD_PARAM_SPECS
from ga_optimizer.config.method_selection import SELECTION_METHOD_PARAM_SPECS
from ga_optimizer.config.schema import GAConfig
from ga_optimizer.experiments.experiment_config import METHOD_PARAM_RANGE_OVERRIDES
from ga_optimizer.problems.function_catalog import get_problem_definition


def _pick_bool(rng: random.Random, values: list[bool]) -> bool:
    return bool(rng.choice(values))


def _pick_int(rng: random.Random, value_range: tuple[int, int]) -> int:
    lo, hi = value_range
    if hi < lo:
        hi = lo
    return rng.randint(int(lo), int(hi))


def _pick_float(rng: random.Random, value_range: tuple[float, float]) -> float:
    lo, hi = value_range
    if hi < lo:
        hi = lo
    return rng.uniform(float(lo), float(hi))


def _sample_from_spec(spec: dict[str, Any], rng: random.Random, population: int, n_vars: int) -> Any:
    key = spec["key"]
    spec_type = spec.get("type")

    if key in METHOD_PARAM_RANGE_OVERRIDES:
        override = METHOD_PARAM_RANGE_OVERRIDES[key]
        if spec_type == "int":
            value = _pick_int(rng, override)
        elif spec_type == "float":
            value = _pick_float(rng, override)
        else:
            value = spec.get("default")
    else:
        if spec_type == "int":
            min_value = int(spec.get("min", 1))
            max_value = int(spec.get("max", max(min_value, spec.get("default", min_value) + 10)))
            value = rng.randint(min_value, max_value)
        elif spec_type == "float":
            min_value = float(spec.get("min", spec.get("min_exclusive", 0.0)))
            max_value = float(spec.get("max", 1.0))
            value = rng.uniform(min_value, max_value)
        elif spec_type == "enum":
            values = spec.get("values", [])
            value = rng.choice(values) if values else spec.get("default")
        elif spec_type == "bool":
            value = rng.choice([True, False])
        else:
            value = spec.get("default")

    if key in {"selection_tournament_k", "selection_best_k", "selection_worst_k"}:
        value = min(int(value), max(2, population))
    if key in {"selection_double_tournament_k1", "selection_double_tournament_k2"}:
        value = min(int(value), max(1, population))
    if key in {"crossover_multi_point_k", "crossover_granular_granularity", "crossover_segment_length"}:
        value = min(int(value), max(1, n_vars))

    return value


def _build_method_params(
    selection_method: str,
    crossover_method: str,
    mutation_method: str,
    rng: random.Random,
    population: int,
    n_vars: int,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    for spec in SELECTION_METHOD_PARAM_SPECS.get(selection_method, []):
        params[spec["key"]] = _sample_from_spec(spec, rng, population, n_vars)

    for spec in CROSSOVER_METHOD_PARAM_SPECS.get(crossover_method, []):
        params[spec["key"]] = _sample_from_spec(spec, rng, population, n_vars)

    for spec in MUTATION_METHOD_PARAM_SPECS.get(mutation_method, []):
        params[spec["key"]] = _sample_from_spec(spec, rng, population, n_vars)

    return params


def build_base_config_for_problem(
    problem_name: str,
    population: int,
    epochs: int,
    run_count: int,
    precision_bits: int,
    seed: str | int | None,
) -> GAConfig:
    """
    Buduje poprawny bazowy config dla wskazanej funkcji.
    Eksperymenty wymuszają:
    - objective_mode='min'
    - precision_mode='bits'
    """
    problem = get_problem_definition(problem_name)
    range_start, range_end = problem.suggested_range

    return GAConfig(
        problem_name=problem_name,
        objective_mode="min",
        n_vars=problem.default_n_vars,
        range_start=float(range_start),
        range_end=float(range_end),
        population=int(population),
        epochs=int(epochs),
        run_count=int(run_count),
        seed=seed,
        precision_mode="bits",
        precision_numeric=0.1,
        precision_bits=int(precision_bits),
        selection_method="tournament",
        crossover_method="two_point",
        mutation_method="scramble",
        inversion_enabled=False,
        elitism_enabled=False,
        method_params={
            "selection_tournament_k": min(6, max(2, int(population))),
            "crossover_two_point_p": 0.7,
            "mutation_scramble_p": 0.03,
        },
    )


def sample_random_config(
    problem_name: str,
    ranges: dict[str, Any],
    rng: random.Random,
    seed: str | int | None,
) -> GAConfig:
    """
    Losuje pełną konfigurację dla wskazanej funkcji na podstawie przedziałów.
    """
    problem = get_problem_definition(problem_name)
    n_vars = problem.default_n_vars
    range_start, range_end = problem.suggested_range

    population = _pick_int(rng, ranges["population"])
    epochs = _pick_int(rng, ranges["epochs"])
    run_count = _pick_int(rng, ranges["run_count"])
    precision_bits = _pick_int(rng, ranges["precision_bits"])

    selection_method = rng.choice(ranges["selection_method"])
    crossover_method = rng.choice(ranges["crossover_method"])
    mutation_method = rng.choice(ranges["mutation_method"])

    inversion_enabled = _pick_bool(rng, ranges["inversion_enabled"])
    elitism_enabled = _pick_bool(rng, ranges["elitism_enabled"])

    method_params = _build_method_params(
        selection_method=selection_method,
        crossover_method=crossover_method,
        mutation_method=mutation_method,
        rng=rng,
        population=population,
        n_vars=n_vars,
    )

    return GAConfig(
        problem_name=problem_name,
        objective_mode="min",
        n_vars=n_vars,
        range_start=float(range_start),
        range_end=float(range_end),
        population=population,
        epochs=epochs,
        run_count=run_count,
        seed=seed,
        precision_mode="bits",
        precision_numeric=0.1,
        precision_bits=precision_bits,
        selection_method=selection_method,
        crossover_method=crossover_method,
        mutation_method=mutation_method,
        inversion_enabled=inversion_enabled,
        elitism_enabled=elitism_enabled,
        method_params=method_params,
    )


def apply_config_overrides(config: GAConfig, overrides: dict[str, Any]) -> GAConfig:
    """
    Nadpisuje wybrane pola configu oraz aktywne parametry metod.
    """
    for key, value in overrides.items():
        if key == "method_params":
            config.method_params.update(dict(value))
        else:
            setattr(config, key, value)
    return config
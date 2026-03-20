from __future__ import annotations

import random
from typing import Any

from ga_optimizer.config.method_crossover import CROSSOVER_METHOD_PARAM_SPECS
from ga_optimizer.config.method_mutation import MUTATION_METHOD_PARAM_SPECS
from ga_optimizer.config.method_selection import SELECTION_METHOD_PARAM_SPECS
from ga_optimizer.config.schema import GAConfig
from ga_optimizer.experiments.experiment_config import METHOD_PARAM_RANGE_OVERRIDES
from ga_optimizer.problems.function_catalog import get_problem_definition, get_problem_names


def _values_from_range_spec(spec: dict[str, Any]) -> list[Any]:
    if "values" in spec:
        return list(spec["values"])

    start = spec["start"]
    end = spec["end"]
    step = spec["step"]

    values = []
    current = start

    if isinstance(start, int) and isinstance(end, int) and isinstance(step, int):
        while current <= end:
            values.append(int(current))
            current += step
    else:
        current = float(start)
        end = float(end)
        step = float(step)
        guard = 0
        while current <= end + 1e-12 and guard < 10000:
            values.append(round(current, 10))
            current += step
            guard += 1

    return values


def _pick_from_spec(rng: random.Random, spec: dict[str, Any]) -> Any:
    values = _values_from_range_spec(spec)
    return rng.choice(values)


def pick_problem_name(problem_pool: str | list[str], rng: random.Random) -> str:
    if problem_pool == "all":
        names = list(get_problem_names())
    elif isinstance(problem_pool, (list, tuple)):
        names = [str(name) for name in problem_pool]
    else:
        names = [str(problem_pool)]

    if not names:
        raise ValueError("Brak dostępnych nazw funkcji w problem_pool.")

    return rng.choice(names)


def _sample_from_method_spec(spec: dict[str, Any], rng: random.Random, population: int, n_vars: int) -> Any:
    key = spec["key"]
    spec_type = spec.get("type")

    if key in METHOD_PARAM_RANGE_OVERRIDES:
        value = _pick_from_spec(rng, METHOD_PARAM_RANGE_OVERRIDES[key])
    else:
        if spec_type == "enum":
            value = rng.choice(spec.get("values", []))
        elif spec_type == "bool":
            value = rng.choice([True, False])
        elif spec_type == "int":
            min_value = int(spec.get("min", 1))
            max_value = int(spec.get("default", min_value))
            value = rng.randint(min_value, max_value)
        elif spec_type == "float":
            min_value = float(spec.get("min", spec.get("min_exclusive", 0.0)))
            max_value = float(spec.get("default", 1.0))
            value = rng.uniform(min_value, max_value)
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
        params[spec["key"]] = _sample_from_method_spec(spec, rng, population, n_vars)

    for spec in CROSSOVER_METHOD_PARAM_SPECS.get(crossover_method, []):
        params[spec["key"]] = _sample_from_method_spec(spec, rng, population, n_vars)

    for spec in MUTATION_METHOD_PARAM_SPECS.get(mutation_method, []):
        params[spec["key"]] = _sample_from_method_spec(spec, rng, population, n_vars)

    return params


def build_base_config_for_problem(
    problem_name: str,
    population: int,
    epochs: int,
    run_count: int,
    precision_bits: int,
    seed: str | int | None,
) -> GAConfig:
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
            "selection_tournament_k": 4,
            "crossover_two_point_p": 0.55,
            "mutation_scramble_p": 0.03,
        },
    )


def sample_random_config(
    problem_name: str,
    ranges: dict[str, Any],
    rng: random.Random,
    seed: str | int | None,
) -> GAConfig:
    problem = get_problem_definition(problem_name)
    n_vars = problem.default_n_vars
    range_start, range_end = problem.suggested_range

    population = _pick_from_spec(rng, ranges["population"])
    epochs = _pick_from_spec(rng, ranges["epochs"])
    run_count = _pick_from_spec(rng, ranges["run_count"])
    precision_bits = _pick_from_spec(rng, ranges["precision_bits"])

    selection_method = _pick_from_spec(rng, ranges["selection_method"])
    crossover_method = _pick_from_spec(rng, ranges["crossover_method"])
    mutation_method = _pick_from_spec(rng, ranges["mutation_method"])

    inversion_enabled = _pick_from_spec(rng, ranges["inversion_enabled"])
    elitism_enabled = _pick_from_spec(rng, ranges["elitism_enabled"])

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
        population=int(population),
        epochs=int(epochs),
        run_count=int(run_count),
        seed=seed,
        precision_mode="bits",
        precision_numeric=0.1,
        precision_bits=int(precision_bits),
        selection_method=selection_method,
        crossover_method=crossover_method,
        mutation_method=mutation_method,
        inversion_enabled=bool(inversion_enabled),
        elitism_enabled=bool(elitism_enabled),
        method_params=method_params,
    )


def apply_config_overrides(config: GAConfig, overrides: dict[str, Any]) -> GAConfig:
    for key, value in overrides.items():
        if key == "method_params":
            config.method_params.update(dict(value))
        else:
            setattr(config, key, value)
    return config
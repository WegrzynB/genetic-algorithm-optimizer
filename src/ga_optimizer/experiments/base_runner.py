# base_runner.py
from __future__ import annotations

import math
import time
from typing import Any, Callable

from ga_optimizer.core.pipeline import run_pipeline
from ga_optimizer.problems.function_catalog import get_problem_definition


PROGRESS_PRINT_EVERY = 1000


def _format_percent(current: int, total: int) -> str:
    if total <= 0:
        return "0.0%"
    return f"{(float(current) / float(total)) * 100.0:.1f}%"


def print_experiment_progress(
    test_name: str,
    current: int,
    total: int,
    step_label: str = "",
) -> None:
    suffix = f" | {step_label}" if step_label else ""
    print(f"[{test_name}] postęp eksperymentu: {current}/{total} ({_format_percent(current, total)}){suffix}")


def make_progress_callback(
    prefix: str,
    experiment_progress: tuple[int, int] | None = None,
    step_label: str = "",
    print_every: int = PROGRESS_PRINT_EVERY,
) -> Callable[[int, int], None]:
    last = {"current": None, "total": None}

    def _callback(current: int, total: int) -> None:
        if total in (None, 0):
            return
        if last["current"] == current and last["total"] == total:
            return

        last["current"] = current
        last["total"] = total

        should_print = (
            current == 1
            or current == total
            or (print_every > 0 and current % print_every == 0)
        )
        if not should_print:
            return

        if experiment_progress is not None:
            exp_current, exp_total = experiment_progress
            experiment_part = f"eksperyment {exp_current}/{exp_total} ({_format_percent(exp_current, exp_total)})"
        else:
            experiment_part = "eksperyment -/-"

        local_part = f"run_engine {current}/{total} ({_format_percent(current, total)})"
        suffix = f" | {step_label}" if step_label else ""
        print(f"{prefix} {experiment_part} | {local_part}{suffix}")

    return _callback


def _euclidean_distance(a: list[float], b: list[float]) -> float:
    length = min(len(a), len(b))
    return math.sqrt(sum((float(a[i]) - float(b[i])) ** 2 for i in range(length)))


def _nearest_global_point_distance(
    point: list[float] | None,
    global_points: list[list[float]] | None,
) -> float | None:
    if point is None or not global_points:
        return None
    distances = [_euclidean_distance(point, gp) for gp in global_points]
    return min(distances) if distances else None


def _percentile_from_sorted(values: list[float], percentile: float) -> float | None:
    if not values:
        return None

    if len(values) == 1:
        return float(values[0])

    position = (len(values) - 1) * percentile
    lower_index = int(position)
    upper_index = min(lower_index + 1, len(values) - 1)
    fraction = position - lower_index

    lower_value = values[lower_index]
    upper_value = values[upper_index]

    return float(lower_value + (upper_value - lower_value) * fraction)


def _median_index_for_sorted_length(length: int) -> int | None:
    if length <= 0:
        return None
    return (length - 1) // 2


def _safe_float_or_none(value: Any) -> float | None:
    if value is None:
        return None
    try:
        return float(value)
    except Exception:
        return None


def _extract_run_population_points(
    run: dict[str, Any],
    problem_definition,
) -> list[dict[str, Any]]:
    decoded_population = run.get("decoded_population") or []
    raw_objectives = run.get("raw_objectives") or []

    if not decoded_population:
        history = run.get("history") or []
        if history:
            last_state = history[-1]
            decoded_population = last_state.get("decoded_population") or []
            raw_objectives = last_state.get("raw_objectives") or []

    if not decoded_population:
        return []

    prepared_points: list[dict[str, Any]] = []

    for idx, point in enumerate(decoded_population):
        if point is None:
            continue

        point_list = [float(x) for x in point]

        raw_value = None
        if idx < len(raw_objectives):
            raw_value = _safe_float_or_none(raw_objectives[idx])

        if raw_value is None:
            try:
                raw_value = float(problem_definition.formula(point_list))
            except Exception:
                continue

        prepared_points.append(
            {
                "point": point_list,
                "raw_objective": raw_value,
                "population_index": idx,
            }
        )

    return prepared_points


def _choose_median_point_from_population(
    points: list[dict[str, Any]],
) -> dict[str, Any] | None:
    if not points:
        return None

    ordered = sorted(points, key=lambda item: item["raw_objective"])
    median_idx = _median_index_for_sorted_length(len(ordered))
    if median_idx is None:
        return None
    return ordered[median_idx]


def _collect_final_population_points(engine_result: dict[str, Any], problem_name: str) -> list[dict[str, Any]]:
    problem = get_problem_definition(problem_name)
    runs = engine_result.get("runs", []) or []

    collected: list[dict[str, Any]] = []

    for run_index, run in enumerate(runs, start=1):
        run_points = _extract_run_population_points(run, problem)
        for item in run_points:
            collected.append(
                {
                    "run_index": run_index,
                    "point": item["point"],
                    "raw_objective": item["raw_objective"],
                    "population_index": item["population_index"],
                }
            )

    return collected


def _choose_global_median_from_all_final_populations(
    engine_result: dict[str, Any],
    problem_name: str,
) -> dict[str, Any] | None:
    all_points = _collect_final_population_points(engine_result, problem_name)
    if not all_points:
        return None

    ordered = sorted(all_points, key=lambda item: item["raw_objective"])
    median_idx = _median_index_for_sorted_length(len(ordered))
    if median_idx is None:
        return None
    return ordered[median_idx]


def _build_engine_summary_from_all_final_populations(
    engine_result: dict[str, Any],
    problem_name: str,
) -> dict[str, Any]:
    all_points = _collect_final_population_points(engine_result, problem_name)
    values = sorted([float(item["raw_objective"]) for item in all_points])

    if not values:
        return {
            "min": None,
            "q1": None,
            "median": None,
            "q3": None,
            "max": None,
            "avg": None,
            "best": None,
            "worst": None,
            "elapsed": engine_result.get("elapsed"),
            "final_population_point_count": 0,
        }

    return {
        "min": values[0],
        "q1": _percentile_from_sorted(values, 0.25),
        "median": _percentile_from_sorted(values, 0.50),
        "q3": _percentile_from_sorted(values, 0.75),
        "max": values[-1],
        "avg": sum(values) / len(values),
        "best": values[0],
        "worst": values[-1],
        "elapsed": engine_result.get("elapsed"),
        "final_population_point_count": len(values),
    }


def run_single_config(
    config,
    progress_prefix: str = "",
    experiment_progress: tuple[int, int] | None = None,
    step_label: str = "",
) -> dict[str, Any]:
    start = time.perf_counter()

    pipeline_result = run_pipeline(
        config,
        progress_callback=make_progress_callback(
            prefix=progress_prefix,
            experiment_progress=experiment_progress,
            step_label=step_label,
            print_every=PROGRESS_PRINT_EVERY,
        ),
        verbose=False,
    )
    engine_result = pipeline_result["engine_result"]

    problem = get_problem_definition(config.problem_name)

    # FINALNY WYNIK RUNU:
    # bierzemy wszystkie punkty ze wszystkich końcowych populacji
    # i wybieramy medianę po raw objective
    chosen_point_record = _choose_global_median_from_all_final_populations(
        engine_result=engine_result,
        problem_name=config.problem_name,
    )

    aggregated_engine_summary = _build_engine_summary_from_all_final_populations(
        engine_result=engine_result,
        problem_name=config.problem_name,
    )

    final_value = None
    signed_value_error = None
    abs_value_error = None
    final_point = None
    nearest_point_distance = None

    if chosen_point_record is not None:
        final_value = float(chosen_point_record["raw_objective"])
        final_point = list(chosen_point_record["point"])
        signed_value_error = final_value - float(problem.global_minimum_value)
        abs_value_error = abs(signed_value_error)
        nearest_point_distance = _nearest_global_point_distance(
            final_point,
            problem.global_minimum_points,
        )

    duration_sec = time.perf_counter() - start

    return {
        "problem_name": config.problem_name,
        "problem_display_name": problem.display_name,
        "global_minimum_value": float(problem.global_minimum_value),
        "global_minimum_points": problem.global_minimum_points,
        "config": {
            "problem_name": config.problem_name,
            "objective_mode": config.objective_mode,
            "n_vars": config.n_vars,
            "range_start": config.range_start,
            "range_end": config.range_end,
            "population": config.population,
            "epochs": config.epochs,
            "run_count": config.run_count,
            "seed": config.seed,
            "precision_mode": config.precision_mode,
            "precision_bits": config.precision_bits,
            "selection_method": config.selection_method,
            "crossover_method": config.crossover_method,
            "mutation_method": config.mutation_method,
            "inversion_enabled": config.inversion_enabled,
            "elitism_enabled": config.elitism_enabled,
            "method_params": dict(config.method_params),
        },
        "engine_summary": aggregated_engine_summary,
        "best_run": chosen_point_record,
        "best_value": final_value,
        "best_point": final_point,
        "signed_value_error": signed_value_error,
        "abs_value_error": abs_value_error,
        "nearest_global_min_point_distance": nearest_point_distance,
        "duration_sec": duration_sec,
    }


def format_global_params_for_print(config) -> str:
    parts = [
        f"problem={config.problem_name}",
        f"population={config.population}",
        f"epochs={config.epochs}",
        f"run_count={config.run_count}",
        f"precision_bits={config.precision_bits}",
        f"selection={config.selection_method}",
        f"crossover={config.crossover_method}",
        f"mutation={config.mutation_method}",
        f"inversion={config.inversion_enabled}",
        f"elitism={config.elitism_enabled}",
        f"seed={config.seed}",
        f"method_params={dict(config.method_params)}",
    ]
    return " | ".join(parts)
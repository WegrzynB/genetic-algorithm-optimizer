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


def _extract_best_run_record(
    engine_result: dict[str, Any],
    problem_name: str,
) -> dict[str, Any] | None:
    runs = engine_result.get("runs", [])
    if not runs:
        return None

    problem = get_problem_definition(problem_name)
    pool: list[dict[str, Any]] = []

    for run in runs:
        summary = run.get("summary", {})
        best_point = summary.get("best_decoded")
        best_chromosome = summary.get("best_chromosome")
        best_raw = summary.get("best_raw_objective")

        if best_raw is None and best_point is not None:
            try:
                best_raw = float(problem.formula(best_point))
            except Exception:
                best_raw = None

        if best_point is None or best_chromosome is None or best_raw is None:
            continue

        pool.append(
            {
                "run_index": int(run.get("run_index", 0)) + 1,
                "seed": run.get("seed"),
                "best_point": list(best_point),
                "best_chromosome": list(best_chromosome),
                "best_raw_objective": float(best_raw),
                "elapsed": float(run.get("elapsed", 0.0)),
            }
        )

    if not pool:
        return None

    return min(pool, key=lambda item: item["best_raw_objective"])


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
    best_run = _extract_best_run_record(
        engine_result=engine_result,
        problem_name=config.problem_name,
    )

    best_value = None
    signed_value_error = None
    abs_value_error = None
    best_point = None
    nearest_point_distance = None

    if best_run is not None:
        best_value = float(best_run["best_raw_objective"])
        signed_value_error = best_value - float(problem.global_minimum_value)
        abs_value_error = abs(signed_value_error)
        best_point = list(best_run["best_point"])
        nearest_point_distance = _nearest_global_point_distance(
            best_point,
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
        "engine_summary": {
            "min": engine_result.get("min"),
            "q1": engine_result.get("q1"),
            "median": engine_result.get("median"),
            "q3": engine_result.get("q3"),
            "max": engine_result.get("max"),
            "avg": engine_result.get("avg"),
            "best": engine_result.get("best"),
            "worst": engine_result.get("worst"),
            "elapsed": engine_result.get("elapsed"),
        },
        "best_run": best_run,
        "best_value": best_value,
        "best_point": best_point,
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
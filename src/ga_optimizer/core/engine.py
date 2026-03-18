# engine.py
# Silnik algorytmu genetycznego oparty o klasę Population.

from __future__ import annotations

import time
from typing import Any, Callable

from ga_optimizer.core.population import Population
from ga_optimizer.utils.helpers import debug_print


def _fmt_float(value: Any) -> str:
    # Pomocnicze formatowanie liczb do 3 miejsc po przecinku.
    if value is None:
        return "-"
    return f"{float(value):.3f}"


def _percentile_from_sorted(values: list[float], percentile: float) -> float | None:
    # Wyznacza percentyl z posortowanej listy metodą liniowej interpolacji.
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


def _build_runs_aggregate(
    runs: list[dict[str, Any]],
    objective_mode: str,
) -> dict[str, Any]:
    # Buduje zbiorcze statystyki po wszystkich uruchomieniach
    # na podstawie RAW objective najlepszego osobnika z każdego runa.
    run_best_raw_values = [
        float(run["summary"]["best_raw_objective"])
        for run in runs
        if run.get("summary", {}).get("best_raw_objective") is not None
    ]
    run_best_raw_values.sort()

    if not run_best_raw_values:
        return {
            "min": None,
            "q1": None,
            "median": None,
            "q3": None,
            "max": None,
            "avg": None,
            "best": None,
            "worst": None,
        }

    min_value = run_best_raw_values[0]
    q1_value = _percentile_from_sorted(run_best_raw_values, 0.25)
    median_value = _percentile_from_sorted(run_best_raw_values, 0.50)
    q3_value = _percentile_from_sorted(run_best_raw_values, 0.75)
    max_value = run_best_raw_values[-1]
    avg_value = sum(run_best_raw_values) / len(run_best_raw_values)

    if objective_mode == "min":
        best_value = min_value
        worst_value = max_value
    elif objective_mode == "max":
        best_value = max_value
        worst_value = min_value
    else:
        raise ValueError(f"Nieobsługiwany typ optymalizacji: {objective_mode}")

    return {
        "min": min_value,
        "q1": q1_value,
        "median": median_value,
        "q3": q3_value,
        "max": max_value,
        "avg": avg_value,
        "best": best_value,
        "worst": worst_value,
    }


def run_engine(
    config_dict: dict[str, Any],
    progress_callback: Callable[[int, int], None] | None = None,
) -> dict[str, Any]:
    # Wykonuje algorytm wielokrotnie zgodnie z run_count,
    # zwiększając seed o 1 przy każdym kolejnym uruchomieniu.
    run_count = int(config_dict.get("run_count", 1))
    base_seed = int(config_dict["seed"])
    verbose = bool(config_dict.get("verbose", False))

    epochs_per_run = int(config_dict["epochs"])
    total_steps = run_count * epochs_per_run
    completed_steps = 0

    total_started_at = time.perf_counter()
    runs: list[dict[str, Any]] = []

    for run_index in range(run_count):
        single_run_config = dict(config_dict)
        single_run_config["seed"] = base_seed + run_index

        debug_print(verbose, "\n\n################################################################")
        debug_print(verbose, f"###################### URUCHOMIENIE {run_index + 1}/{run_count} ######################")
        debug_print(verbose, f"######################## seed = {single_run_config['seed']} ########################")
        debug_print(verbose, "################################################################")

        population = Population(config_dict=single_run_config)

        for epoch_index in range(1, int(single_run_config["epochs"]) + 1):
            population.run_epoch(epoch_index)

            completed_steps += 1
            if progress_callback is not None:
                progress_callback(completed_steps, total_steps)

        population.finish_run()

        run_export = population.to_export_dict()
        run_export["run_index"] = run_index
        runs.append(run_export)

        summary = run_export["summary"]

        debug_print(verbose, "\n=== ENGINE SUMMARY ===")
        debug_print(verbose, f"Problem: {single_run_config['problem_name']}")
        debug_print(verbose, f"Typ optymalizacji: {single_run_config['objective_mode']}")
        debug_print(verbose, f"Seed: {single_run_config['seed']}")
        debug_print(verbose, f"Rozmiar populacji: {population.population_size}")
        debug_print(verbose, f"Liczba zmiennych: {population.n_vars}")
        debug_print(verbose, f"Długość chromosomu: {population.chromosome_length}")
        debug_print(verbose, f"Bity na zmienną: {population.bits_per_variable}")
        debug_print(verbose, f"Precyzja: {_fmt_float(population.precision)}")
        debug_print(verbose, f"Najlepsza wartość funkcji celu: {_fmt_float(summary['best_raw_objective'])}")
        debug_print(verbose, f"Najgorsza wartość funkcji celu: {_fmt_float(summary['worst_raw_objective'])}")
        debug_print(verbose, f"Min fitness: {_fmt_float(summary['min_fitness'])}")
        debug_print(verbose, f"25% fitness: {_fmt_float(summary['q1_fitness'])}")
        debug_print(verbose, f"Mediana fitness: {_fmt_float(summary['median_fitness'])}")
        debug_print(verbose, f"75% fitness: {_fmt_float(summary['q3_fitness'])}")
        debug_print(verbose, f"Max fitness: {_fmt_float(summary['max_fitness'])}")
        debug_print(verbose, f"Średni fitness: {_fmt_float(summary['avg_fitness'])}")
        debug_print(verbose, f"Czas: {_fmt_float(run_export['elapsed'])} s")
        debug_print(verbose, "======================\n")

    total_elapsed = time.perf_counter() - total_started_at
    aggregate = _build_runs_aggregate(
        runs,
        objective_mode=str(config_dict["objective_mode"]),
    )

    debug_print(verbose, "\n====================== ENGINE MULTIRUN SUMMARY ======================")
    debug_print(verbose, f"Liczba uruchomień: {run_count}")
    debug_print(verbose, f"Seed startowy: {base_seed}")
    debug_print(verbose, f"Min best-raw: {_fmt_float(aggregate['min'])}")
    debug_print(verbose, f"25% best-raw: {_fmt_float(aggregate['q1'])}")
    debug_print(verbose, f"Mediana best-raw: {_fmt_float(aggregate['median'])}")
    debug_print(verbose, f"75% best-raw: {_fmt_float(aggregate['q3'])}")
    debug_print(verbose, f"Max best-raw: {_fmt_float(aggregate['max'])}")
    debug_print(verbose, f"Średnia z best-raw: {_fmt_float(aggregate['avg'])}")
    debug_print(verbose, f"Łączny czas: {_fmt_float(total_elapsed)} s")
    debug_print(verbose, "====================================================================")

    return {
        "status": "ok",
        "message": f"Engine wykonany poprawnie ({run_count} uruchomień).",
        "run_count": run_count,
        "base_seed": base_seed,
        "elapsed": total_elapsed,
        "runs": runs,
        "history": [run["history"] for run in runs],
        **aggregate,
    }
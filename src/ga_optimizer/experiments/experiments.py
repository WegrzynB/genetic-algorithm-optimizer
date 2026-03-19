# experiments.py

from __future__ import annotations

from copy import deepcopy
from tkinter import messagebox


def _extract_best_individual(engine_result: dict, objective_mode: str) -> dict | None:
    runs = engine_result.get("runs", [])
    pool: list[dict] = []

    for run in runs:
        summary = run.get("summary", {})
        best_point = summary.get("best_decoded")
        best_chromosome = summary.get("best_chromosome")
        best_fitness = summary.get("max_fitness")
        best_raw_objective = summary.get("best_raw_objective")

        if (
            best_point is None
            or best_chromosome is None
            or best_fitness is None
            or best_raw_objective is None
        ):
            continue

        pool.append(
            {
                "run_index": run.get("run_index", 0) + 1,
                "seed": run.get("seed"),
                "point": list(best_point),
                "chromosome": list(best_chromosome),
                "fitness": float(best_fitness),
                "raw_objective": float(best_raw_objective),
            }
        )

    if not pool:
        return None

    if objective_mode == "min":
        return min(pool, key=lambda item: item["raw_objective"])
    if objective_mode == "max":
        return max(pool, key=lambda item: item["raw_objective"])

    raise ValueError(f"Nieobsługiwany typ optymalizacji: {objective_mode}")


def _format_best_individual(label: str, best: dict | None) -> str:
    if best is None:
        return f"{label}: brak danych"

    point_str = "[" + ", ".join(f"{float(value):.7f}" for value in best["point"]) + "]"

    return (
        f"{label}\n"
        f"  uruchomienie wewnętrzne run_engine: {best['run_index']}\n"
        f"  seed: {best['seed']}\n"
        f"  wartość funkcji celu: {best['raw_objective']:.7f}\n"
        f"  fitness: {best['fitness']:.7f}\n"
        f"  chromosom: {best['chromosome']}\n"
        f"  punkt: {point_str}"
    )


def run_experiments(main_window, name: str) -> None:
    # Na razie:
    # 1. uruchamia aplikację tak jak po kliknięciu Start
    # 2. czeka aż się skończy
    # 3. uruchamia drugi raz
    # 4. zapamiętuje historię obu uruchomień
    # 5. pokazuje najlepszego osobnika z każdego uruchomienia

    experiment_history: list[dict] = []

    for experiment_run_index in range(2):
        main_window._on_start()

        pipeline_result = main_window.last_pipeline_result
        if not pipeline_result:
            messagebox.showerror(
                "Błąd eksperymentu",
                f"Eksperyment '{name}' przerwany: brak last_pipeline_result po uruchomieniu {experiment_run_index + 1}."
            )
            return

        engine_result = pipeline_result.get("engine_result", {})
        if not engine_result:
            messagebox.showerror(
                "Błąd eksperymentu",
                f"Eksperyment '{name}' przerwany: brak engine_result po uruchomieniu {experiment_run_index + 1}."
            )
            return

        experiment_history.append(
            {
                "experiment_run_index": experiment_run_index + 1,
                "pipeline_result": deepcopy(pipeline_result),
                "engine_result": deepcopy(engine_result),
            }
        )

    objective_mode = main_window.vm.objective_mode.get()

    best_from_first = _extract_best_individual(
        experiment_history[0]["engine_result"],
        objective_mode=objective_mode,
    )
    best_from_second = _extract_best_individual(
        experiment_history[1]["engine_result"],
        objective_mode=objective_mode,
    )

    summary_text = (
        f"Eksperyment: {name}\n\n"
        f"{_format_best_individual('Najlepszy osobnik z 1. uruchomienia aplikacji', best_from_first)}\n\n"
        f"{_format_best_individual('Najlepszy osobnik z 2. uruchomienia aplikacji', best_from_second)}"
    )

    print(summary_text)
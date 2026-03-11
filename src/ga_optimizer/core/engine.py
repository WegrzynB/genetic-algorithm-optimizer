# engine.py
# Silnik algorytmu genetycznego oparty o klasę Population i jedną funkcję lifecycle.

from __future__ import annotations

import time
from typing import Any

from ga_optimizer.core.lifecycle import run_lifecycle
from ga_optimizer.core.population import Population


def _fmt_float(value: Any) -> str:
    # Pomocnicze formatowanie liczb do 3 miejsc po przecinku.
    if value is None:
        return "-"
    return f"{float(value):.3f}"


def run_engine(config_dict: dict[str, Any]) -> dict[str, Any]:
    # Start pomiaru czasu całego uruchomienia.
    started_at = time.perf_counter()

    # Tworzymy obiekt populacji na podstawie configu.
    population = Population(config_dict=config_dict)

    # Generujemy startową losową populację chromosomów.
    population.generate_initial_population()

    # Wypisujemy chromosomy startowe.
    print("\n=== STARTOWE CHROMOSOMY ===")
    for index, chromosome in enumerate(population.chromosomes):
        print(f"{index}: {chromosome}")
    print("===========================\n\n\n\n\n")

    # Historia kolejnych epok - później będzie użyta do wykresów i zapisu wyników.
    history: list[dict[str, Any]] = []

    # Główna pętla epok.
    for epoch_index in range(int(config_dict["epochs"])):
        epoch_result = run_lifecycle(
            config_dict=config_dict,
            population=population,
            epoch_index=epoch_index,
        )

        history.append(
            {
                "epoch_index": epoch_result["epoch_index"],
                "best_fitness": epoch_result["summary"]["best_fitness"],
                "avg_fitness": epoch_result["summary"]["avg_fitness"],
                "worst_fitness": epoch_result["summary"]["worst_fitness"],
                "best_raw_objective": epoch_result["summary"]["best_raw_objective"],
                "best_decoded": epoch_result["summary"]["best_decoded"],
            }
        )

        # Wypisujemy chromosomy po zakończeniu epoki.
        print(f"\n=== EPOKA {epoch_index + 1} - CHROMOSOMY ===")
        for index, chromosome in enumerate(population.chromosomes):
            print(f"{index}: {chromosome}")
        print("================================================================================\n\n\n")

    # Po ostatniej epoce jeszcze raz upewniamy się,
    # że cała populacja ma aktualne wyniki ewaluacji.
    population.evaluate_population()

    # Pobieramy końcowe podsumowanie populacji.
    final_summary = population.get_summary()

    # Kończymy pomiar czasu.
    elapsed = time.perf_counter() - started_at

    print("\n=== ENGINE SUMMARY ===")
    print(f"Problem: {config_dict['problem_name']}")
    print(f"Typ optymalizacji: {config_dict['objective_mode']}")
    print(f"Rozmiar populacji: {population.population_size}")
    print(f"Liczba zmiennych: {population.n_vars}")
    print(f"Długość chromosomu: {population.chromosome_length}")
    print(f"Bity na zmienną: {population.bits_per_variable}")
    print(f"Precyzja: {_fmt_float(population.precision)}")
    print(f"Best raw objective: {_fmt_float(final_summary['best_raw_objective'])}")
    print(f"Best fitness: {_fmt_float(final_summary['best_fitness'])}")
    print(f"Avg fitness: {_fmt_float(final_summary['avg_fitness'])}")
    print(f"Worst fitness: {_fmt_float(final_summary['worst_fitness'])}")
    print(f"Czas: {_fmt_float(elapsed)} s")
    print("======================\n\n\n\n\n\n\n\n")

    return {
        "status": "ok",
        "message": "Engine wykonany poprawnie.",
        "best": round(final_summary["best_fitness"], 3) if final_summary["best_fitness"] is not None else None,
        "avg": round(final_summary["avg_fitness"], 3) if final_summary["avg_fitness"] is not None else None,
        "worst": round(final_summary["worst_fitness"], 3) if final_summary["worst_fitness"] is not None else None,
        "elapsed": round(elapsed, 3),
        "best_raw_objective": round(final_summary["best_raw_objective"], 3) if final_summary["best_raw_objective"] is not None else None,
        "best_decoded": [
            round(value, 3) for value in final_summary["best_decoded"]
        ] if final_summary["best_decoded"] is not None else None,
        "population_summary": final_summary,
        "history": history,
    }
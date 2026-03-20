# test_all_functions_global.py
from __future__ import annotations

import random
import time
import traceback

from ga_optimizer.experiments.base_runner import (
    format_global_params_for_print,
    print_experiment_progress,
    run_single_config,
)
from ga_optimizer.experiments.metrics import (
    build_best_per_problem_rows,
    build_operator_ranking_rows,
    summarize_rows_basic,
)
from ga_optimizer.experiments.plotting import (
    save_group_quality_ranking,
    save_problem_metric_bar,
    save_problem_success_rate_bar,
)
from ga_optimizer.experiments.reporting import (
    build_all_functions_report,
    make_experiment_output_dir,
    save_report_md,
    save_summary_csv,
    save_summary_json,
)
from ga_optimizer.experiments.search_spaces import sample_random_config
from ga_optimizer.problems.function_catalog import get_problem_names


def _build_quality_rows(
    rows: list[dict],
    config_key: str,
    label_map: dict | None = None,
) -> list[dict]:
    valid = [r for r in rows if r.get("abs_value_error") is not None]
    grouped: dict[str, list[float]] = {}

    for row in valid:
        raw_label = row["config"][config_key]
        label = label_map.get(raw_label, str(raw_label)) if label_map else str(raw_label)
        grouped.setdefault(label, []).append(float(row["abs_value_error"]))

    result = []
    for label, vals in grouped.items():
        result.append(
            {
                "label": label,
                "mean": sum(vals) / len(vals),
                "median": sorted(vals)[len(vals) // 2] if len(vals) % 2 == 1 else (sorted(vals)[len(vals) // 2 - 1] + sorted(vals)[len(vals) // 2]) / 2.0,
                "count": len(vals),
            }
        )

    result.sort(key=lambda item: (item["mean"], item["median"], item["label"]))
    return result


def run_all_functions_global_operator_search(
    preset_name: str,
    preset: dict,
) -> dict:
    ranges = preset["ranges"]
    executions_per_function = int(preset["executions_per_function"])
    seed = preset.get("seed", "")
    value_tol = float(preset["success_value_abs_tol"])
    point_tol = float(preset["success_point_distance_tol"])
    problem_names = get_problem_names() if preset.get("problem_names") == "all" else list(preset["problem_names"])

    rng = random.Random()
    if seed not in ("", None):
        rng.seed(seed)

    output_dir = make_experiment_output_dir("all_functions_global_operator_search", preset_name)
    total_executions = len(problem_names) * executions_per_function

    print("\n\n[all_functions_global] START TESTU\n")
    print(f"[all_functions_global] funkcji: {len(problem_names)}")
    print(f"[all_functions_global] wykonań na funkcję: {executions_per_function}")
    print(f"[all_functions_global] łącznie wykonań: {total_executions}")
    print(f"[all_functions_global] katalog: {output_dir}\n")

    test_start = time.perf_counter()
    all_rows = []
    errors = []
    global_step = 0

    for problem_index, problem_name in enumerate(problem_names, start=1):
        print(f"[all_functions_global] funkcja {problem_index}/{len(problem_names)}: {problem_name}\n")

        for exec_index in range(executions_per_function):
            global_step += 1
            step_label = (
                f"funkcja={problem_name} | "
                f"lokalnie {exec_index + 1}/{executions_per_function} | "
                f"funkcja {problem_index}/{len(problem_names)}"
            )

            print_experiment_progress("all_functions_global", global_step, total_executions, step_label=step_label)

            config = sample_random_config(problem_name=problem_name, ranges=ranges, rng=rng, seed=seed)
            print(f"[all_functions_global] parametry globalne | {format_global_params_for_print(config)}")

            exp_start = time.perf_counter()
            try:
                row = run_single_config(
                    config,
                    progress_prefix="[all_functions_global]",
                    experiment_progress=(global_step, total_executions),
                    step_label=step_label,
                )
                row["experiment_duration_sec"] = time.perf_counter() - exp_start
                all_rows.append(row)
                print(f"[all_functions_global] czas eksperymentu: {row['experiment_duration_sec']:.3f} s")
            except Exception as exc:
                err = {
                    "step": global_step,
                    "label": step_label,
                    "type": type(exc).__name__,
                    "message": str(exc),
                    "traceback": traceback.format_exc(),
                }
                errors.append(err)
                print(f"[all_functions_global] BŁĄD: {err['type']} | {err['message']}")

            print()

        print()

    test_duration_sec = time.perf_counter() - test_start
    print(f"[all_functions_global] czas całego testu: {test_duration_sec:.3f} s")
    print("\n[all_functions_global] KONIEC TESTU\n\n")

    valid_rows = [row for row in all_rows if row.get("best_value") is not None]
    best_per_problem_rows = build_best_per_problem_rows(valid_rows)
    ranking_rows = build_operator_ranking_rows(valid_rows)
    all_functions_summary = summarize_rows_basic(valid_rows, value_tol=value_tol, point_tol=point_tol)

    selection_quality_rows = _build_quality_rows(valid_rows, "selection_method")
    crossover_quality_rows = _build_quality_rows(valid_rows, "crossover_method")
    mutation_quality_rows = _build_quality_rows(valid_rows, "mutation_method")
    inversion_quality_rows = _build_quality_rows(
        valid_rows,
        "inversion_enabled",
        label_map={True: "inversion=True", False: "inversion=False"},
    )
    elitism_quality_rows = _build_quality_rows(
        valid_rows,
        "elitism_enabled",
        label_map={True: "elitism=True", False: "elitism=False"},
    )

    median_error_by_function = save_problem_metric_bar(
        output_dir=output_dir,
        rows=valid_rows,
        value_key="abs_value_error",
        agg="median",
        title="Mediana błędu per funkcja",
        xlabel="Mediana abs error",
        filename="bar_median_error_by_function.png",
    )
    median_point_distance_by_function = save_problem_metric_bar(
        output_dir=output_dir,
        rows=valid_rows,
        value_key="nearest_global_min_point_distance",
        agg="median",
        title="Mediana odległości od minimum per funkcja",
        xlabel="Mediana odległości",
        filename="bar_median_point_distance_by_function.png",
    )
    success_rate_value_by_function = save_problem_success_rate_bar(
        output_dir=output_dir,
        rows=valid_rows,
        value_tol=value_tol,
        filename="bar_success_rate_value_by_function.png",
        title="Success rate wg wartości per funkcja",
    )

    selection_ranking = save_group_quality_ranking(
        output_dir=output_dir,
        rows=valid_rows,
        config_key="selection_method",
        title="All functions: ranking metod selekcji",
        filename="rank_selection_quality_all_functions.png",
    )
    crossover_ranking = save_group_quality_ranking(
        output_dir=output_dir,
        rows=valid_rows,
        config_key="crossover_method",
        title="All functions: ranking metod crossover",
        filename="rank_crossover_quality_all_functions.png",
    )
    mutation_ranking = save_group_quality_ranking(
        output_dir=output_dir,
        rows=valid_rows,
        config_key="mutation_method",
        title="All functions: ranking metod mutacji",
        filename="rank_mutation_quality_all_functions.png",
    )
    inversion_ranking = save_group_quality_ranking(
        output_dir=output_dir,
        rows=valid_rows,
        config_key="inversion_enabled",
        title="All functions: czy inwersja pomaga?",
        filename="rank_inversion_quality_all_functions.png",
        label_map={True: "inversion=True", False: "inversion=False"},
    )
    elitism_ranking = save_group_quality_ranking(
        output_dir=output_dir,
        rows=valid_rows,
        config_key="elitism_enabled",
        title="All functions: czy elitaryzm pomaga?",
        filename="rank_elitism_quality_all_functions.png",
        label_map={True: "elitism=True", False: "elitism=False"},
    )

    summary = {
        "test_name": "all_functions_global_operator_search",
        "preset_name": preset_name,
        "problem_count": len(problem_names),
        "executions_per_function": executions_per_function,
        "total_executions": total_executions,
        "goal_description": "Celem tego testu jest znaleźć najlepsze wyniki dla każdej konkretnej funkcji, ale przy jednoczesnym zbieraniu globalnych rankingów operatorów z całego przebiegu.",
        "success_value_abs_tol": value_tol,
        "success_point_distance_tol": point_tol,
        "rows": best_per_problem_rows,
        "best_per_problem": best_per_problem_rows,
        "operator_ranking": ranking_rows,
        "top_rows": best_per_problem_rows[:15],
        "top_rows_full": best_per_problem_rows,
        "best_value": all_functions_summary["best_value"],
        "q1_best_value": all_functions_summary["q1_best_value"],
        "median_best_value": all_functions_summary["median_best_value"],
        "mean_best_value": all_functions_summary["mean_best_value"],
        "q3_best_value": all_functions_summary["q3_best_value"],
        "worst_best_value": all_functions_summary["worst_best_value"],
        "mean_abs_error_across_functions": all_functions_summary["mean_abs_error"],
        "median_abs_error_across_functions": all_functions_summary["median_abs_error"],
        "mean_point_distance_across_functions": all_functions_summary["mean_point_distance"],
        "median_point_distance_across_functions": all_functions_summary["median_point_distance"],
        "mean_elapsed_across_functions": all_functions_summary["mean_elapsed"],
        "mean_duration_sec": all_functions_summary["mean_duration_sec"],
        "median_duration_sec": all_functions_summary["median_duration_sec"],
        "success": all_functions_summary["success"],
        "selection_quality_rows": selection_quality_rows,
        "crossover_quality_rows": crossover_quality_rows,
        "mutation_quality_rows": mutation_quality_rows,
        "inversion_quality_rows": inversion_quality_rows,
        "elitism_quality_rows": elitism_quality_rows,
        "plot_paths": {
            "bar_median_error_by_function": median_error_by_function,
            "bar_median_point_distance_by_function": median_point_distance_by_function,
            "bar_success_rate_value_by_function": success_rate_value_by_function,
            "rank_selection_quality": selection_ranking,
            "rank_crossover_quality": crossover_ranking,
            "rank_mutation_quality": mutation_ranking,
            "rank_inversion_quality": inversion_ranking,
            "rank_elitism_quality": elitism_ranking,
        },
        "test_duration_sec": test_duration_sec,
        "errors": errors,
        "output_dir": str(output_dir),
    }

    report_text = build_all_functions_report(summary)
    save_summary_json(output_dir, summary)
    save_summary_csv(output_dir, best_per_problem_rows)
    save_summary_csv(output_dir, ranking_rows, filename="operator_ranking.csv")
    save_report_md(output_dir, report_text)

    return {
        "status": "ok",
        "test_name": "all_functions_global_operator_search",
        "output_dir": str(output_dir),
        "summary": summary,
    }
# test_random_functions.py
from __future__ import annotations

import random
import time
import traceback

from ga_optimizer.experiments.base_runner import (
    format_duration_human,
    format_global_params_for_print,
    print_experiment_progress,
    run_single_config,
)
from ga_optimizer.experiments.metrics import (
    build_operator_ranking_rows,
    summarize_rows_basic,
)
from ga_optimizer.experiments.plotting import (
    save_group_quality_ranking,
    save_problem_counts_bar,
    save_problem_metric_bar,
)
from ga_optimizer.experiments.reporting import (
    build_random_functions_report,
    make_experiment_output_dir,
    save_report_md,
    save_summary_csv,
    save_summary_json,
)
from ga_optimizer.experiments.search_spaces import pick_problem_name, sample_random_config


def _to_csv_rows(rows: list[dict]) -> list[dict]:
    csv_rows = []
    ranked = [row for row in rows if row.get("best_value") is not None]
    ranked.sort(key=lambda row: row["best_value"])

    for index, item in enumerate(ranked, start=1):
        cfg = item["config"]
        csv_rows.append(
            {
                "rank": index,
                "problem_name": item["problem_name"],
                "best_value": item["best_value"],
                "signed_value_error": item["signed_value_error"],
                "abs_value_error": item["abs_value_error"],
                "nearest_global_min_point_distance": item["nearest_global_min_point_distance"],
                "selection_method": cfg["selection_method"],
                "crossover_method": cfg["crossover_method"],
                "mutation_method": cfg["mutation_method"],
                "inversion_enabled": cfg["inversion_enabled"],
                "elitism_enabled": cfg["elitism_enabled"],
                "population": cfg["population"],
                "epochs": cfg["epochs"],
                "run_count": cfg["run_count"],
                "precision_bits": cfg["precision_bits"],
                "seed": cfg["seed"],
                "duration_sec": item.get("duration_sec"),
            }
        )
    return csv_rows


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


def run_random_functions_test(
    preset_name: str,
    preset: dict,
) -> dict:
    executions = int(preset["executions"])
    problem_pool = preset["problem_pool"]
    seed = preset.get("seed", None)
    value_tol = float(preset["success_value_abs_tol"])
    point_tol = float(preset["success_point_distance_tol"])
    ranges = preset["ranges"]

    rng = random.Random()
    if seed is not None:
        rng.seed(seed)

    output_dir = make_experiment_output_dir("random_functions", preset_name)

    print("\n\n[random_functions] START TESTU\n")
    print(f"[random_functions] liczba pełnych wykonań: {executions}")
    print(f"[random_functions] katalog: {output_dir}\n")

    test_start = time.perf_counter()
    rows = []
    errors = []

    for exec_index in range(executions):
        current_step = exec_index + 1
        problem_name = pick_problem_name(problem_pool, rng)
        step_label = f"funkcja={problem_name}"

        print_experiment_progress("random_functions", current_step, executions, step_label=step_label)

        config = sample_random_config(problem_name=problem_name, ranges=ranges, rng=rng, seed=seed)
        print(f"[random_functions] parametry globalne | {format_global_params_for_print(config)}")

        exp_start = time.perf_counter()
        try:
            row = run_single_config(
                config,
                progress_prefix="[random_functions]",
                experiment_progress=(current_step, executions),
                step_label=step_label,
            )
            row["experiment_duration_sec"] = time.perf_counter() - exp_start
            rows.append(row)
            print(f"[random_functions] czas eksperymentu: {format_duration_human(row['experiment_duration_sec'])}")
        except Exception as exc:
            err = {
                "step": current_step,
                "label": step_label,
                "type": type(exc).__name__,
                "message": str(exc),
                "traceback": traceback.format_exc(),
            }
            errors.append(err)
            print(f"[random_functions] BŁĄD: {err['type']} | {err['message']}")

        print()

    test_duration_sec = time.perf_counter() - test_start
    print(f"[random_functions] czas całego testu: {format_duration_human(test_duration_sec)}")
    print("\n[random_functions] KONIEC TESTU\n\n")

    csv_rows = _to_csv_rows(rows)
    summary_basic = summarize_rows_basic(rows, value_tol=value_tol, point_tol=point_tol)
    ranking_rows = build_operator_ranking_rows([row for row in rows if row.get("best_value") is not None])

    selection_quality_rows = _build_quality_rows(rows, "selection_method")
    crossover_quality_rows = _build_quality_rows(rows, "crossover_method")
    mutation_quality_rows = _build_quality_rows(rows, "mutation_method")
    inversion_quality_rows = _build_quality_rows(
        rows,
        "inversion_enabled",
        label_map={True: "inversion=True", False: "inversion=False"},
    )
    elitism_quality_rows = _build_quality_rows(
        rows,
        "elitism_enabled",
        label_map={True: "elitism=True", False: "elitism=False"},
    )

    sampled_problem_counts = save_problem_counts_bar(
        output_dir=output_dir,
        rows=rows,
        filename="bar_problem_counts_random_functions.png",
        title="Liczba wylosowań funkcji",
    )
    median_error_by_problem = save_problem_metric_bar(
        output_dir=output_dir,
        rows=rows,
        value_key="abs_value_error",
        agg="median",
        title="Mediana abs error per funkcja",
        xlabel="Mediana abs error",
        filename="bar_median_error_by_problem_random_functions.png",
    )

    selection_ranking = save_group_quality_ranking(
        output_dir=output_dir,
        rows=rows,
        config_key="selection_method",
        title="Ranking jakości metod selekcji (losowe funkcje)",
        filename="rank_selection_quality_random_functions.png",
    )
    crossover_ranking = save_group_quality_ranking(
        output_dir=output_dir,
        rows=rows,
        config_key="crossover_method",
        title="Ranking jakości metod crossover (losowe funkcje)",
        filename="rank_crossover_quality_random_functions.png",
    )
    mutation_ranking = save_group_quality_ranking(
        output_dir=output_dir,
        rows=rows,
        config_key="mutation_method",
        title="Ranking jakości metod mutacji (losowe funkcje)",
        filename="rank_mutation_quality_random_functions.png",
    )
    inversion_ranking = save_group_quality_ranking(
        output_dir=output_dir,
        rows=rows,
        config_key="inversion_enabled",
        title="Czy inwersja pomaga? (losowe funkcje)",
        filename="rank_inversion_quality_random_functions.png",
        label_map={True: "inversion=True", False: "inversion=False"},
    )
    elitism_ranking = save_group_quality_ranking(
        output_dir=output_dir,
        rows=rows,
        config_key="elitism_enabled",
        title="Czy elitaryzm pomaga? (losowe funkcje)",
        filename="rank_elitism_quality_random_functions.png",
        label_map={True: "elitism=True", False: "elitism=False"},
    )

    summary = {
        "test_name": "random_functions",
        "preset_name": preset_name,
        "executions": executions,
        "problem_pool": problem_pool,
        "success_value_abs_tol": value_tol,
        "success_point_distance_tol": point_tol,
        "best_value": summary_basic["best_value"],
        "q1_best_value": summary_basic["q1_best_value"],
        "median_best_value": summary_basic["median_best_value"],
        "mean_best_value": summary_basic["mean_best_value"],
        "q3_best_value": summary_basic["q3_best_value"],
        "worst_best_value": summary_basic["worst_best_value"],
        "mean_abs_error": summary_basic["mean_abs_error"],
        "median_abs_error": summary_basic["median_abs_error"],
        "mean_point_distance": summary_basic["mean_point_distance"],
        "median_point_distance": summary_basic["median_point_distance"],
        "mean_elapsed": summary_basic["mean_elapsed"],
        "mean_duration_sec": summary_basic["mean_duration_sec"],
        "median_duration_sec": summary_basic["median_duration_sec"],
        "std_best_value": summary_basic["std_best_value"],
        "success": summary_basic["success"],
        "top_rows": csv_rows[:15],
        "top_rows_full": csv_rows,
        "operator_ranking": ranking_rows,
        "selection_quality_rows": selection_quality_rows,
        "crossover_quality_rows": crossover_quality_rows,
        "mutation_quality_rows": mutation_quality_rows,
        "inversion_quality_rows": inversion_quality_rows,
        "elitism_quality_rows": elitism_quality_rows,
        "plot_paths": {
            "bar_problem_counts": sampled_problem_counts,
            "bar_median_error_by_problem": median_error_by_problem,
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

    report_text = build_random_functions_report(summary)
    save_summary_json(output_dir, summary)
    save_summary_csv(output_dir, csv_rows)
    save_summary_csv(output_dir, ranking_rows, filename="operator_ranking.csv")
    save_report_md(output_dir, report_text)

    return {
        "status": "ok",
        "test_name": "random_functions",
        "output_dir": str(output_dir),
        "summary": summary,
    }
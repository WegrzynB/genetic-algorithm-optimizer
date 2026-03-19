from __future__ import annotations

import random

from ga_optimizer.experiments.base_runner import print_experiment_progress, run_single_config
from ga_optimizer.experiments.metrics import (
    build_operator_ranking_rows,
    describe_best_parameter_regions,
    summarize_rows_basic,
)
from ga_optimizer.experiments.plotting import (
    save_bar_operator_wins,
    save_heatmap_best_points,
    save_histogram_best_values,
)
from ga_optimizer.experiments.reporting import (
    build_single_function_operator_report,
    make_experiment_output_dir,
    save_report_md,
    save_summary_csv,
    save_summary_json,
)
from ga_optimizer.experiments.search_spaces import sample_random_config
from ga_optimizer.problems.function_catalog import get_problem_definition


def _to_csv_rows(rows: list[dict]) -> list[dict]:
    csv_rows = []
    ranked = [row for row in rows if row.get("best_value") is not None]
    ranked.sort(key=lambda row: row["best_value"])

    for index, item in enumerate(ranked, start=1):
        cfg = item["config"]
        csv_rows.append(
            {
                "rank": index,
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
            }
        )
    return csv_rows


def _best_or_worst_to_row(row: dict | None) -> dict | None:
    if row is None:
        return None
    cfg = row["config"]
    return {
        "best_value": row["best_value"],
        "abs_value_error": row["abs_value_error"],
        "nearest_global_min_point_distance": row["nearest_global_min_point_distance"],
        "selection_method": cfg["selection_method"],
        "crossover_method": cfg["crossover_method"],
        "mutation_method": cfg["mutation_method"],
        "population": cfg["population"],
        "epochs": cfg["epochs"],
        "run_count": cfg["run_count"],
        "precision_bits": cfg["precision_bits"],
    }


def run_single_function_operator_search(
    preset_name: str,
    preset: dict,
) -> dict:
    """
    Testuje jedną wybraną funkcję dla losowych konfiguracji i wskazuje:
    - najlepsze konkretne kombinacje,
    - najlepsze obszary parametrów,
    - ranking operatorów,
    - skuteczność względem znanego minimum globalnego i punktów minimum.
    """
    problem_name = preset["problem_name"]
    executions = int(preset["executions"])
    seed = preset.get("seed", "")
    value_tol = float(preset["success_value_abs_tol"])
    point_tol = float(preset["success_point_distance_tol"])
    top_fraction_for_regions = float(preset.get("top_fraction_for_regions", 0.25))
    ranges = preset["ranges"]

    rng = random.Random()
    if seed not in ("", None):
        rng.seed(seed)

    output_dir = make_experiment_output_dir("single_function_operator_search", preset_name)
    problem = get_problem_definition(problem_name)

    print(f"[single_function_operator_search] funkcja: {problem_name}")
    print(f"[single_function_operator_search] liczba pełnych wykonań: {executions}")
    print(f"[single_function_operator_search] katalog: {output_dir}")

    rows = []
    for exec_index in range(executions):
        current_step = exec_index + 1
        step_label = f"funkcja={problem_name}"

        print_experiment_progress(
            "single_function_operator_search",
            current_step,
            executions,
            step_label=step_label,
        )

        config = sample_random_config(
            problem_name=problem_name,
            ranges=ranges,
            rng=rng,
            seed=seed,
        )

        print(
            f"[single_function_operator_search] konfiguracja | "
            f"sel={config.selection_method} | "
            f"cross={config.crossover_method} | "
            f"mut={config.mutation_method} | "
            f"pop={config.population} | epochs={config.epochs} | run_count={config.run_count}"
        )

        row = run_single_config(
            config,
            progress_prefix="[single_function_operator_search]",
            experiment_progress=(current_step, executions),
            step_label=step_label,
        )
        rows.append(row)

    csv_rows = _to_csv_rows(rows)
    summary_basic = summarize_rows_basic(rows, value_tol=value_tol, point_tol=point_tol)
    ranking_rows = build_operator_ranking_rows([row for row in rows if row.get("best_value") is not None])
    best_regions = describe_best_parameter_regions(rows, top_fraction=top_fraction_for_regions)

    values = [row["best_value"] for row in rows if row.get("best_value") is not None]
    points = [row["best_point"] for row in rows if row.get("best_point") is not None]

    hist_path = save_histogram_best_values(output_dir, values, filename="hist_single_function.png")
    heatmap_path = None
    if int(problem.default_n_vars) == 2:
        heatmap_path = save_heatmap_best_points(
            output_dir,
            points,
            problem.global_minimum_points,
            filename="heatmap_single_function.png",
        )
    bar_operator_path = save_bar_operator_wins(output_dir, ranking_rows, filename="bar_operator_wins_single_function.png")

    summary = {
        "test_name": "single_function_operator_search",
        "preset_name": preset_name,
        "problem_name": problem.key,
        "problem_display_name": problem.display_name,
        "global_minimum_value": float(problem.global_minimum_value),
        "global_minimum_points": problem.global_minimum_points,
        "executions": executions,
        "success_value_abs_tol": value_tol,
        "success_point_distance_tol": point_tol,
        "mean_best_value": summary_basic["mean_best_value"],
        "median_best_value": summary_basic["median_best_value"],
        "std_best_value": summary_basic["std_best_value"],
        "mean_abs_error": summary_basic["mean_abs_error"],
        "median_abs_error": summary_basic["median_abs_error"],
        "mean_point_distance": summary_basic["mean_point_distance"],
        "median_point_distance": summary_basic["median_point_distance"],
        "mean_elapsed": summary_basic["mean_elapsed"],
        "success": summary_basic["success"],
        "best_overall": _best_or_worst_to_row(summary_basic["best_row"]),
        "worst_overall": _best_or_worst_to_row(summary_basic["worst_row"]),
        "top_rows": csv_rows[:10],
        "operator_ranking": ranking_rows,
        "best_parameter_regions": best_regions,
        "plot_paths": {
            "histogram": hist_path,
            "heatmap": heatmap_path,
            "bar_operator_wins": bar_operator_path,
        },
        "output_dir": str(output_dir),
    }

    report_text = build_single_function_operator_report(summary)
    save_summary_json(output_dir, summary)
    save_summary_csv(output_dir, csv_rows)
    save_summary_csv(output_dir, ranking_rows, filename="operator_ranking.csv")
    save_report_md(output_dir, report_text)

    return {
        "status": "ok",
        "test_name": "single_function_operator_search",
        "output_dir": str(output_dir),
        "summary": summary,
    }
from __future__ import annotations

import random
from statistics import mean, median

from ga_optimizer.experiments.base_runner import print_experiment_progress, run_single_config
from ga_optimizer.experiments.metrics import build_operator_ranking_rows, summarize_rows_basic
from ga_optimizer.experiments.plotting import save_bar_errors_by_function, save_bar_operator_wins
from ga_optimizer.experiments.reporting import (
    build_all_functions_report,
    make_experiment_output_dir,
    save_report_md,
    save_summary_csv,
    save_summary_json,
)
from ga_optimizer.experiments.search_spaces import sample_random_config
from ga_optimizer.problems.function_catalog import get_problem_names


def run_all_functions_global_operator_search(
    preset_name: str,
    preset: dict,
) -> dict:
    """
    Dla każdej funkcji wykonuje określoną liczbę pełnych uruchomień
    i szuka operatorów dobrych globalnie.

    executions_per_function określa, ile razy testowana jest każda funkcja.
    """
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

    print(f"[all_functions_global] funkcji: {len(problem_names)}")
    print(f"[all_functions_global] wykonań na funkcję: {executions_per_function}")
    print(f"[all_functions_global] łącznie wykonań: {total_executions}")
    print(f"[all_functions_global] katalog: {output_dir}")

    best_rows_per_problem = []
    all_rows = []
    global_step = 0

    for problem_index, problem_name in enumerate(problem_names, start=1):
        print(f"\n[all_functions_global] funkcja {problem_index}/{len(problem_names)}: {problem_name}")
        problem_rows = []

        for exec_index in range(executions_per_function):
            global_step += 1
            step_label = (
                f"funkcja={problem_name} | "
                f"lokalnie {exec_index + 1}/{executions_per_function} | "
                f"funkcja {problem_index}/{len(problem_names)}"
            )

            print_experiment_progress(
                "all_functions_global",
                global_step,
                total_executions,
                step_label=step_label,
            )

            config = sample_random_config(
                problem_name=problem_name,
                ranges=ranges,
                rng=rng,
                seed=seed,
            )

            row = run_single_config(
                config,
                progress_prefix="[all_functions_global]",
                experiment_progress=(global_step, total_executions),
                step_label=step_label,
            )
            all_rows.append(row)
            if row.get("best_value") is not None:
                problem_rows.append(row)

        if problem_rows:
            problem_summary = summarize_rows_basic(problem_rows, value_tol=value_tol, point_tol=point_tol)
            best = problem_summary["best_row"]
            if best is not None:
                best_rows_per_problem.append(best)

    summary_rows = []
    for row in best_rows_per_problem:
        cfg = row["config"]
        summary_rows.append(
            {
                "problem_name": row["problem_name"],
                "best_value": row["best_value"],
                "signed_value_error": row["signed_value_error"],
                "abs_value_error": row["abs_value_error"],
                "nearest_global_min_point_distance": row["nearest_global_min_point_distance"],
                "selection_method": cfg["selection_method"],
                "crossover_method": cfg["crossover_method"],
                "mutation_method": cfg["mutation_method"],
                "population": cfg["population"],
                "epochs": cfg["epochs"],
                "run_count": cfg["run_count"],
                "precision_bits": cfg["precision_bits"],
                "seed": cfg["seed"],
            }
        )

    summary_rows.sort(key=lambda row: row["abs_value_error"])
    ranking_rows = build_operator_ranking_rows(best_rows_per_problem)

    all_functions_summary = summarize_rows_basic(best_rows_per_problem, value_tol=value_tol, point_tol=point_tol)

    bar_errors_path = save_bar_errors_by_function(output_dir, [
        {
            "problem_name": row["problem_name"],
            "error_to_global_min": row["abs_value_error"],
        }
        for row in summary_rows
    ], filename="bar_errors_all_functions.png")
    bar_operator_path = save_bar_operator_wins(output_dir, ranking_rows, filename="bar_operator_wins_all_functions.png")

    summary = {
        "test_name": "all_functions_global_operator_search",
        "preset_name": preset_name,
        "problem_count": len(problem_names),
        "executions_per_function": executions_per_function,
        "total_executions": total_executions,
        "success_value_abs_tol": value_tol,
        "success_point_distance_tol": point_tol,
        "rows": summary_rows,
        "operator_ranking": ranking_rows,
        "mean_abs_error_across_functions": all_functions_summary["mean_abs_error"],
        "median_abs_error_across_functions": all_functions_summary["median_abs_error"],
        "mean_point_distance_across_functions": all_functions_summary["mean_point_distance"],
        "median_point_distance_across_functions": all_functions_summary["median_point_distance"],
        "mean_elapsed_across_functions": all_functions_summary["mean_elapsed"],
        "success": all_functions_summary["success"],
        "plot_paths": {
            "bar_errors_by_function": bar_errors_path,
            "bar_operator_wins": bar_operator_path,
        },
        "output_dir": str(output_dir),
    }

    report_text = build_all_functions_report(summary)
    save_summary_json(output_dir, summary)
    save_summary_csv(output_dir, summary_rows)
    save_summary_csv(output_dir, ranking_rows, filename="operator_ranking.csv")
    save_report_md(output_dir, report_text)

    return {
        "status": "ok",
        "test_name": "all_functions_global_operator_search",
        "output_dir": str(output_dir),
        "summary": summary,
    }
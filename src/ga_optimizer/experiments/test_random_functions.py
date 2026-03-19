from __future__ import annotations

import random

from ga_optimizer.experiments.base_runner import print_experiment_progress, run_single_config
from ga_optimizer.experiments.metrics import build_operator_ranking_rows, summarize_rows_basic
from ga_optimizer.experiments.plotting import (
    save_bar_errors_by_function,
    save_bar_operator_wins,
    save_histogram_best_values,
)
from ga_optimizer.experiments.reporting import (
    build_random_functions_report,
    make_experiment_output_dir,
    save_report_md,
    save_summary_csv,
    save_summary_json,
)
from ga_optimizer.experiments.search_spaces import sample_random_config
from ga_optimizer.problems.function_catalog import get_problem_names


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
                "population": cfg["population"],
                "epochs": cfg["epochs"],
                "run_count": cfg["run_count"],
                "precision_bits": cfg["precision_bits"],
                "selection_method": cfg["selection_method"],
                "crossover_method": cfg["crossover_method"],
                "mutation_method": cfg["mutation_method"],
                "inversion_enabled": cfg["inversion_enabled"],
                "elitism_enabled": cfg["elitism_enabled"],
                "seed": cfg["seed"],
            }
        )
    return csv_rows


def run_random_functions_test(
    preset_name: str,
    preset: dict,
) -> dict:
    """
    Testuje losowe funkcje z losowymi konfiguracjami.
    Wszystko jest losowane:
    - funkcja
    - operatorzy
    - parametry
    - seed (jeśli pusty)
    """
    ranges = preset["ranges"]
    executions = int(preset["executions"])
    seed = preset.get("seed", "")
    value_tol = float(preset["success_value_abs_tol"])
    point_tol = float(preset["success_point_distance_tol"])
    pool = get_problem_names()

    rng = random.Random()
    if seed not in ("", None):
        rng.seed(seed)

    output_dir = make_experiment_output_dir("random_functions", preset_name)

    print(f"[random_functions] liczba pełnych wykonań: {executions}")
    print(f"[random_functions] katalog: {output_dir}")

    rows = []
    for exec_index in range(executions):
        current_step = exec_index + 1
        problem_name = rng.choice(pool)
        step_label = f"funkcja={problem_name}"

        print_experiment_progress(
            "random_functions",
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
            f"[random_functions] konfiguracja | "
            f"sel={config.selection_method} | "
            f"cross={config.crossover_method} | "
            f"mut={config.mutation_method} | "
            f"pop={config.population} | epochs={config.epochs} | run_count={config.run_count}"
        )

        row = run_single_config(
            config,
            progress_prefix="[random_functions]",
            experiment_progress=(current_step, executions),
            step_label=step_label,
        )
        rows.append(row)

    csv_rows = _to_csv_rows(rows)
    summary_basic = summarize_rows_basic(rows, value_tol=value_tol, point_tol=point_tol)
    ranking_rows = build_operator_ranking_rows([row for row in rows if row.get("best_value") is not None])

    values = [row["best_value"] for row in rows if row.get("best_value") is not None]
    per_problem_best_rows = []
    best_per_problem = {}
    for row in [r for r in rows if r.get("best_value") is not None]:
        name = row["problem_name"]
        if name not in best_per_problem or row["best_value"] < best_per_problem[name]["best_value"]:
            best_per_problem[name] = row
    for row in best_per_problem.values():
        per_problem_best_rows.append(
            {
                "problem_name": row["problem_name"],
                "error_to_global_min": row["abs_value_error"],
            }
        )

    hist_path = save_histogram_best_values(output_dir, values, filename="hist_random_functions.png")
    bar_problem_path = save_bar_errors_by_function(output_dir, per_problem_best_rows, filename="bar_errors_random_functions.png")
    bar_operator_path = save_bar_operator_wins(output_dir, ranking_rows, filename="bar_operator_wins_random_functions.png")

    best_overall_row = summary_basic["best_row"]
    worst_overall_row = summary_basic["worst_row"]

    def _bestworst_to_dict(row):
        if row is None:
            return None
        cfg = row["config"]
        return {
            "problem_name": row["problem_name"],
            "best_value": row["best_value"],
            "abs_value_error": row["abs_value_error"],
            "nearest_global_min_point_distance": row["nearest_global_min_point_distance"],
            "selection_method": cfg["selection_method"],
            "crossover_method": cfg["crossover_method"],
            "mutation_method": cfg["mutation_method"],
        }

    summary = {
        "test_name": "random_functions",
        "preset_name": preset_name,
        "executions": executions,
        "problem_pool_label": "all",
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
        "best_overall": _bestworst_to_dict(best_overall_row),
        "worst_overall": _bestworst_to_dict(worst_overall_row),
        "top_rows": csv_rows[:10],
        "operator_ranking": ranking_rows,
        "plot_paths": {
            "histogram": hist_path,
            "bar_errors_by_function": bar_problem_path,
            "bar_operator_wins": bar_operator_path,
        },
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
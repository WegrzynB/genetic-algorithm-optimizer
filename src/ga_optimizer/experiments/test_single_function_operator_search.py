# test_single_function_operator_search.py
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
    build_operator_ranking_rows,
    describe_best_parameter_regions,
    summarize_rows_basic,
)
from ga_optimizer.experiments.plotting import (
    save_bar_operator_wins,
    save_boxplot_best_values,
    save_error_vs_distance_scatter,
    save_group_quality_ranking,
    save_histogram_best_values,
    save_median_density_heatmap,
    save_scatter_param_vs_error,
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
                "abs_value_error": item["abs_value_error"],
                "nearest_global_min_point_distance": item["nearest_global_min_point_distance"],
                "selection_method": cfg["selection_method"],
                "crossover_method": cfg["crossover_method"],
                "mutation_method": cfg["mutation_method"],
                "population": cfg["population"],
                "epochs": cfg["epochs"],
                "run_count": cfg["run_count"],
                "precision_bits": cfg["precision_bits"],
                "inversion_enabled": cfg["inversion_enabled"],
                "elitism_enabled": cfg["elitism_enabled"],
            }
        )
    return csv_rows


def _row_to_point(row):
    if row is None:
        return None
    return row.get("best_point")


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


def run_single_function_operator_search(
    preset_name: str,
    preset: dict,
) -> dict:
    problem_name = preset["problem_name"]
    executions = int(preset["executions"])
    seed = preset.get("seed", None)
    value_tol = float(preset["success_value_abs_tol"])
    point_tol = float(preset["success_point_distance_tol"])
    top_fraction_for_regions = float(preset.get("top_fraction_for_regions", 0.25))
    ranges = preset["ranges"]

    heatmap_bins = int(preset.get("heatmap_bins", 18))

    rng = random.Random()
    if seed is not None:
        rng.seed(seed)

    output_dir = make_experiment_output_dir("single_function_operator_search", preset_name)
    problem = get_problem_definition(problem_name)

    print("\n\n[single_function_operator_search] START TESTU\n")
    print(f"[single_function_operator_search] funkcja: {problem_name}")
    print(f"[single_function_operator_search] liczba pełnych wykonań: {executions}")
    print(f"[single_function_operator_search] katalog: {output_dir}\n")

    test_start = time.perf_counter()
    rows = []
    errors = []

    for exec_index in range(executions):
        current_step = exec_index + 1
        step_label = f"funkcja={problem_name}"

        print_experiment_progress("single_function_operator_search", current_step, executions, step_label=step_label)

        config = sample_random_config(problem_name=problem_name, ranges=ranges, rng=rng, seed=seed)
        print(f"[single_function_operator_search] parametry globalne | {format_global_params_for_print(config)}")

        exp_start = time.perf_counter()
        try:
            row = run_single_config(
                config,
                progress_prefix="[single_function_operator_search]",
                experiment_progress=(current_step, executions),
                step_label=step_label,
            )
            row["experiment_duration_sec"] = time.perf_counter() - exp_start
            rows.append(row)
            print(f"[single_function_operator_search] czas eksperymentu: {row['experiment_duration_sec']:.3f} s")
        except Exception as exc:
            err = {
                "step": current_step,
                "label": step_label,
                "type": type(exc).__name__,
                "message": str(exc),
                "traceback": traceback.format_exc(),
            }
            errors.append(err)
            print(f"[single_function_operator_search] BŁĄD: {err['type']} | {err['message']}")

        print()

    test_duration_sec = time.perf_counter() - test_start
    print(f"[single_function_operator_search] czas całego testu: {test_duration_sec:.3f} s")
    print("\n[single_function_operator_search] KONIEC TESTU\n\n")

    csv_rows = _to_csv_rows(rows)
    summary_basic = summarize_rows_basic(rows, value_tol=value_tol, point_tol=point_tol)
    ranking_rows = build_operator_ranking_rows([row for row in rows if row.get("best_value") is not None])
    best_regions = describe_best_parameter_regions(rows, top_fraction=top_fraction_for_regions)

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

    values = [row["best_value"] for row in rows if row.get("best_value") is not None]
    points = [row["best_point"] for row in rows if row.get("best_point") is not None]

    hist_path = save_histogram_best_values(output_dir, values, filename="hist_single_function.png")
    box_path = save_boxplot_best_values(output_dir, values, filename="box_single_function.png")
    bar_operator_path = save_bar_operator_wins(output_dir, ranking_rows, filename="bar_operator_wins_single_function.png")
    scatter_pop = save_scatter_param_vs_error(output_dir, rows, "population", "scatter_population_vs_error_single.png")
    scatter_epochs = save_scatter_param_vs_error(output_dir, rows, "epochs", "scatter_epochs_vs_error_single.png")
    scatter_err_dist = save_error_vs_distance_scatter(output_dir, rows, filename="scatter_error_vs_distance_single.png")

    selection_ranking = save_group_quality_ranking(
        output_dir=output_dir,
        rows=rows,
        config_key="selection_method",
        title="Ranking jakości metod selekcji",
        filename="rank_selection_quality.png",
    )
    crossover_ranking = save_group_quality_ranking(
        output_dir=output_dir,
        rows=rows,
        config_key="crossover_method",
        title="Ranking jakości metod crossover",
        filename="rank_crossover_quality.png",
    )
    mutation_ranking = save_group_quality_ranking(
        output_dir=output_dir,
        rows=rows,
        config_key="mutation_method",
        title="Ranking jakości metod mutacji",
        filename="rank_mutation_quality.png",
    )
    inversion_ranking = save_group_quality_ranking(
        output_dir=output_dir,
        rows=rows,
        config_key="inversion_enabled",
        title="Czy inwersja pomaga?",
        filename="rank_inversion_quality.png",
        label_map={True: "inversion=True", False: "inversion=False"},
    )
    elitism_ranking = save_group_quality_ranking(
        output_dir=output_dir,
        rows=rows,
        config_key="elitism_enabled",
        title="Czy elitaryzm pomaga?",
        filename="rank_elitism_quality.png",
        label_map={True: "elitism=True", False: "elitism=False"},
    )

    median_density_heatmap = None
    if int(problem.default_n_vars) == 2:
        median_density_heatmap = save_median_density_heatmap(
            output_dir=output_dir,
            points=points,
            median_point=_row_to_point(summary_basic["median_row"]),
            global_minimum_points=problem.global_minimum_points,
            title="Heatmapa zagęszczenia punktów wokół obszaru mediany",
            filename="heatmap_median_density.png",
            bins_x=heatmap_bins,
            bins_y=heatmap_bins,
        )

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
        "best_parameter_regions": best_regions,
        "selection_quality_rows": selection_quality_rows,
        "crossover_quality_rows": crossover_quality_rows,
        "mutation_quality_rows": mutation_quality_rows,
        "inversion_quality_rows": inversion_quality_rows,
        "elitism_quality_rows": elitism_quality_rows,
        "plot_paths": {
            "histogram": hist_path,
            "boxplot": box_path,
            "bar_operator_wins": bar_operator_path,
            "scatter_population_vs_error": scatter_pop,
            "scatter_epochs_vs_error": scatter_epochs,
            "scatter_error_vs_distance": scatter_err_dist,
            "heatmap_median_density": median_density_heatmap,
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
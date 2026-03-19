from __future__ import annotations

from statistics import mean, median

from ga_optimizer.experiments.base_runner import print_experiment_progress, run_single_config
from ga_optimizer.experiments.metrics import success_counts
from ga_optimizer.experiments.plotting import save_line_parameter_sensitivity
from ga_optimizer.experiments.reporting import (
    build_sensitivity_report,
    make_experiment_output_dir,
    save_report_md,
    save_summary_csv,
    save_summary_json,
)
from ga_optimizer.experiments.search_spaces import apply_config_overrides, build_base_config_for_problem
from ga_optimizer.problems.function_catalog import get_problem_definition


def _set_parameter_on_config(config, parameter_name: str, parameter_value):
    if parameter_name in {"population", "epochs", "run_count", "precision_bits"}:
        setattr(config, parameter_name, parameter_value)
        return

    if parameter_name == "selection_tournament_k":
        config.selection_method = "tournament"
        config.method_params = {"selection_tournament_k": parameter_value}
        return

    if parameter_name == "crossover_two_point_p":
        config.crossover_method = "two_point"
        config.method_params = {**config.method_params, "crossover_two_point_p": parameter_value}
        return

    if parameter_name == "mutation_scramble_p":
        config.mutation_method = "scramble"
        config.method_params = {**config.method_params, "mutation_scramble_p": parameter_value}
        return

    raise ValueError(f"Nieobsługiwany parametr sensitivity: {parameter_name}")


def run_sensitivity_test(
    preset_name: str,
    preset: dict,
) -> dict:
    """
    Testuje wrażliwość jednej funkcji na pojedynczy parametr.
    Bazowa konfiguracja jest stała, zmienia się tylko badany parametr.
    """
    problem_name = preset["problem_name"]
    parameter_name = preset["sensitivity_parameter"]
    parameter_values = list(preset["parameter_values"][parameter_name])
    executions_per_value = int(preset["executions_per_value"])
    base_cfg_data = dict(preset["base_config"])
    seed = preset.get("seed", "")
    value_tol = float(preset["success_value_abs_tol"])
    point_tol = float(preset["success_point_distance_tol"])

    output_dir = make_experiment_output_dir("sensitivity_test", preset_name)
    problem = get_problem_definition(problem_name)

    total_steps = len(parameter_values) * executions_per_value

    print(f"[sensitivity] funkcja: {problem_name}")
    print(f"[sensitivity] parametr: {parameter_name}")
    print(f"[sensitivity] liczba wartości parametru: {len(parameter_values)}")
    print(f"[sensitivity] wykonań na wartość: {executions_per_value}")
    print(f"[sensitivity] łączny postęp eksperymentu: {total_steps} kroków")
    print(f"[sensitivity] katalog: {output_dir}")

    base_config = build_base_config_for_problem(
        problem_name=problem_name,
        population=base_cfg_data["population"],
        epochs=base_cfg_data["epochs"],
        run_count=base_cfg_data["run_count"],
        precision_bits=base_cfg_data["precision_bits"],
        seed=seed,
    )
    apply_config_overrides(
        base_config,
        {
            "selection_method": base_cfg_data["selection_method"],
            "crossover_method": base_cfg_data["crossover_method"],
            "mutation_method": base_cfg_data["mutation_method"],
            "inversion_enabled": base_cfg_data["inversion_enabled"],
            "elitism_enabled": base_cfg_data["elitism_enabled"],
        },
    )

    summary_rows = []
    all_rows = []

    current_step = 0

    for parameter_value in parameter_values:
        local_results = []
        print(f"\n[sensitivity] wartość {parameter_name}={parameter_value}")

        for repeat_index in range(executions_per_value):
            current_step += 1
            step_label = (
                f"{parameter_name}={parameter_value} | "
                f"powtórzenie {repeat_index + 1}/{executions_per_value}"
            )

            print_experiment_progress(
                "sensitivity",
                current_step,
                total_steps,
                step_label=step_label,
            )

            cfg = build_base_config_for_problem(
                problem_name=problem_name,
                population=base_config.population,
                epochs=base_config.epochs,
                run_count=base_config.run_count,
                precision_bits=base_config.precision_bits,
                seed=seed,
            )
            apply_config_overrides(
                cfg,
                {
                    "selection_method": base_config.selection_method,
                    "crossover_method": base_config.crossover_method,
                    "mutation_method": base_config.mutation_method,
                    "inversion_enabled": base_config.inversion_enabled,
                    "elitism_enabled": base_config.elitism_enabled,
                    "method_params": dict(base_cfg_data.get("method_params", {})),
                },
            )
            _set_parameter_on_config(cfg, parameter_name, parameter_value)

            row = run_single_config(
                cfg,
                progress_prefix="[sensitivity]",
                experiment_progress=(current_step, total_steps),
                step_label=step_label,
            )
            all_rows.append(row)
            if row.get("best_value") is not None:
                local_results.append(row)

        values = [row["best_value"] for row in local_results]
        abs_errors = [row["abs_value_error"] for row in local_results if row.get("abs_value_error") is not None]
        point_distances = [
            row["nearest_global_min_point_distance"]
            for row in local_results
            if row.get("nearest_global_min_point_distance") is not None
        ]
        success = success_counts(local_results, value_tol=value_tol, point_tol=point_tol)

        summary_rows.append(
            {
                "parameter_value": parameter_value,
                "mean_best_value": mean(values) if values else None,
                "median_best_value": median(values) if values else None,
                "best_value": min(values) if values else None,
                "mean_abs_error": mean(abs_errors) if abs_errors else None,
                "mean_point_distance": mean(point_distances) if point_distances else None,
                "value_success_rate": success["value_success_rate"],
                "point_success_rate": success["point_success_rate"],
            }
        )

    valid_rows = [row for row in summary_rows if row.get("mean_abs_error") is not None]
    best_parameter_row = min(valid_rows, key=lambda row: row["mean_abs_error"]) if valid_rows else None
    global_success = success_counts(
        [row for row in all_rows if row.get("best_value") is not None],
        value_tol=value_tol,
        point_tol=point_tol,
    )

    line_path = save_line_parameter_sensitivity(output_dir, summary_rows, parameter_name)

    summary = {
        "test_name": "sensitivity_test",
        "preset_name": preset_name,
        "problem_name": problem.key,
        "problem_display_name": problem.display_name,
        "global_minimum_value": float(problem.global_minimum_value),
        "global_minimum_points": problem.global_minimum_points,
        "sensitivity_parameter": parameter_name,
        "executions_per_value": executions_per_value,
        "rows": summary_rows,
        "best_parameter_row": best_parameter_row,
        "success_by_value": global_success,
        "plot_paths": {
            "line_sensitivity": line_path,
        },
        "output_dir": str(output_dir),
    }

    report_text = build_sensitivity_report(summary)
    save_summary_json(output_dir, summary)
    save_summary_csv(output_dir, summary_rows)
    save_report_md(output_dir, report_text)

    return {
        "status": "ok",
        "test_name": "sensitivity_test",
        "output_dir": str(output_dir),
        "summary": summary,
    }
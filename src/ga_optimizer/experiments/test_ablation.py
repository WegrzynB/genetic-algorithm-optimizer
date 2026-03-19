from __future__ import annotations

from statistics import mean, median

from ga_optimizer.experiments.base_runner import print_experiment_progress, run_single_config
from ga_optimizer.experiments.metrics import success_counts
from ga_optimizer.experiments.plotting import save_bar_variant_means
from ga_optimizer.experiments.reporting import (
    build_ablation_report,
    make_experiment_output_dir,
    save_report_md,
    save_summary_csv,
    save_summary_json,
)
from ga_optimizer.experiments.search_spaces import apply_config_overrides, build_base_config_for_problem
from ga_optimizer.problems.function_catalog import get_problem_definition


def _build_variant_config(base_config, base_cfg_data: dict, variant_name: str):
    cfg = build_base_config_for_problem(
        problem_name=base_config.problem_name,
        population=base_config.population,
        epochs=base_config.epochs,
        run_count=base_config.run_count,
        precision_bits=base_config.precision_bits,
        seed=base_config.seed,
    )

    apply_config_overrides(
        cfg,
        {
            "selection_method": base_cfg_data["selection_method"],
            "crossover_method": base_cfg_data["crossover_method"],
            "mutation_method": base_cfg_data["mutation_method"],
            "inversion_enabled": base_cfg_data["inversion_enabled"],
            "elitism_enabled": base_cfg_data["elitism_enabled"],
            "method_params": dict(base_cfg_data.get("method_params", {})),
        },
    )

    if variant_name == "base":
        return cfg

    if variant_name == "no_elitism":
        cfg.elitism_enabled = False
        return cfg

    if variant_name == "no_inversion":
        cfg.inversion_enabled = False
        return cfg

    if variant_name == "selection_roulette":
        cfg.selection_method = "roulette"
        cfg.method_params = {"selection_roulette_eps": 1e-9}
        return cfg

    if variant_name == "selection_best":
        cfg.selection_method = "best"
        cfg.method_params = {"selection_best_k": 10}
        return cfg

    if variant_name == "crossover_uniform":
        cfg.crossover_method = "uniform"
        cfg.method_params = {**cfg.method_params, "crossover_uniform_p": 0.7}
        return cfg

    if variant_name == "crossover_one_point":
        cfg.crossover_method = "one_point"
        cfg.method_params = {**cfg.method_params, "crossover_one_point_p": 0.7}
        return cfg

    if variant_name == "mutation_bit_flip":
        cfg.mutation_method = "bit_flip"
        cfg.method_params = {**cfg.method_params, "mutation_bit_flip_p": 0.03}
        return cfg

    if variant_name == "mutation_reset":
        cfg.mutation_method = "reset"
        cfg.method_params = {**cfg.method_params, "mutation_reset_p": 0.03}
        return cfg

    raise ValueError(f"Nieobsługiwany wariant ablation: {variant_name}")


def run_ablation_test(
    preset_name: str,
    preset: dict,
) -> dict:
    """
    Porównuje bazową konfigurację z wariantami,
    w których wyłączany albo podmieniany jest pojedynczy element.
    """
    problem_name = preset["problem_name"]
    executions_per_variant = int(preset["executions_per_variant"])
    base_cfg_data = dict(preset["base_config"])
    variant_names = list(preset["variants"])
    seed = preset.get("seed", "")
    value_tol = float(preset["success_value_abs_tol"])
    point_tol = float(preset["success_point_distance_tol"])

    output_dir = make_experiment_output_dir("ablation_test", preset_name)
    problem = get_problem_definition(problem_name)

    total_steps = len(variant_names) * executions_per_variant

    print(f"[ablation] funkcja: {problem_name}")
    print(f"[ablation] wariantów: {len(variant_names)}")
    print(f"[ablation] wykonań na wariant: {executions_per_variant}")
    print(f"[ablation] łączny postęp eksperymentu: {total_steps} kroków")
    print(f"[ablation] katalog: {output_dir}")

    base_config = build_base_config_for_problem(
        problem_name=problem_name,
        population=base_cfg_data["population"],
        epochs=base_cfg_data["epochs"],
        run_count=base_cfg_data["run_count"],
        precision_bits=base_cfg_data["precision_bits"],
        seed=seed,
    )

    rows = []
    current_step = 0

    for variant_name in variant_names:
        print(f"\n[ablation] wariant: {variant_name}")
        local_results = []

        for repeat_index in range(executions_per_variant):
            current_step += 1
            step_label = f"wariant={variant_name} | powtórzenie {repeat_index + 1}/{executions_per_variant}"

            print_experiment_progress(
                "ablation",
                current_step,
                total_steps,
                step_label=step_label,
            )

            cfg = _build_variant_config(base_config, base_cfg_data, variant_name)
            row = run_single_config(
                cfg,
                progress_prefix="[ablation]",
                experiment_progress=(current_step, total_steps),
                step_label=step_label,
            )
            if row.get("best_value") is not None:
                local_results.append(row)

        values = [float(r["best_value"]) for r in local_results if r.get("best_value") is not None]
        abs_errors = [float(r["abs_value_error"]) for r in local_results if r.get("abs_value_error") is not None]
        point_distances = [
            float(r["nearest_global_min_point_distance"])
            for r in local_results
            if r.get("nearest_global_min_point_distance") is not None
        ]
        success = success_counts(local_results, value_tol=value_tol, point_tol=point_tol)

        rows.append(
            {
                "variant_name": variant_name,
                "mean_best_value": mean(values) if values else None,
                "median_best_value": median(values) if values else None,
                "best_value": min(values) if values else None,
                "mean_abs_error": mean(abs_errors) if abs_errors else None,
                "mean_point_distance": mean(point_distances) if point_distances else None,
                "value_success_rate": success["value_success_rate"],
                "point_success_rate": success["point_success_rate"],
                "delta_vs_base": None,
            }
        )

    base_row = next((row for row in rows if row["variant_name"] == "base"), None)
    base_mean = base_row["mean_best_value"] if base_row else None

    for row in rows:
        if base_mean is not None and row["mean_best_value"] is not None:
            row["delta_vs_base"] = row["mean_best_value"] - base_mean
        else:
            row["delta_vs_base"] = None

    valid_rows = [row for row in rows if row.get("mean_best_value") is not None]
    best_variant = min(valid_rows, key=lambda r: r["mean_best_value"]) if valid_rows else None
    worst_variant = max(valid_rows, key=lambda r: r["mean_best_value"]) if valid_rows else None

    bar_path = save_bar_variant_means(output_dir, rows)

    summary = {
        "test_name": "ablation_test",
        "preset_name": preset_name,
        "problem_name": problem.key,
        "problem_display_name": problem.display_name,
        "global_minimum_value": float(problem.global_minimum_value),
        "global_minimum_points": problem.global_minimum_points,
        "executions_per_variant": executions_per_variant,
        "rows": rows,
        "best_variant": best_variant,
        "worst_variant": worst_variant,
        "plot_paths": {
            "bar_variant_means": bar_path,
        },
        "output_dir": str(output_dir),
    }

    report_text = build_ablation_report(summary)
    save_summary_json(output_dir, summary)
    save_summary_csv(output_dir, rows)
    save_report_md(output_dir, report_text)

    return {
        "status": "ok",
        "test_name": "ablation_test",
        "output_dir": str(output_dir),
        "summary": summary,
    }
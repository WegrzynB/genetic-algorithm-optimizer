# src/ga_optimizer/visualization/show_charts.py

from typing import Any
import matplotlib.pyplot as plt

from ga_optimizer.visualization.convergence_plots import plot_convergence
from ga_optimizer.visualization.distribution import plot_fitness_distribution
from ga_optimizer.visualization.function_landscape_plots import (
    plot_function_1d_with_trajectory,
    plot_function_2d_contour_with_trajectory,
    plot_function_2d_surface_with_trajectory,
)
from ga_optimizer.visualization.plot_styles import apply_custom_style


def get_all_figures(
    engine_result: dict[str, Any],
    input_dict: dict[str, Any],
) -> dict[str, plt.Figure]:
    figures: dict[str, plt.Figure] = {}

    if not engine_result.get("runs"):
        print("Brak danych z uruchomień algorytmu do wygenerowania wykresów.")
        return figures

    apply_custom_style()

    first_run_history = engine_result["runs"][0]["history"]
    problem_name = input_dict["problem_name"]
    range_start = input_dict["range_start"]
    range_end = input_dict["range_end"]
    n_vars = input_dict["n_vars"]

    figures["convergence"] = plot_convergence(first_run_history, problem_name)
    figures["distribution"] = plot_fitness_distribution(first_run_history, problem_name)

    if n_vars == 1:
        figures["function_1d"] = plot_function_1d_with_trajectory(
            first_run_history,
            problem_name,
            range_start,
            range_end,
        )
    elif n_vars == 2:
        figures["function_2d_contour"] = plot_function_2d_contour_with_trajectory(
            first_run_history,
            problem_name,
            range_start,
            range_end,
        )
        figures["function_2d_surface"] = plot_function_2d_surface_with_trajectory(
            first_run_history,
            problem_name,
            range_start,
            range_end,
        )

    return figures
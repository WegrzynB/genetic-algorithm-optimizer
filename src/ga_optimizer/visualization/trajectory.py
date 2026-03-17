# src/ga_optimizer/visualization/trajectory.py

import matplotlib.pyplot as plt
import numpy as np
import statistics
from typing import Any

from ga_optimizer.problems.function_catalog import get_problem_definition


def _collect_median_path(history: list[dict[str, Any]]) -> np.ndarray:
    path = []

    for h in history:
        decoded_pop = h.get("decoded_population", [])
        if not decoded_pop:
            continue

        n_vars = len(decoded_pop[0])
        medians = [statistics.median(ind[var_idx] for ind in decoded_pop) for var_idx in range(n_vars)]
        path.append(medians)

    return np.asarray(path, dtype=float)


def plot_trajectory_2d(
    history: list[dict[str, Any]],
    problem_name: str,
    range_start: float,
    range_end: float,
) -> plt.Figure:
    problem_def = get_problem_definition(problem_name)

    grid_res = 100
    x_vals = np.linspace(range_start, range_end, grid_res)
    y_vals = np.linspace(range_start, range_end, grid_res)
    X, Y = np.meshgrid(x_vals, y_vals)
    Z = np.zeros_like(X)

    for i in range(grid_res):
        for j in range(grid_res):
            Z[i, j] = problem_def.formula([X[i, j], Y[i, j]])

    median_path = _collect_median_path(history)

    fig, ax = plt.subplots(figsize=(9, 7))
    contour = ax.contourf(X, Y, Z, levels=50, cmap="viridis", alpha=0.8)
    fig.colorbar(contour, ax=ax, label="Wartość funkcji celu")

    if len(median_path) > 0:
        ax.plot(
            median_path[:, 0],
            median_path[:, 1],
            marker="o",
            linestyle="-",
            linewidth=2,
            markersize=4,
            color="red",
            label="Ścieżka mediany",
        )
        ax.scatter(
            median_path[0, 0],
            median_path[0, 1],
            s=100,
            edgecolor="black",
            zorder=5,
            label="Start",
        )
        ax.scatter(
            median_path[-1, 0],
            median_path[-1, 1],
            marker="*",
            s=200,
            edgecolor="black",
            zorder=5,
            label="Koniec",
        )

    ax.set_title(f"Trajektoria populacji 2D - {problem_name}", fontsize=14)
    ax.set_xlabel("x1", fontsize=12)
    ax.set_ylabel("x2", fontsize=12)
    ax.legend()
    fig.tight_layout()
    return fig


def plot_trajectory_3d(
    history: list[dict[str, Any]],
    problem_name: str,
) -> plt.Figure:
    median_path = _collect_median_path(history)

    fig = plt.figure(figsize=(10, 7))
    ax = fig.add_subplot(111, projection="3d")

    if len(median_path) > 0:
        ax.plot(
            median_path[:, 0],
            median_path[:, 1],
            median_path[:, 2],
            marker="o",
            linestyle="-",
            linewidth=2,
            markersize=4,
            label="Ścieżka mediany",
        )
        ax.scatter(
            median_path[0, 0],
            median_path[0, 1],
            median_path[0, 2],
            s=100,
            edgecolor="black",
            label="Start",
        )
        ax.scatter(
            median_path[-1, 0],
            median_path[-1, 1],
            median_path[-1, 2],
            marker="*",
            s=220,
            edgecolor="black",
            label="Koniec",
        )

    ax.set_title(f"Trajektoria populacji 3D - {problem_name}", fontsize=14)
    ax.set_xlabel("x1", fontsize=12)
    ax.set_ylabel("x2", fontsize=12)
    ax.set_zlabel("x3", fontsize=12)
    ax.legend()
    fig.tight_layout()
    return fig
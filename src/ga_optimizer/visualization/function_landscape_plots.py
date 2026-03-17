# function_landscape_plots.py

import matplotlib.pyplot as plt
import numpy as np
import statistics
from typing import Any

from ga_optimizer.problems.function_catalog import get_problem_definition


def _median_path(history: list[dict[str, Any]]) -> np.ndarray:
    path = []

    for h in history:
        decoded_pop = h.get("decoded_population", [])
        if not decoded_pop:
            continue

        n_vars = len(decoded_pop[0])
        medians = [
            statistics.median(ind[var_idx] for ind in decoded_pop)
            for var_idx in range(n_vars)
        ]
        path.append(medians)

    if not path:
        return np.empty((0, 0), dtype=float)

    return np.asarray(path, dtype=float)


def plot_function_1d_with_trajectory(
    history: list[dict[str, Any]],
    problem_name: str,
    range_start: float,
    range_end: float,
) -> plt.Figure:
    problem_def = get_problem_definition(problem_name)

    x = np.linspace(range_start, range_end, 600)
    z = np.array([problem_def.formula([x_i]) for x_i in x])

    path = _median_path(history)

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(x, z, linewidth=2, label="f(x)")

    if len(path) > 0:
        path_x = path[:, 0]
        path_z = np.array([problem_def.formula([x_i]) for x_i in path_x])

        ax.plot(
            path_x,
            path_z,
            marker="o",
            linestyle="-",
            linewidth=2,
            markersize=4,
            label="Trajektoria mediany populacji",
        )
        ax.scatter(
            path_x[0],
            path_z[0],
            s=90,
            edgecolor="black",
            zorder=5,
            label="Start",
        )
        ax.scatter(
            path_x[-1],
            path_z[-1],
            marker="*",
            s=180,
            edgecolor="black",
            zorder=6,
            label="Koniec",
        )

    ax.set_title(f"Wykres funkcji 1D z trajektorią - {problem_name}", fontsize=14)
    ax.set_xlabel("x", fontsize=12)
    ax.set_ylabel("f(x)", fontsize=12)
    ax.legend()
    fig.tight_layout()
    return fig


def plot_function_2d_contour_with_trajectory(
    history: list[dict[str, Any]],
    problem_name: str,
    range_start: float,
    range_end: float,
) -> plt.Figure:
    problem_def = get_problem_definition(problem_name)

    grid_res = 140
    x_vals = np.linspace(range_start, range_end, grid_res)
    y_vals = np.linspace(range_start, range_end, grid_res)
    X, Y = np.meshgrid(x_vals, y_vals)
    Z = np.zeros_like(X)

    for i in range(grid_res):
        for j in range(grid_res):
            Z[i, j] = problem_def.formula([X[i, j], Y[i, j]])

    path = _median_path(history)

    fig, ax = plt.subplots(figsize=(10, 7))
    contour = ax.contourf(X, Y, Z, levels=60, cmap="viridis")
    ax.contour(X, Y, Z, levels=20, colors="black", linewidths=0.4, alpha=0.35)
    fig.colorbar(contour, ax=ax, label="f(x, y)")

    if len(path) > 0:
        path_x = path[:, 0]
        path_y = path[:, 1]

        ax.plot(
            path_x,
            path_y,
            marker="o",
            linestyle="-",
            linewidth=2,
            markersize=4,
            color="red",
            label="Trajektoria mediany populacji",
        )
        ax.scatter(
            path_x[0],
            path_y[0],
            s=90,
            edgecolor="black",
            zorder=5,
            label="Start",
        )
        ax.scatter(
            path_x[-1],
            path_y[-1],
            marker="*",
            s=180,
            edgecolor="black",
            zorder=6,
            label="Koniec",
        )

    ax.set_title(f"Rzut 2D funkcji z trajektorią - {problem_name}", fontsize=14)
    ax.set_xlabel("x", fontsize=12)
    ax.set_ylabel("y", fontsize=12)
    ax.legend()
    fig.tight_layout()
    return fig


def plot_function_2d_surface_with_trajectory(
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

    path = _median_path(history)

    fig = plt.figure(figsize=(11, 8))
    ax = fig.add_subplot(111, projection="3d")

    surface = ax.plot_surface(
        X,
        Y,
        Z,
        cmap="viridis",
        linewidth=0,
        antialiased=True,
        alpha=0.5,
    )
    fig.colorbar(surface, ax=ax, shrink=0.65, pad=0.08, label="f(x, y)")

    if len(path) > 0:
        path_x = path[:, 0]
        path_y = path[:, 1]
        path_z = np.array([problem_def.formula([x_i, y_i]) for x_i, y_i in zip(path_x, path_y)])

        ax.plot(
            path_x,
            path_y,
            path_z,
            marker="o",
            linewidth=2.2,
            markersize=4,
            color="red",
            label="Trajektoria mediany populacji",
        )
        ax.scatter(
            path_x[0],
            path_y[0],
            path_z[0],
            s=90,
            edgecolor="black",
            label="Start",
        )
        ax.scatter(
            path_x[-1],
            path_y[-1],
            path_z[-1],
            marker="*",
            s=180,
            edgecolor="black",
            label="Koniec",
        )

    ax.set_title(f"Powierzchnia 3D funkcji z trajektorią - {problem_name}", fontsize=14)
    ax.set_xlabel("x", fontsize=12)
    ax.set_ylabel("y", fontsize=12)
    ax.set_zlabel("f(x, y)", fontsize=12)
    ax.legend()
    fig.tight_layout()
    return fig
# src/ga_optimizer/visualization/trajectory.py

import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import statistics
from typing import Any
from ga_optimizer.problems.function_catalog import get_problem_definition

def plot_trajectory(history: list[dict[str, Any]], problem_name: str, range_start: float, range_end: float) -> plt.Figure:
    problem_def = get_problem_definition(problem_name)
    
    grid_res = 100
    x_vals = np.linspace(range_start, range_end, grid_res)
    y_vals = np.linspace(range_start, range_end, grid_res)
    X, Y = np.meshgrid(x_vals, y_vals)
    Z = np.zeros_like(X)
    
    for i in range(grid_res):
        for j in range(grid_res):
            Z[i, j] = problem_def.formula([X[i, j], Y[i, j]])

    fig, ax = plt.subplots(figsize=(9, 7))
    contour = ax.contourf(X, Y, Z, levels=50, cmap="viridis", alpha=0.8)
    fig.colorbar(contour, ax=ax, label="Wartość funkcji celu")

    median_x1, median_x2 = [], []
    for h in history:
        decoded_pop = h["decoded_population"]
        median_x1.append(statistics.median([ind[0] for ind in decoded_pop]))
        median_x2.append(statistics.median([ind[1] for ind in decoded_pop]))

    ax.plot(median_x1, median_x2, marker='o', color='red', linestyle='-', linewidth=2, markersize=4, label='Ścieżka Mediany')
    ax.scatter(median_x1[0], median_x2[0], color='white', s=100, edgecolor='black', zorder=5, label='Start')
    ax.scatter(median_x1[-1], median_x2[-1], color='cyan', marker='*', s=200, edgecolor='black', zorder=5, label='Koniec')

    ax.set_title(f"Trajektoria Populacji - {problem_name}", fontsize=14)
    ax.set_xlabel("Zmienna x1", fontsize=12)
    ax.set_ylabel("Zmienna x2", fontsize=12)
    ax.legend()
    fig.tight_layout()
    
    return fig
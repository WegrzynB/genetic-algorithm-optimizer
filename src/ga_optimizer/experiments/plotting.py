from __future__ import annotations

from pathlib import Path
from typing import Any

import matplotlib.pyplot as plt


def save_histogram_best_values(output_dir: Path, values: list[float], filename: str = "hist_best_values.png") -> str | None:
    if not values:
        return None

    path = output_dir / "plots" / filename
    plt.figure(figsize=(8, 5))
    plt.hist(values, bins=min(12, max(4, len(values))))
    plt.xlabel("Najlepsza wartość funkcji celu")
    plt.ylabel("Liczność")
    plt.title("Histogram najlepszych wartości")
    plt.tight_layout()
    plt.savefig(path, dpi=150)
    plt.close()
    return str(path)


def save_heatmap_best_points(
    output_dir: Path,
    points: list[list[float]],
    global_minimum_points: list[list[float]] | None,
    filename: str = "heatmap_best_points.png",
) -> str | None:
    if not points:
        return None
    if any(len(point) < 2 for point in points):
        return None

    xs = [float(point[0]) for point in points]
    ys = [float(point[1]) for point in points]

    path = output_dir / "plots" / filename
    plt.figure(figsize=(7, 6))
    plt.hist2d(xs, ys, bins=20)
    plt.xlabel("x1")
    plt.ylabel("x2")
    plt.title("Heatmapa najlepszych punktów")

    if global_minimum_points:
        gx = [float(point[0]) for point in global_minimum_points if len(point) >= 2]
        gy = [float(point[1]) for point in global_minimum_points if len(point) >= 2]
        if gx and gy:
            plt.scatter(gx, gy, marker="x", s=120, label="Minimum globalne")
            plt.legend()

    plt.tight_layout()
    plt.savefig(path, dpi=150)
    plt.close()
    return str(path)


def save_boxplot_best_values(output_dir: Path, values: list[float], filename: str = "boxplot_best_values.png") -> str | None:
    if not values:
        return None

    path = output_dir / "plots" / filename
    plt.figure(figsize=(6, 5))
    plt.boxplot(values)
    plt.ylabel("Najlepsza wartość funkcji celu")
    plt.title("Rozkład najlepszych wartości")
    plt.tight_layout()
    plt.savefig(path, dpi=150)
    plt.close()
    return str(path)


def save_bar_errors_by_function(output_dir: Path, rows: list[dict[str, Any]], filename: str = "bar_errors_by_function.png") -> str | None:
    if not rows:
        return None

    path = output_dir / "plots" / filename
    labels = [row["problem_name"] for row in rows]
    values = [float(row["error_to_global_min"]) for row in rows]

    plt.figure(figsize=(12, 5))
    plt.bar(labels, values)
    plt.xticks(rotation=45, ha="right")
    plt.ylabel("Błąd do minimum globalnego")
    plt.title("Najlepszy błąd per funkcja")
    plt.tight_layout()
    plt.savefig(path, dpi=150)
    plt.close()
    return str(path)


def save_bar_operator_wins(output_dir: Path, ranking_rows: list[dict[str, Any]], filename: str = "bar_operator_wins.png") -> str | None:
    if not ranking_rows:
        return None

    labels = [f"{row['group']}:{row['operator']}" for row in ranking_rows]
    values = [int(row["wins"]) for row in ranking_rows]

    path = output_dir / "plots" / filename
    plt.figure(figsize=(12, 6))
    plt.bar(labels, values)
    plt.xticks(rotation=60, ha="right")
    plt.ylabel("Liczba zwycięstw")
    plt.title("Ranking operatorów")
    plt.tight_layout()
    plt.savefig(path, dpi=150)
    plt.close()
    return str(path)


def save_line_parameter_sensitivity(output_dir: Path, rows: list[dict[str, Any]], parameter_name: str, filename: str = "line_sensitivity.png") -> str | None:
    if not rows:
        return None

    xs = [row["parameter_value"] for row in rows]
    ys = [row["mean_best_value"] for row in rows]

    path = output_dir / "plots" / filename
    plt.figure(figsize=(8, 5))
    plt.plot(xs, ys, marker="o")
    plt.xlabel(parameter_name)
    plt.ylabel("Średnia najlepsza wartość")
    plt.title(f"Wrażliwość na parametr: {parameter_name}")
    plt.tight_layout()
    plt.savefig(path, dpi=150)
    plt.close()
    return str(path)


def save_bar_variant_means(output_dir: Path, rows: list[dict[str, Any]], filename: str = "bar_variant_means.png") -> str | None:
    if not rows:
        return None

    labels = [row["variant_name"] for row in rows]
    values = [row["mean_best_value"] for row in rows]

    path = output_dir / "plots" / filename
    plt.figure(figsize=(12, 5))
    plt.bar(labels, values)
    plt.xticks(rotation=45, ha="right")
    plt.ylabel("Średnia najlepsza wartość")
    plt.title("Porównanie wariantów ablation")
    plt.tight_layout()
    plt.savefig(path, dpi=150)
    plt.close()
    return str(path)
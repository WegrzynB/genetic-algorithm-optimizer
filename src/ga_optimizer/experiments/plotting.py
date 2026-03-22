# plotting.py
from __future__ import annotations

from pathlib import Path
from typing import Any

import matplotlib.pyplot as plt
import numpy as np


def _save(path: Path) -> str:
    path.parent.mkdir(parents=True, exist_ok=True)
    plt.tight_layout()
    plt.savefig(path, dpi=180, bbox_inches="tight")
    plt.close()
    return str(path)


def _apply_common_style(ax, title: str, xlabel: str = "", ylabel: str = "") -> None:
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.grid(True, alpha=0.18)


def save_histogram_best_values(
    output_dir: Path,
    values: list[float],
    filename: str = "hist_best_values.png",
) -> str | None:
    return save_histogram_metric_values(
        output_dir=output_dir,
        values=values,
        title="Histogram najlepszych wartości",
        xlabel="Najlepsza wartość funkcji celu",
        filename=filename,
    )


def save_boxplot_best_values(
    output_dir: Path,
    values: list[float],
    filename: str = "boxplot_best_values.png",
) -> str | None:
    return save_boxplot_metric_values(
        output_dir=output_dir,
        values=values,
        title="Rozkład najlepszych wartości",
        ylabel="Najlepsza wartość funkcji celu",
        filename=filename,
    )


def save_histogram_metric_values(
    output_dir: Path,
    values: list[float],
    title: str,
    xlabel: str,
    filename: str,
) -> str | None:
    if not values:
        return None

    arr = np.asarray(values, dtype=float)
    vmin = float(np.min(arr))
    vmax = float(np.max(arr))

    if np.isclose(vmin, vmax):
        pad = max(1e-6, abs(vmin) * 0.02, 0.5)
        bins = np.linspace(vmin - pad, vmax + pad, 8)
    else:
        bin_count = max(6, min(14, len(arr) + 2))
        bins = np.linspace(vmin, vmax, bin_count)

    path = output_dir / "plots" / filename
    fig, ax = plt.subplots(figsize=(8.8, 5.4))
    ax.hist(arr, bins=bins, edgecolor="none", linewidth=0.0, alpha=0.85, color='orange')
    rug_y = np.full_like(arr, 0.02, dtype=float)
    ax.scatter(arr, rug_y, marker="|", s=120)
    _apply_common_style(ax, title, xlabel=xlabel, ylabel="Liczność")
    return _save(path)


def save_boxplot_metric_values(
    output_dir: Path,
    values: list[float],
    title: str,
    ylabel: str,
    filename: str,
) -> str | None:
    if not values:
        return None

    arr = np.asarray(values, dtype=float)
    path = output_dir / "plots" / filename
    fig, ax = plt.subplots(figsize=(6.5, 5.2))
    ax.boxplot(arr, vert=True, patch_artist=False, widths=0.35)
    jitter_x = 1.0 + np.random.uniform(-0.03, 0.03, size=len(arr))
    ax.scatter(jitter_x, arr, alpha=0.6, s=25)
    _apply_common_style(ax, title, xlabel="Próba", ylabel=ylabel)
    ax.set_xticks([1])
    ax.set_xticklabels(["wyniki"])
    return _save(path)


def save_bar_errors_by_function(
    output_dir: Path,
    rows: list[dict[str, Any]],
    filename: str = "bar_errors_by_function.png",
) -> str | None:
    if not rows:
        return None

    labels = [row["problem_name"] for row in rows]
    values = [float(row["error_to_global_min"]) for row in rows]
    order = np.argsort(values)

    labels = [labels[i] for i in order]
    values = [values[i] for i in order]

    path = output_dir / "plots" / filename
    fig, ax = plt.subplots(figsize=(11.5, max(4.5, len(labels) * 0.4)))
    y = np.arange(len(labels))
    bars = ax.barh(y, values, alpha=0.85)
    ax.set_yticks(y)
    ax.set_yticklabels(labels)

    for rect, val in zip(bars, values):
        ax.text(rect.get_width(), rect.get_y() + rect.get_height() / 2, f"  {val:.4f}", va="center")

    _apply_common_style(
        ax,
        "Błąd najlepszego wyniku per funkcja",
        xlabel="Odległość od minimum globalnego",
        ylabel="Funkcja",
    )
    return _save(path)


def save_bar_operator_wins(
    output_dir: Path,
    ranking_rows: list[dict[str, Any]],
    filename: str = "bar_operator_wins.png",
) -> str | None:
    if not ranking_rows:
        return None

    labels = [f"{row['group']}:{row['operator']}" for row in ranking_rows]
    values = [int(row["wins"]) for row in ranking_rows]

    order = np.argsort(values)
    labels = [labels[i] for i in order]
    values = [values[i] for i in order]

    path = output_dir / "plots" / filename
    fig, ax = plt.subplots(figsize=(12, max(5, len(labels) * 0.38)))
    y = np.arange(len(labels))
    bars = ax.barh(y, values, alpha=0.85)
    ax.set_yticks(y)
    ax.set_yticklabels(labels)

    for rect, val in zip(bars, values):
        ax.text(rect.get_width(), rect.get_y() + rect.get_height() / 2, f"  {val}", va="center")

    _apply_common_style(
        ax,
        "Ranking operatorów",
        xlabel="Liczba wystąpień",
        ylabel="Operator",
    )
    return _save(path)


def save_line_parameter_sensitivity(
    output_dir: Path,
    rows: list[dict[str, Any]],
    parameter_name: str,
    filename: str = "line_sensitivity.png",
) -> str | None:
    if not rows:
        return None

    xs = [row["parameter_value"] for row in rows]
    ys_mean = [row["mean_best_value"] for row in rows]
    ys_median = [row["median_best_value"] for row in rows]
    ys_best = [row["best_value"] for row in rows]

    path = output_dir / "plots" / filename
    fig, ax = plt.subplots(figsize=(8.5, 5.2))
    ax.plot(xs, ys_mean, marker="o", label="mean")
    ax.plot(xs, ys_median, marker="s", label="median")
    ax.plot(xs, ys_best, marker="^", label="best")

    _apply_common_style(
        ax,
        f"Wrażliwość na parametr: {parameter_name}",
        xlabel=parameter_name,
        ylabel="Wartość funkcji celu",
    )
    ax.legend()
    return _save(path)


def save_bar_variant_means(
    output_dir: Path,
    rows: list[dict[str, Any]],
    filename: str = "bar_variant_means.png",
) -> str | None:
    if not rows:
        return None

    labels = [row["variant_name"] for row in rows]
    values = [row["mean_best_value"] for row in rows]

    order = np.argsort(values)
    labels = [labels[i] for i in order]
    values = [values[i] for i in order]

    path = output_dir / "plots" / filename
    fig, ax = plt.subplots(figsize=(10.5, max(4.8, len(labels) * 0.38)))
    y = np.arange(len(labels))
    bars = ax.barh(y, values, alpha=0.85)
    ax.set_yticks(y)
    ax.set_yticklabels(labels)

    for rect, val in zip(bars, values):
        ax.text(rect.get_width(), rect.get_y() + rect.get_height() / 2, f"  {val:.4f}", va="center")

    _apply_common_style(
        ax,
        "Porównanie wariantów",
        xlabel="Średnia najlepsza wartość",
        ylabel="Wariant",
    )
    return _save(path)


def save_scatter_param_vs_error(
    output_dir: Path,
    rows: list[dict[str, Any]],
    x_key: str,
    filename: str,
    value_key: str = "nearest_global_min_point_distance",
    title: str | None = None,
    ylabel: str | None = None,
) -> str | None:
    valid = [r for r in rows if r.get(value_key) is not None]
    if not valid:
        return None

    xs = np.asarray([r["config"][x_key] for r in valid], dtype=float)
    ys = np.asarray([r[value_key] for r in valid], dtype=float)

    path = output_dir / "plots" / filename
    fig, ax = plt.subplots(figsize=(7.5, 5.2))
    ax.scatter(xs, ys, alpha=0.45, s=45)

    unique_x = sorted({float(x) for x in xs})
    mean_xs = []
    mean_ys = []
    for x in unique_x:
        group = ys[np.isclose(xs, x)]
        if group.size > 0:
            mean_xs.append(x)
            mean_ys.append(float(np.mean(group)))

    if len(mean_xs) >= 1:
        ax.plot(mean_xs, mean_ys, marker="o", linewidth=1.8, label="średnia dla x")
        ax.legend()

    _apply_common_style(
        ax,
        title or f"{x_key} vs odległość od minimum",
        xlabel=x_key,
        ylabel=ylabel or "Odległość od minimum globalnego",
    )
    return _save(path)


def save_operator_function_heatmap(
    output_dir: Path,
    rows: list[dict[str, Any]],
    operator_key: str,
    filename: str,
) -> str | None:
    if not rows:
        return None

    problems = sorted({row["problem_name"] for row in rows})
    operators = sorted({row[operator_key] for row in rows})
    if not problems or not operators:
        return None

    matrix = np.full((len(operators), len(problems)), np.nan)

    for oi, op in enumerate(operators):
        for pi, pr in enumerate(problems):
            vals = [
                float(row["nearest_global_min_point_distance"])
                for row in rows
                if row["problem_name"] == pr and row[operator_key] == op and row.get("nearest_global_min_point_distance") is not None
            ]
            if vals:
                matrix[oi, pi] = float(np.median(vals))

    path = output_dir / "plots" / filename
    fig, ax = plt.subplots(figsize=(max(8, len(problems) * 0.8), max(4.5, len(operators) * 0.45)))
    im = ax.imshow(matrix, aspect="auto")

    ax.set_xticks(range(len(problems)))
    ax.set_xticklabels(problems, rotation=45, ha="right")
    ax.set_yticks(range(len(operators)))
    ax.set_yticklabels(operators)

    for i in range(len(operators)):
        for j in range(len(problems)):
            if not np.isnan(matrix[i, j]):
                ax.text(j, i, f"{matrix[i, j]:.2f}", ha="center", va="center", fontsize=8)

    _apply_common_style(
        ax,
        f"Heatmapa jakości: {operator_key}",
        xlabel="Funkcja",
        ylabel="Operator",
    )
    fig.colorbar(im, ax=ax, label="Mediana odległości")
    return _save(path)


def save_quantile_value_bar(
    output_dir: Path,
    summary: dict[str, Any],
    filename: str = "quantile_values_bar.png",
) -> str | None:
    labels = ["best", "q1", "median", "mean", "q3", "worst"]
    values = [
        summary.get("best_value"),
        summary.get("q1_best_value"),
        summary.get("median_best_value"),
        summary.get("mean_best_value"),
        summary.get("q3_best_value"),
        summary.get("worst_best_value"),
    ]
    if all(v is None for v in values):
        return None

    path = output_dir / "plots" / filename
    fig, ax = plt.subplots(figsize=(8, 5.2))
    bars = ax.bar(labels, values, alpha=0.85)

    for rect, val in zip(bars, values):
        if val is not None:
            ax.text(rect.get_x() + rect.get_width() / 2, val, f"{val:.2f}", ha="center", va="bottom")

    _apply_common_style(
        ax,
        "Podsumowanie kwantylowe wyników",
        xlabel="Statystyka",
        ylabel="Wartość funkcji celu",
    )
    return _save(path)


def save_error_vs_distance_scatter(
    output_dir: Path,
    rows: list[dict[str, Any]],
    filename: str = "error_vs_distance.png",
) -> str | None:
    valid = [
        r for r in rows
        if r.get("abs_value_error") is not None and r.get("nearest_global_min_point_distance") is not None
    ]
    if not valid:
        return None

    x = np.asarray([r["abs_value_error"] for r in valid], dtype=float)
    y = np.asarray([r["nearest_global_min_point_distance"] for r in valid], dtype=float)

    path = output_dir / "plots" / filename
    fig, ax = plt.subplots(figsize=(7.5, 5.2))
    ax.scatter(x, y, alpha=0.8, s=55)

    _apply_common_style(
        ax,
        "Relacja: błąd wartości vs odległość od minimum",
        xlabel="Abs error wartości",
        ylabel="Odległość od minimum globalnego",
    )
    return _save(path)


def save_problem_dual_neighborhood_rate_bar(
    output_dir: Path,
    rows: list[dict[str, Any]],
    point_tol: float,
    filename: str,
    title: str = "Udział najlepszej i medianowej konfiguracji w otoczeniu minimum",
) -> str | None:
    valid = [row for row in rows if row.get("nearest_global_min_point_distance") is not None]
    if not valid:
        return None

    grouped: dict[str, list[dict[str, Any]]] = {}
    for row in valid:
        grouped.setdefault(str(row["problem_name"]), []).append(row)

    items = []
    for problem_name, group in grouped.items():
        distances = sorted(float(r["nearest_global_min_point_distance"]) for r in group)
        best_hit = 1.0 if distances[0] <= point_tol else 0.0
        median_hit = 1.0 if float(np.median(distances)) <= point_tol else 0.0
        items.append((problem_name, best_hit, median_hit))

    if not items:
        return None

    items.sort(key=lambda x: (-x[1], -x[2], x[0]))
    labels = [x[0] for x in items]
    best_values = [x[1] for x in items]
    median_values = [x[2] for x in items]

    path = output_dir / "plots" / filename
    fig, ax = plt.subplots(figsize=(12.0, max(4.8, len(labels) * 0.42)))
    y = np.arange(len(labels))
    ax.barh(y - 0.18, best_values, height=0.34, label="best w otoczeniu")
    ax.barh(y + 0.18, median_values, height=0.34, label="mediana w otoczeniu", alpha=0.7)
    ax.set_yticks(y)
    ax.set_yticklabels(labels)
    ax.set_xlim(0.0, 1.0)
    for yi, best_val, med_val in zip(y, best_values, median_values):
        ax.text(best_val, yi - 0.18, f"  {100.0 * best_val:.0f}%", va="center", fontsize=9)
        ax.text(med_val, yi + 0.18, f"  {100.0 * med_val:.0f}%", va="center", fontsize=9)

    _apply_common_style(ax, title, xlabel="Udział [%]", ylabel="Funkcja")
    ax.legend()
    return _save(path)


def save_problem_metric_bar(
    output_dir: Path,
    rows: list[dict[str, Any]],
    value_key: str,
    agg: str,
    title: str,
    xlabel: str,
    filename: str,
) -> str | None:
    valid = [row for row in rows if row.get(value_key) is not None]
    if not valid:
        return None

    grouped: dict[str, list[float]] = {}
    for row in valid:
        grouped.setdefault(str(row["problem_name"]), []).append(float(row[value_key]))

    items: list[tuple[str, float]] = []
    for problem_name, vals in grouped.items():
        if agg == "median":
            metric = float(np.median(vals))
        elif agg == "mean":
            metric = float(np.mean(vals))
        elif agg == "best":
            metric = float(np.min(vals))
        else:
            raise ValueError(f"Nieobsługiwane agg: {agg}")
        items.append((problem_name, metric))

    items.sort(key=lambda x: x[1])
    labels = [x[0] for x in items]
    values = [x[1] for x in items]

    path = output_dir / "plots" / filename
    fig, ax = plt.subplots(figsize=(11.5, max(4.8, len(labels) * 0.42)))
    y = np.arange(len(labels))
    bars = ax.barh(y, values, alpha=0.85)
    ax.set_yticks(y)
    ax.set_yticklabels(labels)

    for rect, val in zip(bars, values):
        ax.text(rect.get_width(), rect.get_y() + rect.get_height() / 2, f"  {val:.4f}", va="center")

    _apply_common_style(
        ax,
        title,
        xlabel=xlabel,
        ylabel="Funkcja",
    )
    return _save(path)


def save_problem_success_rate_bar(
    output_dir: Path,
    rows: list[dict[str, Any]],
    value_tol: float,
    filename: str,
    title: str = "Success rate wg wartości per funkcja",
    value_key: str = "abs_value_error",
) -> str | None:
    valid = [row for row in rows if row.get(value_key) is not None]
    if not valid:
        return None

    grouped: dict[str, list[float]] = {}
    for row in valid:
        grouped.setdefault(str(row["problem_name"]), []).append(float(row[value_key]))

    items: list[tuple[str, float]] = []
    for problem_name, vals in grouped.items():
        success_rate = float(sum(v <= value_tol for v in vals) / len(vals))
        items.append((problem_name, success_rate))

    items.sort(key=lambda x: x[1], reverse=True)
    labels = [x[0] for x in items]
    values = [x[1] for x in items]

    path = output_dir / "plots" / filename
    fig, ax = plt.subplots(figsize=(11.5, max(4.8, len(labels) * 0.42)))
    y = np.arange(len(labels))
    bars = ax.barh(y, values, alpha=0.85)
    ax.set_yticks(y)
    ax.set_yticklabels(labels)

    for rect, val in zip(bars, values):
        ax.text(rect.get_width(), rect.get_y() + rect.get_height() / 2, f"  {100.0 * val:.1f}%", va="center")

    ax.set_xlim(0.0, 1.0)
    _apply_common_style(
        ax,
        title,
        xlabel="Success rate",
        ylabel="Funkcja",
    )
    return _save(path)


def save_problem_counts_bar(
    output_dir: Path,
    rows: list[dict[str, Any]],
    filename: str,
    title: str = "Liczba wylosowań funkcji",
) -> str | None:
    if not rows:
        return None

    counts: dict[str, int] = {}
    for row in rows:
        counts[str(row["problem_name"])] = counts.get(str(row["problem_name"]), 0) + 1

    items = sorted(counts.items(), key=lambda x: (-x[1], x[0]))
    labels = [x[0] for x in items]
    values = [x[1] for x in items]

    path = output_dir / "plots" / filename
    fig, ax = plt.subplots(figsize=(11.5, max(4.8, len(labels) * 0.42)))
    y = np.arange(len(labels))
    bars = ax.barh(y, values, alpha=0.85)
    ax.set_yticks(y)
    ax.set_yticklabels(labels)

    for rect, val in zip(bars, values):
        ax.text(rect.get_width(), rect.get_y() + rect.get_height() / 2, f"  {val}", va="center")

    _apply_common_style(
        ax,
        title,
        xlabel="Liczba uruchomień",
        ylabel="Funkcja",
    )
    return _save(path)


def save_problem_metric_spread_bar(
    output_dir: Path,
    rows: list[dict[str, Any]],
    value_key: str,
    filename: str,
    title: str,
    xlabel: str,
) -> str | None:
    valid = [row for row in rows if row.get(value_key) is not None]
    if not valid:
        return None

    grouped: dict[str, list[float]] = {}
    for row in valid:
        grouped.setdefault(str(row["problem_name"]), []).append(float(row[value_key]))

    items = []
    for problem_name, vals in grouped.items():
        spread = float(np.quantile(vals, 0.75) - np.quantile(vals, 0.25)) if vals else 0.0
        items.append((problem_name, spread))

    items.sort(key=lambda x: x[1])
    labels = [x[0] for x in items]
    values = [x[1] for x in items]

    path = output_dir / "plots" / filename
    fig, ax = plt.subplots(figsize=(11.5, max(4.8, len(labels) * 0.42)))
    y = np.arange(len(labels))
    bars = ax.barh(y, values, alpha=0.85)
    ax.set_yticks(y)
    ax.set_yticklabels(labels)
    for rect, val in zip(bars, values):
        ax.text(rect.get_width(), rect.get_y() + rect.get_height() / 2, f"  {val:.4f}", va="center")
    _apply_common_style(ax, title, xlabel=xlabel, ylabel="Funkcja")
    return _save(path)


def save_problem_operator_diversity_bar(
    output_dir: Path,
    rows: list[dict[str, Any]],
    filename: str,
    title: str = "Różnorodność operatorów per funkcja",
) -> str | None:
    if not rows:
        return None

    grouped: dict[str, set[str]] = {}
    for row in rows:
        grouped.setdefault(str(row["problem_name"]), set()).add(
            f"{row['config']['selection_method']}|{row['config']['crossover_method']}|{row['config']['mutation_method']}"
        )

    items = sorted(((problem, len(ops)) for problem, ops in grouped.items()), key=lambda x: (-x[1], x[0]))
    labels = [x[0] for x in items]
    values = [x[1] for x in items]

    path = output_dir / "plots" / filename
    fig, ax = plt.subplots(figsize=(11.5, max(4.8, len(labels) * 0.42)))
    y = np.arange(len(labels))
    bars = ax.barh(y, values, alpha=0.85)
    ax.set_yticks(y)
    ax.set_yticklabels(labels)
    for rect, val in zip(bars, values):
        ax.text(rect.get_width(), rect.get_y() + rect.get_height() / 2, f"  {val}", va="center")
    _apply_common_style(ax, title, xlabel="Liczba unikalnych trójek operatorów", ylabel="Funkcja")
    return _save(path)


def save_problem_operator_group_share_bar(
    output_dir: Path,
    rows: list[dict[str, Any]],
    config_key: str,
    filename: str,
    title: str,
) -> str | None:
    if not rows:
        return None

    grouped: dict[str, dict[str, int]] = {}
    for row in rows:
        problem_name = str(row["problem_name"])
        op = str(row["config"][config_key])
        grouped.setdefault(problem_name, {})
        grouped[problem_name][op] = grouped[problem_name].get(op, 0) + 1

    items = []
    for problem_name, counts in grouped.items():
        total = sum(counts.values())
        dominant = max(counts.values()) / total if total > 0 else 0.0
        items.append((problem_name, dominant))

    items.sort(key=lambda x: x[1], reverse=True)
    labels = [x[0] for x in items]
    values = [x[1] for x in items]

    path = output_dir / "plots" / filename
    fig, ax = plt.subplots(figsize=(11.5, max(4.8, len(labels) * 0.42)))
    y = np.arange(len(labels))
    bars = ax.barh(y, values, alpha=0.85)
    ax.set_yticks(y)
    ax.set_yticklabels(labels)
    ax.set_xlim(0.0, 1.0)
    for rect, val in zip(bars, values):
        ax.text(rect.get_width(), rect.get_y() + rect.get_height() / 2, f"  {100.0 * val:.1f}%", va="center")
    _apply_common_style(ax, title, xlabel="Udział dominującego operatora", ylabel="Funkcja")
    return _save(path)


def _bounds_around_point_cloud(
    points: list[list[float]],
    center_point: list[float] | None,
    quantile_low: float = 0.10,
    quantile_high: float = 0.90,
    min_pad_ratio: float = 0.12,
) -> tuple[tuple[float, float], tuple[float, float]] | None:
    if not points or any(len(point) < 2 for point in points):
        return None

    xs = np.asarray([float(point[0]) for point in points], dtype=float)
    ys = np.asarray([float(point[1]) for point in points], dtype=float)

    x_low = float(np.quantile(xs, quantile_low))
    x_high = float(np.quantile(xs, quantile_high))
    y_low = float(np.quantile(ys, quantile_low))
    y_high = float(np.quantile(ys, quantile_high))

    if center_point is not None and len(center_point) >= 2:
        cx = float(center_point[0])
        cy = float(center_point[1])
        x_low = min(x_low, cx)
        x_high = max(x_high, cx)
        y_low = min(y_low, cy)
        y_high = max(y_high, cy)

    x_span = max(1e-6, x_high - x_low)
    y_span = max(1e-6, y_high - y_low)
    x_pad = max(1e-6, x_span * min_pad_ratio)
    y_pad = max(1e-6, y_span * min_pad_ratio)

    return (x_low - x_pad, x_high + x_pad), (y_low - y_pad, y_high + y_pad)


def _bounds_around_densest_region(
    points: list[list[float]],
    bins_x: int,
    bins_y: int,
    expand_cells_x: int = 2,
    expand_cells_y: int = 2,
) -> tuple[tuple[float, float], tuple[float, float]] | None:
    if not points or any(len(point) < 2 for point in points):
        return None

    xs = np.asarray([float(point[0]) for point in points], dtype=float)
    ys = np.asarray([float(point[1]) for point in points], dtype=float)

    xmin = float(np.min(xs))
    xmax = float(np.max(xs))
    ymin = float(np.min(ys))
    ymax = float(np.max(ys))

    if np.isclose(xmin, xmax):
        pad = max(1e-6, abs(xmin) * 0.1, 1.0)
        xmin -= pad
        xmax += pad
    if np.isclose(ymin, ymax):
        pad = max(1e-6, abs(ymin) * 0.1, 1.0)
        ymin -= pad
        ymax += pad

    H, xedges, yedges = np.histogram2d(xs, ys, bins=[bins_x, bins_y], range=[[xmin, xmax], [ymin, ymax]])
    if H.size == 0:
        return None

    max_index = np.unravel_index(np.argmax(H), H.shape)
    ix = int(max_index[0])
    iy = int(max_index[1])

    x0 = max(0, ix - expand_cells_x)
    x1 = min(len(xedges) - 2, ix + expand_cells_x)
    y0 = max(0, iy - expand_cells_y)
    y1 = min(len(yedges) - 2, iy + expand_cells_y)

    return (float(xedges[x0]), float(xedges[x1 + 1])), (float(yedges[y0]), float(yedges[y1 + 1]))


def _compute_square_grid_counts(
    points: list[list[float]],
    xlim: tuple[float, float],
    ylim: tuple[float, float],
    bins_x: int,
    bins_y: int,
):
    xs = np.asarray([float(p[0]) for p in points], dtype=float)
    ys = np.asarray([float(p[1]) for p in points], dtype=float)

    H, xedges, yedges = np.histogram2d(
        xs,
        ys,
        bins=[bins_x, bins_y],
        range=[[xlim[0], xlim[1]], [ylim[0], ylim[1]]],
    )
    return H.T, xedges, yedges


def _render_density_heatmap(
    output_dir: Path,
    points: list[list[float]],
    median_point: list[float] | None,
    global_minimum_points: list[list[float]] | None,
    title: str,
    filename: str,
    xlim: tuple[float, float],
    ylim: tuple[float, float],
    bins_x: int,
    bins_y: int,
) -> str | None:
    H, xedges, yedges = _compute_square_grid_counts(points=points, xlim=xlim, ylim=ylim, bins_x=bins_x, bins_y=bins_y)
    if H.size == 0:
        return None

    max_count = float(np.max(H)) if np.size(H) else 0.0
    H_norm = H / max_count if max_count > 0.0 else H.copy()
    H_masked = np.ma.masked_where(H <= 0.0, H_norm)

    path = output_dir / "plots" / filename
    fig, ax = plt.subplots(figsize=(8.2, 6.8))
    cmap = plt.cm.Reds.copy()
    cmap.set_bad(color="white")

    mesh = ax.pcolormesh(
        xedges,
        yedges,
        H_masked,
        shading="auto",
        cmap=cmap,
        vmin=0.0,
        vmax=1.0,
        edgecolors="#d9d9d9",
        linewidth=0.45,
    )

    if global_minimum_points:
        gx = [float(point[0]) for point in global_minimum_points if len(point) >= 2]
        gy = [float(point[1]) for point in global_minimum_points if len(point) >= 2]
        if gx and gy:
            ax.scatter(gx, gy, marker="x", s=180, c="black", linewidths=2.4, zorder=7, label="minimum globalne")

    if median_point is not None and len(median_point) >= 2:
        ax.scatter(
            [float(median_point[0])],
            [float(median_point[1])],
            marker="o",
            s=170,
            c="#ff8c00",
            edgecolors="black",
            linewidths=1.8,
            zorder=8,
            label="mediana",
        )

    ax.set_xlim(*xlim)
    ax.set_ylim(*ylim)
    _apply_common_style(ax, title, xlabel="x1", ylabel="x2")
    cbar = fig.colorbar(mesh, ax=ax)
    cbar.set_label("Znormalizowana liczba punktów w kwadracie")
    ax.legend(loc="best", frameon=True, facecolor="white", framealpha=0.95, edgecolor="black")
    return _save(path)


def save_median_density_heatmap(
    output_dir: Path,
    points: list[list[float]],
    median_point: list[float] | None,
    global_minimum_points: list[list[float]] | None,
    title: str,
    filename: str,
    bins_x: int,
    bins_y: int,
) -> str | None:
    if not points or any(len(point) < 2 for point in points):
        return None
    bounds = _bounds_around_point_cloud(points=points, center_point=median_point)
    if bounds is None:
        return None
    xlim, ylim = bounds
    return _render_density_heatmap(output_dir, points, median_point, global_minimum_points, title, filename, xlim, ylim, bins_x, bins_y)


def save_dense_region_heatmap(
    output_dir: Path,
    points: list[list[float]],
    median_point: list[float] | None,
    global_minimum_points: list[list[float]] | None,
    title: str,
    filename: str,
    bins_x: int,
    bins_y: int,
) -> str | None:
    if not points or any(len(point) < 2 for point in points):
        return None
    bounds = _bounds_around_densest_region(points=points, bins_x=max(10, bins_x), bins_y=max(10, bins_y), expand_cells_x=2, expand_cells_y=2)
    if bounds is None:
        return None
    xlim, ylim = bounds
    return _render_density_heatmap(output_dir, points, median_point, global_minimum_points, title, filename, xlim, ylim, bins_x, bins_y)


def save_group_quality_ranking(
    output_dir: Path,
    rows: list[dict[str, Any]],
    config_key: str,
    title: str,
    filename: str,
    label_map: dict[Any, str] | None = None,
    metric_key: str = "nearest_global_min_point_distance",
    xlabel: str = "Mediana odległości od minimum (niżej = lepiej)",
) -> str | None:
    valid = [r for r in rows if r.get(metric_key) is not None]
    if not valid:
        return None

    grouped: dict[Any, list[float]] = {}
    for row in valid:
        key_val = row["config"][config_key]
        grouped.setdefault(key_val, []).append(float(row[metric_key]))

    plot_rows = []
    for key_val, vals in grouped.items():
        plot_rows.append(
            {
                "label": label_map.get(key_val, str(key_val)) if label_map else str(key_val),
                "median": float(np.median(vals)),
                "count": len(vals),
            }
        )

    plot_rows.sort(key=lambda item: (item["median"], item["label"]))

    labels = [r["label"] for r in plot_rows]
    medians = [r["median"] for r in plot_rows]

    path = output_dir / "plots" / filename
    fig, ax = plt.subplots(figsize=(9.2, max(4.2, len(labels) * 0.45)))
    y = np.arange(len(labels))
    ax.barh(y, medians, height=0.5, alpha=0.8)
    ax.set_yticks(y)
    ax.set_yticklabels(labels)

    for yi, median_val, row in zip(y, medians, plot_rows):
        ax.text(median_val, yi, f"  {median_val:.3f} (n={row['count']})", va="center", fontsize=9)

    _apply_common_style(ax, title, xlabel=xlabel, ylabel="Wariant")
    return _save(path)
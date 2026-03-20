# metrics.py
from __future__ import annotations

from collections import Counter, defaultdict
from statistics import mean, median, pstdev
from typing import Any


def safe_mean(values: list[float]) -> float | None:
    return mean(values) if values else None


def safe_median(values: list[float]) -> float | None:
    return median(values) if values else None


def safe_std(values: list[float]) -> float | None:
    if not values:
        return None
    if len(values) == 1:
        return 0.0
    return pstdev(values)


def percentile(values: list[float], q: float) -> float | None:
    if not values:
        return None
    ordered = sorted(values)
    if len(ordered) == 1:
        return ordered[0]
    pos = (len(ordered) - 1) * q
    low = int(pos)
    high = min(low + 1, len(ordered) - 1)
    frac = pos - low
    return ordered[low] * (1.0 - frac) + ordered[high] * frac


def best_row(rows: list[dict[str, Any]]) -> dict[str, Any] | None:
    valid = [row for row in rows if row.get("best_value") is not None]
    if not valid:
        return None
    return min(valid, key=lambda row: float(row["best_value"]))


def worst_row(rows: list[dict[str, Any]]) -> dict[str, Any] | None:
    valid = [row for row in rows if row.get("best_value") is not None]
    if not valid:
        return None
    return max(valid, key=lambda row: float(row["best_value"]))


def nearest_row_to_value(rows: list[dict[str, Any]], target: float | None) -> dict[str, Any] | None:
    valid = [row for row in rows if row.get("best_value") is not None]
    if not valid or target is None:
        return None
    return min(valid, key=lambda row: abs(float(row["best_value"]) - float(target)))


def group_rows_by_problem(rows: list[dict[str, Any]]) -> dict[str, list[dict[str, Any]]]:
    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        grouped[row["problem_name"]].append(row)
    return dict(grouped)


def success_counts(
    rows: list[dict[str, Any]],
    value_tol: float,
    point_tol: float,
) -> dict[str, Any]:
    valid = [row for row in rows if row.get("best_value") is not None]

    value_hits = sum(
        1
        for row in valid
        if row.get("abs_value_error") is not None
        and float(row["abs_value_error"]) <= float(value_tol)
    )
    point_hits = sum(
        1
        for row in valid
        if row.get("nearest_global_min_point_distance") is not None
        and float(row["nearest_global_min_point_distance"]) <= float(point_tol)
    )

    total = len(valid)
    return {
        "total": total,
        "value_hits": value_hits,
        "point_hits": point_hits,
        "value_success_rate": (value_hits / total) if total > 0 else 0.0,
        "point_success_rate": (point_hits / total) if total > 0 else 0.0,
    }


def summarize_rows_basic(
    rows: list[dict[str, Any]],
    value_tol: float | None = None,
    point_tol: float | None = None,
) -> dict[str, Any]:
    valid = [row for row in rows if row.get("best_value") is not None]

    values = [float(row["best_value"]) for row in valid]
    signed_errors = [float(row["signed_value_error"]) for row in valid if row.get("signed_value_error") is not None]
    abs_errors = [float(row["abs_value_error"]) for row in valid if row.get("abs_value_error") is not None]
    point_distances = [
        float(row["nearest_global_min_point_distance"])
        for row in valid
        if row.get("nearest_global_min_point_distance") is not None
    ]
    elapsed_values = [
        float(row["engine_summary"]["elapsed"])
        for row in valid
        if row.get("engine_summary", {}).get("elapsed") is not None
    ]
    duration_values = [
        float(row["duration_sec"])
        for row in valid
        if row.get("duration_sec") is not None
    ]

    best_v = min(values) if values else None
    worst_v = max(values) if values else None
    q1_v = percentile(values, 0.25)
    med_v = safe_median(values)
    mean_v = safe_mean(values)
    q3_v = percentile(values, 0.75)

    summary = {
        "count": len(valid),
        "best_value": best_v,
        "q1_best_value": q1_v,
        "median_best_value": med_v,
        "mean_best_value": mean_v,
        "q3_best_value": q3_v,
        "worst_best_value": worst_v,
        "std_best_value": safe_std(values),
        "mean_signed_error": safe_mean(signed_errors),
        "median_signed_error": safe_median(signed_errors),
        "best_abs_error": min(abs_errors) if abs_errors else None,
        "q1_abs_error": percentile(abs_errors, 0.25),
        "mean_abs_error": safe_mean(abs_errors),
        "median_abs_error": safe_median(abs_errors),
        "q3_abs_error": percentile(abs_errors, 0.75),
        "worst_abs_error": max(abs_errors) if abs_errors else None,
        "std_abs_error": safe_std(abs_errors),
        "best_point_distance": min(point_distances) if point_distances else None,
        "q1_point_distance": percentile(point_distances, 0.25),
        "mean_point_distance": safe_mean(point_distances),
        "median_point_distance": safe_median(point_distances),
        "q3_point_distance": percentile(point_distances, 0.75),
        "worst_point_distance": max(point_distances) if point_distances else None,
        "std_point_distance": safe_std(point_distances),
        "mean_elapsed": safe_mean(elapsed_values),
        "median_elapsed": safe_median(elapsed_values),
        "mean_duration_sec": safe_mean(duration_values),
        "median_duration_sec": safe_median(duration_values),
        "best_row": best_row(valid),
        "worst_row": worst_row(valid),
        "q1_row": nearest_row_to_value(valid, q1_v),
        "median_row": nearest_row_to_value(valid, med_v),
        "mean_row": nearest_row_to_value(valid, mean_v),
        "q3_row": nearest_row_to_value(valid, q3_v),
    }

    if value_tol is not None and point_tol is not None:
        summary["success"] = success_counts(valid, value_tol=value_tol, point_tol=point_tol)
    else:
        summary["success"] = None

    return summary


def operator_win_counters(rows: list[dict[str, Any]]) -> dict[str, dict[str, int]]:
    selection_counter: Counter[str] = Counter()
    crossover_counter: Counter[str] = Counter()
    mutation_counter: Counter[str] = Counter()

    for row in rows:
        cfg = row["config"]
        selection_counter[str(cfg["selection_method"])] += 1
        crossover_counter[str(cfg["crossover_method"])] += 1
        mutation_counter[str(cfg["mutation_method"])] += 1

    return {
        "selection": dict(selection_counter),
        "crossover": dict(crossover_counter),
        "mutation": dict(mutation_counter),
    }


def build_operator_ranking_rows(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    valid = [row for row in rows if row.get("best_value") is not None]
    counters = operator_win_counters(valid)
    ranking_rows: list[dict[str, Any]] = []

    for group_name, group_counts in counters.items():
        for operator_name, count in group_counts.items():
            op_rows = []
            for row in valid:
                cfg = row["config"]
                if group_name == "selection" and str(cfg["selection_method"]) == operator_name:
                    op_rows.append(row)
                elif group_name == "crossover" and str(cfg["crossover_method"]) == operator_name:
                    op_rows.append(row)
                elif group_name == "mutation" and str(cfg["mutation_method"]) == operator_name:
                    op_rows.append(row)

            best_vals = [float(r["best_value"]) for r in op_rows if r.get("best_value") is not None]
            abs_errs = [float(r["abs_value_error"]) for r in op_rows if r.get("abs_value_error") is not None]

            ranking_rows.append(
                {
                    "group": group_name,
                    "operator": operator_name,
                    "wins": count,
                    "avg_best_value": safe_mean(best_vals),
                    "avg_abs_error": safe_mean(abs_errs),
                }
            )

    ranking_rows.sort(
        key=lambda row: (
            row["group"],
            -(row["wins"] if row["wins"] is not None else -1),
            row["avg_abs_error"] if row["avg_abs_error"] is not None else float("inf"),
            row["operator"],
        )
    )
    return ranking_rows


def build_best_per_problem_rows(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    grouped = group_rows_by_problem(rows)
    result: list[dict[str, Any]] = []

    for problem_name, problem_rows in grouped.items():
        best = best_row(problem_rows)
        if best is None:
            continue

        cfg = best["config"]
        result.append(
            {
                "problem_name": problem_name,
                "best_value": best.get("best_value"),
                "error_to_global_min": best.get("abs_value_error"),
                "nearest_global_min_point_distance": best.get("nearest_global_min_point_distance"),
                "selection_method": cfg.get("selection_method"),
                "crossover_method": cfg.get("crossover_method"),
                "mutation_method": cfg.get("mutation_method"),
                "inversion_enabled": cfg.get("inversion_enabled"),
                "elitism_enabled": cfg.get("elitism_enabled"),
                "population": cfg.get("population"),
                "epochs": cfg.get("epochs"),
                "run_count": cfg.get("run_count"),
                "precision_bits": cfg.get("precision_bits"),
                "seed": cfg.get("seed"),
                "duration_sec": best.get("duration_sec"),
            }
        )

    result.sort(
        key=lambda row: (
            float(row["error_to_global_min"]) if row.get("error_to_global_min") is not None else float("inf"),
            row["problem_name"],
        )
    )
    return result


def describe_numeric_region(values: list[float | int]) -> dict[str, Any]:
    numeric = [float(v) for v in values]
    if not numeric:
        return {
            "min": None,
            "max": None,
            "mean": None,
            "median": None,
            "q1": None,
            "q3": None,
        }
    return {
        "min": min(numeric),
        "max": max(numeric),
        "mean": safe_mean(numeric),
        "median": safe_median(numeric),
        "q1": percentile(numeric, 0.25),
        "q3": percentile(numeric, 0.75),
    }


def describe_best_parameter_regions(
    rows: list[dict[str, Any]],
    top_fraction: float = 0.25,
) -> dict[str, Any]:
    valid = [row for row in rows if row.get("best_value") is not None]
    if not valid:
        return {}

    ordered = sorted(valid, key=lambda row: float(row["best_value"]))
    top_count = max(1, int(len(ordered) * float(top_fraction)))
    top_rows = ordered[:top_count]

    populations = [row["config"]["population"] for row in top_rows]
    epochs = [row["config"]["epochs"] for row in top_rows]
    run_counts = [row["config"]["run_count"] for row in top_rows]
    precision_bits = [row["config"]["precision_bits"] for row in top_rows]

    selection_counter = Counter(row["config"]["selection_method"] for row in top_rows)
    crossover_counter = Counter(row["config"]["crossover_method"] for row in top_rows)
    mutation_counter = Counter(row["config"]["mutation_method"] for row in top_rows)
    inversion_counter = Counter(bool(row["config"]["inversion_enabled"]) for row in top_rows)
    elitism_counter = Counter(bool(row["config"]["elitism_enabled"]) for row in top_rows)

    method_param_values: dict[str, list[float]] = defaultdict(list)
    for row in top_rows:
        for key, value in row["config"]["method_params"].items():
            try:
                method_param_values[str(key)].append(float(value))
            except Exception:
                continue

    method_param_regions = {
        key: describe_numeric_region(values)
        for key, values in method_param_values.items()
    }

    return {
        "top_count": top_count,
        "population_region": describe_numeric_region(populations),
        "epochs_region": describe_numeric_region(epochs),
        "run_count_region": describe_numeric_region(run_counts),
        "precision_bits_region": describe_numeric_region(precision_bits),
        "selection_modes": dict(selection_counter),
        "crossover_modes": dict(crossover_counter),
        "mutation_modes": dict(mutation_counter),
        "inversion_modes": dict(inversion_counter),
        "elitism_modes": dict(elitism_counter),
        "method_param_regions": method_param_regions,
    }
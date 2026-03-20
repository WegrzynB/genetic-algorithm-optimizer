# reporting.py
from __future__ import annotations

import csv
import json
from datetime import datetime
from pathlib import Path
from typing import Any


_TEST_NAME_SHORTCUTS = {
    "random_functions": "rand",
    "all_functions_global_operator_search": "allglob",
    "single_function_operator_search": "single",
}


def _ensure_output_dir(output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "plots").mkdir(parents=True, exist_ok=True)


def make_experiment_output_dir(test_name: str, preset_name: str) -> Path:
    short_name = _TEST_NAME_SHORTCUTS.get(test_name, test_name)
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    out = Path("data") / "output" / "tests" / f"{short_name}__{ts}"
    return out


def save_summary_json(output_dir: Path, summary: dict[str, Any], filename: str = "summary.json") -> str:
    _ensure_output_dir(output_dir)
    path = output_dir / filename
    with open(path, "w", encoding="utf-8") as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)
    return str(path)


def save_summary_csv(output_dir: Path, rows: list[dict[str, Any]], filename: str = "results.csv") -> str | None:
    if not rows:
        return None

    _ensure_output_dir(output_dir)
    path = output_dir / filename

    fieldnames: list[str] = []
    for row in rows:
        for key in row.keys():
            if key not in fieldnames:
                fieldnames.append(key)

    with open(path, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)

    return str(path)


def save_report_md(output_dir: Path, text: str, filename: str = "report.md") -> str:
    _ensure_output_dir(output_dir)
    path = output_dir / filename
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)
    return str(path)


def _fmt(v: Any, ndigits: int = 7) -> str:
    if v is None:
        return "-"
    if isinstance(v, float):
        return f"{v:.{ndigits}f}"
    return str(v)


def _fmt_percent(v: Any, ndigits: int = 2) -> str:
    if v is None:
        return "-"
    try:
        return f"{100.0 * float(v):.{ndigits}f}%"
    except Exception:
        return str(v)


def _render_simple_bullet_stat(label: str, value: Any) -> str:
    return f"- {label}: **{_fmt(value)}**"


def _render_top_rows(top_rows: list[dict[str, Any]], limit: int = 10) -> str:
    if not top_rows:
        return "_brak danych_"

    lines = [
        "| rank | problem_name | best_value | abs_value_error | nearest_global_min_point_distance | selection_method | crossover_method | mutation_method | population | epochs | run_count | precision_bits |",
        "| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |",
    ]
    for row in top_rows[:limit]:
        lines.append(
            "| {rank} | {problem_name} | {best_value} | {abs_value_error} | {nearest_global_min_point_distance} | {selection_method} | {crossover_method} | {mutation_method} | {population} | {epochs} | {run_count} | {precision_bits} |".format(
                rank=row.get("rank", "-"),
                problem_name=row.get("problem_name", "-"),
                best_value=_fmt(row.get("best_value")),
                abs_value_error=_fmt(row.get("abs_value_error")),
                nearest_global_min_point_distance=_fmt(row.get("nearest_global_min_point_distance")),
                selection_method=row.get("selection_method", "-"),
                crossover_method=row.get("crossover_method", "-"),
                mutation_method=row.get("mutation_method", "-"),
                population=row.get("population", "-"),
                epochs=row.get("epochs", "-"),
                run_count=row.get("run_count", "-"),
                precision_bits=row.get("precision_bits", "-"),
            )
        )
    return "\n".join(lines)


def _render_top_rows_single(top_rows: list[dict[str, Any]], limit: int = 10) -> str:
    if not top_rows:
        return "_brak danych_"

    lines = [
        "| rank | best_value | abs_value_error | nearest_global_min_point_distance | selection_method | crossover_method | mutation_method | population | epochs | run_count | precision_bits |",
        "| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |",
    ]
    for row in top_rows[:limit]:
        lines.append(
            "| {rank} | {best_value} | {abs_value_error} | {nearest_global_min_point_distance} | {selection_method} | {crossover_method} | {mutation_method} | {population} | {epochs} | {run_count} | {precision_bits} |".format(
                rank=row.get("rank", "-"),
                best_value=_fmt(row.get("best_value")),
                abs_value_error=_fmt(row.get("abs_value_error")),
                nearest_global_min_point_distance=_fmt(row.get("nearest_global_min_point_distance")),
                selection_method=row.get("selection_method", "-"),
                crossover_method=row.get("crossover_method", "-"),
                mutation_method=row.get("mutation_method", "-"),
                population=row.get("population", "-"),
                epochs=row.get("epochs", "-"),
                run_count=row.get("run_count", "-"),
                precision_bits=row.get("precision_bits", "-"),
            )
        )
    return "\n".join(lines)


def _render_best_per_problem(rows: list[dict[str, Any]]) -> str:
    if not rows:
        return "_brak danych_"

    lines = [
        "| problem_name | best_value | error_to_global_min | point_distance | selection | crossover | mutation | inversion | elitism | population | epochs | run_count | precision_bits |",
        "| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |",
    ]
    for row in rows:
        lines.append(
            "| {problem_name} | {best_value} | {error_to_global_min} | {nearest_global_min_point_distance} | {selection_method} | {crossover_method} | {mutation_method} | {inversion_enabled} | {elitism_enabled} | {population} | {epochs} | {run_count} | {precision_bits} |".format(
                problem_name=row.get("problem_name", "-"),
                best_value=_fmt(row.get("best_value")),
                error_to_global_min=_fmt(row.get("error_to_global_min")),
                nearest_global_min_point_distance=_fmt(row.get("nearest_global_min_point_distance")),
                selection_method=row.get("selection_method", "-"),
                crossover_method=row.get("crossover_method", "-"),
                mutation_method=row.get("mutation_method", "-"),
                inversion_enabled=row.get("inversion_enabled", "-"),
                elitism_enabled=row.get("elitism_enabled", "-"),
                population=row.get("population", "-"),
                epochs=row.get("epochs", "-"),
                run_count=row.get("run_count", "-"),
                precision_bits=row.get("precision_bits", "-"),
            )
        )
    return "\n".join(lines)


def _render_operator_ranking(rows: list[dict[str, Any]], limit: int = 30) -> str:
    if not rows:
        return "_brak danych_"

    lines = [
        "| group | operator | wins | avg_best_value | avg_abs_error |",
        "| --- | --- | --- | --- | --- |",
    ]
    for row in rows[:limit]:
        lines.append(
            f"| {row.get('group', '-')} | {row.get('operator', '-')} | {row.get('wins', '-')} | "
            f"{_fmt(row.get('avg_best_value'))} | {_fmt(row.get('avg_abs_error'))} |"
        )
    return "\n".join(lines)


def _render_quality_table(rows: list[dict[str, Any]]) -> str:
    if not rows:
        return "_brak danych_"

    lines = [
        "| label | mean | median | count |",
        "| --- | --- | --- | --- |",
    ]
    for row in rows:
        lines.append(
            f"| {row.get('label', '-')} | {_fmt(row.get('mean'))} | {_fmt(row.get('median'))} | {row.get('count', '-')} |"
        )
    return "\n".join(lines)


def _render_boolean_quality_comment(rows: list[dict[str, Any]], feature_name: str) -> str:
    if not rows or len(rows) < 2:
        return f"Brak wystarczających danych, żeby ocenić wpływ ustawienia **{feature_name}**."

    sorted_rows = sorted(rows, key=lambda r: (r.get("mean", float("inf")), r.get("median", float("inf"))))
    best = sorted_rows[0]
    second = sorted_rows[1]

    if best.get("mean") is None or second.get("mean") is None:
        return f"Brak wystarczających danych, żeby ocenić wpływ ustawienia **{feature_name}**."

    advantage = float(second["mean"]) - float(best["mean"])
    return (
        f"Lepiej wypada wariant **{best.get('label')}**. "
        f"Przewaga wg średniego abs error wynosi około **{advantage:.4f}**."
    )


def _render_success(summary: dict[str, Any]) -> str:
    success = summary.get("success")
    if not success:
        return "_brak danych o sukcesach_"

    return "\n".join(
        [
            f"- Trafienia wg wartości: **{success.get('value_hits')}/{success.get('total')}**",
            f"- Success rate wg wartości: **{_fmt_percent(success.get('value_success_rate'))}**",
            f"- Trafienia wg punktu: **{success.get('point_hits')}/{success.get('total')}**",
            f"- Success rate wg punktu: **{_fmt_percent(success.get('point_success_rate'))}**",
        ]
    )


def _render_parameter_regions(data: Any) -> str:
    if not data:
        return "_brak danych_"

    if isinstance(data, dict):
        lines: list[str] = []

        def add_line(label: str, value: Any) -> None:
            lines.append(f"- {label}: **{value}**")

        add_line("Top_count", data.get("top_count"))
        add_line("Population region", data.get("population_region"))
        add_line("Epochs region", data.get("epochs_region"))
        add_line("Run_count region", data.get("run_count_region"))
        add_line("Precision_bits region", data.get("precision_bits_region"))
        add_line("Selection modes", data.get("selection_modes"))
        add_line("Crossover modes", data.get("crossover_modes"))
        add_line("Mutation modes", data.get("mutation_modes"))
        add_line("Inversion modes", data.get("inversion_modes"))
        add_line("Elitism modes", data.get("elitism_modes"))

        method_param_regions = data.get("method_param_regions")
        if method_param_regions:
            lines.append("\n## Regiony parametrów metod\n")
            for param_name, region in method_param_regions.items():
                lines.append(f"- `{param_name}`: {region}")

        return "\n".join(lines)

    return f"`{data}`"


def _render_plot_list(plot_paths: dict[str, Any]) -> str:
    if not plot_paths:
        return "_brak wykresów_"

    lines = []
    for _, value in plot_paths.items():
        if value:
            lines.append(f"- `{value}`")
    return "\n".join(lines) if lines else "_brak wykresów_"


def _render_errors(errors: list[dict[str, Any]], limit: int = 10) -> str:
    if not errors:
        return "- Brak błędów."

    lines = [
        "| step | label | type | message |",
        "| --- | --- | --- | --- |",
    ]
    for err in errors[:limit]:
        msg = str(err.get("message", "")).replace("\n", " ").replace("|", "/")
        lines.append(
            f"| {err.get('step', '-')} | {err.get('label', '-')} | {err.get('type', '-')} | {msg} |"
        )
    return "\n".join(lines)


def build_random_functions_report(summary: dict[str, Any]) -> str:
    return f"""# Raport eksperymentu: random_functions

## Zakres eksperymentu

- Preset: **{summary.get("preset_name")}**
- Wykonań: **{summary.get("executions")}**
- Pula funkcji: **{summary.get("problem_pool")}**

## Statystyki wyników

{_render_simple_bullet_stat("Best", summary.get("best_value"))}
{_render_simple_bullet_stat("Q1", summary.get("q1_best_value"))}
{_render_simple_bullet_stat("Median", summary.get("median_best_value"))}
{_render_simple_bullet_stat("Mean", summary.get("mean_best_value"))}
{_render_simple_bullet_stat("Q3", summary.get("q3_best_value"))}
{_render_simple_bullet_stat("Worst", summary.get("worst_best_value"))}
{_render_simple_bullet_stat("Std", summary.get("std_best_value"))}
{_render_simple_bullet_stat("Mean abs error", summary.get("mean_abs_error"))}
{_render_simple_bullet_stat("Median abs error", summary.get("median_abs_error"))}
{_render_simple_bullet_stat("Mean point distance", summary.get("mean_point_distance"))}
{_render_simple_bullet_stat("Median point distance", summary.get("median_point_distance"))}

## Sukces algorytmu

{_render_success(summary)}

## Czasy

- Czas całego testu: **{_fmt(summary.get("test_duration_sec"), 3)} s**
- Średni czas pojedynczego eksperymentu: **{_fmt(summary.get("mean_duration_sec"), 3)} s**
- Mediana czasu pojedynczego eksperymentu: **{_fmt(summary.get("median_duration_sec"), 3)} s**

## Top konfiguracje

{_render_top_rows(summary.get("top_rows", []), limit=15)}

## Ranking operatorów

{_render_operator_ranking(summary.get("operator_ranking", []), limit=30)}

## Jakość selekcji

### Metody selekcji

{_render_quality_table(summary.get("selection_quality_rows", []))}

## Jakość crossoverów

### Metody crossover

{_render_quality_table(summary.get("crossover_quality_rows", []))}

## Jakość mutacji

### Metody mutacji

{_render_quality_table(summary.get("mutation_quality_rows", []))}

## Wpływ inwersji

### Inwersja

{_render_quality_table(summary.get("inversion_quality_rows", []))}

{_render_boolean_quality_comment(summary.get("inversion_quality_rows", []), "inversion")}

## Wpływ elitaryzmu

### Elitaryzm

{_render_quality_table(summary.get("elitism_quality_rows", []))}

{_render_boolean_quality_comment(summary.get("elitism_quality_rows", []), "elitism")}

## Interpretacja rankingów jakości

- Rankingi jakości są liczone na podstawie **abs error**: im niższa wartość, tym lepiej.
- Warto patrzeć jednocześnie na **mean** i **median**.
- Mean pokazuje ogólną jakość.
- Median jest odporniejsza na pojedyncze bardzo słabe uruchomienia.
- Jeśli operator ma niską medianę, ale wyższą średnią, to zwykle działa dobrze, ale czasem trafia słabsze przypadki.
- Jeśli operator ma jednocześnie niską średnią i niską medianę, to jest dobrym kandydatem na ustawienie stabilne.
- W tym teście ważne jest, że funkcje są losowane, więc ranking mówi o jakości operatorów **w ujęciu ogólnym**, a nie dla jednej konkretnej funkcji.

## Wykresy

{_render_plot_list(summary.get("plot_paths", {}))}

## Błędy

{_render_errors(summary.get("errors", []), limit=10)}
"""


def build_all_functions_report(summary: dict[str, Any]) -> str:
    return f"""# Raport eksperymentu: all_functions_global_operator_search

## Zakres eksperymentu

- Preset: **{summary.get("preset_name")}**
- Liczba funkcji: **{summary.get("problem_count")}**
- Wykonań na funkcję: **{summary.get("executions_per_function")}**
- Łącznie wykonań: **{summary.get("total_executions")}**

## Statystyki wyników

{_render_simple_bullet_stat("Best", summary.get("best_value"))}
{_render_simple_bullet_stat("Q1", summary.get("q1_best_value"))}
{_render_simple_bullet_stat("Median", summary.get("median_best_value"))}
{_render_simple_bullet_stat("Mean", summary.get("mean_best_value"))}
{_render_simple_bullet_stat("Q3", summary.get("q3_best_value"))}
{_render_simple_bullet_stat("Worst", summary.get("worst_best_value"))}
{_render_simple_bullet_stat("Mean abs error", summary.get("mean_abs_error_across_functions"))}
{_render_simple_bullet_stat("Median abs error", summary.get("median_abs_error_across_functions"))}
{_render_simple_bullet_stat("Mean point distance", summary.get("mean_point_distance_across_functions"))}
{_render_simple_bullet_stat("Median point distance", summary.get("median_point_distance_across_functions"))}

## Sukces algorytmu

{_render_success(summary)}

## Czasy

- Czas całego testu: **{_fmt(summary.get("test_duration_sec"), 3)} s**
- Średni czas pojedynczego eksperymentu: **{_fmt(summary.get("mean_duration_sec"), 3)} s**
- Mediana czasu pojedynczego eksperymentu: **{_fmt(summary.get("median_duration_sec"), 3)} s**

## Najlepszy wynik dla każdej funkcji

{_render_best_per_problem(summary.get("best_per_problem", summary.get("rows", [])))}

## Ranking operatorów

{_render_operator_ranking(summary.get("operator_ranking", []), limit=30)}

## Jakość selekcji

### Metody selekcji

{_render_quality_table(summary.get("selection_quality_rows", []))}

## Jakość crossoverów

### Metody crossover

{_render_quality_table(summary.get("crossover_quality_rows", []))}

## Jakość mutacji

### Metody mutacji

{_render_quality_table(summary.get("mutation_quality_rows", []))}

## Wpływ inwersji

### Inwersja

{_render_quality_table(summary.get("inversion_quality_rows", []))}

{_render_boolean_quality_comment(summary.get("inversion_quality_rows", []), "inversion")}

## Wpływ elitaryzmu

### Elitaryzm

{_render_quality_table(summary.get("elitism_quality_rows", []))}

{_render_boolean_quality_comment(summary.get("elitism_quality_rows", []), "elitism")}

## Interpretacja rankingów jakości

- W tym teście porównujesz operatorów na pełnym przekroju funkcji.
- Dla wykresu błędu per funkcja używana jest **mediana abs error**, a nie najlepszy pojedynczy wynik.
- Dzięki temu porównanie jest bardziej odporne na pojedyncze wyjątkowo dobre uruchomienia.
- Warto patrzeć jednocześnie na ranking operatorów oraz na jakość per funkcja.

## Wykresy

{_render_plot_list(summary.get("plot_paths", {}))}

## Błędy

{_render_errors(summary.get("errors", []), limit=10)}
"""


def build_all_functions_global_report(summary: dict[str, Any]) -> str:
    return build_all_functions_report(summary)


def build_single_function_operator_report(summary: dict[str, Any]) -> str:
    return f"""# Raport eksperymentu: single_function_operator_search

## Zakres eksperymentu

- Preset: **{summary.get("preset_name")}**
- Funkcja: **{summary.get("problem_name")}**
- Wykonań: **{summary.get("executions")}**
- Minimum globalne: **{_fmt(summary.get("global_minimum_value"))}**
- Punkty minimum globalnego: **{summary.get("global_minimum_points")}**

## Statystyki wyników

{_render_simple_bullet_stat("Best", summary.get("best_value"))}
{_render_simple_bullet_stat("Q1", summary.get("q1_best_value"))}
{_render_simple_bullet_stat("Median", summary.get("median_best_value"))}
{_render_simple_bullet_stat("Mean", summary.get("mean_best_value"))}
{_render_simple_bullet_stat("Q3", summary.get("q3_best_value"))}
{_render_simple_bullet_stat("Worst", summary.get("worst_best_value"))}
{_render_simple_bullet_stat("Mean abs error", summary.get("mean_abs_error"))}
{_render_simple_bullet_stat("Mean point distance", summary.get("mean_point_distance"))}

## Sukces algorytmu

{_render_success(summary)}

## Czasy

- Czas całego testu: **{_fmt(summary.get("test_duration_sec"), 3)} s**
- Średni czas pojedynczego eksperymentu: **{_fmt(summary.get("mean_duration_sec"), 3)} s**
- Mediana czasu pojedynczego eksperymentu: **{_fmt(summary.get("median_duration_sec"), 3)} s**

## Top konfiguracje

{_render_top_rows_single(summary.get("top_rows", []), limit=15)}

## Najlepsze obszary parametrów

{_render_parameter_regions(summary.get("best_parameter_regions", []))}

## Ranking operatorów

{_render_operator_ranking(summary.get("operator_ranking", []), limit=30)}

## Jakość selekcji

### Metody selekcji

{_render_quality_table(summary.get("selection_quality_rows", []))}

## Jakość crossoverów

### Metody crossover

{_render_quality_table(summary.get("crossover_quality_rows", []))}

## Jakość mutacji

### Metody mutacji

{_render_quality_table(summary.get("mutation_quality_rows", []))}

## Wpływ inwersji

### Inwersja

{_render_quality_table(summary.get("inversion_quality_rows", []))}

{_render_boolean_quality_comment(summary.get("inversion_quality_rows", []), "inversion")}

## Wpływ elitaryzmu

### Elitaryzm

{_render_quality_table(summary.get("elitism_quality_rows", []))}

{_render_boolean_quality_comment(summary.get("elitism_quality_rows", []), "elitism")}

## Interpretacja rankingów jakości

- Rankingi jakości są liczone na podstawie **abs error**: im niższa wartość, tym lepiej.
- Warto patrzeć jednocześnie na **mean** i **median**.
- Mean pokazuje ogólną jakość, a median jest odporniejsza na pojedyncze bardzo słabe uruchomienia.
- Jeśli operator ma niską medianę, ale wyższą średnią, to zwykle działa dobrze, ale czasem trafia słabsze przypadki.
- Jeśli operator ma jednocześnie niską średnią i niską medianę, to jest dobrym kandydatem na ustawienie stabilne.
- Porównania `inversion=True/False` oraz `elitism=True/False` pokazują, czy te mechanizmy realnie poprawiają jakość dla tej funkcji.

## Wykresy

{_render_plot_list(summary.get("plot_paths", {}))}

## Błędy

{_render_errors(summary.get("errors", []), limit=10)}
"""
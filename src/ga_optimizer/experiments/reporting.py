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
    return Path("data") / "output" / "tests" / f"{short_name}__{ts}"


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


def _fmt_duration(seconds: Any) -> str:
    if seconds is None:
        return "-"
    try:
        total_seconds = float(seconds)
    except Exception:
        return str(seconds)

    if total_seconds < 60.0:
        return f"{total_seconds:.3f} s"
    if total_seconds < 3600.0:
        return f"{total_seconds / 60.0:.3f} min"
    return f"{total_seconds / 3600.0:.3f} h"


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

    has_median_value = any(row.get("median_value") is not None for row in top_rows[:limit])

    if has_median_value:
        lines = [
            "| rank | best_value | median_value | abs_value_error | nearest_global_min_point_distance | selection_method | crossover_method | mutation_method | population | epochs | run_count | precision_bits |",
            "| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |",
        ]
        for row in top_rows[:limit]:
            lines.append(
                "| {rank} | {best_value} | {median_value} | {abs_value_error} | {nearest_global_min_point_distance} | {selection_method} | {crossover_method} | {mutation_method} | {population} | {epochs} | {run_count} | {precision_bits} |".format(
                    rank=row.get("rank", "-"),
                    best_value=_fmt(row.get("best_value")),
                    median_value=_fmt(row.get("median_value")),
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

    has_median_cols = any(
        row.get("median_point_distance") is not None or row.get("median_best_value") is not None
        for row in rows[:limit]
    )

    if has_median_cols:
        lines = [
            "| group | operator | wins | median_best_value | median_point_distance |",
            "| --- | --- | --- | --- | --- |",
        ]
        for row in rows[:limit]:
            lines.append(
                f"| {row.get('group', '-')} | {row.get('operator', '-')} | {row.get('wins', '-')} | "
                f"{_fmt(row.get('median_best_value', row.get('avg_best_value')))} | {_fmt(row.get('median_point_distance', row.get('avg_abs_error')))} |"
            )
        return "\n".join(lines)

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
        "| label | median | count |",
        "| --- | --- | --- |",
    ]
    for row in rows:
        lines.append(
            f"| {row.get('label', '-')} | {_fmt(row.get('median'))} | {row.get('count', '-')} |"
        )
    return "\n".join(lines)


def _render_boolean_quality_comment(rows: list[dict[str, Any]], feature_name: str) -> str:
    if not rows or len(rows) < 2:
        return f"Brak wystarczających danych, żeby ocenić wpływ ustawienia **{feature_name}**."

    sorted_rows = sorted(rows, key=lambda r: (r.get("median", float("inf")), str(r.get("label", ""))))
    best = sorted_rows[0]
    second = sorted_rows[1]

    if best.get("median") is None or second.get("median") is None:
        return f"Brak wystarczających danych, żeby ocenić wpływ ustawienia **{feature_name}**."

    advantage = float(second["median"]) - float(best["median"])
    return (
        f"Lepiej wypada wariant **{best.get('label')}**. "
        f"Przewaga wg mediany odległości od minimum wynosi około **{advantage:.4f}**."
    )


def _render_success(summary: dict[str, Any]) -> str:
    success = summary.get("success")
    if not success:
        return "_brak danych o sukcesach_"

    return "\n".join(
        [
            f"- Trafienia wg wartości: **{success.get('value_hits')}/{success.get('total')}**",
            f"- Success rate wg wartości: **{_fmt_percent(success.get('value_success_rate'))}**",
            f"- Trafienia wg położenia punktu: **{success.get('point_hits')}/{success.get('total')}**",
            f"- Success rate wg położenia punktu: **{_fmt_percent(success.get('point_success_rate'))}**",
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
- Katalog wynikowy: **{summary.get("output_dir")}**

## Jak interpretować jakość w tym teście

- Główna miara jakości to teraz **odległość od minimum globalnego w przestrzeni argumentów**, czyli `nearest_global_min_point_distance`.
- To znaczy, że patrzymy przede wszystkim na to, **jak blisko prawdziwego minimum leży znaleziony punkt**, a nie tylko jaką ma wartość funkcji.
- To jest ważne zwłaszcza dla funkcji, które mają bardzo strome okolice minimum: można mieć relatywnie duży błąd wartości, a jednocześnie być geometrycznie blisko minimum.
- `Otoczenie minimum` oznacza, że punkt końcowy wpadł w kulę o promieniu `SUCCESS_POINT_DISTANCE_TOL` wokół jednego z minimów globalnych.

## Statystyki wyników

{_render_simple_bullet_stat("Best", summary.get("best_value"))}
{_render_simple_bullet_stat("Q1", summary.get("q1_best_value"))}
{_render_simple_bullet_stat("Median", summary.get("median_best_value"))}
{_render_simple_bullet_stat("Mean", summary.get("mean_best_value"))}
{_render_simple_bullet_stat("Q3", summary.get("q3_best_value"))}
{_render_simple_bullet_stat("Worst", summary.get("worst_best_value"))}
{_render_simple_bullet_stat("Std", summary.get("std_best_value"))}
{_render_simple_bullet_stat("Mean distance to global minimum", summary.get("mean_point_distance"))}
{_render_simple_bullet_stat("Median distance to global minimum", summary.get("median_point_distance"))}
{_render_simple_bullet_stat("Mean abs error wartości", summary.get("mean_abs_error"))}
{_render_simple_bullet_stat("Median abs error wartości", summary.get("median_abs_error"))}

## Sukces algorytmu

{_render_success(summary)}

## Czasy

- Czas całego testu: **{_fmt_duration(summary.get("test_duration_sec"))}**
- Średni czas pojedynczego eksperymentu: **{_fmt_duration(summary.get("mean_duration_sec"))}**
- Mediana czasu pojedynczego eksperymentu: **{_fmt_duration(summary.get("median_duration_sec"))}**

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

- Rankingi jakości są liczone na podstawie **median odległości od minimum globalnego**: im niższa wartość, tym lepiej.
- Średnia nie jest tu używana do porządkowania rankingów jakości.
- W tym teście funkcje są losowane, więc ranking mówi o jakości operatorów **w ujęciu ogólnym**, a nie dla jednej konkretnej funkcji.
- Gdy operator ma niską medianę odległości, oznacza to, że zwykle ląduje blisko prawdziwego minimum, nawet jeśli poszczególne wartości funkcji są między problemami nieporównywalne.

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
- Katalog wynikowy: **{summary.get("output_dir")}**

## Jak interpretować jakość w tym teście

- Główna miara jakości to **odległość od minimum globalnego**, a nie sam błąd wartości funkcji.
- Dzięki temu porównanie jest sensowne także wtedy, gdy funkcja w pobliżu minimum opada bardzo gwałtownie albo ma dużą skalę wartości.
- `Otoczenie minimum` oznacza, że punkt leży w promieniu `SUCCESS_POINT_DISTANCE_TOL` od jednego z minimów globalnych.
- Na wykresie `best vs median in neighbourhood`:
  - **best w otoczeniu** = czy najlepszy uzyskany punkt dla danej funkcji wpada w to otoczenie,
  - **mediana w otoczeniu** = czy mediana odległości dla tej funkcji też wpada w to otoczenie.
- To pozwala odróżnić sytuację „czasem trafiamy dobrze” od „typowy wynik też ląduje blisko minimum”.

## Statystyki wyników

{_render_simple_bullet_stat("Best", summary.get("best_value"))}
{_render_simple_bullet_stat("Q1", summary.get("q1_best_value"))}
{_render_simple_bullet_stat("Median", summary.get("median_best_value"))}
{_render_simple_bullet_stat("Mean", summary.get("mean_best_value"))}
{_render_simple_bullet_stat("Q3", summary.get("q3_best_value"))}
{_render_simple_bullet_stat("Worst", summary.get("worst_best_value"))}
{_render_simple_bullet_stat("Mean distance to global minimum", summary.get("mean_point_distance_across_functions"))}
{_render_simple_bullet_stat("Median distance to global minimum", summary.get("median_point_distance_across_functions"))}

## Sukces algorytmu

{_render_success(summary)}

## Czasy

- Czas całego testu: **{_fmt_duration(summary.get("test_duration_sec"))}**
- Średni czas pojedynczego eksperymentu: **{_fmt_duration(summary.get("mean_duration_sec"))}**
- Mediana czasu pojedynczego eksperymentu: **{_fmt_duration(summary.get("median_duration_sec"))}**

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
- Rankingi jakości operatorów są liczone na podstawie **median odległości od minimum globalnego**.
- Dla wykresów per funkcja używana jest głównie **mediana odległości**, a nie średnia i nie sam błąd wartości.
- Dzięki temu porównanie jest bardziej odporne na pojedyncze wyjątkowo dobre uruchomienia i lepiej pokazuje typowe zachowanie algorytmu.

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
- Nazwa wyświetlana: **{summary.get("problem_display_name")}**
- Wykonań: **{summary.get("executions")}**
- Minimum globalne: **{_fmt(summary.get("global_minimum_value"))}**
- Punkty minimum globalnego: **{summary.get("global_minimum_points")}**
- Katalog wynikowy: **{summary.get("output_dir")}**

## Jak interpretować jakość w tym teście

- Główna miara jakości to **odległość od minimum globalnego**, czyli `nearest_global_min_point_distance`.
- To właśnie ta odległość jest podstawą rankingów operatorów i wykresów jakości.
- Błąd wartości funkcji (`abs_value_error`) nadal jest raportowany pomocniczo, ale nie jest już główną miarą rankingu.
- `Otoczenie minimum` oznacza odległość nie większą niż `SUCCESS_POINT_DISTANCE_TOL` od jednego z minimów globalnych.
- Dla wykresów heatmap:
  - jedna pokazuje zagęszczenie punktów wokół obszaru mediany,
  - druga pokazuje zagęszczenie w najgęstszym lokalnym obszarze punktów.

## Statystyki wyników

{_render_simple_bullet_stat("Best", summary.get("best_value"))}
{_render_simple_bullet_stat("Q1", summary.get("q1_best_value"))}
{_render_simple_bullet_stat("Median", summary.get("median_best_value"))}
{_render_simple_bullet_stat("Mean", summary.get("mean_best_value"))}
{_render_simple_bullet_stat("Q3", summary.get("q3_best_value"))}
{_render_simple_bullet_stat("Worst", summary.get("worst_best_value"))}
{_render_simple_bullet_stat("Mean distance to global minimum", summary.get("mean_point_distance"))}
{_render_simple_bullet_stat("Median distance to global minimum", summary.get("median_point_distance"))}
{_render_simple_bullet_stat("Mean abs error wartości", summary.get("mean_abs_error"))}
{_render_simple_bullet_stat("Median abs error wartości", summary.get("median_abs_error"))}

## Sukces algorytmu

{_render_success(summary)}

## Czasy

- Czas całego testu: **{_fmt_duration(summary.get("test_duration_sec"))}**
- Średni czas pojedynczego eksperymentu: **{_fmt_duration(summary.get("mean_duration_sec"))}**
- Mediana czasu pojedynczego eksperymentu: **{_fmt_duration(summary.get("median_duration_sec"))}**

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

- Rankingi jakości są liczone na podstawie **median odległości od minimum globalnego**: im niższa wartość, tym lepiej.
- Na scatterach linia nie jest regresją liniową — pokazuje **średnią wartość y dla każdego unikalnego x**.
- Osobno raportowane są też rozkłady dla:
  - najlepszych wartości,
  - median wartości końcowej populacji.
- Dzięki temu możesz porównać zarówno „jak dobry bywa najlepszy wynik”, jak i „jak wygląda typowy środek końcowej populacji”.

## Wykresy

{_render_plot_list(summary.get("plot_paths", {}))}

## Błędy

{_render_errors(summary.get("errors", []), limit=10)}
"""
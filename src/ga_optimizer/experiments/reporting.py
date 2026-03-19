from __future__ import annotations

import csv
import json
from datetime import datetime
from pathlib import Path
from typing import Any


def make_experiment_output_dir(test_name: str, preset_name: str) -> Path:
    timestamp = datetime.now().strftime("%Y_%m_%d_%H%M%S")
    output_dir = Path("data") / "output" / "tests" / f"{test_name}_{preset_name}_{timestamp}"
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "plots").mkdir(parents=True, exist_ok=True)
    return output_dir


def save_summary_json(output_dir: Path, data: dict[str, Any]) -> Path:
    path = output_dir / "summary.json"
    with path.open("w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    return path


def save_summary_csv(output_dir: Path, rows: list[dict[str, Any]], filename: str = "summary.csv") -> Path:
    path = output_dir / filename
    if not rows:
        path.write_text("", encoding="utf-8")
        return path

    fieldnames = list(rows[0].keys())
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)

    return path


def save_report_md(output_dir: Path, report_text: str) -> Path:
    path = output_dir / "report.md"
    path.write_text(report_text, encoding="utf-8")
    return path


def _fmt(value: Any, digits: int = 7) -> str:
    if value is None:
        return "-"
    if isinstance(value, float):
        return f"{value:.{digits}f}"
    return str(value)


def _md_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    if not rows:
        return "_Brak danych._"

    header = "| " + " | ".join(columns) + " |"
    sep = "| " + " | ".join(["---"] * len(columns)) + " |"
    body = []
    for row in rows:
        body.append("| " + " | ".join(_fmt(row.get(col)) for col in columns) + " |")
    return "\n".join([header, sep, *body])


def build_random_functions_report(summary: dict[str, Any]) -> str:
    success = summary["success"]
    best = summary["best_overall"]
    worst = summary["worst_overall"]

    lines: list[str] = []
    lines.append(f"# Raport eksperymentu: {summary['test_name']}")
    lines.append("")
    lines.append("## 1. Zakres eksperymentu")
    lines.append("")
    lines.append(f"- Preset: **{summary['preset_name']}**")
    lines.append(f"- Liczba pełnych wykonań: **{summary['executions']}**")
    lines.append(f"- Pula funkcji: **{summary['problem_pool_label']}**")
    lines.append(f"- Próg sukcesu wartości: **abs(error) <= {summary['success_value_abs_tol']}**")
    lines.append(f"- Próg sukcesu punktu: **distance <= {summary['success_point_distance_tol']}**")
    lines.append("")

    lines.append("## 2. Najważniejsze metryki")
    lines.append("")
    lines.append(f"- Średnia najlepszych wartości: **{_fmt(summary['mean_best_value'])}**")
    lines.append(f"- Mediana najlepszych wartości: **{_fmt(summary['median_best_value'])}**")
    lines.append(f"- Odchylenie standardowe najlepszych wartości: **{_fmt(summary['std_best_value'])}**")
    lines.append(f"- Średni błąd bezwzględny wartości: **{_fmt(summary['mean_abs_error'])}**")
    lines.append(f"- Mediana błędu bezwzględnego wartości: **{_fmt(summary['median_abs_error'])}**")
    lines.append(f"- Średnia odległość od najbliższego minimum globalnego: **{_fmt(summary['mean_point_distance'])}**")
    lines.append(f"- Mediana odległości od najbliższego minimum globalnego: **{_fmt(summary['median_point_distance'])}**")
    lines.append(f"- Średni czas wykonania configu: **{_fmt(summary['mean_elapsed'], 3)} s**")
    lines.append("")

    lines.append("## 3. Sukces algorytmu")
    lines.append("")
    lines.append(f"- Trafienia wg wartości: **{success['value_hits']}/{success['total']}**")
    lines.append(f"- Success rate wg wartości: **{_fmt(success['value_success_rate'] * 100.0, 2)}%**")
    lines.append(f"- Trafienia wg punktu: **{success['point_hits']}/{success['total']}**")
    lines.append(f"- Success rate wg punktu: **{_fmt(success['point_success_rate'] * 100.0, 2)}%**")
    lines.append("")

    lines.append("## 4. Najlepszy i najgorszy wynik")
    lines.append("")
    if best:
        lines.append(f"- Najlepszy wynik: funkcja **{best['problem_name']}**, wartość **{_fmt(best['best_value'])}**, abs error **{_fmt(best['abs_value_error'])}**, point distance **{_fmt(best['nearest_global_min_point_distance'])}**")
        lines.append(f"- Operatory najlepszego wyniku: selection **{best['selection_method']}**, crossover **{best['crossover_method']}**, mutation **{best['mutation_method']}**")
    if worst:
        lines.append(f"- Najgorszy wynik: funkcja **{worst['problem_name']}**, wartość **{_fmt(worst['best_value'])}**, abs error **{_fmt(worst['abs_value_error'])}**, point distance **{_fmt(worst['nearest_global_min_point_distance'])}**")
    lines.append("")

    lines.append("## 5. Top konfiguracje")
    lines.append("")
    lines.append(_md_table(
        summary.get("top_rows", []),
        [
            "rank",
            "problem_name",
            "best_value",
            "abs_value_error",
            "nearest_global_min_point_distance",
            "selection_method",
            "crossover_method",
            "mutation_method",
            "population",
            "epochs",
            "run_count",
            "precision_bits",
        ],
    ))
    lines.append("")

    lines.append("## 6. Ranking operatorów")
    lines.append("")
    lines.append(_md_table(
        summary.get("operator_ranking", []),
        ["group", "operator", "wins"],
    ))
    lines.append("")

    lines.append("## 7. Interpretacja")
    lines.append("")
    lines.append("- Ten test losuje jednocześnie funkcję i konfigurację operatorów, więc dobrze nadaje się do ogólnego rekonesansu przestrzeni ustawień.")
    lines.append("- Dwa główne kryteria jakości to: zbieżność wartości funkcji do minimum globalnego oraz zbieżność punktu do jednego z podanych minimów globalnych.")
    lines.append("- Kombinacje operatorów, które często trafiają niskie błędy wartości i małe odległości punktu, są naturalnymi kandydatami do dalszego strojenia.")
    lines.append("")

    lines.append("## 8. Wykresy")
    lines.append("")
    for _, plot_path in summary.get("plot_paths", {}).items():
        if plot_path:
            lines.append(f"- `{plot_path}`")
    lines.append("")

    return "\n".join(lines)


def build_all_functions_report(summary: dict[str, Any]) -> str:
    success = summary["success"]

    lines: list[str] = []
    lines.append(f"# Raport eksperymentu: {summary['test_name']}")
    lines.append("")
    lines.append("## 1. Zakres eksperymentu")
    lines.append("")
    lines.append(f"- Preset: **{summary['preset_name']}**")
    lines.append(f"- Liczba funkcji: **{summary['problem_count']}**")
    lines.append(f"- Wykonań na funkcję: **{summary['executions_per_function']}**")
    lines.append(f"- Łączna liczba pełnych wykonań: **{summary['total_executions']}**")
    lines.append(f"- Próg sukcesu wartości: **abs(error) <= {summary['success_value_abs_tol']}**")
    lines.append(f"- Próg sukcesu punktu: **distance <= {summary['success_point_distance_tol']}**")
    lines.append("")

    lines.append("## 2. Agregaty globalne")
    lines.append("")
    lines.append(f"- Średni błąd bezwzględny po funkcjach: **{_fmt(summary['mean_abs_error_across_functions'])}**")
    lines.append(f"- Mediana błędu bezwzględnego po funkcjach: **{_fmt(summary['median_abs_error_across_functions'])}**")
    lines.append(f"- Średnia odległość punktu od minimum globalnego: **{_fmt(summary['mean_point_distance_across_functions'])}**")
    lines.append(f"- Średni czas najlepszego configu per funkcja: **{_fmt(summary['mean_elapsed_across_functions'], 3)} s**")
    lines.append("")

    lines.append("## 3. Sukces algorytmu")
    lines.append("")
    lines.append(f"- Trafienia wg wartości: **{success['value_hits']}/{success['total']}**")
    lines.append(f"- Success rate wg wartości: **{_fmt(success['value_success_rate'] * 100.0, 2)}%**")
    lines.append(f"- Trafienia wg punktu: **{success['point_hits']}/{success['total']}**")
    lines.append(f"- Success rate wg punktu: **{_fmt(success['point_success_rate'] * 100.0, 2)}%**")
    lines.append("")

    lines.append("## 4. Wyniki per funkcja")
    lines.append("")
    lines.append(_md_table(
        summary.get("rows", []),
        [
            "problem_name",
            "best_value",
            "abs_value_error",
            "nearest_global_min_point_distance",
            "selection_method",
            "crossover_method",
            "mutation_method",
            "population",
            "epochs",
            "run_count",
            "precision_bits",
        ],
    ))
    lines.append("")

    lines.append("## 5. Ranking operatorów")
    lines.append("")
    lines.append(_md_table(
        summary.get("operator_ranking", []),
        ["group", "operator", "wins"],
    ))
    lines.append("")

    lines.append("## 6. Wnioski")
    lines.append("")
    lines.append("- Ten test najlepiej nadaje się do szukania operatorów dobrych „globalnie”, bo każda funkcja dostaje taką samą liczbę prób.")
    lines.append("- Dzięki wykorzystaniu znanych minimów globalnych można porówniać nie tylko same wartości funkcji, ale też to, czy algorytm dociera do właściwego obszaru przestrzeni.")
    lines.append("- Operatory, które często wygrywają na wielu funkcjach, są dobrymi kandydatami na sensowne ustawienia domyślne.")
    lines.append("")

    lines.append("## 7. Wykresy")
    lines.append("")
    for _, plot_path in summary.get("plot_paths", {}).items():
        if plot_path:
            lines.append(f"- `{plot_path}`")
    lines.append("")

    return "\n".join(lines)


def build_single_function_operator_report(summary: dict[str, Any]) -> str:
    success = summary["success"]
    best = summary["best_overall"]
    worst = summary["worst_overall"]
    regions = summary["best_parameter_regions"]

    lines: list[str] = []
    lines.append(f"# Raport eksperymentu: {summary['test_name']}")
    lines.append("")
    lines.append("## 1. Zakres eksperymentu")
    lines.append("")
    lines.append(f"- Preset: **{summary['preset_name']}**")
    lines.append(f"- Funkcja: **{summary['problem_name']}**")
    lines.append(f"- Liczba pełnych wykonań: **{summary['executions']}**")
    lines.append(f"- Minimum globalne wartości: **{_fmt(summary['global_minimum_value'])}**")
    lines.append(f"- Punkty minimum globalnego: **{summary['global_minimum_points']}**")
    lines.append(f"- Próg sukcesu wartości: **abs(error) <= {summary['success_value_abs_tol']}**")
    lines.append(f"- Próg sukcesu punktu: **distance <= {summary['success_point_distance_tol']}**")
    lines.append("")
    lines.append("## 2. Agregaty jakości")
    lines.append("")
    lines.append(f"- Średnia najlepszych wartości: **{_fmt(summary['mean_best_value'])}**")
    lines.append(f"- Mediana najlepszych wartości: **{_fmt(summary['median_best_value'])}**")
    lines.append(f"- Odchylenie standardowe najlepszych wartości: **{_fmt(summary['std_best_value'])}**")
    lines.append(f"- Średni błąd bezwzględny wartości: **{_fmt(summary['mean_abs_error'])}**")
    lines.append(f"- Mediana błędu bezwzględnego wartości: **{_fmt(summary['median_abs_error'])}**")
    lines.append(f"- Średnia odległość od najbliższego minimum globalnego: **{_fmt(summary['mean_point_distance'])}**")
    lines.append(f"- Mediana odległości od najbliższego minimum globalnego: **{_fmt(summary['median_point_distance'])}**")
    lines.append(f"- Średni czas wykonania configu: **{_fmt(summary['mean_elapsed'], 3)} s**")
    lines.append("")
    lines.append("## 3. Sukces algorytmu")
    lines.append("")
    lines.append(f"- Trafienia wg wartości: **{success['value_hits']}/{success['total']}**")
    lines.append(f"- Success rate wg wartości: **{_fmt(success['value_success_rate'] * 100.0, 2)}%**")
    lines.append(f"- Trafienia wg punktu: **{success['point_hits']}/{success['total']}**")
    lines.append(f"- Success rate wg punktu: **{_fmt(success['point_success_rate'] * 100.0, 2)}%**")
    lines.append("")
    lines.append("## 4. Najlepsza i najgorsza kombinacja")
    lines.append("")
    if best:
        lines.append(f"- Najlepsza kombinacja: wartość **{_fmt(best['best_value'])}**, abs error **{_fmt(best['abs_value_error'])}**, point distance **{_fmt(best['nearest_global_min_point_distance'])}**")
        lines.append(f"- Operatory: selection **{best['selection_method']}**, crossover **{best['crossover_method']}**, mutation **{best['mutation_method']}**")
        lines.append(f"- Parametry główne: population **{best['population']}**, epochs **{best['epochs']}**, run_count **{best['run_count']}**, bits **{best['precision_bits']}**")
    if worst:
        lines.append(f"- Najgorsza kombinacja: wartość **{_fmt(worst['best_value'])}**, abs error **{_fmt(worst['abs_value_error'])}**, point distance **{_fmt(worst['nearest_global_min_point_distance'])}**")
    lines.append("")
    lines.append("## 5. Top kombinacje")
    lines.append("")
    lines.append(_md_table(
        summary.get("top_rows", []),
        [
            "rank",
            "best_value",
            "abs_value_error",
            "nearest_global_min_point_distance",
            "selection_method",
            "crossover_method",
            "mutation_method",
            "population",
            "epochs",
            "run_count",
            "precision_bits",
        ],
    ))
    lines.append("")
    lines.append("## 6. Najlepsze obszary parametrów")
    lines.append("")
    lines.append(f"- Top część wyników użyta do estymacji obszarów: **{regions.get('top_count', 0)}** konfiguracji")
    lines.append(f"- Population region: **min={_fmt(regions.get('population_region', {}).get('min'))}, max={_fmt(regions.get('population_region', {}).get('max'))}, mean={_fmt(regions.get('population_region', {}).get('mean'))}, median={_fmt(regions.get('population_region', {}).get('median'))}**")
    lines.append(f"- Epochs region: **min={_fmt(regions.get('epochs_region', {}).get('min'))}, max={_fmt(regions.get('epochs_region', {}).get('max'))}, mean={_fmt(regions.get('epochs_region', {}).get('mean'))}, median={_fmt(regions.get('epochs_region', {}).get('median'))}**")
    lines.append(f"- Run count region: **min={_fmt(regions.get('run_count_region', {}).get('min'))}, max={_fmt(regions.get('run_count_region', {}).get('max'))}, mean={_fmt(regions.get('run_count_region', {}).get('mean'))}, median={_fmt(regions.get('run_count_region', {}).get('median'))}**")
    lines.append(f"- Precision bits region: **min={_fmt(regions.get('precision_bits_region', {}).get('min'))}, max={_fmt(regions.get('precision_bits_region', {}).get('max'))}, mean={_fmt(regions.get('precision_bits_region', {}).get('mean'))}, median={_fmt(regions.get('precision_bits_region', {}).get('median'))}**")
    lines.append("")
    lines.append("### Dominujące operatory w top wynikach")
    lines.append("")
    lines.append(f"- Selection: **{regions.get('selection_modes', {})}**")
    lines.append(f"- Crossover: **{regions.get('crossover_modes', {})}**")
    lines.append(f"- Mutation: **{regions.get('mutation_modes', {})}**")
    lines.append(f"- Inversion: **{regions.get('inversion_modes', {})}**")
    lines.append(f"- Elitism: **{regions.get('elitism_modes', {})}**")
    lines.append("")
    lines.append("### Regiony parametrów metod")
    lines.append("")
    method_regions = regions.get("method_param_regions", {})
    if not method_regions:
        lines.append("- Brak danych o parametrach metod.")
    else:
        for key, value in method_regions.items():
            lines.append(
                f"- `{key}`: min={_fmt(value.get('min'))}, max={_fmt(value.get('max'))}, "
                f"mean={_fmt(value.get('mean'))}, median={_fmt(value.get('median'))}"
            )
    lines.append("")
    lines.append("## 7. Ranking operatorów")
    lines.append("")
    lines.append(_md_table(
        summary.get("operator_ranking", []),
        ["group", "operator", "wins"],
    ))
    lines.append("")
    lines.append("## 8. Interpretacja")
    lines.append("")
    lines.append("- Ten test służy do strojenia jednej konkretnej funkcji.")
    lines.append("- Oprócz najlepszych pojedynczych kombinacji pokazuje też obszary parametrów, które najczęściej pojawiają się w top wynikach.")
    lines.append("- Dzięki wykorzystaniu informacji o punktach minimum globalnego możesz odróżnić konfiguracje, które tylko dają niską wartość funkcji, od tych które rzeczywiście trafiają w poprawny obszar rozwiązania.")
    lines.append("- Najbardziej wartościowe są kombinacje i regiony parametrów, które jednocześnie dają niski błąd wartości, małą odległość punktu i wysokie success rate.")
    lines.append("")
    lines.append("## 9. Wykresy")
    lines.append("")
    for _, plot_path in summary.get("plot_paths", {}).items():
        if plot_path:
            lines.append(f"- `{plot_path}`")
    lines.append("")

    return "\n".join(lines)


def build_sensitivity_report(summary: dict[str, Any]) -> str:
    success = summary["success_by_value"]

    lines: list[str] = []
    lines.append(f"# Raport eksperymentu: {summary['test_name']}")
    lines.append("")
    lines.append("## 1. Zakres eksperymentu")
    lines.append("")
    lines.append(f"- Preset: **{summary['preset_name']}**")
    lines.append(f"- Funkcja: **{summary['problem_name']}**")
    lines.append(f"- Parametr: **{summary['sensitivity_parameter']}**")
    lines.append(f"- Wykonań na wartość parametru: **{summary['executions_per_value']}**")
    lines.append(f"- Minimum globalne wartości: **{_fmt(summary['global_minimum_value'])}**")
    lines.append(f"- Punkty minimum globalnego: **{summary['global_minimum_points']}**")
    lines.append("")

    lines.append("## 2. Wyniki per wartość parametru")
    lines.append("")
    lines.append(_md_table(
        summary.get("rows", []),
        [
            "parameter_value",
            "mean_best_value",
            "median_best_value",
            "best_value",
            "mean_abs_error",
            "mean_point_distance",
            "value_success_rate",
            "point_success_rate",
        ],
    ))
    lines.append("")

    lines.append("## 3. Najlepsza wartość parametru")
    lines.append("")
    best_row = summary.get("best_parameter_row")
    if best_row:
        lines.append(f"- Najlepsza wartość parametru: **{best_row['parameter_value']}**")
        lines.append(f"- Średnia najlepsza wartość: **{_fmt(best_row['mean_best_value'])}**")
        lines.append(f"- Średni abs error: **{_fmt(best_row['mean_abs_error'])}**")
        lines.append(f"- Średnia odległość punktu: **{_fmt(best_row['mean_point_distance'])}**")
    else:
        lines.append("- Brak danych.")
    lines.append("")

    lines.append("## 4. Interpretacja")
    lines.append("")
    lines.append("- Sensitivity test pokazuje, czy zwiększanie badanego parametru daje realną poprawę jakości, czy tylko zwiększa koszt obliczeń.")
    lines.append("- W tym raporcie jakość mierzona jest zarówno przez błąd wartości funkcji, jak i przez odległość od najbliższego znanego minimum globalnego.")
    lines.append("- Najlepsza wartość parametru to taka, która daje niski błąd i rozsądną stabilność, a nie tylko jeden przypadkowo dobry wynik.")
    lines.append("")

    lines.append("## 5. Zagregowane sukcesy")
    lines.append("")
    lines.append(f"- Łączne success rate wg wartości: **{_fmt(success['value_success_rate'] * 100.0, 2)}%**")
    lines.append(f"- Łączne success rate wg punktu: **{_fmt(success['point_success_rate'] * 100.0, 2)}%**")
    lines.append("")

    lines.append("## 6. Wykresy")
    lines.append("")
    for _, plot_path in summary.get("plot_paths", {}).items():
        if plot_path:
            lines.append(f"- `{plot_path}`")
    lines.append("")

    return "\n".join(lines)


def build_ablation_report(summary: dict[str, Any]) -> str:
    lines: list[str] = []
    lines.append(f"# Raport eksperymentu: {summary['test_name']}")
    lines.append("")
    lines.append("## 1. Zakres eksperymentu")
    lines.append("")
    lines.append(f"- Preset: **{summary['preset_name']}**")
    lines.append(f"- Funkcja: **{summary['problem_name']}**")
    lines.append(f"- Wykonań na wariant: **{summary['executions_per_variant']}**")
    lines.append(f"- Minimum globalne wartości: **{_fmt(summary['global_minimum_value'])}**")
    lines.append(f"- Punkty minimum globalnego: **{summary['global_minimum_points']}**")
    lines.append("")

    lines.append("## 2. Wyniki wariantów")
    lines.append("")
    lines.append(_md_table(
        summary.get("rows", []),
        [
            "variant_name",
            "mean_best_value",
            "median_best_value",
            "best_value",
            "mean_abs_error",
            "mean_point_distance",
            "delta_vs_base",
            "value_success_rate",
            "point_success_rate",
        ],
    ))
    lines.append("")

    lines.append("## 3. Najważniejsze obserwacje")
    lines.append("")
    best_variant = summary.get("best_variant")
    worst_variant = summary.get("worst_variant")
    if best_variant:
        lines.append(f"- Najlepszy wariant wg średniej jakości: **{best_variant['variant_name']}**")
    if worst_variant:
        lines.append(f"- Najgorszy wariant wg średniej jakości: **{worst_variant['variant_name']}**")
    lines.append("- Dodatnie `delta_vs_base` oznacza pogorszenie względem wariantu bazowego.")
    lines.append("- Ujemne `delta_vs_base` oznacza poprawę względem wariantu bazowego.")
    lines.append("")

    lines.append("## 4. Interpretacja")
    lines.append("")
    lines.append("- Ablation test pozwala ocenić, które elementy konfiguracji naprawdę pomagają, a które nie są potrzebne.")
    lines.append("- Dzięki użyciu informacji o minimum globalnym można rozróżnić sytuację, w której operator poprawia tylko wartość celu, od sytuacji, w której rzeczywiście prowadzi do poprawnego obszaru minimum.")
    lines.append("")

    lines.append("## 5. Wykresy")
    lines.append("")
    for _, plot_path in summary.get("plot_paths", {}).items():
        if plot_path:
            lines.append(f"- `{plot_path}`")
    lines.append("")

    return "\n".join(lines)
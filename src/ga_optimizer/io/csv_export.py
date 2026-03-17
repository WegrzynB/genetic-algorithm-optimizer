# csv_export.py
# Eksportuje dane wynikowe i historię przebiegu do formatu CSV

import csv
from pathlib import Path
from typing import Any

def export_to_csv(engine_result: dict[str, Any], output_dir: Path) -> None:
    """
    Eksportuje wyniki działania silnika do plików CSV w zadanym folderze.
    Tworzy dwa pliki:
    - runs_summary.csv (podsumowanie każdego uruchomienia)
    - full_history.csv (historia epoka po epoce)
    """
    output_dir.mkdir(parents=True, exist_ok=True)
    
    runs = engine_result.get("runs", [])
    if not runs:
        return

    _export_runs_summary(runs, output_dir / "runs_summary.csv")
    _export_full_history(runs, output_dir / "full_history.csv")


def _export_runs_summary(runs: list[dict[str, Any]], filepath: Path) -> None:
    """Zapisuje podsumowanie poszczególnych uruchomień (runów), w tym najlepszego osobnika."""
    headers = [
        "run_index", "seed", "min_fitness", "q1_fitness", 
        "median_fitness", "q3_fitness", "max_fitness", "avg_fitness", 
        "best_decoded", "best_chromosome", "elapsed_s"
    ]
    
    with open(filepath, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        
        for run in runs:
            summary = run.get("summary", {})
            writer.writerow([
                run.get("run_index"),
                run.get("seed"),
                summary.get("min_fitness"),
                summary.get("q1_fitness"),
                summary.get("median_fitness"),
                summary.get("q3_fitness"),
                summary.get("max_fitness"),
                summary.get("avg_fitness"),
                summary.get("best_decoded"),     # Zdekodowane zmienne x1, x2...
                summary.get("best_chromosome"),  # Surowe geny
                run.get("elapsed")
            ])


def _export_full_history(runs: list[dict[str, Any]], filepath: Path) -> None:
    """Zapisuje szczegółową historię każdej epoki dla wszystkich uruchomień."""
    headers = [
        "run_index", "epoch_index", "min_fitness", "q1_fitness", 
        "median_fitness", "q3_fitness", "max_fitness", "avg_fitness"
    ]
    
    with open(filepath, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        
        for run in runs:
            run_idx = run.get("run_index")
            history = run.get("history", [])
            
            for epoch in history:
                summary = epoch.get("summary", {})
                writer.writerow([
                    run_idx,
                    epoch.get("epoch_index"),
                    summary.get("min_fitness"),
                    summary.get("q1_fitness"),
                    summary.get("median_fitness"),
                    summary.get("q3_fitness"),
                    summary.get("max_fitness"),
                    summary.get("avg_fitness")
                ])
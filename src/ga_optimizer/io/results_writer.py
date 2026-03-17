# Zapisuje wyniki uruchomień do plików i odpowiednich folderów
# src/ga_optimizer/io/results_writer.py

from pathlib import Path
from datetime import datetime
from typing import Any

from ga_optimizer.io.csv_export import export_to_csv
from ga_optimizer.io.json_export import export_to_json

def save_run_results(engine_result: dict[str, Any], format_type: str = "all") -> str:
    """
    Główna funkcja zapisująca wyniki uruchomienia algorytmu.
    Tworzy folder data/output/runs/run_YYYY_MM_DD_HHMMSS/ i wywołuje odpowiednie eksportery.
    
    :param format_type: 'csv', 'json' lub 'all'
    :return: Ścieżka do utworzonego folderu.
    """
    # 1. Tworzenie głównego folderu z datą i czasem
    base_dir = Path("data/output/runs")
    base_dir.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%Y_%m_%d_%H%M%S")
    run_dir = base_dir / f"run_{timestamp}"
    run_dir.mkdir(parents=True, exist_ok=True)

    format_type = format_type.lower()

    # 2. Odpalanie poszczególnych eksporterów
    if format_type in ("csv", "all"):
        export_to_csv(engine_result, run_dir)
        
    if format_type in ("json", "all"):
        export_to_json(engine_result, run_dir)

    print(f"[I/O] Pomyślnie zapisano wyniki w formacie '{format_type}' do: {run_dir}")
    return str(run_dir)
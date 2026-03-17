# Eksportuje konfiguracje i metryki do formatu JSON
# src/ga_optimizer/io/json_export.py

import json
from pathlib import Path
from typing import Any

from ga_optimizer.io.serializers import SafeJSONEncoder

def export_to_json(engine_result: dict[str, Any], output_dir: Path) -> None:
    """
    Eksportuje pełne dane wynikowe algorytmu do pliku JSON w zadanym folderze.
    """
    output_dir.mkdir(parents=True, exist_ok=True)
    filepath = output_dir / "full_results.json"
    
    with open(filepath, mode="w", encoding="utf-8") as f:
        json.dump(
            engine_result, 
            f, 
            indent=4, 
            ensure_ascii=False, 
            cls=SafeJSONEncoder
        )
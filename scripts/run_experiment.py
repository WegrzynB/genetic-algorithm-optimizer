from __future__ import annotations

# JAK UŻYĆ:
# 1. Otwórz: src/ga_optimizer/experiments/experiment_config.py
# 2. Ustaw test w:
#    ACTIVE_EXPERIMENT_NAME = "single_function_operator_search_default"
#    dostępne też:
#    - "random_functions_default"
#    - "all_functions_global_default"
#    - "sensitivity_default"
#    - "ablation_default"
# 3. Jeśli test jest jednofunkcyjny, ustaw funkcję w:
#    TARGET_PROBLEM_NAME = "Rosenbrock"
# 4. Liczbę wykonań testów zmieniasz też w experiment_config.py
#    (np. SINGLE_FUNCTION_EXECUTIONS, RANDOM_FUNCTIONS_EXECUTIONS itd.)
# 5. Uruchamiasz normalnie:
#    python scripts/run_experiment.py
# 6. Wyniki zapisują się do:
#    data/output/tests/...
#    Najpierw czytaj: report.md

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = PROJECT_ROOT / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from ga_optimizer.experiments.experiment_config import ACTIVE_EXPERIMENT_NAME, EXPERIMENT_PRESETS
from ga_optimizer.experiments.experiments import run_experiment_by_name


def main() -> None:
    if ACTIVE_EXPERIMENT_NAME not in EXPERIMENT_PRESETS:
        raise KeyError(
            f"Nieznany ACTIVE_EXPERIMENT_NAME: {ACTIVE_EXPERIMENT_NAME}. "
            f"Sprawdź src/ga_optimizer/experiments/experiment_config.py"
        )

    preset = EXPERIMENT_PRESETS[ACTIVE_EXPERIMENT_NAME]

    print("\n=== RUN EXPERIMENT ===")
    print(f"Aktywny preset: {ACTIVE_EXPERIMENT_NAME}")
    print(f"Typ testu: {preset['test_name']}")
    print(f"Opis: {preset.get('description', '-')}")
    print("======================\n")

    result = run_experiment_by_name(
        name=preset["test_name"],
        preset_name=ACTIVE_EXPERIMENT_NAME,
        preset=preset,
    )

    print("\n=== EKSPERYMENT ZAKOŃCZONY ===")
    print(f"Preset: {ACTIVE_EXPERIMENT_NAME}")
    print(f"Test: {result.get('test_name')}")
    print(f"Katalog wynikowy: {result.get('output_dir')}")
    print("==============================\n")


if __name__ == "__main__":
    main()
# presets.py
# Presety konfiguracji GUI.

from copy import deepcopy

from ga_optimizer.config.schema import GAConfig
from ga_optimizer.config.defaults import build_default_config


def _config_to_preset_dict(config: GAConfig) -> dict:
    # Zamienia obiekt configu na zwykły słownik presetu.
    return {
        "problem_name": config.problem_name,
        "objective_mode": config.objective_mode,
        "n_vars": config.n_vars,
        "range_start": config.range_start,
        "range_end": config.range_end,
        "population": config.population,
        "epochs": config.epochs,
        "run_count": config.run_count,
        "seed": config.seed,
        "precision_mode": config.precision_mode,
        "precision_numeric": config.precision_numeric,
        "precision_bits": config.precision_bits,
        "selection_method": config.selection_method,
        "crossover_method": config.crossover_method,
        "mutation_method": config.mutation_method,
        "inversion_enabled": config.inversion_enabled,
        "elitism_enabled": config.elitism_enabled,
        "method_params": deepcopy(config.method_params),
    }


_default_cfg = build_default_config()
DEFAULT_PRESET = _config_to_preset_dict(_default_cfg)

TEST_CUSTOM_PRESET = deepcopy(DEFAULT_PRESET)
TEST_CUSTOM_PRESET.update(
    {
        "population": 20,
        "epochs": 15,
        "run_count": 3,
        "seed": 123,
        "precision_mode": "bits",
        "precision_bits": 10,
        "selection_method": "tournament",
        "crossover_method": "two_point",
        "mutation_method": "scramble",
        "inversion_enabled": False,
        "elitism_enabled": False,
        "method_params": {
            **deepcopy(DEFAULT_PRESET["method_params"]),
            # wpisz tylko te klucze, które faktycznie istnieją u Ciebie
            "selection_tournament_k": 8,
            "crossover_two_point_p": 0.5,
            "mutation_scramble_p": 0.6,
        },
    }
)

PRESETS = {
    "Default": DEFAULT_PRESET,
    "test_custom": TEST_CUSTOM_PRESET,
}
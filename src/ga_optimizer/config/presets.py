# presets.py
# Proste presety do szybkiej zmiany charakteru eksperymentu.

from copy import deepcopy

from ga_optimizer.config.defaults import build_default_config
from ga_optimizer.config.schema import (
    CROSSOVER_METHOD_PARAM_SPECS,
    GAConfig,
    MUTATION_METHOD_PARAM_SPECS,
    SELECTION_METHOD_PARAM_SPECS,
)


PRESETS = {
    "quick": {
        "population": 40,
        "epochs": 50,
        "epsilon": 0.01,
        "precision_mode": "Dokładność liczbowa",
        "precision_numeric": 0.01,
        "selection_method": "Tournament",
        "crossover_method": "One point",
        "mutation_method": "One point",
        "method_params": {
            "tournament_k": 3,
            "crossover_p": 0.7,
            "mutation_p": 0.03,
        },
    },
    "standard": {
        "population": 100,
        "epochs": 200,
        "epsilon": 0.0001,
        "precision_mode": "Dokładność liczbowa",
        "precision_numeric": 0.001,
        "selection_method": "Tournament",
        "crossover_method": "Two point",
        "mutation_method": "One point",
        "method_params": {
            "tournament_k": 3,
            "crossover_p": 0.8,
            "mutation_p": 0.02,
        },
    },
    "accurate": {
        "population": 250,
        "epochs": 800,
        "epsilon": 0.000001,
        "precision_mode": "Dokładność liczbowa",
        "precision_numeric": 0.0001,
        "selection_method": "Tournament",
        "crossover_method": "Uniform",
        "mutation_method": "Two point",
        "method_params": {
            "tournament_k": 5,
            "crossover_p": 0.9,
            "uniform_gene_p": 0.5,
            "mutation_p": 0.01,
        },
    },
}


def _fill_missing_active_method_defaults(config: GAConfig) -> None:
    for spec in SELECTION_METHOD_PARAM_SPECS.get(config.selection_method, []):
        config.method_params.setdefault(spec["key"], deepcopy(spec.get("default")))

    for spec in CROSSOVER_METHOD_PARAM_SPECS.get(config.crossover_method, []):
        config.method_params.setdefault(spec["key"], deepcopy(spec.get("default")))

    for spec in MUTATION_METHOD_PARAM_SPECS.get(config.mutation_method, []):
        config.method_params.setdefault(spec["key"], deepcopy(spec.get("default")))


def apply_preset(
    preset_name: str,
    base_config: GAConfig | None = None,
) -> GAConfig:
    if preset_name not in PRESETS:
        raise KeyError(f"Nieznany preset: {preset_name}")

    preset = PRESETS[preset_name]
    config = deepcopy(base_config) if base_config is not None else build_default_config()

    for key, value in preset.items():
        if key == "method_params":
            continue
        setattr(config, key, value)

    method_params = deepcopy(config.method_params)
    method_params.update(deepcopy(preset.get("method_params", {})))
    config.method_params = method_params

    _fill_missing_active_method_defaults(config)
    return config
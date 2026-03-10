# schema.py
# Jedno źródło prawdy dla struktury konfiguracji i specyfikacji pól formularza.

from dataclasses import dataclass, field
from typing import Any

from ga_optimizer.config.method_crossover import (
    CROSSOVER_METHOD_LABELS,
    CROSSOVER_METHOD_PARAM_SPECS,
)
from ga_optimizer.config.method_mutation import (
    MUTATION_METHOD_LABELS,
    MUTATION_METHOD_PARAM_SPECS,
)
from ga_optimizer.config.method_selection import (
    SELECTION_METHOD_LABELS,
    SELECTION_METHOD_PARAM_SPECS,
)


def build_reverse_labels_map(labels_map: dict[str, str]) -> dict[str, str]:
    # Buduje mapowanie odwrotne: label -> key.
    return {label: key for key, label in labels_map.items()}


PRECISION_MODE_LABELS = {
    "numeric": "Dokładność liczbowa",
    "bits": "Liczba bitów",
}

PRECISION_MODE_OPTIONS = list(PRECISION_MODE_LABELS.keys())
PRECISION_MODE_LABELS_REVERSED = build_reverse_labels_map(PRECISION_MODE_LABELS)

SELECTION_METHOD_OPTIONS = list(SELECTION_METHOD_PARAM_SPECS.keys())
SELECTION_METHOD_LABELS_REVERSED = build_reverse_labels_map(SELECTION_METHOD_LABELS)

CROSSOVER_METHOD_OPTIONS = list(CROSSOVER_METHOD_PARAM_SPECS.keys())
CROSSOVER_METHOD_LABELS_REVERSED = build_reverse_labels_map(CROSSOVER_METHOD_LABELS)

MUTATION_METHOD_OPTIONS = list(MUTATION_METHOD_PARAM_SPECS.keys())
MUTATION_METHOD_LABELS_REVERSED = build_reverse_labels_map(MUTATION_METHOD_LABELS)


GENERAL_FIELD_SPECS = {
    "problem_name": {
        "label": "Wybór funkcji",
        "type": "enum",
        "values": [],
        "default": "Hypersphere",
    },
    "n_vars": {
        "label": "Liczba zmiennych",
        "type": "int",
        "min": 1,
        "default": 2,
    },
    "range_start": {
        "label": "Przedział: Początek",
        "type": "float",
        "default": -5.0,
    },
    "range_end": {
        "label": "Przedział: Koniec",
        "type": "float",
        "default": 5.0,
    },
}

GA_MAIN_FIELD_SPECS = {
    "population": {
        "label": "Wielkość populacji",
        "type": "int",
        "min": 2,
        "default": 100,
    },
    "epochs": {
        "label": "Liczba epok",
        "type": "int",
        "min": 1,
        "default": 200,
    },
    "epsilon": {
        "label": "Epsilon (tolerancja / warunek stopu)",
        "type": "float",
        "min_exclusive": 0.0,
        "default": 0.0001,
    },
    "seed": {
        "label": "Seed",
        "type": "int",
        "default": 42,
    },
}

PRECISION_FIELD_SPECS = {
    "precision_mode": {
        "label": "Rodzaj dokładności",
        "type": "enum",
        "values": PRECISION_MODE_OPTIONS,
        "default": "numeric",
    },
    "precision_numeric": {
        "label": "Dokładność (np. 0.001)",
        "type": "float",
        "min_exclusive": 0.0,
        "default": 0.001,
    },
    "precision_bits": {
        "label": "Liczba bitów",
        "type": "int",
        "min": 1,
        "default": 16,
    },
}

OPERATOR_FIELD_SPECS = {
    "selection_method": {
        "label": "Metoda selekcji",
        "type": "enum",
        "values": SELECTION_METHOD_OPTIONS,
        "default": "roulette",
    },
    "crossover_method": {
        "label": "Metoda krzyżowania",
        "type": "enum",
        "values": CROSSOVER_METHOD_OPTIONS,
        "default": "one_point",
    },
    "mutation_method": {
        "label": "Metoda mutacji",
        "type": "enum",
        "values": MUTATION_METHOD_OPTIONS,
        "default": "one_point",
    },
    "inversion_enabled": {
        "label": "Wybór operatora inwersji",
        "type": "bool",
        "default": False,
    },
    "elitism_enabled": {
        "label": "Wybór strategii elitarnej",
        "type": "bool",
        "default": False,
    },
}

METHOD_PARAM_SPECS = {
    "selection": SELECTION_METHOD_PARAM_SPECS,
    "crossover": CROSSOVER_METHOD_PARAM_SPECS,
    "mutation": MUTATION_METHOD_PARAM_SPECS,
}


@dataclass
class GAConfig:
    # Główny model konfiguracji aplikacji.
    problem_name: str
    n_vars: int
    range_start: float
    range_end: float

    population: int
    epochs: int
    epsilon: float
    seed: int

    precision_mode: str
    precision_numeric: float
    precision_bits: int

    selection_method: str
    crossover_method: str
    mutation_method: str

    inversion_enabled: bool
    elitism_enabled: bool

    method_params: dict[str, Any] = field(default_factory=dict)

    def get_active_method_specs(self) -> dict[str, list[dict[str, Any]]]:
        # Zwraca tylko parametry aktywnych metod.
        return {
            "selection": SELECTION_METHOD_PARAM_SPECS.get(self.selection_method, []),
            "crossover": CROSSOVER_METHOD_PARAM_SPECS.get(self.crossover_method, []),
            "mutation": MUTATION_METHOD_PARAM_SPECS.get(self.mutation_method, []),
        }

    def get_active_method_param_keys(self) -> list[str]:
        # Zwraca klucze aktywnych parametrów metod.
        keys: list[str] = []
        for specs in self.get_active_method_specs().values():
            keys.extend([spec["key"] for spec in specs])
        return keys


def get_flat_method_param_specs() -> dict[str, dict[str, Any]]:
    # Spłaszcza specyfikacje parametrów metod do jednego słownika.
    flat_specs: dict[str, dict[str, Any]] = {}

    for group_specs in METHOD_PARAM_SPECS.values():
        for method_specs in group_specs.values():
            for spec in method_specs:
                flat_specs[spec["key"]] = spec

    return flat_specs


def get_all_static_field_specs() -> dict[str, dict[str, Any]]:
    # Zwraca wszystkie specyfikacje pól w jednej mapie.
    specs: dict[str, dict[str, Any]] = {}
    specs.update(GENERAL_FIELD_SPECS)
    specs.update(GA_MAIN_FIELD_SPECS)
    specs.update(PRECISION_FIELD_SPECS)
    specs.update(OPERATOR_FIELD_SPECS)
    specs.update(get_flat_method_param_specs())
    return specs


def get_method_specs(group: str, method_name: str) -> list[dict[str, Any]]:
    # Zwraca specyfikacje parametrów dla konkretnej grupy i metody.
    return METHOD_PARAM_SPECS.get(group, {}).get(method_name, [])
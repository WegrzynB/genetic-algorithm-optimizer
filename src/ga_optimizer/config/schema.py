# schema.py
# Jedno źródło prawdy dla struktury konfiguracji i specyfikacji pól formularza.

from dataclasses import dataclass, field
from typing import Any


PRECISION_MODE_OPTIONS = [
    "Dokładność liczbowa",
    "Liczba bitów",
]

SELECTION_METHOD_OPTIONS = [
    "Best",
    "Roulette",
    "Tournament",
]

CROSSOVER_METHOD_OPTIONS = [
    "One point",
    "Two point",
    "Uniform",
    "Granular",
]

MUTATION_METHOD_OPTIONS = [
    "Edge",
    "One point",
    "Two point",
]


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
        "default": "Dokładność liczbowa",
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
        "default": "Tournament",
    },
    "crossover_method": {
        "label": "Metoda krzyżowania",
        "type": "enum",
        "values": CROSSOVER_METHOD_OPTIONS,
        "default": "Two point",
    },
    "mutation_method": {
        "label": "Metoda mutacji",
        "type": "enum",
        "values": MUTATION_METHOD_OPTIONS,
        "default": "One point",
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

# Parametry metod selekcji.
SELECTION_METHOD_PARAM_SPECS = {
    "Best": [
        {
            "key": "best_k",
            "label": "K (ile najlepszych)",
            "type": "int",
            "default": 2,
            "min": 1,
        },
    ],
    "Roulette": [
        {
            "key": "roulette_eps",
            "label": "Eps (stabilizacja)",
            "type": "float",
            "default": 1e-9,
            "min_exclusive": 0.0,
        },
    ],
    "Tournament": [
        {
            "key": "tournament_k",
            "label": "K (rozmiar turnieju)",
            "type": "int",
            "default": 3,
            "min": 2,
        },
        {
            "key": "tournament_2",
            "label": "K2",
            "type": "int",
            "default": 3,
            "min": 2,
        },
        {
            "key": "tournament_3",
            "label": "K3",
            "type": "int",
            "default": 23,
            "min": 2,
        },
        {
            "key": "tournament_4",
            "label": "K4",
            "type": "int",
            "default": 63,
            "min": 2,
        },
        {
            "key": "tournament_5",
            "label": "K5",
            "type": "int",
            "default": 33,
            "min": 2,
        },
        {
            "key": "tournament_6",
            "label": "K6",
            "type": "int",
            "default": 3,
            "min": 2,
        },
        {
            "key": "tournament_7",
            "label": "K7",
            "type": "int",
            "default": 7,
            "min": 2,
        },
        
    ],
}

# Parametry metod krzyżowania.
CROSSOVER_METHOD_PARAM_SPECS = {
    "One point": [
        {
            "key": "crossover_p_one",
            "label": "P (krzyżowanie)",
            "type": "float",
            "default": 0.2,
            "min": 0.0,
            "max": 1.0,
        },
    ],
    "Two point": [
        {
            "key": "crossover_p_two",
            "label": "P (krzyżowanie)",
            "type": "float",
            "default": 0.4,
            "min": 0.0,
            "max": 1.0,
        },
    ],
    "Uniform": [
        {
            "key": "crossover_p_uniform",
            "label": "P (krzyżowanie)",
            "type": "float",
            "default": 0.3,
            "min": 0.0,
            "max": 1.0,
        },
        {
            "key": "uniform_gene_p",
            "label": "P (gen od rodzica A)",
            "type": "float",
            "default": 0.5,
            "min": 0.0,
            "max": 1.0,
        },
    ],
    "Granular": [
        {
            "key": "crossover_p_granular",
            "label": "P (krzyżowanie)",
            "type": "float",
            "default": 0.8,
            "min": 0.0,
            "max": 1.0,
        },
        {
            "key": "granularity",
            "label": "Ziarnistość",
            "type": "int",
            "default": 2,
            "min": 1,
        },
    ],
}

# Parametry metod mutacji.
MUTATION_METHOD_PARAM_SPECS = {
    "Edge": [
        {
            "key": "mutation_p_edge",
            "label": "P (mutacja)",
            "type": "float",
            "default": 0.02,
            "min": 0.0,
            "max": 1.0,
        },
        {
            "key": "edge_mode",
            "label": "Tryb brzegowy",
            "type": "enum",
            "values": ["Ends", "First_last", "Both"],
            "default": "Ends",
        },
    ],
    "One point": [
        {
            "key": "mutation_p_one",
            "label": "P (mutacja)",
            "type": "float",
            "default": 0.05,
            "min": 0.0,
            "max": 1.0,
        },
    ],
    "Two point": [
        {
            "key": "mutation_p_two",
            "label": "P (mutacja)",
            "type": "float",
            "default": 0.07,
            "min": 0.0,
            "max": 1.0,
        },
    ],
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
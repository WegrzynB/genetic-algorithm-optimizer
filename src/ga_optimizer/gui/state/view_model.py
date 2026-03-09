# view_model.py
# Przechowuje i synchronizuje stan interfejsu między widokami a kontrolerami

import tkinter as tk


# Specyfikacja pól ogólnych (problem, liczba zmiennych, przedział poszukiwań)
FIELDS_GENERAL = {
    "problem": {
        "label": "Wybór funkcji",
        "type": "enum",
        "values": ["Rosenbrock", "Sphere", "Rastrigin"],
        "default": "Rosenbrock",
    },

    "n_vars": {
        "label": "Liczba zmiennych",
        "type": "int",
        "min": 1,
        "default": 5
    },

    "range_start": {
        "label": "Przedział: Początek",
        "type": "float",
        "default": -5.0
    },

    "range_end": {
        "label": "Przedział: Koniec",
        "type": "float",
        "default": 5.0
    },
}

# Specyfikacja podstawowych parametrów algorytmu genetycznego (populacja, epoki, epsilon, seed)
FIELDS_GA_MAIN = {
    "population": {"label": "Wielkość populacji", "type": "int", "min": 2, "default": 100},
    "epochs": {"label": "Liczba epok", "type": "int", "min": 1, "default": 200},
    "epsilon": {"label": "Epsilon (tolerancja / warunek stopu)", "type": "float", "default": 0.0001},
    "seed": {"label": "Seed", "type": "int", "default": 42},
}

# Specyfikacja ustawień dokładności kodowania (tryb i wartość zależna od trybu)
FIELDS_PRECISION = {
    "precision_mode": {
        "label": "Rodzaj dokładności",
        "type": "enum",
        "values": ["Dokładność liczbowa", "Liczba bitów"],
        "default": "Dokładność liczbowa",
    },
    "precision_numeric": {"label": "Dokładność (np. 0.001)", "type": "float", "min": 0.0, "default": 0.001},
    "precision_bits": {"label": "Liczba bitów", "type": "int", "min": 1, "default": 16},
}

# Specyfikacja wyboru operatorów GA i dodatkowych przełączników (inwersja, elitaryzm)
FIELDS_OPERATORS = {
    "selection_method": {
        "label": "Metoda selekcji",
        "type": "enum",
        "values": ["Best", "Roulette", "Tournament"],
        "default": "Tournament",
    },
    "crossover_method": {
        "label": "Metoda krzyżowania",
        "type": "enum",
        "values": ["One point", "Two point", "Uniform", "Granular"],
        "default": "Two point",
    },
    "mutation_method": {
        "label": "Metoda mutacji",
        "type": "enum",
        "values": ["Edge", "One point", "Two point"],
        "default": "One point",
    },
    "inversion_enabled": {"label": "Wybór operatora inwersji", "type": "bool", "default": False},
    "elitism_enabled": {"label": "Wybór strategii elitarnej", "type": "bool", "default": False},
}

# Specyfikacja parametrów metod dla selekcji/krzyżowania/mutacji (GUI buduje z tego pola w zakładkach)
METHOD_PARAM_SPECS = {
    "selection": {
        "Best": [
            {"key": "best_k", "label": "K (ile najlepszych)", "type": "int", "default": 2, "min": 1},
        ],
        "Roulette": [
            {"key": "roulette_eps", "label": "Eps (stabilizacja)", "type": "float", "default": 1e-9, "min": 0.0},
        ],
        "Tournament": [
            {"key": "tournament_k", "label": "K (rozmiar turnieju)", "type": "int", "default": 3, "min": 2},
            {"key": "tournament_k2", "label": "K2 (rozmiar turnieju)", "type": "int", "default": 7, "min": 2},
            {"key": "tournament_k3", "label": "K3 (rozmiar turnieju)", "type": "int", "default": 3, "min": 2},
            {"key": "tournament_k4", "label": "K4 (rozmiar turnieju)", "type": "int", "default": 322, "min": 2},
            {"key": "tournament_k5", "label": "K5 (rozmiar turnieju)", "type": "int", "default": 31, "min": 2},
            {"key": "tournament_k6", "label": "K6 (rozmiar turnieju)", "type": "int", "default": 32, "min": 2},
            {"key": "tournament_k7", "label": "K7 (rozmiar turnieju)", "type": "int", "default": 33, "min": 2},
            {"key": "tournament_k8", "label": "K8 (rozmiar turnieju)", "type": "int", "default": 34, "min": 2},
        ],
    },
    "crossover": {
        "One point": [
            {"key": "crossover_p", "label": "P (krzyżowanie)", "type": "float", "default": 0.8, "min": 0.0, "max": 1.0},
        ],
        "Two point": [
            {"key": "crossover_p", "label": "P (krzyżowanie)", "type": "float", "default": 0.8, "min": 0.0, "max": 1.0},
        ],
        "Uniform": [
            {"key": "crossover_p", "label": "P (krzyżowanie)", "type": "float", "default": 0.8, "min": 0.0, "max": 1.0},
            {"key": "uniform_gene_p", "label": "P (gen od rodzica A)", "type": "float", "default": 0.5, "min": 0.0, "max": 1.0},
        ],
        "Granular": [
            {"key": "crossover_p", "label": "P (krzyżowanie)", "type": "float", "default": 0.8, "min": 0.0, "max": 1.0},
            {"key": "granularity", "label": "Ziarnistość", "type": "int", "default": 2, "min": 1},
        ],
    },
    "mutation": {
        "Edge": [
            {"key": "mutation_p", "label": "P (mutacja)", "type": "float", "default": 0.02, "min": 0.0, "max": 1.0},
            {"key": "edge_mode", "label": "Tryb brzegowy", "type": "enum", "values": ["Ends", "First_last", "Both"], "default": "Ends"},
        ],
        "One point": [
            {"key": "mutation_p", "label": "P (mutacja)", "type": "float", "default": 0.02, "min": 0.0, "max": 1.0},
        ],
        "Two point": [
            {"key": "mutation_p", "label": "P (mutacja)", "type": "float", "default": 0.02, "min": 0.0, "max": 1.0},
        ],
    },
}


class ViewModel:
    def __init__(self, root: tk.Misc):
        # Zmienne GUI dla wyboru problemu i ustawień ogólnych
        self.problem = tk.StringVar(root, value=str(FIELDS_GENERAL["problem"]["default"]))
        self.n_vars = tk.StringVar(root, value=str(FIELDS_GENERAL["n_vars"]["default"]))
        self.range_start = tk.StringVar(root, value=str(FIELDS_GENERAL["range_start"]["default"]))
        self.range_end = tk.StringVar(root, value=str(FIELDS_GENERAL["range_end"]["default"]))

        # Zmienne GUI dla podstawowych parametrów GA
        self.population = tk.StringVar(root, value=str(FIELDS_GA_MAIN["population"]["default"]))
        self.epochs = tk.StringVar(root, value=str(FIELDS_GA_MAIN["epochs"]["default"]))
        self.epsilon = tk.StringVar(root, value=str(FIELDS_GA_MAIN["epsilon"]["default"]))
        self.seed = tk.StringVar(root, value=str(FIELDS_GA_MAIN["seed"]["default"]))

        # Zmienne GUI dla trybu dokładności oraz wartości zależnej od trybu
        self.precision_mode = tk.StringVar(root, value=str(FIELDS_PRECISION["precision_mode"]["default"]))
        self.precision_numeric = tk.StringVar(root, value=str(FIELDS_PRECISION["precision_numeric"]["default"]))
        self.precision_bits = tk.StringVar(root, value=str(FIELDS_PRECISION["precision_bits"]["default"]))

        # Zmienne GUI dla wyboru operatorów GA
        self.selection_method = tk.StringVar(root, value=str(FIELDS_OPERATORS["selection_method"]["default"]))
        self.crossover_method = tk.StringVar(root, value=str(FIELDS_OPERATORS["crossover_method"]["default"]))
        self.mutation_method = tk.StringVar(root, value=str(FIELDS_OPERATORS["mutation_method"]["default"]))

        # Zmienne GUI dla przełączników dodatkowych (inwersja, elitaryzm)
        self.inversion_enabled = tk.BooleanVar(root, value=bool(FIELDS_OPERATORS["inversion_enabled"]["default"]))
        self.elitism_enabled = tk.BooleanVar(root, value=bool(FIELDS_OPERATORS["elitism_enabled"]["default"]))

        # Słownik zmiennych GUI dla parametrów zależnych od wybranej metody (np. tournament_k)
        self.method_params = {}
        self._init_method_params(root)

    def _init_method_params(self, root: tk.Misc) -> None:
        # Tworzy tk.StringVar dla każdego parametru metod, aby GUI mogło łatwo wiązać pola z danymi
        for group, methods in METHOD_PARAM_SPECS.items():
            for _, params in methods.items():
                for p in params:
                    key = p["key"]
                    if key in self.method_params:
                        continue
                    self.method_params[key] = tk.StringVar(root, value=str(p.get("default", "")))
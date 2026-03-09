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
        "default": 5,
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

# Specyfikacja podstawowych parametrów algorytmu genetycznego (populacja, epoki, epsilon, seed)
FIELDS_GA_MAIN = {
    "population": {"label": "Wielkość populacji", "type": "int", "min": 2, "default": 100},
    "epochs": {"label": "Liczba epok", "type": "int", "min": 1, "default": 200},
    "epsilon": {
        "label": "Epsilon (tolerancja / warunek stopu)",
        "type": "float",
        "min_exclusive": 0.0,
        "default": 0.0001,
    },
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
    "precision_numeric": {
        "label": "Dokładność (np. 0.001)",
        "type": "float",
        "min_exclusive": 0.0,
        "default": 0.001,
    },
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

        # Rejestr specyfikacji i powiązanych zmiennych.
        # Dzięki temu GUI może łatwo pytać VM o reguły walidacji dla konkretnego pola.
        self.field_specs = self._build_field_specs()
        self.field_vars = self._build_field_vars()

    def _init_method_params(self, root: tk.Misc) -> None:
        # Tworzy tk.StringVar dla każdego parametru metod, aby GUI mogło łatwo wiązać pola z danymi
        for group, methods in METHOD_PARAM_SPECS.items():
            for _, params in methods.items():
                for p in params:
                    key = p["key"]
                    if key in self.method_params:
                        continue
                    self.method_params[key] = tk.StringVar(root, value=str(p.get("default", "")))

    def _build_field_specs(self) -> dict:
        # Spłaszcza wszystkie specyfikacje do jednego słownika:
        # key -> spec. Ułatwia to późniejszą walidację i budowę widgetów.
        specs = {}
        specs.update(FIELDS_GENERAL)
        specs.update(FIELDS_GA_MAIN)
        specs.update(FIELDS_PRECISION)

        for methods in METHOD_PARAM_SPECS.values():
            for params in methods.values():
                for param in params:
                    specs[param["key"]] = param

        return specs

    def _build_field_vars(self) -> dict:
        # Mapowanie klucz pola -> tk.Variable.
        # To jest główny punkt dostępu dla logiki walidacji.
        vars_map = {
            "problem": self.problem,
            "n_vars": self.n_vars,
            "range_start": self.range_start,
            "range_end": self.range_end,
            "population": self.population,
            "epochs": self.epochs,
            "epsilon": self.epsilon,
            "seed": self.seed,
            "precision_mode": self.precision_mode,
            "precision_numeric": self.precision_numeric,
            "precision_bits": self.precision_bits,
        }
        vars_map.update(self.method_params)
        return vars_map

    def get_field_spec(self, key: str) -> dict | None:
        # Zwraca specyfikację danego pola albo None, jeśli pole nie jest zarejestrowane.
        return self.field_specs.get(key)

    def get_field_label(self, key: str) -> str:
        # Przyjazna nazwa pola do pokazania w komunikacie błędu.
        spec = self.get_field_spec(key)
        return spec.get("label", key) if spec else key

    def get_active_method_param_keys(self) -> list[str]:
        # Zwraca tylko parametry aktywne dla aktualnie wybranych metod.
        keys = []

        selection_params = METHOD_PARAM_SPECS["selection"].get(self.selection_method.get(), [])
        crossover_params = METHOD_PARAM_SPECS["crossover"].get(self.crossover_method.get(), [])
        mutation_params = METHOD_PARAM_SPECS["mutation"].get(self.mutation_method.get(), [])

        keys.extend([param["key"] for param in selection_params])
        keys.extend([param["key"] for param in crossover_params])
        keys.extend([param["key"] for param in mutation_params])

        return keys

    def get_active_field_keys(self) -> list[str]:
        # Zwraca wszystkie pola, które aktualnie biorą udział w walidacji.
        # Np. z precyzji walidujemy tylko aktywne pole zależne od radiobuttona.
        keys = [
            "n_vars",
            "range_start",
            "range_end",
            "population",
            "epochs",
            "epsilon",
            "seed",
        ]

        if self.precision_mode.get() == "Dokładność liczbowa":
            keys.append("precision_numeric")
        else:
            keys.append("precision_bits")

        keys.extend(self.get_active_method_param_keys())
        return keys

    def is_allowed_partial_value(self, key: str, value: str) -> bool:
        # Walidacja "na żywo" dla wpisywania do Entry.
        # Tutaj nie sprawdzamy jeszcze min/max, bo użytkownik może być w trakcie pisania.
        # Blokujemy jedynie ewidentnie nie-numeryczne znaki.
        spec = self.get_field_spec(key)
        if not spec:
            return True

        field_type = spec.get("type")
        if field_type == "int":
            if value in ("", "-"):
                return True
            try:
                int(value)
                return True
            except ValueError:
                return False

        if field_type == "float":
            # Dopuszczamy stany przejściowe podczas pisania liczby.
            if value in ("", "-", ".", "-."):
                return True
            try:
                float(value)
                return True
            except ValueError:
                return False

        return True

    def validate_all(self) -> dict[str, str]:
        # Główna walidacja uruchamiana po kliknięciu Start.
        # Zwraca słownik: key -> komunikat błędu.
        errors: dict[str, str] = {}

        for key in self.get_active_field_keys():
            value = self.field_vars[key].get()
            spec = self.get_field_spec(key)
            error = self._validate_value_against_spec(key=key, value=value, spec=spec)
            if error:
                errors[key] = error

        # Walidacja zależności między polami przedziału.
        if "range_start" not in errors and "range_end" not in errors:
            start = float(self.range_start.get())
            end = float(self.range_end.get())
            if start >= end:
                msg = 'Pole "Przedział (Start / koniec)" wymaga, aby Start był mniejszy od końca.'
                errors["range_start"] = msg
                errors["range_end"] = msg

        return errors

    def _validate_value_against_spec(self, key: str, value: str, spec: dict | None) -> str | None:
        # Walidacja pełnej wartości pola względem specyfikacji:
        # - czy nie jest puste,
        # - czy da się sparsować,
        # - czy mieści się w min/max.
        if spec is None:
            return None

        label = spec.get("label", key)
        field_type = spec.get("type")

        if field_type not in {"int", "float"}:
            return None

        if value.strip() == "":
            return f'Pole "{label}" nie może być puste.'

        try:
            parsed_value = int(value) if field_type == "int" else float(value)
        except ValueError:
            expected = "liczbą całkowitą" if field_type == "int" else "liczbą zmiennoprzecinkową"
            return f'Pole "{label}" musi być {expected}.'

        min_value = spec.get("min")
        min_exclusive = spec.get("min_exclusive")
        max_value = spec.get("max")

        if min_value is not None and parsed_value < min_value:
            return f'Pole "{label}" musi mieć wartość >= {min_value}.'

        if min_exclusive is not None and parsed_value <= min_exclusive:
            return f'Pole "{label}" musi mieć wartość > {min_exclusive}.'

        if max_value is not None and parsed_value > max_value:
            return f'Pole "{label}" musi mieć wartość <= {max_value}.'

        return None
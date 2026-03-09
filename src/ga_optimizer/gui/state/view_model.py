# view_model.py
# Model stanu GUI. Trzyma tylko tk.Variable i mapuje GUI <-> config.

import tkinter as tk

from ga_optimizer.config.defaults import build_default_config
from ga_optimizer.config.schema import (
    GA_MAIN_FIELD_SPECS,
    GENERAL_FIELD_SPECS,
    OPERATOR_FIELD_SPECS,
    PRECISION_FIELD_SPECS,
    CROSSOVER_METHOD_PARAM_SPECS,
    MUTATION_METHOD_PARAM_SPECS,
    SELECTION_METHOD_PARAM_SPECS,
    get_all_static_field_specs,
)
from ga_optimizer.problems.function_catalog import (
    get_problem_definition,
    get_problem_names,
)


class ViewModel:
    def __init__(self, root: tk.Misc):
        # Referencja do roota potrzebna do tworzenia tk.Variable.
        self.root = root

        # Bazowy config z wartościami startowymi aplikacji.
        self._base_config = build_default_config()

        # Wszystkie znane specyfikacje pól używane przez GUI.
        self._all_field_specs = self._build_field_specs()

        # Zmienne podstawowych ustawień problemu.
        self.problem_name = tk.StringVar(root, value=self._base_config.problem_name)
        self.n_vars = tk.StringVar(root, value=str(self._base_config.n_vars))
        self.range_start = tk.StringVar(root, value=str(self._base_config.range_start))
        self.range_end = tk.StringVar(root, value=str(self._base_config.range_end))

        # Zmienne głównych parametrów algorytmu.
        self.population = tk.StringVar(root, value=str(self._base_config.population))
        self.epochs = tk.StringVar(root, value=str(self._base_config.epochs))
        self.epsilon = tk.StringVar(root, value=str(self._base_config.epsilon))
        self.seed = tk.StringVar(root, value=str(self._base_config.seed))

        # Zmienne związane z dokładnością kodowania.
        self.precision_mode = tk.StringVar(root, value=self._base_config.precision_mode)
        self.precision_numeric = tk.StringVar(root, value=str(self._base_config.precision_numeric))
        self.precision_bits = tk.StringVar(root, value=str(self._base_config.precision_bits))

        # Zmienne wyboru metod operatorów.
        self.selection_method = tk.StringVar(root, value=self._base_config.selection_method)
        self.crossover_method = tk.StringVar(root, value=self._base_config.crossover_method)
        self.mutation_method = tk.StringVar(root, value=self._base_config.mutation_method)

        # Flagi dodatkowych opcji operatorów.
        self.inversion_enabled = tk.BooleanVar(root, value=self._base_config.inversion_enabled)
        self.elitism_enabled = tk.BooleanVar(root, value=self._base_config.elitism_enabled)

        # Zmienne parametrów zależnych od wybranych metod.
        self.method_params: dict[str, tk.StringVar] = {}
        self._init_method_params(root)

        # Mapa wszystkich pól GUI do ich zmiennych.
        self.field_vars = self._build_field_vars()

    def _build_field_specs(self) -> dict[str, dict]:
        # Buduje pełną mapę specyfikacji pól dla GUI.
        specs = get_all_static_field_specs()
        specs["problem_name"] = {
            **GENERAL_FIELD_SPECS["problem_name"],
            "values": get_problem_names(),
        }
        return specs

    def _init_method_params(self, root: tk.Misc) -> None:
        # Tworzy zmienne dla wszystkich znanych parametrów metod.
        unique_specs: dict[str, dict] = {}

        for method_specs in SELECTION_METHOD_PARAM_SPECS.values():
            for spec in method_specs:
                unique_specs[spec["key"]] = spec

        for method_specs in CROSSOVER_METHOD_PARAM_SPECS.values():
            for spec in method_specs:
                unique_specs[spec["key"]] = spec

        for method_specs in MUTATION_METHOD_PARAM_SPECS.values():
            for spec in method_specs:
                unique_specs[spec["key"]] = spec

        for key, spec in unique_specs.items():
            default_value = self._base_config.method_params.get(key, spec.get("default", ""))
            self.method_params[key] = tk.StringVar(root, value=str(default_value))

    def _build_field_vars(self) -> dict[str, tk.Variable]:
        # Składa wszystkie zmienne GUI do jednej mapy key -> tk.Variable.
        vars_map = {
            "problem_name": self.problem_name,
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
            "selection_method": self.selection_method,
            "crossover_method": self.crossover_method,
            "mutation_method": self.mutation_method,
            "inversion_enabled": self.inversion_enabled,
            "elitism_enabled": self.elitism_enabled,
        }
        vars_map.update(self.method_params)
        return vars_map

    def get_problem_names(self) -> list[str]:
        # Zwraca listę funkcji dostępnych do wyboru w GUI.
        return get_problem_names()

    def get_problem_definition(self):
        # Zwraca pełny opis aktualnie wybranej funkcji.
        return get_problem_definition(self.problem_name.get())

    def is_n_vars_locked(self) -> bool:
        # Informuje, czy liczba zmiennych ma być zablokowana dla tej funkcji.
        return self.get_problem_definition().fixed_n_vars

    def apply_problem_defaults(self) -> None:
        # Ustawia pola zależne od wybranej funkcji na jej domyślne wartości.
        problem = self.get_problem_definition()

        self.range_start.set(str(problem.suggested_range[0]))
        self.range_end.set(str(problem.suggested_range[1]))
        self.n_vars.set(str(problem.default_n_vars))

    def get_field_spec(self, key: str) -> dict | None:
        # Zwraca specyfikację danego pola, jeśli istnieje.
        return self._all_field_specs.get(key)

    def get_active_method_param_keys(self) -> list[str]:
        # Zwraca tylko klucze parametrów aktywnych dla wybranych metod.
        keys: list[str] = []

        for spec in SELECTION_METHOD_PARAM_SPECS.get(self.selection_method.get(), []):
            keys.append(spec["key"])

        for spec in CROSSOVER_METHOD_PARAM_SPECS.get(self.crossover_method.get(), []):
            keys.append(spec["key"])

        for spec in MUTATION_METHOD_PARAM_SPECS.get(self.mutation_method.get(), []):
            keys.append(spec["key"])

        return keys

    def get_payload(self) -> dict:
        # Składa aktualny stan GUI do słownika gotowego do budowy configu.
        method_params = {
            key: self.method_params[key].get()
            for key in self.get_active_method_param_keys()
        }

        return {
            "problem_name": self.problem_name.get(),
            "n_vars": self.n_vars.get(),
            "range_start": self.range_start.get(),
            "range_end": self.range_end.get(),
            "population": self.population.get(),
            "epochs": self.epochs.get(),
            "epsilon": self.epsilon.get(),
            "seed": self.seed.get(),
            "precision_mode": self.precision_mode.get(),
            "precision_numeric": self.precision_numeric.get(),
            "precision_bits": self.precision_bits.get(),
            "selection_method": self.selection_method.get(),
            "crossover_method": self.crossover_method.get(),
            "mutation_method": self.mutation_method.get(),
            "inversion_enabled": self.inversion_enabled.get(),
            "elitism_enabled": self.elitism_enabled.get(),
            "method_params": method_params,
        }

    def is_allowed_partial_value(self, key: str, value: str) -> bool:
        # Sprawdza, czy wpisywana wartość jest dozwolonym stanem pośrednim.
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
            if value in ("", "-", ".", "-."):
                return True
            try:
                float(value)
                return True
            except ValueError:
                return False

        return True
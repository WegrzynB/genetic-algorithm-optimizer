# validators.py
# Składanie configu z danych GUI oraz wspólna walidacja semantyczna.

from dataclasses import dataclass, field
from typing import Any

from ga_optimizer.config.schema import (
    GAConfig,
    GA_MAIN_FIELD_SPECS,
    GENERAL_FIELD_SPECS,
    OPERATOR_FIELD_SPECS,
    PRECISION_FIELD_SPECS,
    get_method_specs,
)
from ga_optimizer.problems.function_catalog import (
    get_problem_definition,
    get_problem_names,
)


@dataclass
class ValidationResult:
    # Wynik walidacji z listą błędów po kluczach pól.
    errors: dict[str, str] = field(default_factory=dict)

    @property
    def ok(self) -> bool:
        return not self.errors

    def add_error(self, key: str, message: str) -> None:
        if key not in self.errors:
            self.errors[key] = message


def _parse_value(
    key: str,
    raw_value: Any,
    spec: dict[str, Any],
    result: ValidationResult,
) -> Any:
    # Parsuje pojedynczą wartość wejściową zgodnie ze specyfikacją pola.
    label = spec.get("label", key)
    field_type = spec.get("type")

    if field_type == "bool":
        return bool(raw_value)

    if raw_value is None or (isinstance(raw_value, str) and raw_value.strip() == ""):
        if spec.get("allow_empty", False):
            return None
        result.add_error(key, f'Pole "{label}" nie może być puste.')
        return None

    if field_type == "int":
        try:
            return int(raw_value)
        except (TypeError, ValueError):
            result.add_error(key, f'Pole "{label}" musi być liczbą całkowitą.')
            return None

    if field_type == "float":
        try:
            return float(raw_value)
        except (TypeError, ValueError):
            result.add_error(key, f'Pole "{label}" musi być liczbą zmiennoprzecinkową.')
            return None

    if field_type == "enum":
        value = str(raw_value)
        allowed_values = spec.get("values", [])
        if allowed_values and value not in allowed_values:
            result.add_error(key, f'Pole "{label}" ma niedozwoloną wartość.')
            return None
        return value

    return raw_value


def _validate_against_spec(
    key: str,
    value: Any,
    spec: dict[str, Any],
    result: ValidationResult,
) -> None:
    # Sprawdza min/max dla już sparsowanej wartości.
    if value is None:
        return

    label = spec.get("label", key)
    min_value = spec.get("min")
    max_value = spec.get("max")
    min_exclusive = spec.get("min_exclusive")
    max_exclusive = spec.get("max_exclusive")

    if min_value is not None and value < min_value:
        result.add_error(key, f'Pole "{label}" musi mieć wartość >= {min_value}.')

    if min_exclusive is not None and value <= min_exclusive:
        result.add_error(key, f'Pole "{label}" musi mieć wartość > {min_exclusive}.')

    if max_value is not None and value > max_value:
        result.add_error(key, f'Pole "{label}" musi mieć wartość <= {max_value}.')

    if max_exclusive is not None and value >= max_exclusive:
        result.add_error(key, f'Pole "{label}" musi mieć wartość < {max_exclusive}.')


def build_config_from_payload(payload: dict[str, Any]) -> tuple[GAConfig | None, ValidationResult]:
    # Składa config z payloadu z GUI i uruchamia pełną walidację.
    result = ValidationResult()

    parsed_problem_name = _parse_value(
        "problem_name",
        payload.get("problem_name"),
        {
            **GENERAL_FIELD_SPECS["problem_name"],
            "values": get_problem_names(),
        },
        result,
    )

    parsed_objective_mode = _parse_value(
        "objective_mode",
        payload.get("objective_mode"),
        GA_MAIN_FIELD_SPECS["objective_mode"],
        result,
    )

    parsed_n_vars = _parse_value("n_vars", payload.get("n_vars"), GENERAL_FIELD_SPECS["n_vars"], result)
    parsed_range_start = _parse_value("range_start", payload.get("range_start"), GENERAL_FIELD_SPECS["range_start"], result)
    parsed_range_end = _parse_value("range_end", payload.get("range_end"), GENERAL_FIELD_SPECS["range_end"], result)

    parsed_population = _parse_value("population", payload.get("population"), GA_MAIN_FIELD_SPECS["population"], result)
    parsed_epochs = _parse_value("epochs", payload.get("epochs"), GA_MAIN_FIELD_SPECS["epochs"], result)
    parsed_run_count = _parse_value("run_count", payload.get("run_count"), GA_MAIN_FIELD_SPECS["run_count"], result)
    parsed_seed = _parse_value("seed", payload.get("seed"), GA_MAIN_FIELD_SPECS["seed"], result)

    parsed_precision_mode = _parse_value("precision_mode", payload.get("precision_mode"), PRECISION_FIELD_SPECS["precision_mode"], result)
    parsed_precision_numeric = _parse_value("precision_numeric", payload.get("precision_numeric"), PRECISION_FIELD_SPECS["precision_numeric"], result)
    parsed_precision_bits = _parse_value("precision_bits", payload.get("precision_bits"), PRECISION_FIELD_SPECS["precision_bits"], result)

    parsed_selection_method = _parse_value("selection_method", payload.get("selection_method"), OPERATOR_FIELD_SPECS["selection_method"], result)
    parsed_crossover_method = _parse_value("crossover_method", payload.get("crossover_method"), OPERATOR_FIELD_SPECS["crossover_method"], result)
    parsed_mutation_method = _parse_value("mutation_method", payload.get("mutation_method"), OPERATOR_FIELD_SPECS["mutation_method"], result)

    parsed_inversion_enabled = _parse_value("inversion_enabled", payload.get("inversion_enabled"), OPERATOR_FIELD_SPECS["inversion_enabled"], result)
    parsed_elitism_enabled = _parse_value("elitism_enabled", payload.get("elitism_enabled"), OPERATOR_FIELD_SPECS["elitism_enabled"], result)

    for key, value, spec in (
        ("n_vars", parsed_n_vars, GENERAL_FIELD_SPECS["n_vars"]),
        ("range_start", parsed_range_start, GENERAL_FIELD_SPECS["range_start"]),
        ("range_end", parsed_range_end, GENERAL_FIELD_SPECS["range_end"]),
        ("population", parsed_population, GA_MAIN_FIELD_SPECS["population"]),
        ("epochs", parsed_epochs, GA_MAIN_FIELD_SPECS["epochs"]),
        ("run_count", parsed_run_count, GA_MAIN_FIELD_SPECS["run_count"]),
        ("seed", parsed_seed, GA_MAIN_FIELD_SPECS["seed"]),
        ("precision_numeric", parsed_precision_numeric, PRECISION_FIELD_SPECS["precision_numeric"]),
        ("precision_bits", parsed_precision_bits, PRECISION_FIELD_SPECS["precision_bits"]),
    ):
        _validate_against_spec(key, value, spec, result)

    raw_method_params = payload.get("method_params", {})
    parsed_method_params: dict[str, Any] = {}

    if parsed_selection_method is not None:
        for spec in get_method_specs("selection", parsed_selection_method):
            parsed_value = _parse_value(spec["key"], raw_method_params.get(spec["key"]), spec, result)
            _validate_against_spec(spec["key"], parsed_value, spec, result)
            parsed_method_params[spec["key"]] = parsed_value

    if parsed_crossover_method is not None:
        for spec in get_method_specs("crossover", parsed_crossover_method):
            parsed_value = _parse_value(spec["key"], raw_method_params.get(spec["key"]), spec, result)
            _validate_against_spec(spec["key"], parsed_value, spec, result)
            parsed_method_params[spec["key"]] = parsed_value

    if parsed_mutation_method is not None:
        for spec in get_method_specs("mutation", parsed_mutation_method):
            parsed_value = _parse_value(spec["key"], raw_method_params.get(spec["key"]), spec, result)
            _validate_against_spec(spec["key"], parsed_value, spec, result)
            parsed_method_params[spec["key"]] = parsed_value

    if not result.ok:
        return None, result

    config = GAConfig(
        problem_name=parsed_problem_name,
        objective_mode=parsed_objective_mode,
        n_vars=parsed_n_vars,
        range_start=parsed_range_start,
        range_end=parsed_range_end,
        population=parsed_population,
        epochs=parsed_epochs,
        run_count=parsed_run_count,
        seed=parsed_seed,
        precision_mode=parsed_precision_mode,
        precision_numeric=parsed_precision_numeric,
        precision_bits=parsed_precision_bits,
        selection_method=parsed_selection_method,
        crossover_method=parsed_crossover_method,
        mutation_method=parsed_mutation_method,
        inversion_enabled=parsed_inversion_enabled,
        elitism_enabled=parsed_elitism_enabled,
        method_params=parsed_method_params,
    )

    validate_config(config, result)
    if not result.ok:
        return None, result

    return config, result


def validate_config(
    config: GAConfig,
    result: ValidationResult | None = None,
) -> ValidationResult:
    # Walidacja zależności między polami i reguł specyficznych dla problemu/metody.
    validation = result or ValidationResult()

    if config.problem_name not in get_problem_names():
        validation.add_error("problem_name", "Wybrana funkcja nie istnieje w katalogu problemów.")
        return validation

    problem = get_problem_definition(config.problem_name)

    if config.range_start >= config.range_end:
        message = 'Pole "Przedział (Start / koniec)" wymaga, aby Start był mniejszy od końca.'
        validation.add_error("range_start", message)
        validation.add_error("range_end", message)

    if config.precision_mode == "numeric" and config.precision_numeric <= 0.0:
        validation.add_error("precision_numeric", 'Pole "Dokładność (np. 0.001)" musi mieć wartość > 0.0.')

    if config.precision_mode == "bits" and config.precision_bits < 1:
        validation.add_error("precision_bits", 'Pole "Liczba bitów" musi mieć wartość >= 1.')

    if problem.fixed_n_vars and config.n_vars != problem.default_n_vars:
        validation.add_error(
            "n_vars",
            f'Funkcja "{problem.display_name}" wymaga dokładnie {problem.default_n_vars} zmiennych.',
        )

    if config.selection_method == "tournament":
        tournament_k = config.method_params.get("tournament_k")
        if isinstance(tournament_k, int) and tournament_k > config.population:
            validation.add_error(
                "tournament_k",
                'Pole "K (rozmiar turnieju)" nie może być większe niż wielkość populacji.',
            )

    if config.selection_method == "best":
        best_k = config.method_params.get("best_k")
        if isinstance(best_k, int) and best_k > config.population:
            validation.add_error(
                "best_k",
                'Pole "K (ile najlepszych)" nie może być większe niż wielkość populacji.',
            )

    if config.crossover_method == "granular":
        granularity = config.method_params.get("granularity")
        if isinstance(granularity, int) and granularity > config.n_vars:
            validation.add_error(
                "granularity",
                'Pole "Ziarnistość" nie może być większe niż liczba zmiennych.',
            )

    return validation
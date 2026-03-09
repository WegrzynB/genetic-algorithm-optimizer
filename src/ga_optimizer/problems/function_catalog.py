# function_catalog.py
# Jedyny plik będący źródłem informacji o funkcjach dostępnych w GUI.

from collections.abc import Callable
from dataclasses import dataclass

from ga_optimizer.problems.function_impl import hypersphere


@dataclass(frozen=True)
class ProblemDefinition:
    # Opis pojedynczej funkcji testowej dostępnej w aplikacji.
    key: str
    display_name: str
    formula: Callable[[list[float]], float]
    suggested_range: tuple[float, float]
    global_minimum_value: float
    global_minimum_points: list[list[float]]
    default_n_vars: int = 2
    fixed_n_vars: bool = False


FUNCTION_CATALOG = {
    "Hypersphere": ProblemDefinition(
        key="Hypersphere",
        display_name="Hypersphere",
        formula=hypersphere,
        suggested_range=(-5.0, 5.0),
        global_minimum_value=0.0,
        global_minimum_points=[
            [0.0, 0.0],
        ],
        default_n_vars=2,
        fixed_n_vars=False,
    ),
}


def get_problem_names() -> list[str]:
    # Zwraca listę nazw funkcji do pokazania w GUI.
    return list(FUNCTION_CATALOG.keys())


def get_default_problem_name() -> str:
    # Zwraca domyślną nazwę funkcji.
    return next(iter(FUNCTION_CATALOG.keys()))


def get_problem_definition(problem_name: str) -> ProblemDefinition:
    # Zwraca pełny opis funkcji po jej nazwie.
    if problem_name not in FUNCTION_CATALOG:
        raise KeyError(f"Nieznana funkcja problemowa: {problem_name}")
    return FUNCTION_CATALOG[problem_name]
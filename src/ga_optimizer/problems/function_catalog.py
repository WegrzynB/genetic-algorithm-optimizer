# function_catalog.py
# Jedyny plik będący źródłem informacji o funkcjach dostępnych w GUI.

from collections.abc import Callable
from dataclasses import dataclass
import math

from ga_optimizer.problems.function_impl import hypersphere, hyperellipsoid, schwefel, ackley, michalewicz, rastrigin, rosenbrock, dejong3, martin_gaddy, griewank


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

    "Hyperellipsoid": ProblemDefinition(
        key="Hyperellipsoid",
        display_name="Hyperellipsoid",
        formula=hyperellipsoid,
        suggested_range=(-65.536, 65.536),
        global_minimum_value=0.0,
        global_minimum_points=[[0.0, 0.0]],
        default_n_vars=2,
        fixed_n_vars=False,
    ),
    
    "Schwefel": ProblemDefinition(
        key="Schwefel",
        display_name="Schwefel",
        formula=schwefel,
        suggested_range=(-500.0, 500.0),
        global_minimum_value=2.545567497236334e-05,
        global_minimum_points=[[420.9687, 420.9687], [-302.5249351839932, 420.9687467475071]],
        default_n_vars=2,
        fixed_n_vars=False,
    ),

    "Ackley": ProblemDefinition(
        key="Ackley",
        display_name="Ackley",
        formula=ackley,
        suggested_range=(-32.768, 32.768),
        global_minimum_value=4.440892098500626e-16,
        global_minimum_points=[[0.0, 0.0]],
        default_n_vars=2,
        fixed_n_vars=False,
    ),

    "Michalewicz": ProblemDefinition(
        key="Michalewicz",
        display_name="Michalewicz",
        formula=michalewicz,
        suggested_range=(0.0, math.pi),
        global_minimum_value=-1.8013034100904854,
        global_minimum_points=[[2.202906, 1.570796], [2.202900552, 2.71157148384]],
        default_n_vars=2,
        fixed_n_vars=False,
    ),

    "Rastrigin": ProblemDefinition(
        key="Rastrigin",
        display_name="Rastrigin",
        formula=rastrigin,
        suggested_range=(-5.12, 5.12),
        global_minimum_value=0.0,
        global_minimum_points=[[0.0, 0.0]],
        default_n_vars=2,
        fixed_n_vars=False,
    ),

    "Rosenbrock": ProblemDefinition(
        key="Rosenbrock",
        display_name="Rosenbrock",
        formula=rosenbrock,
        suggested_range=(-2.048, 2.048),
        global_minimum_value=0.0,
        global_minimum_points=[[1.0, 1.0]],
        default_n_vars=2,
        fixed_n_vars=False,
    ),

    "DeJong3": ProblemDefinition(
        key="DeJong3",
        display_name="De Jong 3",
        formula=dejong3,
        suggested_range=(3.8, 3.8),
        global_minimum_value=-8.0,  # Najniższe z wymienionych w opisie
        global_minimum_points=[[-3.5, -3.5]],
        default_n_vars=2,
        fixed_n_vars=False,
    ),

    "MartinGaddy": ProblemDefinition(
        key="MartinGaddy",
        display_name="Martin and Gaddy",
        formula=martin_gaddy,
        suggested_range=(-20.0, 20.0),
        global_minimum_value=0.0,
        global_minimum_points=[[5.0, 5.0]],
        default_n_vars=2,
        fixed_n_vars=True,
    ),

    "Griewank": ProblemDefinition(
        key="Griewank",
        display_name="Griewank",
        formula=griewank,
        suggested_range=(-600.0, 600.0),
        global_minimum_value=0.0,
        global_minimum_points=[[0.0, 0.0]],
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
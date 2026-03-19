# function_catalog.py
# Jedyny plik będący źródłem informacji o funkcjach dostępnych w GUI.

from collections.abc import Callable
from dataclasses import dataclass
import math

from ga_optimizer.problems.function_impl import hypersphere, hyperellipsoid, schwefel, ackley, michalewicz, rastrigin, rosenbrock, dejong3, martin_gaddy, griewank, dejong5, easom, goldstein_price, picheny_goldstein_price, styblinski_tang, mccormick, rana, eggholder, schaffer2, himmelblau, pits_and_holes


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
        global_minimum_points=[[420.9687, 420.9687]],
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
        global_minimum_points=[[2.202906, 1.570796]],
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
        suggested_range=(-3.8, 3.8),
        global_minimum_value=-8.0,
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

    "DeJong5": ProblemDefinition(
        key="DeJong5",
        display_name="De Jong 5",
        formula=dejong5,
        suggested_range=(-65.536, 65.536),
        global_minimum_value=0.9980038377944496,
        global_minimum_points=[[-31.9783, -31.9783]],
        fixed_n_vars=True,
    ),

    "Easom": ProblemDefinition(
        key="Easom",
        display_name="Easom",
        formula=easom,
        suggested_range=(-100, 100),
        global_minimum_value=-1.0,
        global_minimum_points=[[math.pi, math.pi]],
        fixed_n_vars=True,
    ),

    "GoldsteinPrice": ProblemDefinition(
        key="GoldsteinPrice",
        display_name="Goldstein and Price",
        formula=goldstein_price,
        suggested_range=(-2, 2),
        global_minimum_value=3.0,
        global_minimum_points=[[0.0, -1.0]],
        fixed_n_vars=True,
    ),

    "PichenyGoldsteinPrice": ProblemDefinition(
        key="PichenyGoldsteinPrice",
        display_name="Picheny Goldstein Price",
        formula=picheny_goldstein_price,
        suggested_range=(-2, 2),
        global_minimum_value=-3.129125550610585,
        global_minimum_points=[[0.5, 0.25]],
        fixed_n_vars=True,
    ),

    "StyblinskiTang": ProblemDefinition(
        key="StyblinskiTang",
        display_name="Styblinski-Tang",
        formula=styblinski_tang,
        suggested_range=(-5, 5),
        global_minimum_value=-78.3323314075428,
        global_minimum_points=[[-2.903534, -2.903534]],
    ),

    "McCormick": ProblemDefinition(
        key="McCormick",
        display_name="McCormick",
        formula=mccormick,
        suggested_range=(-3, 4),
        global_minimum_value=-1.913222954882274,
        global_minimum_points=[[-0.54719, -1.54719]],
        fixed_n_vars=True,
    ),

    "Rana": ProblemDefinition(
        key="Rana",
        display_name="Rana",
        formula=rana,
        suggested_range=(-512, 512),
        global_minimum_value=-511.73288188661934,
        global_minimum_points=[[-488.632577, 512]],
    ),

    "Eggholder": ProblemDefinition(
        key="Eggholder",
        display_name="Egg Holder",
        formula=eggholder,
        suggested_range=(-512, 512),
        global_minimum_value=-959.7133283100513,
        global_minimum_points=[[512.0214, 404.2510]],
    ),

    "Schaffer2": ProblemDefinition(
        key="Schaffer2",
        display_name="Schaffer 2",
        formula=schaffer2,
        suggested_range=(-100, 100),
        global_minimum_value=0.0,
        global_minimum_points=[[0.0, 0.0]],
        fixed_n_vars=True,
    ),

    "Himmelblau": ProblemDefinition(
        key="Himmelblau",
        display_name="Himmelblau",
        formula=himmelblau,
        suggested_range=(-5, 5),
        global_minimum_value=0.0,
        global_minimum_points=[[3.0, 2.0]],
        fixed_n_vars=True,
    ),

    "PitsAndHoles": ProblemDefinition(
        key="PitsAndHoles",
        display_name="Pits and Holes",
        formula=pits_and_holes,
        suggested_range=(-20, 20),
        global_minimum_value=-0.23874320826749335,
        global_minimum_points=[[-10, -10]],
        fixed_n_vars=True,
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
# engine.py
# Placeholder silnika algorytmu genetycznego.
# Na razie ma już docelowy punkt wejścia, ale nie wykonuje jeszcze właściwego GA.

from ga_optimizer.config.schema import GAConfig
from ga_optimizer.problems.function_catalog import ProblemDefinition


def run_engine(config: GAConfig, problem: ProblemDefinition) -> dict:
    # Docelowo tutaj będzie pełne uruchomienie algorytmu:
    # - inicjalizacja populacji,
    # - kolejne epoki,
    # - historia best/avg/worst,
    # - warunki stopu,
    # - wynik końcowy.
    #
    # Na razie zwracamy placeholder w ustalonym formacie.
    return {
        "status": "placeholder",
        "message": f'Engine placeholder dla problemu "{problem.display_name}".',
        "best": None,
        "avg": None,
        "worst": None,
        "elapsed": None,
    }
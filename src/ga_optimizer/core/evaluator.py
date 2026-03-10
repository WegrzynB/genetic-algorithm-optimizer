# ocena osobników na podstawie wybranego problemu / funkcji celu

from dataclasses import dataclass
from collections.abc import Callable
from .fitness import calculate_fitness

@dataclass
class EvaluationResult:
    raw_objective: float
    fitness: float

class Evaluator:
    def __init__(self, objective_func: Callable[[list[float]], float], optimization_type: str = 'min'):
        self.objective_func = objective_func
        self.optimization_type = optimization_type

    def evaluate(self, genes: list[float]) -> EvaluationResult:
        raw_obj = self.objective_func(genes)
        fit = calculate_fitness(raw_obj, self.optimization_type)

        return EvaluationResult(raw_objective=raw_obj, fitness=fit)
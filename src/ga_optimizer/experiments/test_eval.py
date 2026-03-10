# test_eval.py
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from ga_optimizer.problems.function_catalog import get_problem_definition, get_default_problem_name
from ga_optimizer.core.evaluator import Evaluator

def run_test():
    problem_name = get_default_problem_name()
    problem_def = get_problem_definition(problem_name)
    
    print(f"Testujemy ewaluację dla problemu: {problem_def.display_name}")
    evaluator = Evaluator(objective_func=problem_def.formula, optimization_type='min')
    test_vectors = [
        [0.0, 0.0],
        [1.0, 1.0],
        [5.0, -5.0]
    ]
    for genes in test_vectors:
        result = evaluator.evaluate(genes)
        print(f"Geny: {str(genes):15} | Raw Obj: {result.raw_objective:6.2f} | Fitness: {result.fitness:.4f}")

if __name__ == "__main__":
    run_test()
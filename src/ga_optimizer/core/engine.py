# engine.py
# Silnik algorytmu genetycznego z podpiętą ewaluacją osobników.

from ga_optimizer.problems.function_catalog import get_problem_definition
from ga_optimizer.core.encoding import bits_required, chromosome_length
from ga_optimizer.core.population import Population
from ga_optimizer.core.evaluator import Evaluator
from ga_optimizer.core.lifecycle import run_lifecycle


def run_engine(config_dict: dict) -> dict:

    # 1. Pobranie definicji problemu (funkcji celu)
    problem_def = get_problem_definition(config_dict["problem_name"])
    
    # 2. Inicjalizacja ewaluatora
    evaluator = Evaluator(objective_func=problem_def.formula, optimization_type=config_dict["objective_mode"])

    # 3. Wyliczenie precyzji i długości chromosomu
    if config_dict["precision_mode"] == "numeric":
        precision = config_dict["precision_numeric"]
    elif config_dict["precision_mode"] == "bits":
        precision = (config_dict["range_end"] - config_dict["range_start"]) / (2 ** config_dict["precision_bits"] - 1)

    bounds = [(config_dict["range_start"], config_dict["range_end"])] * config_dict["n_vars"]

    bits = bits_required(bounds, precision)
    chrom_length = chromosome_length(bits)

    # print("\n=== ENGINE INPUT ===")
    # print(f"Problem: {problem_def.display_name}")
    # print("Długość chromosomu:", chrom_length)
    # print("Rozmiar populacji:", config_dict["population"])

    # 4. Inicjalizacja populacji
    population = Population.random(
        size=config_dict["population"],
        chromosome_length=chrom_length,
        seed=config_dict["seed"]
    )

    parameters_dict = {
        "population": population,
        "evaluator": evaluator,
        "bounds": bounds,
        "bits": bits,
        "chrom_length": chrom_length,
    }


    for epoch in range(config_dict["epochs"]):
        lifecycle = run_lifecycle(config_dict=config_dict, parameters_dict=parameters_dict)

        # print(population)
        population = lifecycle["chromosomes"]
        # print(population)


    return {
        "population": population
    }

    
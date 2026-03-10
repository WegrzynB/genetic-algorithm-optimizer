# engine.py
# Silnik algorytmu genetycznego z podpiętą ewaluacją osobników.

from ga_optimizer.config.schema import GAConfig
from ga_optimizer.problems.function_catalog import get_problem_definition

from ga_optimizer.core.encoding import bits_required, chromosome_length
from ga_optimizer.core.population import Population
from ga_optimizer.core.decoding import decode_chromosome
from ga_optimizer.core.evaluator import Evaluator


def run_engine(config: GAConfig) -> dict:

    n_vars = config.n_vars
    range_start = config.range_start
    range_end = config.range_end
    population_size = config.population
    seed = config.seed

    # 1. Pobranie definicji problemu (funkcji celu)
    # Zakładam, że config.problem przechowuje klucz problemu (np. "Hypersphere")
    problem_def = get_problem_definition(config.problem_name)
    
    # 2. Inicjalizacja ewaluatora
    # Zgodnie z założeniami z problem_catalog minimalizujemy funkcje
    evaluator = Evaluator(objective_func=problem_def.formula, optimization_type='min')

    # 3. Wyliczenie precyzji i długości chromosomu
    if config.precision_mode == "numeric":
        precision = config.precision_numeric
    else:
        precision = (range_end - range_start) / (2 ** config.precision_bits)

    bounds = [(range_start, range_end)] * n_vars

    bits = bits_required(bounds, precision)
    chrom_length = chromosome_length(bits)

    print("\n=== ENGINE INPUT ===")
    print(f"Problem: {problem_def.display_name}")
    print("Długość chromosomu:", chrom_length)
    print("Rozmiar populacji:", population_size)

    # 4. Inicjalizacja populacji
    population = Population.random(
        size=population_size,
        chromosome_length=chrom_length,
        seed=seed
    )

    chromosomes = []
    decoded_population = []
    evaluation_result = []  # Tu przechowujemy obiekty EvaluationResult

    # 5. Ewaluacja każdego osobnika w populacji
    for individual in population:
        chrom_str = "".join(map(str, individual.chromosome.genes))

        # Dekodowanie genotypu (bity) na fenotyp (wartości rzeczywiste / floaty)
        decoded = decode_chromosome(
            individual.chromosome,
            bounds,
            bits
        )

        # Wyliczenie funkcji celu i fitnessu
        eval_result = evaluator.evaluate(decoded)
        
        # Zapisanie fitnessu bezpośrednio do obiektu osobnika
        individual.fitness = eval_result.fitness

        chromosomes.append(chrom_str)
        decoded_population.append(decoded)
        evaluation_result.append(eval_result)

    print("\nPopulacja:")
    print(", ".join(chromosomes))

    print("\nZdekodowane wartości:")
    # Formatujemy wyjście dla czytelności (2 miejsca po przecinku dla zdekodowanych)
    print(", ".join(f"[{', '.join(f'{v:.2f}' for v in dec)}]" for dec in decoded_population))

    print("\nWyniki oceny (Raw Objective | Fitness):")
    # Zgrabne wypisanie połączonego wyniku
    print(", ".join(f"({res.raw_objective:.2f} | {res.fitness:.4f})" for res in evaluation_result))
    print("======================\n")

    return {
        "population_size": population_size,
        "chromosome_length": chrom_length,
        "bits_per_variable": bits,
        "chromosomes": chromosomes,
        "decoded_population": decoded_population,
        # Możesz eksportować same wyniki raw, sam fitness, lub obiekty EvaluationResult
        "evaluation_result": evaluation_result, 
        "population": population # Dobrze też zwrócić obiekt populacji, przyda się do selekcji
    }
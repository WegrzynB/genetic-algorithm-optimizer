# engine.py
# Placeholder silnika algorytmu genetycznego.
# Na razie ma już docelowy punkt wejścia, ale nie wykonuje jeszcze właściwego GA.

from ga_optimizer.config.schema import GAConfig
from ga_optimizer.problems.function_catalog import ProblemDefinition

from ga_optimizer.core.encoding import bits_required, chromosome_length
from ga_optimizer.core.population import Population
from ga_optimizer.core.decoding import decode_chromosome


def run_engine(config: GAConfig, problem: ProblemDefinition, params: dict) -> dict:

    n_vars = params["n_vars"]
    range_start = params["range_start"]
    range_end = params["range_end"]
    population_size = params["population"]
    seed = params["seed"]

    precision_mode = params["precision_mode"]

    if precision_mode == "numeric":
        precision = params["precision_numeric"]
    else:
        precision = (range_end - range_start) / (2 ** params["precision_bits"])

    bounds = [(range_start, range_end)] * n_vars

    bits = bits_required(bounds, precision)

    chrom_length = chromosome_length(bits)

    print("=== ENGINE ===")
    print("Liczba bitów na zmienną:", bits)
    print("Długość chromosomu:", chrom_length)
    print("Rozmiar populacji:", population_size)
    print()

    population = Population.random(
        size=population_size,
        chromosome_length=chrom_length,
        seed=seed
    )

    decoded_population = []

    sample_size = 10

    print("Pierwsze osobniki populacji:\n")

    for i, individual in enumerate(population):

        decoded = decode_chromosome(
            individual.chromosome,
            bounds,
            bits
        )

        decoded_population.append(decoded)

        if i < sample_size:
            print(f"Osobnik {i + 1}")
            print("Chromosom:", individual.chromosome)
            print("Zdekodowane wartości:", decoded)
            print()

    return {
        "status": "ok",
        "message": "Populacja wygenerowana.",
        "population_size": population_size,
        "chromosome_length": chrom_length,
        "bits_per_variable": bits,
        "decoded_population_sample": decoded_population[:5],
    }
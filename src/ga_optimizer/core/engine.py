# engine.py
# Placeholder silnika algorytmu genetycznego.
# Na razie ma już docelowy punkt wejścia, ale nie wykonuje jeszcze właściwego GA.

from ga_optimizer.config.schema import GAConfig
from ga_optimizer.problems.function_catalog import ProblemDefinition

from ga_optimizer.core.encoding import bits_required, chromosome_length
from ga_optimizer.core.population import Population
from ga_optimizer.core.decoding import decode_chromosome


def run_engine(config: GAConfig, problem: ProblemDefinition) -> dict:

    n_vars = config.n_vars
    range_start = config.range_start
    range_end = config.range_end
    population_size = config.population
    seed = config.seed

    if config.precision_mode == "numeric":
        precision = config.precision_numeric
    else:
        precision = (range_end - range_start) / (2 ** config.precision_bits)

    bounds = [(range_start, range_end)] * n_vars

    bits = bits_required(bounds, precision)
    chrom_length = chromosome_length(bits)

    print("\n=== ENGINE INPUT ===")
    print("Długość chromosomu:", chrom_length)
    print("Rozmiar populacji:", population_size)

    population = Population.random(
        size=population_size,
        chromosome_length=chrom_length,
        seed=seed
    )

    chromosomes = []
    decoded_population = []

    for individual in population:

        chrom_str = "".join(map(str, individual.chromosome.genes))

        decoded = decode_chromosome(
            individual.chromosome,
            bounds,
            bits
        )

        chromosomes.append(chrom_str)
        decoded_population.append(decoded)

    print("\nPopulacja:")
    print(", ".join(chromosomes))

    print("\nZdekodowane wartości:")
    print(", ".join(str(v) for v in decoded_population))
    print("======================\n")

    return {
        "population_size": population_size,
        "chromosome_length": chrom_length,
        "bits_per_variable": bits,
        "chromosomes": chromosomes,
        "decoded_population": decoded_population,
    }
from ga_optimizer.core.encoding import bits_required, chromosome_length
from ga_optimizer.core.population import Population
from ga_optimizer.core.decoding import decode_chromosome


bounds = [(-5, 5), (-10, 10)]
precision = 0.01


bits = bits_required(bounds, precision)

length = chromosome_length(bits)


print("Liczba bitów potrzebnych dla każdej zmiennej:", bits)
print("Całkowita długość chromosomu:", length)


pop = Population.random(
    size=5,
    chromosome_length=length,
    seed=42,
)


print("\nWygenerowana populacja:\n")

for i, ind in enumerate(pop):

    decoded = decode_chromosome(
        ind.chromosome,
        bounds,
        bits,
    )

    print(f"Osobnik {i + 1}")
    print("Chromosom:", ind.chromosome)
    print("Zdekodowane wartości zmiennych:", decoded)
    print()
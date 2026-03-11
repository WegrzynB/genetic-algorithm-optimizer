# zarządza kolejnymi etapami generacji (selekcja, krzyżowanie, mutacja, elitaryzm)

from ga_optimizer.core.decoding import decode_chromosome


def run_lifecycle(config_dict: dict, parameters_dict: dict) -> dict:

    chromosomes = []
    decoded_population = []
    evaluation_result = []  # Tu przechowujemy obiekty EvaluationResult

    # 5. Ewaluacja każdego osobnika w populacji
    for individual in parameters_dict["population"]:
        chrom_str = "".join(map(str, individual.chromosome.genes))

        # Dekodowanie genotypu (bity) na fenotyp (wartości rzeczywiste / floaty)
        decoded = decode_chromosome(
            individual.chromosome,
            parameters_dict["bounds"],
            parameters_dict["bits"]
        )

        # Wyliczenie funkcji celu i fitnessu
        eval_result = parameters_dict["evaluator"].evaluate(decoded)
        
        # Zapisanie fitnessu bezpośrednio do obiektu osobnika
        individual.fitness = eval_result.fitness

        chromosomes.append(chrom_str)
        decoded_population.append(decoded)
        evaluation_result.append(eval_result)

    # print("\nPopulacja:")
    # print(", ".join(chromosomes))

    # print("\nZdekodowane wartości:")
    # Formatujemy wyjście dla czytelności (2 miejsca po przecinku dla zdekodowanych)
    # print(", ".join(f"[{', '.join(f'{v:.2f}' for v in dec)}]" for dec in decoded_population))

    # print("\nWyniki oceny (Raw Objective | Fitness):")
    # Zgrabne wypisanie połączonego wyniku
    # print(", ".join(f"({res.raw_objective:.2f} | {res.fitness:.4f})" for res in evaluation_result))
    # print("======================\n")

    return {
        "population_size": config_dict["population"],
        "chromosome_length": parameters_dict["chrom_length"],
        "bits_per_variable": parameters_dict["bits"],
        "chromosomes": chromosomes,
        "decoded_population": decoded_population,
        # Możesz eksportować same wyniki raw, sam fitness, lub obiekty EvaluationResult
        "evaluation_result": evaluation_result, 
        "population": parameters_dict["population"] # Dobrze też zwrócić obiekt populacji, przyda się do selekcji
    }
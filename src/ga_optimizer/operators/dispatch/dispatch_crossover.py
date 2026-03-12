# dispatch_crossover.py
# Dispatcher metod krzyżowania.
# Na razie zwraca chromosomy bez zmian.

from __future__ import annotations

from typing import Any

from ga_optimizer.operators.crossover.one_point import one_point_crossover
from ga_optimizer.operators.crossover.two_point import two_point_crossover
from ga_optimizer.operators.crossover.uniform   import uniform_crossover
from ga_optimizer.operators.crossover.shuffle import shuffle_crossover
from ga_optimizer.operators.crossover.granular import granular_crossover
from ga_optimizer.operators.crossover.reduced_surro import reduced_surro_crossover
from ga_optimizer.operators.crossover.disruptive import disruptive_crossover
from ga_optimizer.operators.crossover.three_point import three_point_crossover
from ga_optimizer.operators.crossover.multi_point import multi_point_crossover
from ga_optimizer.operators.crossover.majority import majority_crossover
from ga_optimizer.operators.crossover.arithmetic import arithmetic_crossover
from ga_optimizer.operators.crossover.segmented import segmented_crossover



def dispatch_crossover(
    chromosomes: list[list[int]],
    config_dict: dict[str, Any],
) -> list[list[int]]:
    
    method_name = config_dict["crossover_method"]
    crossovered_chromosomes = chromosomes.copy()

    # Przykład chromosomu:
    # [[0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0], [0, 0, 1, 0, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1], 
    # [0, 0, 1, 0, 1, 1, 1, 0, 1, 0, 1, 0, 1, 1], [0, 0, 0, 0, 1, 0, 0, 0, 1, 1, 1, 1, 0, 1]]
    match method_name:
        case "one_point":
            crossovered_chromosomes = one_point_crossover(
                chromosomes,
                config_dict
            )

        case "two_point":
            crossovered_chromosomes = two_point_crossover(
                chromosomes,
                config_dict
            )

        case "three_point":
            crossovered_chromosomes = three_point_crossover(
                chromosomes,
                config_dict
            )

        case "multi_point":
            crossovered_chromosomes = multi_point_crossover(
                chromosomes,
                config_dict
            )

        case "uniform":
            crossovered_chromosomes = uniform_crossover(
                chromosomes,
                config_dict
            )

        case "shuffle":
            crossovered_chromosomes = shuffle_crossover(
                chromosomes,
                config_dict
            )

        case "granular":
            crossovered_chromosomes = granular_crossover(
                chromosomes,
                config_dict
            )

        case "reduced_surro":
            crossovered_chromosomes = reduced_surro_crossover(
                chromosomes,
                config_dict
            )
        case "disruptive":
            crossovered_chromosomes = disruptive_crossover(
                chromosomes,
                config_dict
            )

        case "majority":
            crossovered_chromosomes = majority_crossover(
                chromosomes,
                config_dict
            )

        case "arithmetic":
            crossovered_chromosomes = arithmetic_crossover(
                chromosomes,
                config_dict
            )

        case "segmented":
            crossovered_chromosomes = segmented_crossover(
                chromosomes,
                config_dict
            )

    print(f"[Crossover] Chromosomy dla metody: {method_name}")
    for index, chromosome in enumerate(crossovered_chromosomes):
        print(f"{index}: {chromosome}")
    print("\n")

    return crossovered_chromosomes
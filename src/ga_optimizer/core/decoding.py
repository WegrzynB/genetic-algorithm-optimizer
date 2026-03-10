# dekodowanie chromosomu do wartości wejściowych funkcji celu

from __future__ import annotations

from typing import List, Tuple

from .chromosome import Chromosome


Bounds = Tuple[float, float]


def _bits_to_int(bits: List[int]) -> int:
    value = 0
    for b in bits:
        value = (value << 1) | b
    return value


def decode_chromosome(
    chromosome: Chromosome,
    bounds: List[Bounds],
    bits_per_variable: List[int],
) -> List[float]:

    values: List[float] = []
    index = 0

    for (low, high), bits_count in zip(bounds, bits_per_variable):

        gene_slice = chromosome.genes[index:index + bits_count]
        index += bits_count

        integer_value = _bits_to_int(gene_slice)

        max_int = (2 ** bits_count) - 1

        ratio = integer_value / max_int if max_int > 0 else 0.0

        decoded = low + ratio * (high - low)

        values.append(decoded)

    return values
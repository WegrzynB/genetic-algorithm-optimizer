# kodowanie wartości zmiennych do postaci chromosomu
from __future__ import annotations

import math
from typing import List, Tuple


Bounds = Tuple[float, float]


def bits_required(bounds: List[Bounds], precision: float) -> List[int]:

    bits = []

    for low, high in bounds:
        range_size = high - low
        levels = range_size / precision
        bits_needed = math.ceil(math.log2(levels + 1))
        bits.append(bits_needed)

    return bits


def chromosome_length(bits_per_variable: List[int]) -> int:
    return sum(bits_per_variable)
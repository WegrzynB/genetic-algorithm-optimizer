# chromosom i podstawowe operacje na jego strukturze

from __future__ import annotations

import random
from dataclasses import dataclass
from typing import List


@dataclass
class Chromosome:
    genes: List[int]

    @classmethod
    def random(cls, length: int, rng: random.Random) -> "Chromosome":
        genes = [rng.randint(0, 1) for _ in range(length)]
        return cls(genes)

    def copy(self) -> "Chromosome":
        return Chromosome(self.genes.copy())

    def __len__(self) -> int:
        return len(self.genes)

    def __repr__(self) -> str:
        return f"Chromosom({''.join(map(str, self.genes))})"
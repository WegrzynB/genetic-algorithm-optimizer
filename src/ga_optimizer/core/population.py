# obsługa tworzenia, przechowywania i operacji na populacji osobników
from __future__ import annotations

import random
from typing import List

from .chromosome import Chromosome
from .individual import Individual


class Population:

    def __init__(self, individuals: List[Individual]):
        self.individuals = individuals

    @classmethod
    def random(
        cls,
        size: int,
        chromosome_length: int,
        seed: int | None = None,
    ) -> "Population":

        rng = random.Random(seed)

        individuals = [
            Individual(Chromosome.random(chromosome_length, rng))
            for _ in range(size)
        ]

        return cls(individuals)

    def __len__(self) -> int:
        return len(self.individuals)

    def __iter__(self):
        return iter(self.individuals)

    def __getitem__(self, item):
        return self.individuals[item]
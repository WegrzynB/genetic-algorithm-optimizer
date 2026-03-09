# pojedynczy osobnik z genotypem i oceną
from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from .chromosome import Chromosome


@dataclass
class Individual:
    chromosome: Chromosome
    fitness: Optional[float] = None

    def invalidate_fitness(self) -> None:
        self.fitness = None

    def __repr__(self) -> str:
        return f"Osobnik(fitness={self.fitness}, chromosom={self.chromosome})"
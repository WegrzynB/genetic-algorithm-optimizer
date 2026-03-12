# population.py
# Klasa populacji trzymająca chromosomy, dekodowane wartości
# oraz całą ewaluację bieżącego stanu populacji.

from __future__ import annotations

import math
import random
from typing import Any

from ga_optimizer.problems.function_catalog import get_problem_definition


class Population:
    def __init__(self, config_dict: dict[str, Any]):
        # Zachowujemy cały config do dalszego użycia.
        self.config_dict = config_dict

        # Podstawowe ustawienia problemu i populacji.
        self.problem_name = str(config_dict["problem_name"])
        self.problem_definition = get_problem_definition(self.problem_name)
        self.objective_mode = str(config_dict["objective_mode"])

        self.population_size = int(config_dict["population"])
        self.n_vars = int(config_dict["n_vars"])
        self.range_start = float(config_dict["range_start"])
        self.range_end = float(config_dict["range_end"])

        # Zakresy zmiennych - na razie wszystkie zmienne mają ten sam zakres.
        self.bounds: list[tuple[float, float]] = [
            (self.range_start, self.range_end)
            for _ in range(self.n_vars)
        ]

        # Tryb dokładności decyduje o liczbie bitów albo o precyzji.
        self.precision_mode = str(config_dict["precision_mode"])

        if self.precision_mode == "bits":
            bits_value = int(config_dict["precision_bits"])
            self.bits_per_variable = [bits_value for _ in range(self.n_vars)]
            self.precision = (self.range_end - self.range_start) / ((2 ** bits_value) - 1)

        elif self.precision_mode == "numeric":
            self.precision = float(config_dict["precision_numeric"])
            self.bits_per_variable = []

            for low, high in self.bounds:
                levels = (high - low) / self.precision
                bits_needed = math.ceil(math.log2(levels + 1))
                self.bits_per_variable.append(bits_needed)

        else:
            raise ValueError(f'Nieobsługiwany tryb dokładności: {self.precision_mode}')

        # Całkowita długość jednego chromosomu.
        self.chromosome_length = sum(self.bits_per_variable)

        # Generator losowy dla populacji.
        self.seed = int(config_dict["seed"])
        self.rng = random.Random(self.seed)

        # Główne dane populacji.
        self.chromosomes: list[list[int]] = []
        self.decoded_population: list[list[float]] = []

        # Wyniki ewaluacji.
        self.raw_objectives: list[float | None] = []
        self.fitness_values: list[float | None] = []

    def generate_initial_population(self) -> None:
        # Tworzy losową populację startową.
        self.chromosomes = [
            [self.rng.randint(0, 1) for _ in range(self.chromosome_length)]
            for _ in range(self.population_size)
        ]
        self.update_after_chromosome_change()

    def set_chromosomes(self, chromosomes: list[list[int]]) -> None:
        # Podmienia chromosomy i odświeża wszystkie dane zależne.
        copied = [chromosome.copy() for chromosome in chromosomes]

        for chromosome in copied:
            if len(chromosome) != self.chromosome_length:
                raise ValueError(
                    f"Niepoprawna długość chromosomu: {len(chromosome)}. "
                    f"Oczekiwano {self.chromosome_length}."
                )

        self.chromosomes = copied
        self.population_size = len(copied)
        self.update_after_chromosome_change()

    def update_after_chromosome_change(self) -> None:
        # Po zmianie chromosomów aktualizujemy wszystko,
        # co od nich zależy.
        self.decoded_population = [
            self.decode_chromosome(chromosome)
            for chromosome in self.chromosomes
        ]

        self.raw_objectives = []
        self.fitness_values = []

        for values in self.decoded_population:
            raw_value = self.problem_definition.formula(values)
            fitness = self.calculate_fitness(raw_value)

            self.raw_objectives.append(raw_value)
            self.fitness_values.append(fitness)

    def decode_chromosome(self, chromosome: list[int]) -> list[float]:
        # Dekoduje pojedynczy chromosom na listę wartości rzeczywistych.
        values: list[float] = []
        start_index = 0

        for (low, high), bits_count in zip(self.bounds, self.bits_per_variable):
            gene_bits = chromosome[start_index:start_index + bits_count]
            start_index += bits_count

            integer_value = int("".join(str(bit) for bit in gene_bits), 2)
            max_int = (2 ** bits_count) - 1

            if max_int == 0:
                decoded_value = low
            else:
                decoded_value = low + (integer_value / max_int) * (high - low)

            values.append(decoded_value)

        return values

    def encode_values_to_chromosome(self, values: list[float]) -> list[int]:
        # Enkoduje listę wartości rzeczywistych do jednego chromosomu.
        if len(values) != self.n_vars:
            raise ValueError(
                f"Niepoprawna liczba zmiennych: {len(values)}. Oczekiwano {self.n_vars}."
            )

        chromosome: list[int] = []

        for value, (low, high), bits_count in zip(values, self.bounds, self.bits_per_variable):
            clamped_value = min(max(value, low), high)
            max_int = (2 ** bits_count) - 1

            if high == low:
                integer_value = 0
            else:
                ratio = (clamped_value - low) / (high - low)
                integer_value = round(ratio * max_int)

            bits_str = format(integer_value, f"0{bits_count}b")
            chromosome.extend(int(bit) for bit in bits_str)

        return chromosome

    def calculate_fitness(self, raw_objective: float) -> float:
        # Liczy fitness na podstawie raw objective i trybu min/max.
        if self.objective_mode == "min":
            return 1.0 / (1.0 + abs(raw_objective))

        if self.objective_mode == "max":
            return max(0.0, raw_objective)

        raise ValueError(f"Nieobsługiwany typ optymalizacji: {self.objective_mode}")

    def evaluate_population(self) -> None:
        # Przelicza ewaluację dla całej populacji.
        self.update_after_chromosome_change()

    def get_best_index(self) -> int | None:
        # Zwraca indeks najlepszego osobnika według fitness.
        if not self.fitness_values:
            return None

        return max(range(len(self.fitness_values)), key=lambda idx: self.fitness_values[idx])

    def get_summary(self) -> dict[str, Any]:
        # Zwraca podstawowe podsumowanie populacji.
        best_index = self.get_best_index()

        if best_index is None:
            return {
                "size": self.population_size,
                "chromosome_length": self.chromosome_length,
                "precision": self.precision,
                "bits_per_variable": self.bits_per_variable,
                "best_index": None,
                "best_chromosome": None,
                "best_decoded": None,
                "best_raw_objective": None,
                "best_fitness": None,
                "avg_fitness": None,
                "worst_fitness": None,
            }

        fitness_values = [float(value) for value in self.fitness_values]

        return {
            "size": self.population_size,
            "chromosome_length": self.chromosome_length,
            "precision": self.precision,
            "bits_per_variable": self.bits_per_variable,
            "best_index": best_index,
            "best_chromosome": self.chromosomes[best_index],
            "best_decoded": self.decoded_population[best_index],
            "best_raw_objective": self.raw_objectives[best_index],
            "best_fitness": self.fitness_values[best_index],
            "avg_fitness": sum(fitness_values) / len(fitness_values),
            "worst_fitness": min(fitness_values),
        }

    def __len__(self) -> int:
        return self.population_size

    def __repr__(self) -> str:
        return (
            f"Population(size={self.population_size}, "
            f"n_vars={self.n_vars}, "
            f"chromosome_length={self.chromosome_length})"
        )
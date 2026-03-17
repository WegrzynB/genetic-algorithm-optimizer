# population.py
# Klasa populacji trzymająca chromosomy, dekodowane wartości
# oraz całą ewaluację bieżącego stanu populacji i historię jednego runa.

from __future__ import annotations

import math
import random
import time
from copy import deepcopy
from typing import Any

from ga_optimizer.operators.dispatch.dispatch_crossover import dispatch_crossover
from ga_optimizer.operators.dispatch.dispatch_elitism import dispatch_elitism
from ga_optimizer.operators.dispatch.dispatch_inversion import dispatch_inversion
from ga_optimizer.operators.dispatch.dispatch_mutation import dispatch_mutation
from ga_optimizer.operators.dispatch.dispatch_selection import dispatch_selection
from ga_optimizer.problems.function_catalog import get_problem_definition
from ga_optimizer.utils.helpers import debug_print


def _percentile_from_sorted(values: list[float], percentile: float) -> float | None:
    # Wyznacza percentyl z posortowanej listy metodą liniowej interpolacji.
    if not values:
        return None

    if len(values) == 1:
        return float(values[0])

    position = (len(values) - 1) * percentile
    lower_index = int(position)
    upper_index = min(lower_index + 1, len(values) - 1)
    fraction = position - lower_index

    lower_value = values[lower_index]
    upper_value = values[upper_index]

    return float(lower_value + (upper_value - lower_value) * fraction)


class Population:
    def __init__(self, config_dict: dict[str, Any]):
        # Zachowujemy cały config do dalszego użycia.
        self.config_dict = dict(config_dict)

        # Parametry wykonania.
        self.seed = int(config_dict["seed"])
        self.verbose = bool(config_dict.get("verbose", False))
        self.started_at = time.perf_counter()
        self.elapsed: float | None = None

        # Podstawowe ustawienia problemu i populacji.
        self.problem_name = str(config_dict["problem_name"])
        self.problem_definition = get_problem_definition(self.problem_name)
        self.objective_mode = str(config_dict["objective_mode"])

        self.population_size = int(config_dict["population"])
        self.n_vars = int(config_dict["n_vars"])
        self.range_start = float(config_dict["range_start"])
        self.range_end = float(config_dict["range_end"])

        self.bounds: list[tuple[float, float]] = [
            (self.range_start, self.range_end)
            for _ in range(self.n_vars)
        ]

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

        self.chromosome_length = sum(self.bits_per_variable)

        # Generator losowy.
        self.rng = random.Random(self.seed)
        self.config_dict["rng"] = self.rng

        # Bieżący stan populacji.
        self.chromosomes: list[list[int]] = []
        self.decoded_population: list[list[float]] = []
        self.raw_objectives: list[float | None] = []
        self.fitness_values: list[float | None] = []

        # Historia i summary.
        self.history: list[dict[str, Any]] = []
        self.final_summary: dict[str, Any] | None = None

        # Od razu generujemy populację startową i zapisujemy ją jako epokę 0.
        self._generate_initial_population()
        self.evaluate_population()
        self.record_history(epoch_index=0)

        debug_print(self.verbose, "\n=== STARTOWE CHROMOSOMY ===")
        for index, chromosome in enumerate(self.chromosomes):
            debug_print(self.verbose, f"{index}: {chromosome}")
        debug_print(self.verbose, "===========================\n")

    def _generate_initial_population(self) -> None:
        # Tworzy losową populację startową.
        self.chromosomes = [
            [self.rng.randint(0, 1) for _ in range(self.chromosome_length)]
            for _ in range(self.population_size)
        ]

    def _copy_chromosomes(self, chromosomes: list[list[int]] | None = None) -> list[list[int]]:
        # Zwraca głęboką kopię listy chromosomów.
        source = self.chromosomes if chromosomes is None else chromosomes
        return [chromosome.copy() for chromosome in source]

    def _copy_decoded_population(self, decoded_population: list[list[float]] | None = None) -> list[list[float]]:
        # Zwraca kopię zdekodowanej populacji.
        source = self.decoded_population if decoded_population is None else decoded_population
        return [values.copy() for values in source]

    def _compute_state_for_chromosomes(
        self,
        chromosomes: list[list[int]],
    ) -> tuple[list[list[float]], list[float], list[float]]:
        # Liczy decode/raw objective/fitness dla przekazanych chromosomów bez zmiany stanu obiektu.
        decoded_population = [
            self.decode_chromosome(chromosome)
            for chromosome in chromosomes
        ]

        raw_objectives: list[float] = []
        fitness_values: list[float] = []

        for values in decoded_population:
            raw_value = self.problem_definition.formula(values)
            fitness = self.calculate_fitness(raw_value)

            raw_objectives.append(raw_value)
            fitness_values.append(fitness)

        return decoded_population, raw_objectives, fitness_values

    def set_chromosomes(self, chromosomes: list[list[int]]) -> None:
        # Podmienia chromosomy i odświeża wszystkie dane zależne.
        copied = self._copy_chromosomes(chromosomes)

        for chromosome in copied:
            if len(chromosome) != self.chromosome_length:
                raise ValueError(
                    f"Niepoprawna długość chromosomu: {len(chromosome)}. "
                    f"Oczekiwano {self.chromosome_length}."
                )

        self.chromosomes = copied
        self.population_size = len(copied)
        self.evaluate_population()

    def update_after_chromosome_change(self) -> None:
        # Po zmianie chromosomów aktualizujemy wszystko, co od nich zależy.
        decoded_population, raw_objectives, fitness_values = self._compute_state_for_chromosomes(self.chromosomes)

        self.decoded_population = decoded_population
        self.raw_objectives = raw_objectives
        self.fitness_values = fitness_values

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
        # Zwraca podstawowe podsumowanie populacji oparte o fitness.
        best_index = self.get_best_index()

        if best_index is None:
            return {
                "size": self.population_size,
                "chromosome_length": self.chromosome_length,
                "precision": self.precision,
                "bits_per_variable": self.bits_per_variable.copy(),
                "best_index": None,
                "best_chromosome": None,
                "best_decoded": None,
                "avg_fitness": None,
                "min_fitness": None,
                "q1_fitness": None,
                "median_fitness": None,
                "q3_fitness": None,
                "max_fitness": None,
            }

        fitness_values = [float(value) for value in self.fitness_values]
        sorted_fitness = sorted(fitness_values)

        return {
            "size": self.population_size,
            "chromosome_length": self.chromosome_length,
            "precision": self.precision,
            "bits_per_variable": self.bits_per_variable.copy(),
            "best_index": best_index,
            "best_chromosome": self.chromosomes[best_index].copy(),
            "best_decoded": self.decoded_population[best_index].copy(),
            "avg_fitness": sum(fitness_values) / len(fitness_values),
            "min_fitness": sorted_fitness[0],
            "q1_fitness": _percentile_from_sorted(sorted_fitness, 0.25),
            "median_fitness": _percentile_from_sorted(sorted_fitness, 0.50),
            "q3_fitness": _percentile_from_sorted(sorted_fitness, 0.75),
            "max_fitness": sorted_fitness[-1],
        }

    def record_history(self, epoch_index: int) -> None:
        # Dodaje snapshot bieżącego stanu do historii.
        self.history.append(
            {
                "epoch_index": epoch_index,
                "chromosomes": self._copy_chromosomes(),
                "decoded_population": self._copy_decoded_population(),
                "fitness_values": [float(value) for value in self.fitness_values],
                "summary": deepcopy(self.get_summary()),
            }
        )

    def apply_selection(self) -> list[list[int]]:
        # Wykonuje selekcję na aktualnej populacji.
        return dispatch_selection(population=self, config_dict=self.config_dict)

    def apply_crossover(self, chromosomes: list[list[int]]) -> list[list[int]]:
        # Wykonuje krzyżowanie przekazanych chromosomów.
        return dispatch_crossover(chromosomes=chromosomes, config_dict=self.config_dict)

    def apply_mutation(self, chromosomes: list[list[int]]) -> list[list[int]]:
        # Wykonuje mutację przekazanych chromosomów.
        return dispatch_mutation(chromosomes=chromosomes, config_dict=self.config_dict)

    def apply_inversion(self, chromosomes: list[list[int]]) -> list[list[int]]:
        # Wykonuje inwersję przekazanych chromosomów.
        return dispatch_inversion(chromosomes=chromosomes, config_dict=self.config_dict)

    def apply_elitism(
        self,
        chromosomes: list[list[int]],
        previous_chromosomes: list[list[int]],
        previous_fitness: list[float],
    ) -> list[list[int]]:
        # Wykonuje elitaryzm na przekazanych chromosomach.
        _, _, candidate_fitness = self._compute_state_for_chromosomes(chromosomes)

        return dispatch_elitism(
            chromosomes=chromosomes,
            previous_chromosomes=previous_chromosomes,
            config_dict=self.config_dict,
            fitness_values=candidate_fitness,
            previous_fitness=previous_fitness,
        )

    def run_epoch(self, epoch_index: int) -> int:
        # Wykonuje pełną jedną epokę algorytmu i zapisuje snapshot.
        debug_print(self.verbose, f"\n=== START EPOKI {epoch_index} ===")

        previous_chromosomes = self._copy_chromosomes()
        previous_fitness = [float(value) for value in self.fitness_values]

        selected_chromosomes = self.apply_selection()
        crossed_chromosomes = self.apply_crossover(selected_chromosomes)
        mutated_chromosomes = self.apply_mutation(crossed_chromosomes)
        inverted_chromosomes = self.apply_inversion(mutated_chromosomes)
        final_chromosomes = self.apply_elitism(
            chromosomes=inverted_chromosomes,
            previous_chromosomes=previous_chromosomes,
            previous_fitness=previous_fitness,
        )

        self.set_chromosomes(final_chromosomes)
        self.record_history(epoch_index=epoch_index)

        debug_print(self.verbose, f"\n=== EPOKA {epoch_index} - CHROMOSOMY NA KOŃCU EPOKI ===")
        for index, chromosome in enumerate(self.chromosomes):
            debug_print(self.verbose, f"{index}: {chromosome}")
        debug_print(self.verbose, "================================================================================\n")

        return epoch_index

    def finish_run(self) -> None:
        # Domyka run i zapisuje końcowe summary oraz czas.
        self.final_summary = self.get_summary()
        self.elapsed = time.perf_counter() - self.started_at

    def to_summary_dict(self) -> dict[str, Any]:
        # Zwraca lekką strukturę podsumowującą pojedynczy run.
        if self.final_summary is None:
            self.finish_run()

        return {
            "seed": self.seed,
            "elapsed": self.elapsed,
            "summary": deepcopy(self.final_summary),
        }

    def to_export_dict(self) -> dict[str, Any]:
        # Zwraca eksportowalną strukturę jednego runa.
        if self.final_summary is None:
            self.finish_run()

        return {
            "seed": self.seed,
            "elapsed": self.elapsed,
            "summary": deepcopy(self.final_summary),
            "history": deepcopy(self.history),
            "chromosomes": self._copy_chromosomes(),
            "decoded_population": self._copy_decoded_population(),
            "fitness_values": [float(value) for value in self.fitness_values],
            "config": deepcopy(self.config_dict),
        }

    def __len__(self) -> int:
        return self.population_size

    def __repr__(self) -> str:
        return (
            f"Population(size={self.population_size}, "
            f"n_vars={self.n_vars}, "
            f"chromosome_length={self.chromosome_length}, "
            f"seed={self.seed})"
        )
# presets.py
# Presety konfiguracji GUI.

from copy import deepcopy

from ga_optimizer.config.schema import GAConfig
from ga_optimizer.config.defaults import build_default_config


def _config_to_preset_dict(config: GAConfig) -> dict:
    return {
        "problem_name": config.problem_name,
        "objective_mode": config.objective_mode,
        "n_vars": config.n_vars,
        "range_start": config.range_start,
        "range_end": config.range_end,
        "population": config.population,
        "epochs": config.epochs,
        "run_count": config.run_count,
        "seed": config.seed,
        "precision_mode": config.precision_mode,
        "precision_numeric": config.precision_numeric,
        "precision_bits": config.precision_bits,
        "selection_method": config.selection_method,
        "crossover_method": config.crossover_method,
        "mutation_method": config.mutation_method,
        "inversion_enabled": config.inversion_enabled,
        "elitism_enabled": config.elitism_enabled,
        "method_params": deepcopy(config.method_params),
    }


_default_cfg = build_default_config()
DEFAULT_PRESET = _config_to_preset_dict(_default_cfg)


def _make_preset(name: str, range_start: float, range_end: float, updates: dict) -> dict:
    cfg = deepcopy(DEFAULT_PRESET)
    cfg["problem_name"] = name
    cfg["range_start"] = range_start
    cfg["range_end"] = range_end
    cfg["precision_mode"] = "bits"
    cfg.update(updates)
    return cfg


OPTIMAL_PRESETS = {

    "DeJong3": _make_preset("DeJong3", -3.8, 3.8, {
        "selection_method": "roulette",
        "crossover_method": "three_point",
        "mutation_method": "one_point",
        "inversion_enabled": False,
        "elitism_enabled": True,
        "population": 800,
        "epochs": 400,
        "run_count": 35,
        "precision_bits": 10,
    }),

    "Rastrigin": _make_preset("Rastrigin", -5.12, 5.12, {
        "selection_method": "tournament",
        "crossover_method": "arithmetic",
        "mutation_method": "swap",
        "inversion_enabled": False,
        "elitism_enabled": False,
        "population": 800,
        "epochs": 400,
        "run_count": 40,
        "precision_bits": 30,
    }),

    "Hyperellipsoid": _make_preset("Hyperellipsoid", -65.536, 65.536, {
        "selection_method": "best",
        "crossover_method": "reduced_surro",
        "mutation_method": "one_point",
        "inversion_enabled": False,
        "elitism_enabled": False,
        "population": 500,
        "epochs": 350,
        "run_count": 20,
        "precision_bits": 22,
    }),

    "MartinGaddy": _make_preset("MartinGaddy", -20.0, 20.0, {
        "selection_method": "tournament",
        "crossover_method": "shuffle",
        "mutation_method": "edge",
        "inversion_enabled": True,
        "elitism_enabled": False,
        "population": 300,
        "epochs": 400,
        "run_count": 30,
        "precision_bits": 26,
    }),

    "Hypersphere": _make_preset("Hypersphere", -5.0, 5.0, {
        "selection_method": "best",
        "crossover_method": "two_point",
        "mutation_method": "reset",
        "inversion_enabled": True,
        "elitism_enabled": True,
        "population": 700,
        "epochs": 350,
        "run_count": 35,
        "precision_bits": 22,
    }),

    "GoldsteinPrice": _make_preset("GoldsteinPrice", -2.0, 2.0, {
        "selection_method": "tournament",
        "crossover_method": "shuffle",
        "mutation_method": "swap",
        "inversion_enabled": True,
        "elitism_enabled": True,
        "population": 700,
        "epochs": 400,
        "run_count": 50,
        "precision_bits": 24,
    }),

    "DeJong5": _make_preset("DeJong5", -65.536, 65.536, {
        "selection_method": "tournament",
        "crossover_method": "one_point",
        "mutation_method": "reset",
        "inversion_enabled": False,
        "elitism_enabled": True,
        "population": 700,
        "epochs": 300,
        "run_count": 45,
        "precision_bits": 12,
    }),

    "PichenyGoldsteinPrice": _make_preset("PichenyGoldsteinPrice", -2.0, 2.0, {
        "selection_method": "double_tournament",
        "crossover_method": "majority",
        "mutation_method": "two_point",
        "inversion_enabled": False,
        "elitism_enabled": True,
        "population": 500,
        "epochs": 300,
        "run_count": 20,
        "precision_bits": 22,
    }),

    "Michalewicz": _make_preset("Michalewicz", 0.0, 3.141592653589793, {
        "selection_method": "tournament",
        "crossover_method": "two_point",
        "mutation_method": "swap",
        "inversion_enabled": False,
        "elitism_enabled": False,
        "population": 500,
        "epochs": 300,
        "run_count": 50,
        "precision_bits": 16,
    }),

    "Ackley": _make_preset("Ackley", -32.768, 32.768, {
        "selection_method": "tournament",
        "crossover_method": "shuffle",
        "mutation_method": "reset",
        "inversion_enabled": False,
        "elitism_enabled": True,
        "population": 700,
        "epochs": 250,
        "run_count": 15,
        "precision_bits": 28,
    }),

    "McCormick": _make_preset("McCormick", -3.0, 4.0, {
        "selection_method": "double_tournament",
        "crossover_method": "majority",
        "mutation_method": "two_point",
        "inversion_enabled": False,
        "elitism_enabled": True,
        "population": 700,
        "epochs": 350,
        "run_count": 35,
        "precision_bits": 26,
    }),

    "Griewank": _make_preset("Griewank", -600.0, 600.0, {
        "selection_method": "sus",
        "crossover_method": "arithmetic",
        "mutation_method": "scramble",
        "inversion_enabled": False,
        "elitism_enabled": False,
        "population": 300,
        "epochs": 300,
        "run_count": 30,
        "precision_bits": 16,
    }),

    "Himmelblau": _make_preset("Himmelblau", -5.0, 5.0, {
        "selection_method": "double_tournament",
        "crossover_method": "shuffle",
        "mutation_method": "swap",
        "inversion_enabled": False,
        "elitism_enabled": False,
        "population": 400,
        "epochs": 200,
        "run_count": 10,
        "precision_bits": 18,
    }),

    "Schwefel": _make_preset("Schwefel", -500.0, 500.0, {
        "selection_method": "double_tournament",
        "crossover_method": "disruptive",
        "mutation_method": "bit_flip",
        "elitism_enabled": False,
        "inversion_enabled": False,
        "population": 600,
        "epochs": 500,
        "run_count": 15,
        "precision_bits": 18,
    }),

    "PitsAndHoles": _make_preset("PitsAndHoles", -20.0, 20.0, {
        "selection_method": "double_tournament",
        "crossover_method": "segmented",
        "mutation_method": "scramble",
        "inversion_enabled": False,
        "elitism_enabled": True,
        "population": 700,
        "epochs": 450,
        "run_count": 45,
        "precision_bits": 30,
    }),

    "Easom": _make_preset("Easom", -100.0, 100.0, {
        "selection_method": "sus",
        "crossover_method": "shuffle",
        "mutation_method": "two_point",
        "inversion_enabled": False,
        "elitism_enabled": False,
        "population": 200,
        "epochs": 450,
        "run_count": 40,
        "precision_bits": 22,
    }),

    "StyblinskiTang": _make_preset("StyblinskiTang", -5.0, 5.0, {
        "selection_method": "best",
        "crossover_method": "disruptive",
        "mutation_method": "scramble",
        "inversion_enabled": False,
        "elitism_enabled": False,
        "population": 600,
        "epochs": 300,
        "run_count": 50,
        "precision_bits": 10,
    }),

    "Schaffer2": _make_preset("Schaffer2", -100.0, 100.0, {
        "selection_method": "double_tournament",
        "crossover_method": "shuffle",
        "mutation_method": "scramble",
        "inversion_enabled": False,
        "elitism_enabled": False,
        "population": 300,
        "epochs": 350,
        "run_count": 45,
        "precision_bits": 24,
    }),

    "Rosenbrock": _make_preset("Rosenbrock", -2.048, 2.048, {
        "selection_method": "best",
        "crossover_method": "disruptive",
        "mutation_method": "reset",
        "inversion_enabled": False,
        "elitism_enabled": False,
        "population": 300,
        "epochs": 450,
        "run_count": 10,
        "precision_bits": 16,
    }),

    "Rana": _make_preset("Rana", -515.0, 515.0, {
        "selection_method": "sus",
        "crossover_method": "one_point",
        "mutation_method": "reset",
        "inversion_enabled": True,
        "elitism_enabled": True,
        "population": 600,
        "epochs": 400,
        "run_count": 50,
        "precision_bits": 14,
    }),

    "Eggholder": _make_preset("Eggholder", -515.0, 515.0, {
        "selection_method": "double_tournament",
        "crossover_method": "shuffle",
        "mutation_method": "bit_flip",
        "inversion_enabled": False,
        "elitism_enabled": True,
        "population": 700,
        "epochs": 500,
        "run_count": 25,
        "precision_bits": 30,
    }),
}


PRESETS = {
    "Default": DEFAULT_PRESET,
    **OPTIMAL_PRESETS,
}
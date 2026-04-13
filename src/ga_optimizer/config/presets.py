# presets.py
# Presety konfiguracji GUI.

from copy import deepcopy

from ga_optimizer.config.schema import GAConfig
from ga_optimizer.config.defaults import build_default_config


def _config_to_preset_dict(config: GAConfig) -> dict:
    # Zamienia obiekt configu na zwykły słownik presetu.
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

TEST_CUSTOM_PRESET = deepcopy(DEFAULT_PRESET)
TEST_CUSTOM_PRESET.update(
    {
        "population": 20,
        "epochs": 15,
        "run_count": 3,
        "seed": 123,
        "precision_mode": "bits",
        "precision_bits": 10,
        "selection_method": "tournament",
        "crossover_method": "two_point",
        "mutation_method": "scramble",
        "inversion_enabled": False,
        "elitism_enabled": False,
        "method_params": {
            **deepcopy(DEFAULT_PRESET["method_params"]),
            "selection_tournament_k": 8,
            "crossover_two_point_p": 0.5,
            "mutation_scramble_p": 0.6,
        },
    }
)


# ---------------------------------------------------------------------------
# Pomocnik: buduje preset funkcji na bazie DEFAULT_PRESET.
# Nadpisuje tylko te klucze, które różnią się od domyślnych.
# method_params zawsze dziedziczy pełen zestaw kluczy z DEFAULT_PRESET
# (żeby nie brakło żadnego klucza wymaganego przez schemat).
# ---------------------------------------------------------------------------
def _function_preset(overrides: dict) -> dict:
    preset = deepcopy(DEFAULT_PRESET)
    method_params_overrides = overrides.pop("method_params", {})
    preset.update(overrides)
    preset["method_params"] = {
        **deepcopy(DEFAULT_PRESET["method_params"]),
        **method_params_overrides,
    }
    return preset

DEJONG3_PRESET = _function_preset({
    "problem_name": "DeJong3",
    "objective_mode": "min",
    "selection_method": "roulette",
    "crossover_method": "three_point",
    "mutation_method": "one_point",
    "inversion_enabled": False,
    "elitism_enabled": True,
    "population": 800,
    "epochs": 400,
    "run_count": 35,
    "precision_mode": "bits",
    "precision_bits": 10,
})

RASTRIGIN_PRESET = _function_preset({
    "problem_name": "Rastrigin",
    "objective_mode": "min",
    "selection_method": "tournament",
    "crossover_method": "arithmetic",
    "mutation_method": "swap",
    "inversion_enabled": False,
    "elitism_enabled": False,
    "population": 800,
    "epochs": 400,
    "run_count": 40,
    "precision_mode": "bits",
    "precision_bits": 30,
})


HYPERELLIPSOID_PRESET = _function_preset({
    "problem_name": "Hyperellipsoid",
    "objective_mode": "min",
    "selection_method": "best",
    "crossover_method": "reduced_surro",
    "mutation_method": "one_point",
    "inversion_enabled": False,
    "elitism_enabled": False,
    "population": 500,
    "epochs": 350,
    "run_count": 20,
    "precision_mode": "bits",
    "precision_bits": 22,
})


MARTINGADDY_PRESET = _function_preset({
    "problem_name": "MartinGaddy",
    "objective_mode": "min",
    "selection_method": "tournament",
    "crossover_method": "shuffle",
    "mutation_method": "edge",
    "inversion_enabled": True,
    "elitism_enabled": False,
    "population": 300,
    "epochs": 400,
    "run_count": 30,
    "precision_mode": "bits",
    "precision_bits": 26,
})


HYPERSPHERE_PRESET = _function_preset({
    "problem_name": "Hypersphere",
    "objective_mode": "min",
    "selection_method": "best",
    "crossover_method": "two_point",
    "mutation_method": "reset",
    "inversion_enabled": True,
    "elitism_enabled": True,
    "population": 700,
    "epochs": 350,
    "run_count": 35,
    "precision_mode": "bits",
    "precision_bits": 22,
})


GOLDSTEINPRICE_PRESET = _function_preset({
    "problem_name": "GoldsteinPrice",
    "objective_mode": "min",
    "selection_method": "tournament",
    "crossover_method": "shuffle",
    "mutation_method": "swap",
    "inversion_enabled": True,
    "elitism_enabled": True,
    "population": 700,
    "epochs": 400,
    "run_count": 50,
    "precision_mode": "bits",
    "precision_bits": 24,
})


DEJONG5_PRESET = _function_preset({
    "problem_name": "DeJong5",
    "objective_mode": "min",
    "selection_method": "tournament",
    "crossover_method": "one_point",
    "mutation_method": "reset",
    "inversion_enabled": False,
    "elitism_enabled": True,
    "population": 700,
    "epochs": 300,
    "run_count": 45,
    "precision_mode": "bits",
    "precision_bits": 12,
})

PICHENYGOLDSTEINPRICE_PRESET = _function_preset({
    "problem_name": "PichenyGoldsteinPrice",
    "objective_mode": "min",
    "selection_method": "double_tournament",
    "crossover_method": "majority",
    "mutation_method": "two_point",
    "inversion_enabled": False,
    "elitism_enabled": True,
    "population": 500,
    "epochs": 300,
    "run_count": 20,
    "precision_mode": "bits",
    "precision_bits": 22,
})


MICHALEWICZ_PRESET = _function_preset({
    "problem_name": "Michalewicz",
    "objective_mode": "min",
    "selection_method": "tournament",
    "crossover_method": "two_point",
    "mutation_method": "swap",
    "inversion_enabled": False,
    "elitism_enabled": False,
    "population": 500,
    "epochs": 300,
    "run_count": 50,
    "precision_mode": "bits",
    "precision_bits": 16,
})


ACKLEY_PRESET = _function_preset({
    "problem_name": "Ackley",
    "objective_mode": "min",
    "selection_method": "tournament",
    "crossover_method": "shuffle",
    "mutation_method": "reset",
    "inversion_enabled": False,
    "elitism_enabled": True,
    "population": 700,
    "epochs": 250,
    "run_count": 15,
    "precision_mode": "bits",
    "precision_bits": 28,
})


MCCORMICK_PRESET = _function_preset({
    "problem_name": "McCormick",
    "objective_mode": "min",
    "selection_method": "double_tournament",
    "crossover_method": "majority",
    "mutation_method": "two_point",
    "inversion_enabled": False,
    "elitism_enabled": True,
    "population": 700,
    "epochs": 350,
    "run_count": 35,
    "precision_mode": "bits",
    "precision_bits": 26,
})


GRIEWANK_PRESET = _function_preset({
    "problem_name": "Griewank",
    "objective_mode": "min",
    "selection_method": "sus",
    "crossover_method": "arithmetic",
    "mutation_method": "scramble",
    "inversion_enabled": False,
    "elitism_enabled": False,
    "population": 300,
    "epochs": 300,
    "run_count": 30,
    "precision_mode": "bits",
    "precision_bits": 16,
})


HIMMELBLAU_PRESET = _function_preset({
    "problem_name": "Himmelblau",
    "objective_mode": "min",
    "selection_method": "double_tournament",
    "crossover_method": "shuffle",
    "mutation_method": "swap",
    "inversion_enabled": False,
    "elitism_enabled": False,
    "population": 400,
    "epochs": 200,
    "run_count": 10,
    "precision_mode": "bits",
    "precision_bits": 18,
})


SCHWEFEL_PRESET = _function_preset({
    "problem_name": "Schwefel",
    "objective_mode": "min",
    "selection_method": "double_tournament",
    "crossover_method": "disruptive",
    "mutation_method": "bit_flip",
    "inversion_enabled": False,
    "elitism_enabled": False,
    "population": 600,
    "epochs": 500,
    "run_count": 15,
    "precision_mode": "bits",
    "precision_bits": 18,
})


PITSANDHOLES_PRESET = _function_preset({
    "problem_name": "PitsAndHoles",
    "objective_mode": "min",
    "selection_method": "double_tournament",
    "crossover_method": "segmented",
    "mutation_method": "scramble",
    "inversion_enabled": False,
    "elitism_enabled": True,
    "population": 700,
    "epochs": 450,
    "run_count": 45,
    "precision_mode": "bits",
    "precision_bits": 30,
})


EASOM_PRESET = _function_preset({
    "problem_name": "Easom",
    "objective_mode": "min",
    "selection_method": "sus",
    "crossover_method": "shuffle",
    "mutation_method": "two_point",
    "inversion_enabled": False,
    "elitism_enabled": False,
    "population": 200,
    "epochs": 450,
    "run_count": 40,
    "precision_mode": "bits",
    "precision_bits": 22,
})


STYBLINSKITANG_PRESET = _function_preset({
    "problem_name": "StyblinskiTang",
    "objective_mode": "min",
    "selection_method": "best",
    "crossover_method": "disruptive",
    "mutation_method": "scramble",
    "inversion_enabled": False,
    "elitism_enabled": False,
    "population": 600,
    "epochs": 300,
    "run_count": 50,
    "precision_mode": "bits",
    "precision_bits": 10,
})


SCHAFFER2_PRESET = _function_preset({
    "problem_name": "Schaffer2",
    "objective_mode": "min",
    "selection_method": "double_tournament",
    "crossover_method": "shuffle",
    "mutation_method": "scramble",
    "inversion_enabled": False,
    "elitism_enabled": False,
    "population": 300,
    "epochs": 350,
    "run_count": 45,
    "precision_mode": "bits",
    "precision_bits": 24,
})


ROSENBROCK_PRESET = _function_preset({
    "problem_name": "Rosenbrock",
    "objective_mode": "min",
    "selection_method": "best",
    "crossover_method": "disruptive",
    "mutation_method": "reset",
    "inversion_enabled": False,
    "elitism_enabled": False,
    "population": 300,
    "epochs": 450,
    "run_count": 10,
    "precision_mode": "bits",
    "precision_bits": 16,
})


RANA_PRESET = _function_preset({
    "problem_name": "Rana",
    "objective_mode": "min",
    "selection_method": "sus",
    "crossover_method": "one_point",
    "mutation_method": "reset",
    "inversion_enabled": True,
    "elitism_enabled": True,
    "population": 600,
    "epochs": 400,
    "run_count": 50,
    "precision_mode": "bits",
    "precision_bits": 14,
})

EGGHOLDER_PRESET = _function_preset({
    "problem_name": "Eggholder",
    "objective_mode": "min",
    "selection_method": "double_tournament",
    "crossover_method": "shuffle",
    "mutation_method": "bit_flip",
    "inversion_enabled": False,
    "elitism_enabled": True,
    "population": 700,
    "epochs": 500,
    "run_count": 25,
    "precision_mode": "bits",
    "precision_bits": 30,
})


PRESETS = {
    "Default": DEFAULT_PRESET,
    "test_custom": TEST_CUSTOM_PRESET,

    # Presety per-funkcja
    "DeJong3":               DEJONG3_PRESET,
    "Rastrigin":             RASTRIGIN_PRESET,
    "Hyperellipsoid":        HYPERELLIPSOID_PRESET,
    "MartinGaddy":           MARTINGADDY_PRESET,
    "Hypersphere":           HYPERSPHERE_PRESET,
    "GoldsteinPrice":        GOLDSTEINPRICE_PRESET,
    "DeJong5":               DEJONG5_PRESET,
    "PichenyGoldsteinPrice": PICHENYGOLDSTEINPRICE_PRESET,
    "Michalewicz":           MICHALEWICZ_PRESET,
    "Ackley":                ACKLEY_PRESET,
    "McCormick":             MCCORMICK_PRESET,
    "Griewank":              GRIEWANK_PRESET,
    "Himmelblau":            HIMMELBLAU_PRESET,
    "Schwefel":              SCHWEFEL_PRESET,
    "PitsAndHoles":          PITSANDHOLES_PRESET,
    "Easom":                 EASOM_PRESET,
    "StyblinskiTang":        STYBLINSKITANG_PRESET,
    "Schaffer2":             SCHAFFER2_PRESET,
    "Rosenbrock":            ROSENBROCK_PRESET,
    "Rana":                  RANA_PRESET,
    "Eggholder":             EGGHOLDER_PRESET,
}
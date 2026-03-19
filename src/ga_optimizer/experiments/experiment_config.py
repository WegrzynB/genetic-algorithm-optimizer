from __future__ import annotations

from ga_optimizer.config.method_crossover import CROSSOVER_METHOD_PARAM_SPECS
from ga_optimizer.config.method_mutation import MUTATION_METHOD_PARAM_SPECS
from ga_optimizer.config.method_selection import SELECTION_METHOD_PARAM_SPECS

# ============================================================
# AKTYWNY PRESET
# ============================================================
ACTIVE_EXPERIMENT_NAME = "random_functions_default"

# Inne:
# ACTIVE_EXPERIMENT_NAME = "single_function_operator_search_default"
# ACTIVE_EXPERIMENT_NAME = "random_functions_default"
# ACTIVE_EXPERIMENT_NAME = "all_functions_global_default"
# ACTIVE_EXPERIMENT_NAME = "sensitivity_default"
# ACTIVE_EXPERIMENT_NAME = "ablation_default"

# ============================================================
# FUNKCJA DO TESTÓW JEDNOFUNKCYJNYCH
# ============================================================
TARGET_PROBLEM_NAME = "Rosenbrock"
# inne:
# TARGET_PROBLEM_NAME = "Ackley"
# TARGET_PROBLEM_NAME = "Hypersphere"
# TARGET_PROBLEM_NAME = "Rastrigin"
# TARGET_PROBLEM_NAME = "Himmelblau"
# TARGET_PROBLEM_NAME = "Schwefel"
# TARGET_PROBLEM_NAME = "Michalewicz"
# TARGET_PROBLEM_NAME = "Easom"
# TARGET_PROBLEM_NAME = "McCormick"

# ============================================================
# PROGI DO OCENY JAKOŚCI
# ============================================================
SUCCESS_VALUE_ABS_TOL = 1e-2
SUCCESS_POINT_DISTANCE_TOL = 0.5

# ============================================================
# ZAKRESY GŁÓWNE
# ============================================================
GLOBAL_RANDOM_RANGES = {
    "population": (200, 500),
    "epochs": (200, 500),
    "run_count": (10, 50),
    "precision_bits": (8, 30),
    "inversion_enabled": [True, False],
    "elitism_enabled": [True, False],
    "selection_method": list(SELECTION_METHOD_PARAM_SPECS.keys()),
    "crossover_method": list(CROSSOVER_METHOD_PARAM_SPECS.keys()),
    "mutation_method": list(MUTATION_METHOD_PARAM_SPECS.keys()),
}

# ============================================================
# SENSOWNE ZAKRESY PARAMETRÓW METOD
# Dobierane względem defaultów/speców:
# - selection k: raczej małe/średnie
# - crossover p: głównie okolice sensownych środków
# - mutation p: raczej niskie
# ============================================================
METHOD_PARAM_RANGE_OVERRIDES = {
    # =========================
    # SELECTION
    # =========================
    # best / worst: default 2, min 1
    "selection_best_k": (2, 10),
    "selection_worst_k": (2, 10),

    # tournament: default 3, min 2
    "selection_tournament_k": (2, 12),

    # double tournament: defaults 3 / 3, min 1
    "selection_double_tournament_k1": (2, 8),
    "selection_double_tournament_k2": (2, 8),

    # roulette / sus: tylko stabilizacja, sensownie bardzo małe
    "selection_roulette_eps": (1e-10, 1e-8),
    "selection_sus_eps": (1e-10, 1e-8),

    # =========================
    # CROSSOVER
    # =========================
    # one_point default 0.3
    "crossover_one_point_p": (0.25, 0.60),

    # two_point default 0.4
    "crossover_two_point_p": (0.30, 0.70),

    # three_point default 0.4
    "crossover_three_point_p": (0.30, 0.70),

    # multi_point default 0.5
    "crossover_multi_point_p": (0.35, 0.75),
    "crossover_multi_point_k": (2, 6),

    # uniform default 0.5
    "crossover_uniform_p": (0.35, 0.70),

    # shuffle default 0.5
    "crossover_shuffle_p": (0.35, 0.75),

    # granular default 0.8
    "crossover_granular_p": (0.60, 0.90),
    "crossover_granular_granularity": (2, 6),

    # segmented default 3
    "crossover_segment_length": (2, 6),

    # arithmetic default 0.5
    "crossover_arithmetic_alpha": (0.30, 0.70),

    # reduced_surro default 0.5
    "crossover_reduced_surro_p": (0.35, 0.75),

    # disruptive default 0.5
    "crossover_disruptive_p": (0.35, 0.75),

    # majority default 0.5
    "crossover_majority_p": (0.35, 0.75),

    # =========================
    # MUTATION
    # =========================
    # defaults są małe: 0.04 - 0.10
    "mutation_bit_flip_p": (0.02, 0.12),
    "mutation_one_point_p": (0.01, 0.08),
    "mutation_two_point_p": (0.01, 0.08),
    "mutation_edge_p": (0.02, 0.12),
    "mutation_reset_p": (0.01, 0.07),
    "mutation_scramble_p": (0.01, 0.07),
    "mutation_swap_p": (0.01, 0.08),
}

# ============================================================
# ILOŚĆ WYKONAŃ TESTÓW
# ============================================================
RANDOM_FUNCTIONS_EXECUTIONS = 10
ALL_FUNCTIONS_EXECUTIONS_PER_FUNCTION = 3
SINGLE_FUNCTION_EXECUTIONS = 20
SENSITIVITY_EXECUTIONS_PER_VALUE = 3
ABLATION_EXECUTIONS_PER_VARIANT = 3

# ============================================================
# PRESETY
# ============================================================
EXPERIMENT_PRESETS = {
    "random_functions_default": {
        "test_name": "random_functions",
        "description": "Losuje funkcję i konfigurację operatorów. Wszystko jest losowe.",
        "seed": "",
        "save_plots": True,
        "executions": RANDOM_FUNCTIONS_EXECUTIONS,
        "problem_pool": "all",
        "success_value_abs_tol": SUCCESS_VALUE_ABS_TOL,
        "success_point_distance_tol": SUCCESS_POINT_DISTANCE_TOL,
        "ranges": {
            **GLOBAL_RANDOM_RANGES,
        },
    },

    "all_functions_global_default": {
        "test_name": "all_functions_global_operator_search",
        "description": "Dla każdej funkcji wykonuje określoną liczbę pełnych uruchomień i szuka operatorów dobrych globalnie.",
        "seed": "",
        "save_plots": True,
        "problem_names": "all",
        "executions_per_function": ALL_FUNCTIONS_EXECUTIONS_PER_FUNCTION,
        "success_value_abs_tol": SUCCESS_VALUE_ABS_TOL,
        "success_point_distance_tol": SUCCESS_POINT_DISTANCE_TOL,
        "ranges": {
            **GLOBAL_RANDOM_RANGES,
        },
    },

    "single_function_operator_search_default": {
        "test_name": "single_function_operator_search",
        "description": "Testuje jedną wybraną funkcję dla losowych konfiguracji i wskazuje najlepsze kombinacje oraz najlepsze obszary parametrów.",
        "seed": "",
        "save_plots": True,
        "problem_name": TARGET_PROBLEM_NAME,
        "executions": SINGLE_FUNCTION_EXECUTIONS,
        "success_value_abs_tol": SUCCESS_VALUE_ABS_TOL,
        "success_point_distance_tol": SUCCESS_POINT_DISTANCE_TOL,
        "top_fraction_for_regions": 0.25,
        "ranges": {
            **GLOBAL_RANDOM_RANGES,
        },
    },

    "sensitivity_default": {
        "test_name": "sensitivity_test",
        "description": "Bada wrażliwość jednej funkcji na pojedynczy parametr.",
        "seed": "",
        "save_plots": True,
        "problem_name": TARGET_PROBLEM_NAME,
        "sensitivity_parameter": "population",
        # inne:
        # "epochs", "run_count", "precision_bits",
        # "selection_tournament_k",
        # "crossover_two_point_p",
        # "mutation_scramble_p"
        "parameter_values": {
            "population": [200, 275, 350, 425, 500],
            "epochs": [200, 275, 350, 425, 500],
            "run_count": [10, 20, 30, 40, 50],
            "precision_bits": [8, 12, 16, 24, 30],
            "selection_tournament_k": [2, 4, 8, 12],
            "crossover_two_point_p": [0.30, 0.45, 0.55, 0.65, 0.70],
            "mutation_scramble_p": [0.01, 0.02, 0.03, 0.05, 0.07],
        },
        "executions_per_value": SENSITIVITY_EXECUTIONS_PER_VALUE,
        "success_value_abs_tol": SUCCESS_VALUE_ABS_TOL,
        "success_point_distance_tol": SUCCESS_POINT_DISTANCE_TOL,
        "base_config": {
            "selection_method": "tournament",
            "crossover_method": "two_point",
            "mutation_method": "scramble",
            "inversion_enabled": True,
            "elitism_enabled": True,
            "population": 300,
            "epochs": 300,
            "run_count": 20,
            "precision_bits": 12,
            "method_params": {
                "selection_tournament_k": 6,
                "crossover_two_point_p": 0.55,
                "mutation_scramble_p": 0.03,
            },
        },
        "ranges": {
            **GLOBAL_RANDOM_RANGES,
        },
    },

    "ablation_default": {
        "test_name": "ablation_test",
        "description": "Porównuje bazową konfigurację z wariantami po wyłączeniu lub podmianie pojedynczego składnika.",
        "seed": "",
        "save_plots": True,
        "problem_name": TARGET_PROBLEM_NAME,
        "executions_per_variant": ABLATION_EXECUTIONS_PER_VARIANT,
        "success_value_abs_tol": SUCCESS_VALUE_ABS_TOL,
        "success_point_distance_tol": SUCCESS_POINT_DISTANCE_TOL,
        "base_config": {
            "selection_method": "tournament",
            "crossover_method": "two_point",
            "mutation_method": "scramble",
            "inversion_enabled": True,
            "elitism_enabled": True,
            "population": 300,
            "epochs": 300,
            "run_count": 20,
            "precision_bits": 12,
            "method_params": {
                "selection_tournament_k": 6,
                "crossover_two_point_p": 0.55,
                "mutation_scramble_p": 0.03,
            },
        },
        "variants": [
            "base",
            "no_elitism",
            "no_inversion",
            "selection_roulette",
            "selection_best",
            "crossover_uniform",
            "crossover_one_point",
            "mutation_bit_flip",
            "mutation_reset",
        ],
        "ranges": {
            **GLOBAL_RANDOM_RANGES,
        },
    },
}
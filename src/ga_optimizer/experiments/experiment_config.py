# experiment_config.py
from __future__ import annotations

from ga_optimizer.config.method_crossover import CROSSOVER_METHOD_PARAM_SPECS
from ga_optimizer.config.method_mutation import MUTATION_METHOD_PARAM_SPECS
from ga_optimizer.config.method_selection import SELECTION_METHOD_PARAM_SPECS

# ============================================================
# AKTYWNY PRESET
# ============================================================
ACTIVE_EXPERIMENT_NAME = "single_function_operator_search_default"

# Inne:
# ACTIVE_EXPERIMENT_NAME = "random_functions_default"
# ACTIVE_EXPERIMENT_NAME = "all_functions_global_default"
# ACTIVE_EXPERIMENT_NAME = "single_function_operator_search_default"

# ============================================================
# ILOŚĆ WYKONAŃ TESTÓW
# ============================================================
RANDOM_FUNCTIONS_EXECUTIONS = 100
ALL_FUNCTIONS_EXECUTIONS_PER_FUNCTION = 10
SINGLE_FUNCTION_EXECUTIONS = 300

# ============================================================
# FUNKCJA DO TESTÓW JEDNOFUNKCYJNYCH
# ============================================================
TARGET_PROBLEM_NAME = "Eggholder"
# inne:
# TARGET_PROBLEM_NAME = "Eggholder"
# TARGET_PROBLEM_NAME = "Rosenbrock"
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
# value tol zostawiam pomocniczo
SUCCESS_VALUE_ABS_TOL = 1e-1

# to jest teraz ważniejszy próg
# 0.25 = dość wymagający
# 0.5 = rozsądny środek
# 1.0 = bardziej łagodny
SUCCESS_POINT_DISTANCE_TOL = 1.0

# ============================================================
# ZAKRESY GŁÓWNE Z KROKIEM
# Losowanie jest dyskretne po step, nie ciągłe.
# ============================================================
GLOBAL_RANDOM_RANGES = {
    # "population": {"start": 200, "end": 800, "step": 100}, # DOMYŚLNE
    "population": {"start": 600, "end": 1000, "step": 100},

    # "epochs": {"start": 200, "end": 500, "step": 50}, # DOMYŚLNE
    "epochs": {"start": 300, "end": 500, "step": 50},

    # "run_count": {"start": 10, "end": 50, "step": 5}, # DOMYŚLNE
    "run_count": {"start": 10, "end": 10, "step": 1},

    # "precision_bits": {"start": 8, "end": 30, "step": 2}, # DOMYŚLNE
    "precision_bits": {"start": 20, "end": 20, "step": 2},

    "inversion_enabled": {"values": [True, False]},
    "elitism_enabled": {"values": [True, False]},
    "selection_method": {"values": list(SELECTION_METHOD_PARAM_SPECS.keys())},
    "crossover_method": {"values": list(CROSSOVER_METHOD_PARAM_SPECS.keys())},
    "mutation_method": {"values": list(MUTATION_METHOD_PARAM_SPECS.keys())},
}

# ============================================================
# ZAKRESY PARAMETRÓW METOD Z KROKIEM
# ============================================================
METHOD_PARAM_RANGE_OVERRIDES = {
    # SELECTION
    "selection_best_k": {"start": 3, "end": 7, "step": 1},
    "selection_worst_k": {"start": 3, "end": 7, "step": 1},
    "selection_tournament_k": {"start": 3, "end": 8, "step": 1},
    "selection_double_tournament_k1": {"start": 3, "end": 6, "step": 1},
    "selection_double_tournament_k2": {"start": 3, "end": 6, "step": 1},
    "selection_roulette_eps": {"values": [1e-9, 1e-8]},
    "selection_sus_eps": {"values": [1e-9, 1e-8]},

    # CROSSOVER
    "crossover_one_point_p": {"start": 0.35, "end": 0.55, "step": 0.05},
    "crossover_two_point_p": {"start": 0.40, "end": 0.60, "step": 0.05},
    "crossover_three_point_p": {"start": 0.40, "end": 0.60, "step": 0.05},
    "crossover_multi_point_p": {"start": 0.45, "end": 0.65, "step": 0.05},
    "crossover_multi_point_k": {"start": 2, "end": 4, "step": 1},
    "crossover_uniform_p": {"start": 0.45, "end": 0.65, "step": 0.05},
    "crossover_shuffle_p": {"start": 0.45, "end": 0.65, "step": 0.05},
    "crossover_granular_p": {"start": 0.70, "end": 0.85, "step": 0.05},
    "crossover_granular_granularity": {"start": 2, "end": 4, "step": 1},
    "crossover_segment_length": {"start": 2, "end": 4, "step": 1},
    "crossover_arithmetic_alpha": {"start": 0.40, "end": 0.60, "step": 0.05},
    "crossover_reduced_surro_p": {"start": 0.45, "end": 0.65, "step": 0.05},
    "crossover_disruptive_p": {"start": 0.45, "end": 0.65, "step": 0.05},
    "crossover_majority_p": {"start": 0.45, "end": 0.65, "step": 0.05},

    # MUTATION
    "mutation_edge_p": {"start": 0.02, "end": 0.05, "step": 0.01},
    "mutation_edge_mode": {"values": ["Ends", "First_last", "Both"]},
    "mutation_one_point_p": {"start": 0.02, "end": 0.05, "step": 0.01},
    "mutation_two_point_p": {"start": 0.02, "end": 0.05, "step": 0.01},
    "mutation_bit_flip_p": {"start": 0.02, "end": 0.05, "step": 0.01},
    "mutation_swap_p": {"start": 0.02, "end": 0.05, "step": 0.01},
    "mutation_scramble_p": {"start": 0.02, "end": 0.05, "step": 0.01},
    "mutation_reset_p": {"start": 0.015, "end": 0.040, "step": 0.005},
}

# ============================================================
# PRESETY
# ============================================================
EXPERIMENT_PRESETS = {
    "random_functions_default": {
        "test_name": "random_functions",
        "description": "Losuje funkcję i konfigurację operatorów. Ten test służy do znalezienia operatorów dobrych ogólnie, niezależnie od konkretnej funkcji.",
        "seed": None,
        "save_plots": True,
        "executions": RANDOM_FUNCTIONS_EXECUTIONS,
        "problem_pool": "all",
        "success_value_abs_tol": SUCCESS_VALUE_ABS_TOL,
        "success_point_distance_tol": SUCCESS_POINT_DISTANCE_TOL,
        "ranges": {**GLOBAL_RANDOM_RANGES},
    },

    "all_functions_global_default": {
        "test_name": "all_functions_global_operator_search",
        "description": "Dla każdej funkcji wykonuje określoną liczbę pełnych uruchomień i szuka operatorów dobrych dla konkretnych funkcji oraz porównuje zachowanie między funkcjami.",
        "seed": None,
        "save_plots": True,
        "problem_names": "all",
        "executions_per_function": ALL_FUNCTIONS_EXECUTIONS_PER_FUNCTION,
        "success_value_abs_tol": SUCCESS_VALUE_ABS_TOL,
        "success_point_distance_tol": SUCCESS_POINT_DISTANCE_TOL,
        "ranges": {**GLOBAL_RANDOM_RANGES},
    },

    "single_function_operator_search_default": {
        "test_name": "single_function_operator_search",
        "description": "Testuje jedną wybraną funkcję dla losowych konfiguracji i wskazuje najlepsze kombinacje oraz najlepsze obszary parametrów dla tej konkretnej funkcji.",
        "seed": None,
        "save_plots": True,
        "problem_name": TARGET_PROBLEM_NAME,
        "executions": SINGLE_FUNCTION_EXECUTIONS,
        "success_value_abs_tol": SUCCESS_VALUE_ABS_TOL,
        "success_point_distance_tol": SUCCESS_POINT_DISTANCE_TOL,
        "top_fraction_for_regions": 0.25,
        "heatmap_bins": 40,
        "ranges": {**GLOBAL_RANDOM_RANGES},
    },
}
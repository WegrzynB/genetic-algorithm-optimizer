# method_selection.py
# Specyfikacje parametrów metod selekcji.

SELECTION_METHOD_LABELS = {
    "best": "Najlepsza",
    "worst": "Najgorszych",
    "unbiased": "Beztendencyjna",
    "roulette": "Ruletka",
    "sus": "Stochastyczny dobór uniwersalny",
    "tournament": "Turniejowa",
    "double_tournament": "Podwójna turniejowa",
}

SELECTION_METHOD_PARAM_SPECS = {
    "best": [
        {
            "key": "selection_best_k",
            "label": "K (ile najlepszych)",
            "type": "int",
            "default": 2,
            "min": 1,
        },
    ],

    "worst": [
        {
            "key": "selection_worst_k",
            "label": "K (ile najgorszych)",
            "type": "int",
            "default": 2,
            "min": 1,
        },
    ],

    "unbiased": [
        # Ta metoda jest czysto losowa, nie potrzebuje żadnych parametrów
    ],

    "roulette": [
        {
            "key": "selection_roulette_eps",
            "label": "Eps (stabilizacja)",
            "type": "float",
            "default": 1e-9,
            "min_exclusive": 0.0,
        },
    ],

    "sus": [
        {
            "key": "selection_sus_eps",
            "label": "Eps (stabilizacja)",
            "type": "float",
            "default": 1e-9,
            "min_exclusive": 0.0,
        },
    ],

    "tournament": [
        {
            "key": "selection_tournament_k",
            "label": "K (rozmiar turnieju)",
            "type": "int",
            "default": 4,
            "min": 2,
        },
    ],

    "double_tournament": [
        {
            "key": "selection_double_tournament_k1",
            "label": "K1 (rozmiar małego turnieju)",
            "type": "int",
            "default": 3,
            "min": 1,
        },
        {
            "key": "selection_double_tournament_k2",
            "label": "K2 (liczba turniejów w finale)",
            "type": "int",
            "default": 4,
            "min": 1,
        },
    ],
}
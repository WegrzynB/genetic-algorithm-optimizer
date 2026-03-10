# method_selection.py
# Specyfikacje parametrów metod selekcji.

SELECTION_METHOD_LABELS = {
    "best": "Najlepsza",
    "roulette": "Ruletka",
    "roulette copy": "Ruletka kopia",
    "tournament": "Turniejowa",
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


    "roulette": [
        {
            "key": "selection_roulette_eps",
            "label": "Eps (stabilizacja)",
            "type": "float",
            "default": 1e-9,
            "min_exclusive": 0.0,
        },
    ],


    "roulette copy": [
        {
            "key": "selection_roulette_copy_eps",
            "label": "Eps (stabilizacja)",
            "type": "float",
            "default": 0.2,
            "min_exclusive": 0.0,
        },
    ],


    "tournament": [
        {
            "key": "selection_tournament_k",
            "label": "K (rozmiar turnieju)",
            "type": "int",
            "default": 3,
            "min": 2,
        },
        {
            "key": "selection_tournament_k2",
            "label": "K2",
            "type": "int",
            "default": 3,
            "min": 2,
        },
        {
            "key": "selection_tournament_k3",
            "label": "K3",
            "type": "int",
            "default": 23,
            "min": 2,
        },
        {
            "key": "selection_tournament_k4",
            "label": "K4",
            "type": "int",
            "default": 63,
            "min": 2,
        },
        {
            "key": "selection_tournament_k5",
            "label": "K5",
            "type": "int",
            "default": 33,
            "min": 2,
        },
        {
            "key": "selection_tournament_k6",
            "label": "K6",
            "type": "int",
            "default": 3,
            "min": 2,
        },
        {
            "key": "selection_tournament_k7",
            "label": "K7",
            "type": "int",
            "default": 7,
            "min": 2,
        },
    ],


    
}
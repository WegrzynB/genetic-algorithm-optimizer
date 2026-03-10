# method_crossover.py
# Specyfikacje parametrów metod krzyżowania.

CROSSOVER_METHOD_LABELS = {
    "one_point": "Jednopunktowe",
    "two_point": "Dwupunktowe",
    "granular": "Granularne",
}



CROSSOVER_METHOD_PARAM_SPECS = {
    "one_point": [
        {
            "key": "crossover_one_point_p",
            "label": "P (krzyżowanie)",
            "type": "float",
            "default": 0.2,
            "min": 0.0,
            "max": 1.0,
        },
    ],


    "two_point": [
        {
            "key": "crossover_two_point_p",
            "label": "P (krzyżowanie)",
            "type": "float",
            "default": 0.4,
            "min": 0.0,
            "max": 1.0,
        },
    ],


    "granular": [
        {
            "key": "crossover_granular_p",
            "label": "P (krzyżowanie)",
            "type": "float",
            "default": 0.8,
            "min": 0.0,
            "max": 1.0,
        },
        {
            "key": "crossover_granular_granularity",
            "label": "Ziarnistość",
            "type": "int",
            "default": 2,
            "min": 1,
        },
    ],


    
}
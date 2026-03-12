# method_crossover.py
# Specyfikacje parametrów metod krzyżowania.

CROSSOVER_METHOD_LABELS = {
    "one_point": "Jednopunktowe",
    "two_point": "Dwupunktowe",
    "three_point": "Trzypunktowe",
    "multi_point": "Wielopunktowe",
    "uniform": "Równomierne",
    "shuffle": "Tasujące",
    "granular": "Ziarniste",
    "segmented": "Segmentowe ",
    "arithmetic": "Arytmetyczne",
    "reduced_surro": "Zastępujące",
    "disruptive": "Niszczące",
    "majority": "Większościowe",
}


CROSSOVER_METHOD_PARAM_SPECS = {
    "one_point": [
        {
            "key": "crossover_one_point_p",
            "label": "P (krzyżowanie)",
            "type": "float",
            "default": 0.3,
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

    "three_point": [
        {
            "key": "crossover_three_point_p",
            "label": "P (krzyżowanie)",
            "type": "float",
            "default": 0.4,
            "min": 0.0,
            "max": 1.0,
        },
    ],

    "multi_point": [
        {
            "key": "crossover_multi_point_p",
            "label": "P (krzyżowanie)",
            "type": "float",
            "default": 0.5,
            "min": 0.0,
            "max": 1.0,
        },
        {
            "key": "crossover_multi_point_k",
            "label": "Liczba punktów",
            "type": "int",
            "default": 4,
            "min": 1,
        },
    ],

    "uniform": [
        {
            "key": "crossover_uniform_p",
            "label": "P (zamiana genu)",
            "type": "float",
            "default": 0.5,
            "min": 0.0,
            "max": 1.0,
        },
    ],

    "shuffle": [
        {
            "key": "crossover_shuffle_p",
            "label": "P (krzyżowanie)",
            "type": "float",
            "default": 0.5,
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

    "segmented": [
        {
            "key": "crossover_segment_length",
            "label": "Długość segmentu",
            "type": "int",
            "default": 3,
            "min": 1,
        },
    ],

    "arithmetic": [
        {
            "key": "crossover_arithmetic_alpha",
            "label": "Alpha",
            "type": "float",
            "default": 0.5,
            "min": 0.0,
            "max": 1.0,
        },
    ],


    "reduced_surro": [
        {
            "key": "crossover_reduced_surro_p",
            "label": "P (krzyżowanie)",
            "type": "float",
            "default": 0.5,
            "min": 0.0,
            "max": 1.0,
        },
    ],

    "disruptive": [
        {
            "key": "crossover_disruptive_p",
            "label": "P (krzyżowanie)",
            "type": "float",
            "default": 0.5,
            "min": 0.0,
            "max": 1.0,
        },
    ],

    "majority": [
        {
            "key": "crossover_majority_p",
            "label": "P (krzyżowanie)",
            "type": "float",
            "default": 0.5,
            "min": 0.0,
            "max": 1.0,
        },
    ],

}
# method_mutation.py
# Specyfikacje parametrów metod mutacji.

MUTATION_METHOD_LABELS = {
    "one_point": "Jednopunktowa",
    "two_point": "Dwupunktowa",
    "edge": "Krawędziowa",
    "bit_flip": "Bitowa",
    "swap": "Zamiany",
    "scramble": "Tasowania",
    "reset": "Resetowania"
}


MUTATION_METHOD_PARAM_SPECS = {
    "edge": [
        {
            "key": "mutation_edge_p",
            "label": "P (mutacja)",
            "type": "float",
            "default": 0.03,
            "min": 0.0,
            "max": 1.0,
        },
        {
            "key": "mutation_edge_mode",
            "label": "Tryb brzegowy",
            "type": "enum",
            "values": ["Ends", "First_last", "Both"],
            "default": "Ends",
        },
    ],

    "one_point": [
        {
            "key": "mutation_one_point_p",
            "label": "P (mutacja)",
            "type": "float",
            "default": 0.02,
            "min": 0.0,
            "max": 1.0,
        },
    ],

    "two_point": [
        {
            "key": "mutation_two_point_p",
            "label": "P (mutacja)",
            "type": "float",
            "default": 0.02,
            "min": 0.0,
            "max": 1.0,
        },
    ],

    "bit_flip": [
        {
            "key": "mutation_bit_flip_p",
            "label": "P (mutacja)",
            "type": "float",
            "default": 0.03,
            "min": 0.0,
            "max": 1.0,
        },
    ],

    "swap": [
        {
            "key": "mutation_swap_p",
            "label": "P (mutacja)",
            "type": "float",
            "default": 0.02,
            "min": 0.0,
            "max": 1.0,
        },
    ],

    "scramble": [
        {
            "key": "mutation_scramble_p",
            "label": "P (mutacja)",
            "type": "float",
            "default": 0.02,
            "min": 0.0,
            "max": 1.0,
        },
    ],

    "reset": [
        {
            "key": "mutation_reset_p",
            "label": "P (mutacja)",
            "type": "float",
            "default": 0.015,
            "min": 0.0,
            "max": 1.0,
        },
    ],
}
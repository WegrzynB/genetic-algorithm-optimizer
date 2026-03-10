# method_mutation.py
# Specyfikacje parametrów metod mutacji.

MUTATION_METHOD_LABELS = {
    "edge": "Krawędźowa",
    "one_point": "Jednopunktowa",
    "one_point_copy": "Jednopunktowa kopia",
    "two_point": "Dwupunktowa",
}



MUTATION_METHOD_PARAM_SPECS = {
    "edge": [
        {
            "key": "mutation_edge_p",
            "label": "P (mutacja)",
            "type": "float",
            "default": 0.02,
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
            "default": 0.05,
            "min": 0.0,
            "max": 1.0,
        },
    ],


    "one_point_copy": [
        {
            "key": "mutation_one_point_copy_p",
            "label": "P (mutacja)",
            "type": "float",
            "default": 0.05,
            "min": 0.0,
            "max": 1.0,
        },
    ],


    "two_point": [
        {
            "key": "mutation_two_point_p",
            "label": "P (mutacja)",
            "type": "float",
            "default": 0.07,
            "min": 0.0,
            "max": 1.0,
        },
    ],


    
}
# src/ga_optimizer/visualization/show_charts.py

from typing import Any
import matplotlib.pyplot as plt

from ga_optimizer.visualization.convergence_plots import plot_convergence
from ga_optimizer.visualization.distribution import plot_fitness_distribution
from ga_optimizer.visualization.trajectory import plot_trajectory
from ga_optimizer.visualization.plot_styles import apply_custom_style

def get_all_figures(engine_result: dict[str, Any], input_dict: dict[str, Any]) -> dict[str, plt.Figure]:
    """Generuje wykresy jako obiekty Figure i zwraca w formie słownika, aby GUI mogło je odebrać."""
    
    figures = {}
    
    if not engine_result.get("runs"):
        print("Brak danych z uruchomień algorytmu do wygenerowania wykresów.")
        return figures

    # Nakładamy styl z Twojego pliku (nie musisz tworzyć nowego)
    apply_custom_style()
        
    first_run_history = engine_result["runs"][0]["history"]
    problem_name = input_dict["problem_name"]
    range_start = input_dict["range_start"]
    range_end = input_dict["range_end"]
    n_vars = input_dict["n_vars"]

    # Generujemy wykresy (funkcje w tych plikach MUSZĄ zwracać fig, a nie używać plt.show()!)
    figures["convergence"] = plot_convergence(first_run_history, problem_name)
    figures["distribution"] = plot_fitness_distribution(first_run_history, problem_name)

    # Trajektoria ma sens tylko dla funkcji 2D
    if n_vars == 2:
        figures["trajectory"] = plot_trajectory(first_run_history, problem_name, range_start, range_end)

    return figures
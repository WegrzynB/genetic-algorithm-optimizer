# src/ga_optimizer/visualization/convergence_plots.py

import matplotlib.pyplot as plt
import seaborn as sns
from typing import Any

def plot_convergence(history: list[dict[str, Any]], problem_name: str) -> plt.Figure:
    epochs = [h["epoch_index"] for h in history]
    max_fit = [h["summary"]["max_fitness"] for h in history]
    avg_fit = [h["summary"]["avg_fitness"] for h in history]
    min_fit = [h["summary"]["min_fitness"] for h in history]

    # Tworzymy obiekt figury i osi
    fig, ax = plt.subplots(figsize=(10, 6))

    sns.lineplot(x=epochs, y=max_fit, label="Max Fitness", color="green", linewidth=2, ax=ax)
    sns.lineplot(x=epochs, y=avg_fit, label="Średni Fitness", color="blue", linewidth=2, ax=ax)
    sns.lineplot(x=epochs, y=min_fit, label="Min Fitness", color="red", linewidth=2, linestyle="--", ax=ax)

    ax.set_title(f"Zbieżność Algorytmu - {problem_name}", fontsize=14)
    ax.set_xlabel("Epoka", fontsize=12)
    ax.set_ylabel("Wartość Fitness", fontsize=12)
    ax.legend()
    fig.tight_layout()
    
    return fig
# src/ga_optimizer/visualization/distribution.py

import matplotlib.pyplot as plt
import seaborn as sns
from typing import Any

def plot_fitness_distribution(history: list[dict[str, Any]], problem_name: str) -> plt.Figure:
    num_epochs = len(history)
    step = max(1, num_epochs // 10)
    selected_epochs = history[::step]
    if history[-1] not in selected_epochs:
        selected_epochs.append(history[-1])

    data_for_boxplot = []
    labels = []
    for h in selected_epochs:
        data_for_boxplot.append(h["fitness_values"])
        labels.append(f"Ep. {h['epoch_index']}")

    fig, ax = plt.subplots(figsize=(10, 6))
    
    sns.boxplot(data=data_for_boxplot, palette="Set3", ax=ax)
    
    ax.set_xticks(range(len(labels)))
    ax.set_xticklabels(labels, rotation=45)
    ax.set_title(f"Rozkład Fitnessu - {problem_name}", fontsize=14)
    ax.set_ylabel("Fitness", fontsize=12)
    fig.tight_layout()
    
    return fig
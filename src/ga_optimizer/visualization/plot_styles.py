# src/ga_optimizer/visualization/plot_styles.py

import matplotlib.pyplot as plt
import seaborn as sns

def apply_custom_style() -> None:
    """Ustawia globalny, spójny styl dla wszystkich wykresów w aplikacji."""
    
    # Bazowy motyw z Seaborn (whitegrid jest świetny do danych naukowych)
    sns.set_theme(
        style="whitegrid", 
        palette="deep",     # Ładne, stonowane kolory
        font_scale=1.1      # Lekko powiększona czcionka bazowa
    )
    
    # Dopieszczamy detale w samym Matplotlib
    plt.rcParams.update({
        "figure.figsize": (10, 6),       # Domyślny rozmiar okna
        "axes.titlesize": 15,            # Rozmiar tytułu wykresu
        "axes.titleweight": "bold",      # Pogrubiony tytuł
        "axes.labelsize": 12,            # Rozmiar etykiet osi (X, Y)
        "lines.linewidth": 2.5,          # Domyślna grubość linii
        "legend.fontsize": 11,           # Rozmiar tekstu w legendzie
        "figure.autolayout": True,       # Zastępuje plt.tight_layout() (automatyczne marginesy)
        "lines.markersize": 8            # Wielkość punktów na wykresach
    })
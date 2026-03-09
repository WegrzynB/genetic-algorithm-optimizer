# app.py
# Składa aplikację GUI, inicjalizuje okno główne i uruchamia pętlę Tkintera

import tkinter as tk
from tkinter import ttk

import sv_ttk

from ga_optimizer.gui.views.main_window import MainWindow


def run_app() -> None:
    # Tworzy główne okno aplikacji (root) dla Tkintera
    root = tk.Tk()

    # Ustawia motyw dla widgetów ttk (można przełączyć na jasny)
    sv_ttk.set_theme("dark")
    # sv_ttk.set_theme("light")

    # Konfiguracja podstawowych stylów (np. nagłówki i etykiety ramek)
    style = ttk.Style(root)
    style.configure("TLabelframe.Label", font=("Segoe UI", 10, "bold"))
    style.configure("Header.TLabel", font=("Segoe UI", 14, "bold"))

    # Buduje i wyświetla główne okno aplikacji
    app = MainWindow(root)
    app.build()

    # Startuje główną pętlę zdarzeń GUI
    root.mainloop()
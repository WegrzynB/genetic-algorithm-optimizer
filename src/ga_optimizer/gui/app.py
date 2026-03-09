# app.py
# Start aplikacji GUI.

import tkinter as tk
from tkinter import ttk

import sv_ttk

from ga_optimizer.gui.views.main_window import MainWindow


def run_app() -> None:
    # Tworzy główne okno aplikacji Tkinter.
    root = tk.Tk()

    # Ustawia motyw widgetów ttk.
    sv_ttk.set_theme("dark")
    # sv_ttk.set_theme("light")

    # Konfiguruje podstawowe style używane w GUI.
    style = ttk.Style(root)
    style.configure("TLabelframe.Label", font=("Segoe UI", 10, "bold"))
    style.configure("Header.TLabel", font=("Segoe UI", 14, "bold"))

    # Styl dla pól oznaczonych jako błędne po walidacji.
    style.configure("Invalid.TEntry", fieldbackground="#5A1E1E")

    # Buduje główne okno aplikacji i wszystkie panele.
    app = MainWindow(root)
    app.build()

    # Uruchamia pętlę zdarzeń GUI.
    root.mainloop()
# Składa aplikację GUI, inicjalizuje okno główne i uruchamia pętlę Tkintera

import tkinter as tk
from gui.views.main_window import MainWindow


def run_app() -> None:
    root = tk.Tk()
    app = MainWindow(root)
    app.build()
    root.mainloop()
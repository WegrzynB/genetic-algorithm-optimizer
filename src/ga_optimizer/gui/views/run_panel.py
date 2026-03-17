# run_panel.py
# Definiuje panel sterowania uruchomieniem oraz podglądu statusu/czasu.

import tkinter as tk
from tkinter import ttk


class RunPanel:
    def __init__(self, parent, on_start):
        # Przechowuje callback do uruchomienia algorytmu.
        self.parent = parent
        self.on_start = on_start

        # Elementy UI oraz zmienne stanu.
        self.frame = None
        self.progress = None
        self.status_var = tk.StringVar(value="Gotowy do uruchomienia.")

    def build(self) -> None:
        # Buduje panel sterowania: Start, pasek postępu i status.
        self.frame = ttk.LabelFrame(self.parent, text="Uruchamianie", padding=10)
        self.frame.columnconfigure(2, weight=1)

        ttk.Button(self.frame, text="Start algorytmu", command=self._start).grid(
            row=0,
            column=0,
            padx=(0, 12),
            sticky="w",
        )
        ttk.Label(self.frame, text="Postęp:").grid(row=0, column=1, sticky="e", padx=(0, 8))

        self.progress = ttk.Progressbar(self.frame, maximum=100)
        self.progress.grid(row=0, column=2, sticky="ew")

        ttk.Label(self.frame, textvariable=self.status_var).grid(
            row=1,
            column=0,
            columnspan=3,
            sticky="w",
            pady=(8, 0),
        )

    def set_status(self, text: str) -> None:
        self.status_var.set(text)

    def set_progress(self, value: int) -> None:
        if self.progress is not None:
            self.progress["value"] = max(0, min(100, int(value)))

    def _start(self) -> None:
        if callable(self.on_start):
            self.on_start()
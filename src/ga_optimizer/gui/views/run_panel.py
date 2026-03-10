# run_panel.py
# Definiuje panel sterowania uruchomieniem oraz podglądu statusu/czasu

import tkinter as tk
from tkinter import ttk


class RunPanel:
    def __init__(self, parent, on_start, on_save):
        # Przechowuje callbacki do uruchomienia algorytmu i zapisu wyników
        self.parent = parent
        self.on_start = on_start
        self.on_save = on_save

        # Elementy UI oraz zmienne stanu
        self.frame = None
        self.progress = None
        self.status_var = tk.StringVar(value="Gotowy")
        self.save_btn = None

    def build(self) -> None:
        # Buduje panel sterowania: Start, pasek postępu, zapis oraz status
        self.frame = ttk.LabelFrame(self.parent, text="Sterowanie", padding=10)
        self.frame.columnconfigure(2, weight=1)

        ttk.Button(self.frame, text="Start algorytmu", command=self._start).grid(row=0, column=0, padx=(0, 12))
        ttk.Label(self.frame, text="Postęp:").grid(row=0, column=1, sticky="e", padx=(0, 8))

        self.progress = ttk.Progressbar(self.frame, maximum=100)
        self.progress.grid(row=0, column=2, sticky="ew", padx=(0, 12))

        # Przycisk zapisu jest domyślnie wyłączony (włącza się po uruchomieniu algorytmu)
        self.save_btn = ttk.Button(self.frame, text="Zapisz (plik / baza)", command=self._save, state=tk.DISABLED)
        self.save_btn.grid(row=0, column=3, sticky="e")

        ttk.Label(self.frame, textvariable=self.status_var).grid(
            row=1, column=0, columnspan=4, sticky="w", pady=(8, 0)
        )

    def set_status(self, text: str) -> None:
        # Ustawia tekst statusu w panelu sterowania
        self.status_var.set(text)

    def set_progress(self, value: int) -> None:
        # Aktualizuje wartość paska postępu (0..100)
        if self.progress is not None:
            self.progress["value"] = max(0, min(100, int(value)))

    def enable_save(self, enabled: bool) -> None:
        # Włącza lub wyłącza przycisk zapisu
        if self.save_btn is None:
            return
        self.save_btn.configure(state=tk.NORMAL if enabled else tk.DISABLED)

    def _start(self) -> None:
        # Obsługa kliknięcia Start
        self.set_progress(0)
        self.set_status("Uruchamianie ...")
        if callable(self.on_start):
            self.on_start()

    def _save(self) -> None:
        # Obsługa kliknięcia Zapisz (na razie wywołuje callback)
        if callable(self.on_save):
            self.on_save()
# Definiuje główne okno aplikacji i układ nadrzędny interfejsu

import tkinter as tk
from tkinter import ttk


class MainWindow:
    def __init__(self, root: tk.Tk):
        self.root = root

        self.main_frame = None
        self.header_frame = None
        self.content_frame = None
        self.left_panel = None
        self.right_panel = None
        self.status_bar = None

        self.run_button = None
        self.stop_button = None
        self.save_button = None

        self.problem_var = tk.StringVar(value="sphere")
        self.mode_var = tk.StringVar(value="min")
        self.population_var = tk.StringVar(value="100")
        self.epochs_var = tk.StringVar(value="200")
        self.status_var = tk.StringVar(value="Gotowy")

    def build(self) -> None:
        self._configure_root()
        self._build_layout()
        self._build_header()
        self._build_left_panel()
        self._build_right_panel()
        self._build_status_bar()

    def _configure_root(self) -> None:
        self.root.title("GA Optimizer")
        self.root.geometry("1100x700")
        self.root.minsize(900, 600)

    def _build_layout(self) -> None:
        self.main_frame = ttk.Frame(self.root, padding=12)
        self.main_frame.pack(fill="both", expand=True)

        self.header_frame = ttk.Frame(self.main_frame)
        self.header_frame.pack(fill="x", pady=(0, 10))

        self.content_frame = ttk.Frame(self.main_frame)
        self.content_frame.pack(fill="both", expand=True)

        self.left_panel = ttk.LabelFrame(self.content_frame, text="Konfiguracja", padding=10)
        self.left_panel.pack(side="left", fill="y", padx=(0, 10))

        self.right_panel = ttk.LabelFrame(self.content_frame, text="Wyniki / Podgląd", padding=10)
        self.right_panel.pack(side="left", fill="both", expand=True)

    def _build_header(self) -> None:
        title = ttk.Label(
            self.header_frame,
            text="Optymalizacja funkcji metodą algorytmu genetycznego",
            font=("Segoe UI", 14, "bold"),
        )
        title.pack(side="left")

        buttons_frame = ttk.Frame(self.header_frame)
        buttons_frame.pack(side="right")

        self.run_button = ttk.Button(buttons_frame, text="Start", command=self._on_run)
        self.run_button.pack(side="left", padx=(0, 6))

        self.stop_button = ttk.Button(buttons_frame, text="Stop", command=self._on_stop)
        self.stop_button.pack(side="left", padx=(0, 6))

        self.save_button = ttk.Button(buttons_frame, text="Zapisz wynik", command=self._on_save)
        self.save_button.pack(side="left")

    def _build_left_panel(self) -> None:
        row = 0

        ttk.Label(self.left_panel, text="Funkcja testowa:").grid(row=row, column=0, sticky="w", pady=4)
        ttk.Combobox(
            self.left_panel,
            textvariable=self.problem_var,
            values=["sphere", "rastrigin", "rosenbrock"],
            state="readonly",
            width=18,
        ).grid(row=row, column=1, sticky="ew", pady=4)
        row += 1

        ttk.Label(self.left_panel, text="Tryb optymalizacji:").grid(row=row, column=0, sticky="w", pady=4)
        ttk.Combobox(
            self.left_panel,
            textvariable=self.mode_var,
            values=["min", "max"],
            state="readonly",
            width=18,
        ).grid(row=row, column=1, sticky="ew", pady=4)
        row += 1

        ttk.Label(self.left_panel, text="Liczebność populacji:").grid(row=row, column=0, sticky="w", pady=4)
        ttk.Entry(self.left_panel, textvariable=self.population_var, width=20).grid(
            row=row, column=1, sticky="ew", pady=4
        )
        row += 1

        ttk.Label(self.left_panel, text="Liczba epok:").grid(row=row, column=0, sticky="w", pady=4)
        ttk.Entry(self.left_panel, textvariable=self.epochs_var, width=20).grid(
            row=row, column=1, sticky="ew", pady=4
        )
        row += 1

        ttk.Separator(self.left_panel, orient="horizontal").grid(
            row=row, column=0, columnspan=2, sticky="ew", pady=(10, 10)
        )
        row += 1

        ttk.Label(self.left_panel, text="Parametry operatorów (placeholder)").grid(
            row=row, column=0, columnspan=2, sticky="w", pady=4
        )
        row += 1

        ttk.Checkbutton(self.left_panel, text="Elitaryzm").grid(
            row=row, column=0, columnspan=2, sticky="w", pady=2
        )
        row += 1

        ttk.Checkbutton(self.left_panel, text="Inwersja").grid(
            row=row, column=0, columnspan=2, sticky="w", pady=2
        )
        row += 1

        self.left_panel.columnconfigure(0, weight=0)
        self.left_panel.columnconfigure(1, weight=1)

    def _build_right_panel(self) -> None:
        top_stats = ttk.LabelFrame(self.right_panel, text="Podsumowanie", padding=10)
        top_stats.pack(fill="x", pady=(0, 10))

        ttk.Label(top_stats, text="Najlepszy fitness:").grid(row=0, column=0, sticky="w", padx=(0, 8), pady=3)
        ttk.Label(top_stats, text="-").grid(row=0, column=1, sticky="w", pady=3)

        ttk.Label(top_stats, text="Średni fitness:").grid(row=1, column=0, sticky="w", padx=(0, 8), pady=3)
        ttk.Label(top_stats, text="-").grid(row=1, column=1, sticky="w", pady=3)

        ttk.Label(top_stats, text="Czas wykonania:").grid(row=2, column=0, sticky="w", padx=(0, 8), pady=3)
        ttk.Label(top_stats, text="-").grid(row=2, column=1, sticky="w", pady=3)

        output_frame = ttk.LabelFrame(self.right_panel, text="Log / Wyniki tekstowe", padding=10)
        output_frame.pack(fill="both", expand=True)

        self.output_text = tk.Text(output_frame, height=20, wrap="word")
        self.output_text.pack(side="left", fill="both", expand=True)

        scrollbar = ttk.Scrollbar(output_frame, orient="vertical", command=self.output_text.yview)
        scrollbar.pack(side="right", fill="y")
        self.output_text.configure(yscrollcommand=scrollbar.set)

        self.output_text.insert("end", "Aplikacja uruchomiona.\n")
        self.output_text.insert("end", "To jest okrojony widok startowy GUI.\n")
        self.output_text.configure(state="disabled")

    def _build_status_bar(self) -> None:
        self.status_bar = ttk.Frame(self.root, padding=(8, 4))
        self.status_bar.pack(fill="x", side="bottom")

        ttk.Separator(self.root, orient="horizontal").pack(fill="x", side="bottom")

        ttk.Label(self.status_bar, textvariable=self.status_var, anchor="w").pack(side="left")

    def _append_log(self, message: str) -> None:
        self.output_text.configure(state="normal")
        self.output_text.insert("end", message + "\n")
        self.output_text.see("end")
        self.output_text.configure(state="disabled")

    def _on_run(self) -> None:
        self.status_var.set("Uruchamianie...")
        self._append_log(
            f"Start | problem={self.problem_var.get()}, tryb={self.mode_var.get()}, "
            f"populacja={self.population_var.get()}, epoki={self.epochs_var.get()}"
        )
        self.status_var.set("Gotowy (symulacja startu)")

    def _on_stop(self) -> None:
        self.status_var.set("Zatrzymano")
        self._append_log("Zatrzymano obliczenia (placeholder).")

    def _on_save(self) -> None:
        self.status_var.set("Zapisano (placeholder)")
        self._append_log("Zapis wyników (placeholder).")
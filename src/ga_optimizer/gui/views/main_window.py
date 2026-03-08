# Definiuje główne okno aplikacji i układ nadrzędny interfejsu

import tkinter as tk
from tkinter import ttk


class MainWindow:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.status_var = tk.StringVar(value="Gotowy")

        self.main_frame = None
        self.header_frame = None
        self.body_frame = None
        self.output_text = None

    def build(self) -> None:
        self._configure_root()
        self._build_layout()
        self._build_header()
        self._build_body()

    def _configure_root(self) -> None:
        self.root.title("GA Optimizer")
        self.root.geometry("1000x650")
        self.root.minsize(800, 550)

    def _build_layout(self) -> None:
        self.main_frame = ttk.Frame(self.root, padding=12)
        self.main_frame.pack(fill="both", expand=True)

        self.header_frame = ttk.Frame(self.main_frame)
        self.header_frame.pack(fill="x", pady=(0, 10))

        self.body_frame = ttk.Frame(self.main_frame)
        self.body_frame.pack(fill="both", expand=True)

    def _build_header(self) -> None:
        title = ttk.Label(
            self.header_frame,
            text="Optymalizacja funkcji metodą algorytmu genetycznego",
            font=("Segoe UI", 14, "bold"),
        )
        title.pack(side="left")

        status = ttk.Label(self.header_frame, textvariable=self.status_var, anchor="e")
        status.pack(side="right")

    def _build_body(self) -> None:
        output_frame = ttk.LabelFrame(self.body_frame, text="Log", padding=10)
        output_frame.pack(fill="both", expand=True)

        self.output_text = tk.Text(output_frame, wrap="word", height=10)
        self.output_text.pack(side="left", fill="both", expand=True)

        scrollbar = ttk.Scrollbar(output_frame, orient="vertical", command=self.output_text.yview)
        scrollbar.pack(side="right", fill="y")
        self.output_text.configure(yscrollcommand=scrollbar.set)

        self._append_log("Aplikacja uruchomiona.")
        self._append_log("To jest minimalny szkielet GUI (placeholder).")

    def _append_log(self, message: str) -> None:
        if self.output_text is None:
            return
        self.output_text.insert("end", message + "\n")
        self.output_text.see("end")
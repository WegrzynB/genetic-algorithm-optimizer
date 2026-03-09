# results_panel.py
# Definiuje panel prezentacji wyników liczbowych i podsumowania runa

from tkinter import ttk


class ResultsPanel:
    def __init__(self, parent):
        # Przechowuje kontener nadrzędny oraz referencje do elementów UI
        self.parent = parent
        self.frame = None
        self.term_label = None
        self.summary_label = None
        self.tree = None

    def build(self) -> None:
        # Buduje panel wyników: powód zakończenia, podsumowanie oraz tabela najlepszych osobników
        self.frame = ttk.LabelFrame(self.parent, text="Wyniki końcowe i najlepsi osobnicy", padding=10)
        self.frame.columnconfigure(0, weight=1)

        top = ttk.Frame(self.frame)
        top.grid(row=0, column=0, sticky="ew", pady=(0, 10))
        top.columnconfigure(0, weight=1)

        # Tekst informujący, dlaczego algorytm zakończył działanie (placeholder)
        self.term_label = ttk.Label(top, text="Zakończenie: -")
        self.term_label.grid(row=0, column=0, sticky="w")

        # Podsumowanie wartości (best/avg/worst/czas) po zakończeniu runa (placeholder)
        self.summary_label = ttk.Label(top, text="Best: - | Avg: - | Worst: - | Czas: -")
        self.summary_label.grid(row=1, column=0, sticky="w", pady=(4, 0))

        table_frame = ttk.LabelFrame(self.frame, text="Najlepsi osobnicy w epoce (placeholder)", padding=8)
        table_frame.grid(row=1, column=0, sticky="ew")
        table_frame.columnconfigure(0, weight=1)

        columns = ("epoch", "rank", "fitness", "objective", "x_preview")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=8)

        self.tree.heading("epoch", text="Epoka")
        self.tree.heading("rank", text="Rank")
        self.tree.heading("fitness", text="Fitness")
        self.tree.heading("objective", text="Wartość f(x)")
        self.tree.heading("x_preview", text="X (podgląd)")

        self.tree.column("epoch", width=80, anchor="center")
        self.tree.column("rank", width=70, anchor="center")
        self.tree.column("fitness", width=140, anchor="e")
        self.tree.column("objective", width=140, anchor="e")
        self.tree.column("x_preview", width=820, anchor="w")

        self.tree.grid(row=0, column=0, sticky="ew")
        sb = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        sb.grid(row=0, column=1, sticky="ns")
        self.tree.configure(yscrollcommand=sb.set)

        # Placeholder najlepszych osobników (docelowo aktualizowane po runie lub w trakcie)
        for i in range(1, 6):
            self.tree.insert("", "end", values=(0, i, "-", "-", "-"))

    def set_termination_reason(self, text: str) -> None:
        # Ustawia powód zakończenia algorytmu w UI
        self.term_label.configure(text=text)

    def set_summary(self, best: str, avg: str, worst: str, elapsed: str) -> None:
        # Ustawia podsumowanie wyników końcowych w UI
        self.summary_label.configure(text=f"Best: {best} | Avg: {avg} | Worst: {worst} | Czas: {elapsed}")
# results_panel.py
# Definiuje panel wyników: sekcja podsumowania, zapis oraz notebook z danymi.

from __future__ import annotations

import tkinter as tk
from tkinter import ttk
from ga_optimizer.gui.views.plots_panel import PlotsPanel


def _fmt_value(value, digits: int = 7) -> str:
    if value in (None, ""):
        return "-"
    try:
        return f"{float(value):.{digits}f}"
    except (TypeError, ValueError):
        return str(value)


def _fmt_time(value) -> str:
    if value in (None, ""):
        return "-"
    try:
        return f"{float(value):.2f} s"
    except (TypeError, ValueError):
        return str(value)


class ResultsPanel:
    def __init__(self, parent, on_save):
        # Przechowuje kontener nadrzędny oraz callback zapisu wyników.
        self.parent = parent
        self.on_save = on_save

        # Referencje do głównych elementów UI.
        self.frame = None
        self.summary_frame = None
        self.nb = None

        # Etykiety sekcji górnej.
        self.summary_label = None
        self.extrema_label = None
        self.save_btn = None

        # Zakładki notebooka.
        self.results_tab = None
        self.run_history_tab = None
        self.full_history_tab = None
        self.plots_tab = None

        # Widgety zakładek.
        self.results_text = None
        self.run_history_table = None
        self.full_history_table = None

        # Panel na wykresy
        self.plots_panel = None

    def build(self) -> None:
        # Buduje panel wyników: górne podsumowanie + notebook.
        self.frame = ttk.LabelFrame(self.parent, text="Wyniki", padding=10)
        self.frame.columnconfigure(0, weight=1)
        self.frame.rowconfigure(1, weight=1)

        self.summary_frame = ttk.Frame(self.frame)
        self.summary_frame.grid(row=0, column=0, sticky="ew", pady=(0, 10))
        self.summary_frame.columnconfigure(0, weight=1)
        self.summary_frame.columnconfigure(1, weight=0)

        info = ttk.Frame(self.summary_frame)
        info.grid(row=0, column=0, sticky="ew")
        info.columnconfigure(0, weight=1)

        self.summary_label = ttk.Label(
            info,
            text="FITNESS -- Min: -  |  25%: -  |  Mediana: -  |  75%: -  |  Max: -  |  Czas: -",
        )
        self.summary_label.grid(row=0, column=0, sticky="w")

        self.extrema_label = ttk.Label(info, text="Minimum globalne: -")
        self.extrema_label.grid(row=1, column=0, sticky="w", pady=(4, 0))

        self.save_btn = ttk.Button(
            self.summary_frame,
            text="Zapisz (plik / baza)",
            command=self._save,
            state=tk.DISABLED,
        )
        self.save_btn.grid(row=0, column=1, rowspan=2, sticky="ne", padx=(12, 0))

        self.nb = ttk.Notebook(self.frame)
        self.nb.grid(row=1, column=0, sticky="nsew")

        self.results_tab = ttk.Frame(self.nb, padding=10)
        self.run_history_tab = ttk.Frame(self.nb, padding=10)
        self.full_history_tab = ttk.Frame(self.nb, padding=10)
        self.plots_tab = ttk.Frame(self.nb, padding=10)

        self.nb.add(self.results_tab, text="Wyniki")
        self.nb.add(self.run_history_tab, text="Historia uruchomień")
        self.nb.add(self.full_history_tab, text="Pełna historia")
        self.nb.add(self.plots_tab, text="Wykresy")

        self._build_results_tab()
        self._build_run_history_tab()
        self._build_full_history_tab()
        self._build_plots_tab()

        self.configure_history_tabs(run_count=1)

    def _build_results_tab(self) -> None:
        # Zakładka z tekstowym opisem najważniejszych informacji.
        self.results_tab.columnconfigure(0, weight=1)
        self.results_tab.rowconfigure(0, weight=1)

        self.results_text = tk.Text(self.results_tab, wrap="word", height=20)
        self.results_text.grid(row=0, column=0, sticky="nsew")

        sb = ttk.Scrollbar(self.results_tab, orient="vertical", command=self.results_text.yview)
        sb.grid(row=0, column=1, sticky="ns")
        self.results_text.configure(yscrollcommand=sb.set)

        self.results_text.insert("1.0", "Tutaj pojawi się opis wyników po uruchomieniu algorytmu.")
        self.results_text.configure(state="disabled")

    def _build_run_history_tab(self) -> None:
        # Zakładka historii uruchomień - tylko końcowe statystyki każdego runa.
        self.run_history_tab.columnconfigure(0, weight=1)
        self.run_history_tab.rowconfigure(0, weight=1)

        columns = ("run", "seed", "min", "q1", "median", "q3", "max", "avg", "elapsed")
        self.run_history_table = ttk.Treeview(self.run_history_tab, columns=columns, show="headings", height=12)

        self.run_history_table.heading("run", text="Uruchomienie")
        self.run_history_table.heading("seed", text="Seed")
        self.run_history_table.heading("min", text="Min")
        self.run_history_table.heading("q1", text="25%")
        self.run_history_table.heading("median", text="Mediana")
        self.run_history_table.heading("q3", text="75%")
        self.run_history_table.heading("max", text="Max")
        self.run_history_table.heading("avg", text="Średnia")
        self.run_history_table.heading("elapsed", text="Czas [s]")

        self.run_history_table.column("run", width=110, anchor="center")
        self.run_history_table.column("seed", width=110, anchor="center")
        self.run_history_table.column("min", width=110, anchor="e")
        self.run_history_table.column("q1", width=110, anchor="e")
        self.run_history_table.column("median", width=110, anchor="e")
        self.run_history_table.column("q3", width=110, anchor="e")
        self.run_history_table.column("max", width=110, anchor="e")
        self.run_history_table.column("avg", width=110, anchor="e")
        self.run_history_table.column("elapsed", width=100, anchor="e")

        self.run_history_table.grid(row=0, column=0, sticky="nsew")
        sb = ttk.Scrollbar(self.run_history_tab, orient="vertical", command=self.run_history_table.yview)
        sb.grid(row=0, column=1, sticky="ns")
        self.run_history_table.configure(yscrollcommand=sb.set)

    def _build_full_history_tab(self) -> None:
        # Zakładka pełnej historii: run + epoka + kwartyle.
        self.full_history_tab.columnconfigure(0, weight=1)
        self.full_history_tab.rowconfigure(0, weight=1)

        columns = ("run", "epoch", "min", "q1", "median", "q3", "max", "avg")
        self.full_history_table = ttk.Treeview(self.full_history_tab, columns=columns, show="headings", height=12)

        self.full_history_table.heading("run", text="Uruchomienie")
        self.full_history_table.heading("epoch", text="Epoka")
        self.full_history_table.heading("min", text="Min")
        self.full_history_table.heading("q1", text="25%")
        self.full_history_table.heading("median", text="Mediana")
        self.full_history_table.heading("q3", text="75%")
        self.full_history_table.heading("max", text="Max")
        self.full_history_table.heading("avg", text="Średnia")

        self.full_history_table.column("run", width=110, anchor="center")
        self.full_history_table.column("epoch", width=90, anchor="center")
        self.full_history_table.column("min", width=110, anchor="e")
        self.full_history_table.column("q1", width=110, anchor="e")
        self.full_history_table.column("median", width=110, anchor="e")
        self.full_history_table.column("q3", width=110, anchor="e")
        self.full_history_table.column("max", width=110, anchor="e")
        self.full_history_table.column("avg", width=110, anchor="e")

        self.full_history_table.grid(row=0, column=0, sticky="nsew")
        sb = ttk.Scrollbar(self.full_history_tab, orient="vertical", command=self.full_history_table.yview)
        sb.grid(row=0, column=1, sticky="ns")
        self.full_history_table.configure(yscrollcommand=sb.set)

    def _build_plots_tab(self) -> None:
        self.plots_tab.columnconfigure(0, weight=1)
        self.plots_tab.rowconfigure(0, weight=1)

        self.plots_panel = PlotsPanel(self.plots_tab)
        self.plots_panel.build()

    def set_plots(self, engine_result: dict, input_dict: dict) -> None:
        if self.plots_panel is not None:
            self.plots_panel.set_plots(engine_result=engine_result, input_dict=input_dict)

    def select_results_tab(self) -> None:
        if self.nb is not None and self.results_tab is not None:
            self.nb.select(self.results_tab)

    def configure_history_tabs(self, run_count: int) -> None:
        # Przy jednym uruchomieniu pokazujemy tylko pełną historię.
        current_tabs = self.nb.tabs()
        run_tab_id = str(self.run_history_tab)
        full_tab_id = str(self.full_history_tab)

        if run_count <= 1:
            if run_tab_id in current_tabs:
                self.nb.hide(self.run_history_tab)
            if full_tab_id in current_tabs:
                self.nb.tab(self.full_history_tab, text="Pełna historia")
        else:
            if run_tab_id not in current_tabs:
                self.nb.add(self.run_history_tab, text="Historia uruchomień")
            else:
                self.nb.tab(self.run_history_tab, state="normal")

    def set_summary(
        self,
        min_value,
        q1,
        median,
        q3,
        max_value,
        elapsed,
    ) -> None:
        self.summary_label.configure(
            text=(
                f"FITNESS -- Min: {_fmt_value(min_value)}  |  25%: {_fmt_value(q1)}  |  "
                f"Mediana: {_fmt_value(median)}  |  75%: {_fmt_value(q3)}  |  "
                f"Max: {_fmt_value(max_value)}  |  Czas: {_fmt_time(elapsed)}"
            )
        )

    def set_global_minimum_info(self, text: str) -> None:
        self.extrema_label.configure(text=text)

    def set_results_text(self, text: str) -> None:
        self.results_text.configure(state="normal")
        self.results_text.delete("1.0", "end")
        self.results_text.insert("1.0", text)
        self.results_text.configure(state="disabled")

    def set_run_history(self, runs: list[dict]) -> None:
        for item in self.run_history_table.get_children():
            self.run_history_table.delete(item)

        for index, run in enumerate(runs, start=1):
            summary = run.get("summary", {})
            self.run_history_table.insert(
                "",
                "end",
                values=(
                    index,
                    run.get("seed", "-"),
                    _fmt_value(summary.get("min_fitness")),
                    _fmt_value(summary.get("q1_fitness")),
                    _fmt_value(summary.get("median_fitness")),
                    _fmt_value(summary.get("q3_fitness")),
                    _fmt_value(summary.get("max_fitness")),
                    _fmt_value(summary.get("avg_fitness")),
                    _fmt_value(run.get("elapsed"), digits=2),
                ),
            )

    def set_full_history(self, runs: list[dict]) -> None:
        for item in self.full_history_table.get_children():
            self.full_history_table.delete(item)

        for run_index, run in enumerate(runs, start=1):
            for epoch_row in run.get("history", []):
                summary = epoch_row.get("summary", {})
                self.full_history_table.insert(
                    "",
                    "end",
                    values=(
                        run_index,
                        epoch_row.get("epoch_index", "-"),
                        _fmt_value(summary.get("min_fitness")),
                        _fmt_value(summary.get("q1_fitness")),
                        _fmt_value(summary.get("median_fitness")),
                        _fmt_value(summary.get("q3_fitness")),
                        _fmt_value(summary.get("max_fitness")),
                        _fmt_value(summary.get("avg_fitness")),
                    ),
                )

    def enable_save(self, enabled: bool) -> None:
        if self.save_btn is None:
            return
        self.save_btn.configure(state=tk.NORMAL if enabled else tk.DISABLED)

    def _save(self) -> None:
        if callable(self.on_save):
            self.on_save()

    def reset(self) -> None:
        # Czyści panel wyników przed nowym uruchomieniem.
        if self.plots_panel is not None:
            self.plots_panel.reset()
            
        self.set_summary("-", "-", "-", "-", "-", "-")
        self.set_global_minimum_info("Minimum globalne: -")
        self.set_results_text("Tutaj pojawi się opis wyników po uruchomieniu algorytmu.")
        self.enable_save(False)

        if self.run_history_table is not None:
            for item in self.run_history_table.get_children():
                self.run_history_table.delete(item)

        if self.full_history_table is not None:
            for item in self.full_history_table.get_children():
                self.full_history_table.delete(item)

        self.configure_history_tabs(run_count=1)

        if self.plots_panel is not None:
            self.plots_panel.reset()
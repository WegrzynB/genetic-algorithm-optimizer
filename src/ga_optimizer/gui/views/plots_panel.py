# plots_panel.py
# Definiuje panel wyświetlania wykresów i wizualizacji wyników

from tkinter import ttk


class PlotsPanel:
    def __init__(self, parent):
        # Przechowuje kontener nadrzędny oraz referencje do elementów UI
        self.parent = parent
        self.frame = None
        self.nb = None
        self.plot_tab = None
        self.history_tab = None
        self.history_table = None

    def build(self) -> None:
        # Buduje panel z notebookiem: zakładka wykresu oraz historia (tabela)
        self.frame = ttk.LabelFrame(self.parent, text="Wykres / historia", padding=10)
        self.frame.columnconfigure(0, weight=1)
        self.frame.rowconfigure(0, weight=1)

        self.nb = ttk.Notebook(self.frame)
        self.nb.grid(row=0, column=0, sticky="nsew")

        self.plot_tab = ttk.Frame(self.nb, padding=10)
        self.history_tab = ttk.Frame(self.nb, padding=10)

        self.nb.add(self.plot_tab, text="Wykres")
        self.nb.add(self.history_tab, text="Historia")

        self._build_plot_tab()
        self._build_history_tab()

    def _build_plot_tab(self) -> None:
        # Zakładka wykresu (placeholder; docelowo osadzony Matplotlib)
        self.plot_tab.columnconfigure(0, weight=1)
        self.plot_tab.rowconfigure(0, weight=1)
        ttk.Label(
            self.plot_tab,
            text="Placeholder wykresu (docelowo Matplotlib)."
        ).grid(row=0, column=0, sticky="nsew")

    def _build_history_tab(self) -> None:
        # Zakładka historii: tabela epoka/best/avg/worst
        self.history_tab.columnconfigure(0, weight=1)
        self.history_tab.rowconfigure(0, weight=1)

        columns = ("epoch", "best", "avg", "worst")
        self.history_table = ttk.Treeview(self.history_tab, columns=columns, show="headings", height=12)

        self.history_table.heading("epoch", text="Epoka")
        self.history_table.heading("best", text="Best")
        self.history_table.heading("avg", text="Avg")
        self.history_table.heading("worst", text="Worst")

        self.history_table.column("epoch", width=90, anchor="center")
        self.history_table.column("best", width=180, anchor="e")
        self.history_table.column("avg", width=180, anchor="e")
        self.history_table.column("worst", width=180, anchor="e")

        self.history_table.grid(row=0, column=0, sticky="nsew")
        sb = ttk.Scrollbar(self.history_tab, orient="vertical", command=self.history_table.yview)
        sb.grid(row=0, column=1, sticky="ns")
        self.history_table.configure(yscrollcommand=sb.set)

        # Placeholder danych historii (docelowo uzupełniane po uruchomieniu algorytmu)
        for e in range(1, 8):
            self.history_table.insert("", "end", values=(e, "-", "-", "-"))
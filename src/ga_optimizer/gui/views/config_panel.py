# config_panel.py
# Definiuje panel ustawień parametrów algorytmu i problemu

import tkinter as tk
from tkinter import ttk

from ga_optimizer.gui.state.view_model import (
    FIELDS_GENERAL,
    FIELDS_GA_MAIN,
    FIELDS_OPERATORS,
    FIELDS_PRECISION,
    METHOD_PARAM_SPECS,
    ViewModel,
)


class ScrollableTab(ttk.Frame):
    def __init__(self, parent, padding=10):
        # Tworzy przewijalną zakładkę (Canvas + Frame) dla długich list parametrów
        super().__init__(parent)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        self.canvas = tk.Canvas(self, highlightthickness=0)
        self.canvas.grid(row=0, column=0, sticky="nsew")

        self.vsb = ttk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.vsb.grid(row=0, column=1, sticky="ns")

        self.canvas.configure(yscrollcommand=self.vsb.set)

        self.inner = ttk.Frame(self.canvas, padding=padding)
        self.inner.columnconfigure(1, weight=1)

        self._window_id = self.canvas.create_window((0, 0), window=self.inner, anchor="nw")

        self.inner.bind("<Configure>", self._on_frame_configure)
        self.canvas.bind("<Configure>", self._on_canvas_configure)

        # Umożliwia scrollowanie myszką tylko wtedy, gdy kursor jest nad daną zakładką
        self._bind_mousewheel()

    def _on_frame_configure(self, event=None):
        # Aktualizuje obszar przewijania po zmianie rozmiaru zawartości
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def _on_canvas_configure(self, event):
        # Dopasowuje szerokość wewnętrznej ramki do szerokości canvasa
        self.canvas.itemconfigure(self._window_id, width=event.width)

    def _bind_mousewheel(self) -> None:
        # Podpina/odpina obsługę kółka myszy dla tej zakładki (żeby scroll działał per-tab)
        def _on_enter(_event):
            self.canvas.bind_all("<MouseWheel>", self._on_mousewheel, add=True)
            self.canvas.bind_all("<Shift-MouseWheel>", self._on_shift_mousewheel, add=True)

        def _on_leave(_event):
            self.canvas.unbind_all("<MouseWheel>")
            self.canvas.unbind_all("<Shift-MouseWheel>")

        self.canvas.bind("<Enter>", _on_enter)
        self.canvas.bind("<Leave>", _on_leave)
        self.inner.bind("<Enter>", _on_enter)
        self.inner.bind("<Leave>", _on_leave)

    def _on_mousewheel(self, event):
        # Przewijanie pionowe kółkiem myszy (Windows)
        try:
            self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
        except Exception:
            pass

    def _on_shift_mousewheel(self, event):
        # Przewijanie poziome przy Shift (opcjonalnie, jeśli kiedyś będzie potrzebne)
        try:
            self.canvas.xview_scroll(int(-1 * (event.delta / 120)), "units")
        except Exception:
            pass


class ConfigPanel:
    def __init__(self, parent, vm: ViewModel):
        # Przechowuje rodzica (kontener) oraz wspólny model stanu GUI
        self.parent = parent
        self.vm = vm

        # Kontener panelu oraz notebook zakładek
        self.frame = None
        self.nb = None

        # Zakładki dla parametrów metod (selekcja/krzyżowanie/mutacja)
        self.selection_tab = None
        self.crossover_tab = None
        self.mutation_tab = None

        # Referencje do dynamicznie tworzonych ramek parametrów metod
        self._dynamic_frames = {"selection": None, "crossover": None, "mutation": None}
        self._dynamic_field_keys = {"selection": [], "crossover": [], "mutation": []}

        # Rejestr widgetów powiązanych z polami.
        # Dzięki temu możemy potem oznaczyć błędne Entry i ustawić focus.
        self.field_widgets = {}

        # Widgety dla pól zależnych od trybu dokładności (pokazywane/ukrywane)
        self.precision_numeric_label = None
        self.precision_numeric_entry = None
        self.precision_bits_label = None
        self.precision_bits_entry = None

        # Numery wierszy dla pól dokładności (pomocnicze do układu)
        self.precision_numeric_row = None
        self.precision_bits_row = None

    def build(self) -> None:
        # Buduje panel konfiguracji: pola podstawowe + separatory + notebook opcji metod
        self.frame = ttk.LabelFrame(self.parent, text="Panel konfiguracyjny", padding=12)
        self.frame.columnconfigure(0, weight=1)
        self.frame.rowconfigure(1, weight=1)

        top = ttk.Frame(self.frame)
        top.grid(row=0, column=0, sticky="ew")
        top.columnconfigure(1, weight=1)

        r = 0
        r = self._add_combo(
            top, r, FIELDS_GENERAL["problem"]["label"], self.vm.problem, FIELDS_GENERAL["problem"]["values"]
        )
        r = self._add_entry(top, r, FIELDS_GENERAL["n_vars"]["label"], self.vm.n_vars, field_key="n_vars")
        r = self._add_range(top, r)

        # Separator po ustawieniach przedziału
        r = self._add_separator(top, r)

        r = self._add_entry(
            top,
            r,
            FIELDS_GA_MAIN["population"]["label"],
            self.vm.population,
            field_key="population",
        )
        r = self._add_precision_block(top, r)

        # Separator po polu dokładności / liczby bitów
        r = self._add_separator(top, r)

        r = self._add_entry(top, r, FIELDS_GA_MAIN["epochs"]["label"], self.vm.epochs, field_key="epochs")
        r = self._add_entry(top, r, FIELDS_GA_MAIN["epsilon"]["label"], self.vm.epsilon, field_key="epsilon")
        r = self._add_entry(top, r, FIELDS_GA_MAIN["seed"]["label"], self.vm.seed, field_key="seed")

        # Separator po polu seed
        r = self._add_separator(top, r)

        r = self._add_combo(
            top,
            r,
            FIELDS_OPERATORS["selection_method"]["label"],
            self.vm.selection_method,
            FIELDS_OPERATORS["selection_method"]["values"],
        )
        r = self._add_combo(
            top,
            r,
            FIELDS_OPERATORS["crossover_method"]["label"],
            self.vm.crossover_method,
            FIELDS_OPERATORS["crossover_method"]["values"],
        )
        r = self._add_combo(
            top,
            r,
            FIELDS_OPERATORS["mutation_method"]["label"],
            self.vm.mutation_method,
            FIELDS_OPERATORS["mutation_method"]["values"],
        )

        # Separator po metodzie mutacji
        r = self._add_separator(top, r)

        chk = ttk.Frame(top)
        chk.grid(row=r, column=0, columnspan=2, sticky="ew", pady=(8, 2))
        ttk.Checkbutton(
            chk, text=FIELDS_OPERATORS["inversion_enabled"]["label"], variable=self.vm.inversion_enabled
        ).pack(anchor="w")
        ttk.Checkbutton(
            chk, text=FIELDS_OPERATORS["elitism_enabled"]["label"], variable=self.vm.elitism_enabled
        ).pack(anchor="w")
        r += 1

        # Notebook z parametrami metod (przewijalne zakładki)
        self.nb = ttk.Notebook(self.frame)
        self.nb.grid(row=1, column=0, sticky="nsew", pady=(12, 0))

        self.selection_tab = ScrollableTab(self.nb, padding=10)
        self.crossover_tab = ScrollableTab(self.nb, padding=10)
        self.mutation_tab = ScrollableTab(self.nb, padding=10)

        self.nb.add(self.selection_tab, text="Opcje selekcji")
        self.nb.add(self.crossover_tab, text="Opcje krzyżowania")
        self.nb.add(self.mutation_tab, text="Opcje mutacji")

        # Reakcje na zmiany: przełączanie pól dokładności oraz odświeżanie parametrów metod
        self.vm.precision_mode.trace_add("write", lambda *_: self._refresh_precision_visibility())
        self.vm.selection_method.trace_add("write", lambda *_: self._refresh_method_params("selection"))
        self.vm.crossover_method.trace_add("write", lambda *_: self._refresh_method_params("crossover"))
        self.vm.mutation_method.trace_add("write", lambda *_: self._refresh_method_params("mutation"))

        # Inicjalne ustawienie widoczności i zawartości dynamicznych sekcji
        self._refresh_precision_visibility()
        self._refresh_method_params("selection")
        self._refresh_method_params("crossover")
        self._refresh_method_params("mutation")

    def _add_separator(self, parent, row):
        # Dodaje separator poziomy rozdzielający sekcje w panelu
        ttk.Separator(parent, orient="horizontal").grid(row=row, column=0, columnspan=2, sticky="ew", pady=(10, 10))
        return row + 1

    def _add_entry(self, parent, row, label, var, field_key=None):
        # Dodaje wiersz Label + Entry (powiązany z tk.Variable).
        # Jeśli pole jest numeryczne, dostaje walidację na poziomie wpisywania.
        ttk.Label(parent, text=label + ":").grid(row=row, column=0, sticky="w", pady=4, padx=(0, 12))

        entry = ttk.Entry(parent, textvariable=var)
        entry.grid(row=row, column=1, sticky="ew", pady=4)

        if field_key is not None:
            self._register_entry_widget(field_key, entry)

        return row + 1

    def _add_combo(self, parent, row, label, var, values):
        # Dodaje wiersz Label + Combobox (powiązany z tk.Variable)
        ttk.Label(parent, text=label + ":").grid(row=row, column=0, sticky="w", pady=4, padx=(0, 12))
        cb = ttk.Combobox(parent, textvariable=var, values=values, state="readonly")
        cb.grid(row=row, column=1, sticky="ew", pady=4)
        return row + 1

    def _add_range(self, parent, row):
        # Dodaje wiersz z dwoma polami: początek i koniec przedziału
        ttk.Label(parent, text="Przedział (Start / koniec):").grid(
            row=row, column=0, sticky="w", pady=4, padx=(0, 12)
        )
        box = ttk.Frame(parent)
        box.grid(row=row, column=1, sticky="ew", pady=4)
        box.columnconfigure(0, weight=1)
        box.columnconfigure(1, weight=1)

        start_entry = ttk.Entry(box, textvariable=self.vm.range_start)
        start_entry.grid(row=0, column=0, sticky="ew", padx=(0, 10))
        self._register_entry_widget("range_start", start_entry)

        end_entry = ttk.Entry(box, textvariable=self.vm.range_end)
        end_entry.grid(row=0, column=1, sticky="ew")
        self._register_entry_widget("range_end", end_entry)

        return row + 1

    def _add_precision_block(self, parent, row):
        # Dodaje wybór rodzaju dokładności (radiobuttony) oraz dwa pola (jedno jest ukrywane)
        ttk.Label(parent, text=FIELDS_PRECISION["precision_mode"]["label"] + ":").grid(
            row=row, column=0, sticky="w", pady=4, padx=(0, 12)
        )
        box = ttk.Frame(parent)
        box.grid(row=row, column=1, sticky="ew", pady=4)

        ttk.Radiobutton(
            box,
            text="Dokładność liczbowa",
            value="Dokładność liczbowa",
            variable=self.vm.precision_mode,
        ).pack(anchor="w")
        ttk.Radiobutton(
            box,
            text="Liczba bitów",
            value="Liczba bitów",
            variable=self.vm.precision_mode,
        ).pack(anchor="w")

        row += 1

        self.precision_numeric_row = row
        self.precision_numeric_label = ttk.Label(parent, text=FIELDS_PRECISION["precision_numeric"]["label"] + ":")
        self.precision_numeric_label.grid(row=row, column=0, sticky="w", pady=4, padx=(0, 12))
        self.precision_numeric_entry = ttk.Entry(parent, textvariable=self.vm.precision_numeric)
        self.precision_numeric_entry.grid(row=row, column=1, sticky="ew", pady=4)
        self._register_entry_widget("precision_numeric", self.precision_numeric_entry)

        row += 1

        self.precision_bits_row = row
        self.precision_bits_label = ttk.Label(parent, text=FIELDS_PRECISION["precision_bits"]["label"] + ":")
        self.precision_bits_label.grid(row=row, column=0, sticky="w", pady=4, padx=(0, 12))
        self.precision_bits_entry = ttk.Entry(parent, textvariable=self.vm.precision_bits)
        self.precision_bits_entry.grid(row=row, column=1, sticky="ew", pady=4)
        self._register_entry_widget("precision_bits", self.precision_bits_entry)

        row += 1
        return row

    def _register_entry_widget(self, field_key: str, entry: ttk.Entry) -> None:
        # Rejestruje Entry w słowniku pól i podłącza walidację "na wpisywanie"
        # dla pól liczbowych. Dzięki temu litery są blokowane od razu.
        self.field_widgets[field_key] = entry

        spec = self.vm.get_field_spec(field_key)
        if not spec:
            return

        if spec.get("type") in {"int", "float"}:
            vcmd = (entry.register(lambda proposed, key=field_key: self._validate_numeric_keystroke(key, proposed)), "%P")
            entry.configure(validate="key", validatecommand=vcmd)

    def _validate_numeric_keystroke(self, field_key: str, proposed_value: str) -> bool:
        # Deleguje walidację pojedynczego wpisywanego znaku do ViewModelu.
        return self.vm.is_allowed_partial_value(field_key, proposed_value)

    def _refresh_precision_visibility(self) -> None:
        # Przełącza widoczność pola dokładności: liczbowej albo liczby bitów
        mode = self.vm.precision_mode.get()

        if mode == "Dokładność liczbowa":
            self.precision_numeric_label.grid()
            self.precision_numeric_entry.grid()
            self.precision_bits_label.grid_remove()
            self.precision_bits_entry.grid_remove()
        else:
            self.precision_bits_label.grid()
            self.precision_bits_entry.grid()
            self.precision_numeric_label.grid_remove()
            self.precision_numeric_entry.grid_remove()

        # Po zmianie trybu czyścimy stare oznaczenia błędów.
        self.clear_validation_errors()

    def _refresh_method_params(self, group: str) -> None:
        # Odświeża zakładkę parametrów dla wybranej metody (na podstawie METHOD_PARAM_SPECS)
        if group == "selection":
            tab = self.selection_tab.inner
            method = self.vm.selection_method.get()
        elif group == "crossover":
            tab = self.crossover_tab.inner
            method = self.vm.crossover_method.get()
        else:
            tab = self.mutation_tab.inner
            method = self.vm.mutation_method.get()

        # Usuwamy widgety starej sekcji z rejestru pól.
        for key in self._dynamic_field_keys[group]:
            self.field_widgets.pop(key, None)
        self._dynamic_field_keys[group] = []

        old = self._dynamic_frames.get(group)
        if old is not None:
            old.destroy()

        frame = ttk.LabelFrame(tab, text="Parametry metody", padding=10)
        frame.grid(row=0, column=0, sticky="ew")
        frame.columnconfigure(1, weight=1)

        params = METHOD_PARAM_SPECS[group].get(method, [])
        if not params:
            ttk.Label(frame, text="Brak dodatkowych parametrów.").grid(row=0, column=0, sticky="w")
        else:
            r = 0
            for p in params:
                ttk.Label(frame, text=p["label"] + ":").grid(row=r, column=0, sticky="w", pady=4, padx=(0, 12))
                if p.get("type") == "enum":
                    cb = ttk.Combobox(
                        frame,
                        textvariable=self.vm.method_params[p["key"]],
                        values=p["values"],
                        state="readonly",
                    )
                    cb.grid(row=r, column=1, sticky="ew", pady=4)
                else:
                    entry = ttk.Entry(frame, textvariable=self.vm.method_params[p["key"]])
                    entry.grid(row=r, column=1, sticky="ew", pady=4)
                    self._register_entry_widget(p["key"], entry)
                    self._dynamic_field_keys[group].append(p["key"])
                r += 1

        self._dynamic_frames[group] = frame
        self.clear_validation_errors()

    def clear_validation_errors(self) -> None:
        # Czyści styl "błędnego pola" z wszystkich zarejestrowanych Entry.
        for widget in self.field_widgets.values():
            try:
                widget.configure(style="TEntry")
            except tk.TclError:
                pass

    def show_validation_errors(self, errors: dict[str, str]) -> None:
        # Oznacza błędne pola wizualnie i ustawia focus na pierwszym z nich.
        self.clear_validation_errors()

        if not errors:
            return

        first_widget = None
        first_key = next(iter(errors.keys()))

        for key in errors:
            widget = self.field_widgets.get(key)
            if widget is None:
                continue

            try:
                widget.configure(style="Invalid.TEntry")
            except tk.TclError:
                pass

            if first_widget is None:
                first_widget = widget

        # Jeśli błąd dotyczy dynamicznych zakładek metod, przełącz odpowiednią kartę.
        active_selection_keys = set(self._dynamic_field_keys["selection"])
        active_crossover_keys = set(self._dynamic_field_keys["crossover"])
        active_mutation_keys = set(self._dynamic_field_keys["mutation"])

        if first_key in active_selection_keys:
            self.nb.select(self.selection_tab)
        elif first_key in active_crossover_keys:
            self.nb.select(self.crossover_tab)
        elif first_key in active_mutation_keys:
            self.nb.select(self.mutation_tab)

        if first_widget is not None:
            first_widget.focus_set()
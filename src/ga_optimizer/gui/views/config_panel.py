# config_panel.py
# Panel konfiguracji z budową formularza z configu i poprawionym przewijaniem notebooka.

import tkinter as tk
from tkinter import ttk

from ga_optimizer.config.schema import (
    CROSSOVER_METHOD_LABELS,
    CROSSOVER_METHOD_LABELS_REVERSED,
    CROSSOVER_METHOD_PARAM_SPECS,
    GA_MAIN_FIELD_SPECS,
    GENERAL_FIELD_SPECS,
    MUTATION_METHOD_LABELS,
    MUTATION_METHOD_LABELS_REVERSED,
    MUTATION_METHOD_PARAM_SPECS,
    OPERATOR_FIELD_SPECS,
    PRECISION_FIELD_SPECS,
    PRECISION_MODE_LABELS,
    PRECISION_MODE_LABELS_REVERSED,
    SELECTION_METHOD_LABELS,
    SELECTION_METHOD_LABELS_REVERSED,
    SELECTION_METHOD_PARAM_SPECS,
    OBJECTIVE_MODE_LABELS,
    OBJECTIVE_MODE_LABELS_REVERSED,
)
from ga_optimizer.gui.state.view_model import ViewModel


class ScrollableTab(ttk.Frame):
    def __init__(self, parent, padding=10):
        # Przewijalna zakładka notebooka oparta o Canvas + Frame.
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

        # Aktualizuje obszar przewijania po zmianie zawartości.
        self.inner.bind("<Configure>", self._on_frame_configure)
        self.canvas.bind("<Configure>", self._on_canvas_configure)

    def _on_frame_configure(self, event=None):
        # Dopasowuje scrollregion do aktualnej zawartości.
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def _on_canvas_configure(self, event):
        # Rozciąga wewnętrzną ramkę do szerokości canvasa.
        self.canvas.itemconfigure(self._window_id, width=event.width)

    def refresh_mousewheel_bindings(self) -> None:
        # Odświeża bindowanie scrolla dla całej zakładki i wszystkich dzieci.
        # Dzięki temu scroll działa także nad Entry, Combobox, Label itd.
        self._bind_mousewheel_recursive(self)
        self._bind_mousewheel_recursive(self.inner)

    def _bind_mousewheel_recursive(self, widget) -> None:
        # Rekurencyjnie podpina obsługę scrolla do widgetu i jego dzieci.
        widget.bind("<Enter>", self._activate_mousewheel, add="+")
        widget.bind("<Leave>", self._deactivate_mousewheel, add="+")
        widget.bind("<Button-4>", self._on_linux_scroll_up, add="+")
        widget.bind("<Button-5>", self._on_linux_scroll_down, add="+")

        for child in widget.winfo_children():
            self._bind_mousewheel_recursive(child)

    def _activate_mousewheel(self, _event=None):
        # Aktywuje przewijanie po wejściu kursora nad zakładkę.
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel, add="+")
        self.canvas.bind_all("<Shift-MouseWheel>", self._on_shift_mousewheel, add="+")

    def _deactivate_mousewheel(self, _event=None):
        # Wyłącza globalne bindowanie scrolla po opuszczeniu zakładki.
        self.canvas.unbind_all("<MouseWheel>")
        self.canvas.unbind_all("<Shift-MouseWheel>")

    def _on_mousewheel(self, event):
        # Obsługa scrolla pionowego na Windows.
        try:
            self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
        except Exception:
            pass

    def _on_shift_mousewheel(self, event):
        # Obsługa scrolla poziomego po wciśnięciu Shift.
        try:
            self.canvas.xview_scroll(int(-1 * (event.delta / 120)), "units")
        except Exception:
            pass

    def _on_linux_scroll_up(self, _event):
        # Obsługa scrolla w górę na Linux.
        self.canvas.yview_scroll(-1, "units")

    def _on_linux_scroll_down(self, _event):
        # Obsługa scrolla w dół na Linux.
        self.canvas.yview_scroll(1, "units")


class ConfigPanel:
    def __init__(self, parent, vm: ViewModel):
        # Referencja do rodzica i wspólnego modelu stanu GUI.
        self.parent = parent
        self.vm = vm

        # Główny kontener panelu i notebook zakładek metod.
        self.frame = None
        self.nb = None

        # Zakładki dla parametrów metod.
        self.selection_tab = None
        self.crossover_tab = None
        self.mutation_tab = None

        # Dynamiczne ramki i lista aktywnych pól dla każdej zakładki.
        self._dynamic_frames = {
            "selection": None,
            "crossover": None,
            "mutation": None,
        }
        self._dynamic_field_keys = {
            "selection": [],
            "crossover": [],
            "mutation": [],
        }

        # Rejestr widgetów pól, potrzebny do oznaczania błędów.
        self.field_widgets: dict[str, ttk.Entry] = {}
        self.n_vars_entry = None

        # Referencje do widgetów związanych z dokładnością.
        self.precision_numeric_label = None
        self.precision_numeric_entry = None
        self.precision_bits_label = None
        self.precision_bits_entry = None

    def build(self) -> None:
        # Buduje cały panel konfiguracji.
        self.frame = ttk.LabelFrame(self.parent, text="Panel konfiguracyjny", padding=12)
        self.frame.columnconfigure(0, weight=1)
        self.frame.rowconfigure(1, weight=1)

        top = ttk.Frame(self.frame)
        top.grid(row=0, column=0, sticky="ew")
        top.columnconfigure(1, weight=1)

        row = 0
        row = self._add_combo(
            top,
            row,
            GENERAL_FIELD_SPECS["problem_name"]["label"],
            self.vm.problem_name,
            self.vm.get_problem_names(),
        )

        row = self._add_entry(top, row, GENERAL_FIELD_SPECS["n_vars"]["label"], self.vm.n_vars, "n_vars", store_as="n_vars")

        row = self._add_labeled_combo(
            top,
            row,
            GA_MAIN_FIELD_SPECS["objective_mode"]["label"],
            self.vm.objective_mode,
            OBJECTIVE_MODE_LABELS,
            OBJECTIVE_MODE_LABELS_REVERSED,
        )
        
        row = self._add_range(top, row)
        row = self._add_separator(top, row)

        row = self._add_entry(top, row, GA_MAIN_FIELD_SPECS["population"]["label"], self.vm.population, "population")
        row = self._add_precision_block(top, row)
        row = self._add_separator(top, row)

        row = self._add_entry(top, row, GA_MAIN_FIELD_SPECS["epochs"]["label"], self.vm.epochs, "epochs")
        row = self._add_entry(top, row, GA_MAIN_FIELD_SPECS["epsilon"]["label"], self.vm.epsilon, "epsilon")
        row = self._add_entry(top, row, GA_MAIN_FIELD_SPECS["seed"]["label"], self.vm.seed, "seed")
        row = self._add_separator(top, row)

        row = self._add_labeled_combo(
            top,
            row,
            OPERATOR_FIELD_SPECS["selection_method"]["label"],
            self.vm.selection_method,
            SELECTION_METHOD_LABELS,
            SELECTION_METHOD_LABELS_REVERSED,
        )
        row = self._add_labeled_combo(
            top,
            row,
            OPERATOR_FIELD_SPECS["crossover_method"]["label"],
            self.vm.crossover_method,
            CROSSOVER_METHOD_LABELS,
            CROSSOVER_METHOD_LABELS_REVERSED,
        )
        row = self._add_labeled_combo(
            top,
            row,
            OPERATOR_FIELD_SPECS["mutation_method"]["label"],
            self.vm.mutation_method,
            MUTATION_METHOD_LABELS,
            MUTATION_METHOD_LABELS_REVERSED,
        )
        row = self._add_separator(top, row)

        # Sekcja checkboxów dodatkowych operatorów.
        checks = ttk.Frame(top)
        checks.grid(row=row, column=0, columnspan=2, sticky="ew", pady=(8, 2))
        ttk.Checkbutton(
            checks,
            text=OPERATOR_FIELD_SPECS["inversion_enabled"]["label"],
            variable=self.vm.inversion_enabled,
        ).pack(anchor="w")
        ttk.Checkbutton(
            checks,
            text=OPERATOR_FIELD_SPECS["elitism_enabled"]["label"],
            variable=self.vm.elitism_enabled,
        ).pack(anchor="w")

        # Notebook z opcjami metod.
        self.nb = ttk.Notebook(self.frame)
        self.nb.grid(row=1, column=0, sticky="nsew", pady=(12, 0))

        self.selection_tab = ScrollableTab(self.nb, padding=10)
        self.crossover_tab = ScrollableTab(self.nb, padding=10)
        self.mutation_tab = ScrollableTab(self.nb, padding=10)

        self.nb.add(self.selection_tab, text="Opcje selekcji")
        self.nb.add(self.crossover_tab, text="Opcje krzyżowania")
        self.nb.add(self.mutation_tab, text="Opcje mutacji")

        # Reakcje na zmiany pól zależnych od wyborów użytkownika.
        self.vm.problem_name.trace_add("write", lambda *_: self._on_problem_changed())
        self.vm.precision_mode.trace_add("write", lambda *_: self._refresh_precision_visibility())
        self.vm.selection_method.trace_add("write", lambda *_: self._refresh_method_params("selection"))
        self.vm.crossover_method.trace_add("write", lambda *_: self._refresh_method_params("crossover"))
        self.vm.mutation_method.trace_add("write", lambda *_: self._refresh_method_params("mutation"))

        # Inicjalne odświeżenie widoku.
        self._sync_problem_dependent_fields()
        self._refresh_precision_visibility()
        self._refresh_method_params("selection")
        self._refresh_method_params("crossover")
        self._refresh_method_params("mutation")

        # Podpina obsługę scrolla dla wszystkich zakładek.
        self.selection_tab.refresh_mousewheel_bindings()
        self.crossover_tab.refresh_mousewheel_bindings()
        self.mutation_tab.refresh_mousewheel_bindings()

    def _add_separator(self, parent, row):
        # Dodaje separator poziomy między sekcjami.
        ttk.Separator(parent, orient="horizontal").grid(
            row=row,
            column=0,
            columnspan=2,
            sticky="ew",
            pady=(10, 10),
        )
        return row + 1

    def _add_entry(self, parent, row, label, var, field_key=None, store_as=None):
        # Dodaje pole tekstowe z etykietą.
        ttk.Label(parent, text=label + ":").grid(row=row, column=0, sticky="w", pady=4, padx=(0, 12))
        entry = ttk.Entry(parent, textvariable=var)
        entry.grid(row=row, column=1, sticky="ew", pady=4)

        # Rejestruje pole do walidacji i oznaczania błędów.
        if field_key is not None:
            self._register_entry_widget(field_key, entry)

        # Zapamiętuje widget liczby zmiennych, żeby dało się go blokować.
        if store_as == "n_vars":
            self.n_vars_entry = entry

        return row + 1

    def _add_combo(self, parent, row, label, var, values):
        # Dodaje zwykły combobox z etykietą.
        ttk.Label(parent, text=label + ":").grid(row=row, column=0, sticky="w", pady=4, padx=(0, 12))
        cb = ttk.Combobox(parent, textvariable=var, values=values, state="readonly")
        cb.grid(row=row, column=1, sticky="ew", pady=4)
        return row + 1

    def _add_labeled_combo(self, parent, row, label, var, labels_map, reversed_labels_map):
        # Dodaje combobox, który pokazuje polskie etykiety,
        # ale wewnętrznie zapisuje techniczny klucz do zmiennej.
        ttk.Label(parent, text=label + ":").grid(row=row, column=0, sticky="w", pady=4, padx=(0, 12))

        display_var = tk.StringVar(value=labels_map.get(var.get(), var.get()))
        cb = ttk.Combobox(parent, textvariable=display_var, values=list(labels_map.values()), state="readonly")
        cb.grid(row=row, column=1, sticky="ew", pady=4)

        def _sync_from_gui(_event=None):
            selected_label = display_var.get()
            selected_key = reversed_labels_map.get(selected_label)
            if selected_key is not None:
                var.set(selected_key)

        def _sync_from_model(*_args):
            display_var.set(labels_map.get(var.get(), var.get()))

        cb.bind("<<ComboboxSelected>>", _sync_from_gui)
        var.trace_add("write", _sync_from_model)

        return row + 1

    def _add_range(self, parent, row):
        # Dodaje dwa pola dla początku i końca przedziału.
        ttk.Label(parent, text="Przedział (Start / koniec):").grid(
            row=row,
            column=0,
            sticky="w",
            pady=4,
            padx=(0, 12),
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
        # Dodaje sekcję wyboru rodzaju dokładności i odpowiadające jej pola.
        ttk.Label(parent, text=PRECISION_FIELD_SPECS["precision_mode"]["label"] + ":").grid(
            row=row,
            column=0,
            sticky="w",
            pady=4,
            padx=(0, 12),
        )

        box = ttk.Frame(parent)
        box.grid(row=row, column=1, sticky="ew", pady=4)

        precision_display_var = tk.StringVar(
            value=PRECISION_MODE_LABELS.get(self.vm.precision_mode.get(), self.vm.precision_mode.get())
        )

        def _sync_precision_from_model(*_args):
            precision_display_var.set(
                PRECISION_MODE_LABELS.get(self.vm.precision_mode.get(), self.vm.precision_mode.get())
            )

        def _set_precision_mode(mode_key: str):
            self.vm.precision_mode.set(mode_key)

        self.vm.precision_mode.trace_add("write", _sync_precision_from_model)

        ttk.Radiobutton(
            box,
            text=PRECISION_MODE_LABELS["numeric"],
            value=PRECISION_MODE_LABELS["numeric"],
            variable=precision_display_var,
            command=lambda: _set_precision_mode(PRECISION_MODE_LABELS_REVERSED[precision_display_var.get()]),
        ).pack(anchor="w")

        ttk.Radiobutton(
            box,
            text=PRECISION_MODE_LABELS["bits"],
            value=PRECISION_MODE_LABELS["bits"],
            variable=precision_display_var,
            command=lambda: _set_precision_mode(PRECISION_MODE_LABELS_REVERSED[precision_display_var.get()]),
        ).pack(anchor="w")

        row += 1

        self.precision_numeric_label = ttk.Label(
            parent,
            text=PRECISION_FIELD_SPECS["precision_numeric"]["label"] + ":",
        )
        self.precision_numeric_label.grid(row=row, column=0, sticky="w", pady=4, padx=(0, 12))
        self.precision_numeric_entry = ttk.Entry(parent, textvariable=self.vm.precision_numeric)
        self.precision_numeric_entry.grid(row=row, column=1, sticky="ew", pady=4)
        self._register_entry_widget("precision_numeric", self.precision_numeric_entry)

        row += 1

        self.precision_bits_label = ttk.Label(
            parent,
            text=PRECISION_FIELD_SPECS["precision_bits"]["label"] + ":",
        )
        self.precision_bits_label.grid(row=row, column=0, sticky="w", pady=4, padx=(0, 12))
        self.precision_bits_entry = ttk.Entry(parent, textvariable=self.vm.precision_bits)
        self.precision_bits_entry.grid(row=row, column=1, sticky="ew", pady=4)
        self._register_entry_widget("precision_bits", self.precision_bits_entry)

        return row + 1

    def _register_entry_widget(self, field_key: str, entry: ttk.Entry) -> None:
        # Rejestruje widget pola i podpina walidację wpisywanych wartości.
        self.field_widgets[field_key] = entry

        spec = self.vm.get_field_spec(field_key)

        # to służy do blokowania możliwości wpisywania znaków w miejscu liczb
        # if spec and spec.get("type") in {"int", "float"}:
        #     vcmd = (
        #         entry.register(
        #             lambda proposed, key=field_key: self.vm.is_allowed_partial_value(key, proposed)
        #         ),
        #         "%P",
        #     )
        #     entry.configure(validate="key", validatecommand=vcmd)

    def _on_problem_changed(self) -> None:
        # Po zmianie funkcji ustawia zależne wartości domyślne.
        self.vm.apply_problem_defaults()
        self._sync_problem_dependent_fields()
        self.clear_validation_errors()

    def _sync_problem_dependent_fields(self) -> None:
        # Blokuje lub odblokowuje pole liczby zmiennych zależnie od funkcji.
        if self.n_vars_entry is None:
            return

        if self.vm.is_n_vars_locked():
            self.n_vars_entry.configure(state="disabled")
        else:
            self.n_vars_entry.configure(state="normal")

    def _refresh_precision_visibility(self) -> None:
        # Pokazuje tylko to pole dokładności, które jest aktywne.
        if self.vm.precision_mode.get() == "numeric":
            self.precision_numeric_label.grid()
            self.precision_numeric_entry.grid()
            self.precision_bits_label.grid_remove()
            self.precision_bits_entry.grid_remove()
        else:
            self.precision_bits_label.grid()
            self.precision_bits_entry.grid()
            self.precision_numeric_label.grid_remove()
            self.precision_numeric_entry.grid_remove()

        self.clear_validation_errors()

    def _refresh_method_params(self, group: str) -> None:
        # Odbudowuje dynamiczne pola parametrów dla wybranej metody.
        if group == "selection":
            tab = self.selection_tab.inner
            method_name = self.vm.selection_method.get()
            specs = SELECTION_METHOD_PARAM_SPECS.get(method_name, [])
            tab_widget = self.selection_tab
        elif group == "crossover":
            tab = self.crossover_tab.inner
            method_name = self.vm.crossover_method.get()
            specs = CROSSOVER_METHOD_PARAM_SPECS.get(method_name, [])
            tab_widget = self.crossover_tab
        else:
            tab = self.mutation_tab.inner
            method_name = self.vm.mutation_method.get()
            specs = MUTATION_METHOD_PARAM_SPECS.get(method_name, [])
            tab_widget = self.mutation_tab

        # Usuwa stare pola z rejestru błędów.
        for key in self._dynamic_field_keys[group]:
            self.field_widgets.pop(key, None)
        self._dynamic_field_keys[group] = []

        # Niszczy poprzednią dynamiczną ramkę.
        old_frame = self._dynamic_frames[group]
        if old_frame is not None:
            old_frame.destroy()

        frame = ttk.LabelFrame(tab, text="Parametry metody", padding=10)
        frame.grid(row=0, column=0, sticky="ew")
        frame.columnconfigure(1, weight=1)

        if not specs:
            ttk.Label(frame, text="Brak dodatkowych parametrów.").grid(row=0, column=0, sticky="w")
        else:
            row = 0
            for spec in specs:
                ttk.Label(frame, text=spec["label"] + ":").grid(
                    row=row,
                    column=0,
                    sticky="w",
                    pady=4,
                    padx=(0, 12),
                )

                if spec.get("type") == "enum":
                    cb = ttk.Combobox(
                        frame,
                        textvariable=self.vm.method_params[spec["key"]],
                        values=spec["values"],
                        state="readonly",
                    )
                    cb.grid(row=row, column=1, sticky="ew", pady=4)
                else:
                    entry = ttk.Entry(frame, textvariable=self.vm.method_params[spec["key"]])
                    entry.grid(row=row, column=1, sticky="ew", pady=4)
                    self._register_entry_widget(spec["key"], entry)
                    self._dynamic_field_keys[group].append(spec["key"])

                row += 1

        self._dynamic_frames[group] = frame

        # Po odbudowie pól trzeba odświeżyć obsługę scrolla.
        tab_widget.refresh_mousewheel_bindings()
        self.clear_validation_errors()

    def clear_validation_errors(self) -> None:
        # Czyści wizualne oznaczenia błędów ze wszystkich zarejestrowanych pól.
        for widget in self.field_widgets.values():
            try:
                widget.configure(style="TEntry")
            except tk.TclError:
                pass

    def show_validation_errors(self, errors: dict[str, str]) -> None:
        # Oznacza błędne pola i ustawia focus na pierwszym z nich.
        self.clear_validation_errors()

        if not errors:
            return

        first_key = next(iter(errors.keys()))
        first_widget = None

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

        # Jeśli pierwszy błąd jest w jednej z zakładek metod, przełącza notebook.
        selection_keys = set(self._dynamic_field_keys["selection"])
        crossover_keys = set(self._dynamic_field_keys["crossover"])
        mutation_keys = set(self._dynamic_field_keys["mutation"])

        if first_key in selection_keys:
            self.nb.select(self.selection_tab)
        elif first_key in crossover_keys:
            self.nb.select(self.crossover_tab)
        elif first_key in mutation_keys:
            self.nb.select(self.mutation_tab)

        if first_widget is not None:
            first_widget.focus_set()
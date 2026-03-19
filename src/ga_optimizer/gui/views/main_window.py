# main_window.py
# Główne okno aplikacji. Na Start składamy config z GUI, walidujemy go
# i przekazujemy dalej do warstwy pipeline.

from tkinter import Menu, messagebox, ttk
import matplotlib.pyplot as plt

from ga_optimizer.config.validators import build_config_from_payload
from ga_optimizer.gui.state.view_model import ViewModel
from ga_optimizer.gui.views.config_panel import ConfigPanel
from ga_optimizer.gui.views.results_panel import ResultsPanel
from ga_optimizer.gui.views.run_panel import RunPanel
from ga_optimizer.core.pipeline import run_pipeline
from ga_optimizer.config.presets import PRESETS
from ga_optimizer.io.results_writer import save_run_results


class MainWindow:
    LEFT_PANEL_RATIO = 0.31
    RIGHT_TOP_RATIO = 0.12
    RESIZE_DEBOUNCE_MS = 80


    def __init__(self, root):
        # Referencja do głównego okna Tkinter.
        self.root = root

        # Wspólny model stanu GUI.
        self.vm = ViewModel(root)

        # Główne kontenery układu okna.
        self.main_frame = None
        self.header_frame = None
        self.body_frame = None

        # Lewa i prawa część głównego widoku.
        self.left_frame = None
        self.right_frame = None

        # Panele składowe GUI.
        self.config_panel = None
        self.run_panel = None
        self.results_panel = None

        # Ostatni poprawnie zwalidowany config.
        self.last_validated_config = None

        # Ostatni wynik pipeline.
        self.last_pipeline_result = None

        self._resize_after_id = None

    def build(self) -> None:
        # Buduje całe okno aplikacji.
        self._configure_root()
        self._build_menu()
        self._build_layout()
        self._build_header()
        self._build_panels()
        self.root.protocol("WM_DELETE_WINDOW", self._on_close)

    def _configure_root(self) -> None:
        # Ustawia podstawowe parametry okna.
        self.root.title("GA Optimizer")
        self.root.geometry("1700x900")
        self.root.minsize(1400, 800)
        self.root.state("zoomed")

    def _build_menu(self) -> None:
        # Buduje górne menu aplikacji.
        menubar = Menu(self.root)

        presets_menu = Menu(menubar, tearoff=0)
        for preset_name in PRESETS.keys():
            presets_menu.add_command(
                label=preset_name,
                command=lambda name=preset_name: self._apply_preset(name),
            )

        menubar.add_cascade(label="Presets", menu=presets_menu)
        self.root.config(menu=menubar)



    def _apply_preset(self, preset_name: str) -> None:
        # Aplikuje preset do ViewModel i odświeża panel konfiguracji.
        self.vm.apply_preset(preset_name)

        if self.config_panel is not None:
            self.config_panel._sync_problem_dependent_fields()
            self.config_panel._refresh_precision_visibility()
            self.config_panel._refresh_method_params("selection")
            self.config_panel._refresh_method_params("crossover")
            self.config_panel._refresh_method_params("mutation")
            self.config_panel.clear_validation_errors()
            self.config_panel.refresh_layout()

        if self.run_panel is not None:
            self.run_panel.set_status(f"Załadowano preset: {preset_name}")

    def _build_layout(self) -> None:
        # Tworzy główny układ okna: nagłówek + ciało.
        self.main_frame = ttk.Frame(self.root, padding=10)
        self.main_frame.pack(fill="both", expand=True)

        self.main_frame.columnconfigure(0, weight=1)
        self.main_frame.rowconfigure(1, weight=1)

        self.header_frame = ttk.Frame(self.main_frame)
        self.header_frame.grid(row=0, column=0, sticky="ew", pady=(0, 8))

        self.body_frame = ttk.Frame(self.main_frame)
        self.body_frame.grid(row=1, column=0, sticky="nsew")

        # Grid główny: lewy panel config + prawa kolumna.
        self.body_frame.columnconfigure(0, weight=31, uniform="body_cols")
        self.body_frame.columnconfigure(1, weight=69, uniform="body_cols")
        self.body_frame.rowconfigure(0, weight=1)

        self.left_frame = ttk.Frame(self.body_frame)
        self.left_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 6))

        self.right_frame = ttk.Frame(self.body_frame)
        self.right_frame.grid(row=0, column=1, sticky="nsew")

        # Prawa kolumna: uruchamianie u góry, wyniki poniżej.
        self.right_frame.columnconfigure(0, weight=1)
        self.right_frame.rowconfigure(0, weight=12, uniform="right_rows")
        self.right_frame.rowconfigure(1, weight=88, uniform="right_rows")

        self._apply_percent_layout()

    def _build_header(self) -> None:
        # Buduje pasek nagłówka okna.
        ttk.Label(
            self.header_frame,
            text="Algorytm genetyczny - GUI",
            style="Header.TLabel",
        ).pack(side="left")

    def _build_panels(self) -> None:
        # Buduje panel konfiguracji po lewej stronie.
        self.config_panel = ConfigPanel(self.left_frame, self.vm)
        self.config_panel.build()
        self.config_panel.frame.grid(row=0, column=0, sticky="nsew")

        self.left_frame.columnconfigure(0, weight=1)
        self.left_frame.rowconfigure(0, weight=1)

        # Buduje panel sterowania uruchomieniem.
        self.run_panel = RunPanel(self.right_frame, on_start=self._on_start)
        self.run_panel.build()
        self.run_panel.frame.grid(row=0, column=0, sticky="nsew", pady=(0, 4))

        # Buduje panel wyników końcowych + notebook.
        self.results_panel = ResultsPanel(self.right_frame, on_save=self._on_save)
        self.results_panel.build()
        self.results_panel.frame.grid(row=1, column=0, sticky="nsew")

    def _bind_resize_handlers(self) -> None:
        # Aktualizuje procentowe rozmiary paneli po zmianie rozmiaru okna.
        self.root.bind("<Configure>", self._on_root_resize, add="+")

    def _on_root_resize(self, event) -> None:
        # Debounce dla resize, żeby nie przeliczać layoutu zbyt często.
        if event.widget is not self.root:
            return

        if self._resize_after_id is not None:
            try:
                self.root.after_cancel(self._resize_after_id)
            except Exception:
                pass

        self._resize_after_id = self.root.after(self.RESIZE_DEBOUNCE_MS, self._apply_percent_layout)

    def _apply_percent_layout(self) -> None:
        # Ustawia minimalne rozmiary gridu procentowo względem rozmiaru okna.
        width = max(self.root.winfo_width(), 1400)
        height = max(self.root.winfo_height(), 800)

        # Zostawiam dodatkowy margines bezpieczeństwa, żeby prawa część
        # nie wyglądała jakby wychodziła poza ekran.
        available_width = max(1200, width - 24)

        left_width = int(available_width * self.LEFT_PANEL_RATIO)
        right_width = max(380, available_width - left_width - 8)

        run_height = int((height - 70) * self.RIGHT_TOP_RATIO)
        results_height = max(320, (height - 70) - run_height)

        self.body_frame.grid_columnconfigure(0, minsize=left_width)
        self.body_frame.grid_columnconfigure(1, minsize=right_width)

        self.right_frame.grid_rowconfigure(0, minsize=run_height)
        self.right_frame.grid_rowconfigure(1, minsize=results_height)

        if self.config_panel is not None:
            self.config_panel.refresh_layout()

    def _on_start(self) -> None:
        # Resetuje stan poprzedniego uruchomienia.
        self._reset_run_state()

        # Składa payload z aktualnych wartości GUI.
        payload = self.vm.get_payload()

        # Buduje config i uruchamia walidację.
        config, validation = build_config_from_payload(payload)

        # Jeśli są błędy, zaznacza pola i pokazuje komunikat.
        if not validation.ok:
            self.config_panel.show_validation_errors(validation.errors)

            error_lines = "\n".join(f"- {message}" for message in validation.errors.values())
            messagebox.showerror(
                "Błędna konfiguracja",
                f"Popraw konfigurację przed uruchomieniem:\n\n{error_lines}",
            )

            self.run_panel.set_progress(0)
            self.results_panel.enable_save(False)
            self.results_panel.select_results_tab()
            self.run_panel.set_status("Uruchomienie przerwane: błędna konfiguracja.")
            return

        # Zapamiętuje ostatni poprawny config.
        self.last_validated_config = config

        # Czyści oznaczenia błędów po poprawnej walidacji.
        self.config_panel.clear_validation_errors()

        # Przekazuje sterowanie do warstwy pipeline.
        self.results_panel.enable_save(False)
        self.results_panel.select_results_tab()

        pipeline_result = run_pipeline(
            config,
            progress_callback=self._on_engine_progress,
        )
        self.last_pipeline_result = pipeline_result

        # Aktualizuje GUI po wykonaniu pipeline.
        self.run_panel.set_progress(100)
        self.results_panel.enable_save(True)

        finish_message = pipeline_result.get("message", "Algorytm zakończył działanie.")
        self.run_panel.set_status(f"Ukończono. {finish_message}")

        engine_result = pipeline_result.get("engine_result", {})
        problem = self.vm.get_problem_definition()

        self.results_panel.set_summary(
            min_value=engine_result.get("min", "-"),
            q1=engine_result.get("q1", "-"),
            median=engine_result.get("median", "-"),
            q3=engine_result.get("q3", "-"),
            max_value=engine_result.get("max", "-"),
            elapsed=engine_result.get("elapsed", "-"),
        )

        self.results_panel.set_global_minimum_info(
            self._build_global_minimum_info(problem)
        )

        runs = engine_result.get("runs", [])
        self.results_panel.configure_history_tabs(run_count=len(runs))
        self.results_panel.set_run_history(runs)
        self.results_panel.set_full_history(runs)
        self.results_panel.set_plots(
            engine_result=engine_result,
            input_dict=pipeline_result.get("input_dict", {}),
        )
        self.results_panel.set_results_text(
            self._build_results_description(problem, engine_result, runs)
        )
        self.results_panel.select_results_tab()

    def _reset_run_state(self) -> None:
        # Czyści stan GUI przed kolejnym uruchomieniem algorytmu.
        self.last_pipeline_result = None

        if self.run_panel is not None:
            self.run_panel.set_progress(0)
            self.run_panel.set_status("Przygotowywanie nowego uruchomienia...")

        if self.results_panel is not None:
            self.results_panel.enable_save(False)
            self.results_panel.reset()

    def _on_engine_progress(self, completed_steps: int, total_steps: int) -> None:
        # Aktualizuje pasek postępu po każdej epoce.
        if total_steps <= 0:
            self.run_panel.set_progress(0)
        else:
            percent = (completed_steps / total_steps) * 100
            self.run_panel.set_progress(percent)

        self.run_panel.set_status(
            f"Trwa uruchamianie algorytmu genetycznego... krok {completed_steps}/{total_steps}"
        )
        self.root.update_idletasks()

    def _format_function_extrema(self) -> str:
        # Próbuje odczytać prawdziwe ekstrema dla aktualnie wybranej funkcji.
        problem = self.vm.get_problem_definition()

        if hasattr(problem, "true_extrema"):
            return str(problem.true_extrema)

        parts = []

        if hasattr(problem, "global_min"):
            parts.append(f"global_min={problem.global_min}")
        if hasattr(problem, "global_max"):
            parts.append(f"global_max={problem.global_max}")
        if hasattr(problem, "optimum"):
            parts.append(f"optimum={problem.optimum}")
        if hasattr(problem, "optimum_value"):
            parts.append(f"optimum_value={problem.optimum_value}")

        return " | ".join(parts) if parts else "Brak danych"
    
    def _build_global_minimum_info(self, problem) -> str:
        # Buduje tekst o minimum globalnym dla panelu górnego.
        if self.vm.objective_mode.get() == "min" and hasattr(problem, "global_minimum_value"):
            points = getattr(problem, "global_minimum_points", [])
            points_str = "; ".join(str(point) for point in points) if points else "brak danych o punktach"
            return (
                f"Minimum globalne: {problem.global_minimum_value:.7f}"
                # f" | Punkty: {points_str}"
            )

        return "Minimum globalne: nie dotyczy (tryb maksymalizacji)."

    def _build_results_description(self, problem, engine_result: dict, runs: list[dict]) -> str:
        lines: list[str] = []
        objective_mode = self.vm.objective_mode.get()

        def _fmt_value(value) -> str:
            if value in (None, ""):
                return "-"
            try:
                return f"{float(value):.7f}"
            except (TypeError, ValueError):
                return str(value)

        def _fmt_point(point) -> str:
            if point in (None, ""):
                return "-"
            try:
                return "[" + ", ".join(f"{float(value):.7f}" for value in point) + "]"
            except Exception:
                return str(point)

        def _build_best_individuals_pool() -> list[dict]:
            pool: list[dict] = []

            for run in runs:
                summary = run.get("summary", {})
                best_point = summary.get("best_decoded")
                best_chromosome = summary.get("best_chromosome")
                best_fitness = summary.get("max_fitness")
                best_raw_objective = summary.get("best_raw_objective")

                if (
                    best_point is None
                    or best_chromosome is None
                    or best_fitness is None
                    or best_raw_objective is None
                ):
                    continue

                pool.append(
                    {
                        "run_index": (run.get("run_index", 0) + 1),
                        "seed": run.get("seed"),
                        "point": list(best_point),
                        "chromosome": list(best_chromosome),
                        "fitness": float(best_fitness),
                        "raw_objective": float(best_raw_objective),
                    }
                )

            return pool

        def _find_closest_individual_by_raw(pool: list[dict], target: float | None):
            if not pool or target in (None, ""):
                return None

            closest_item = None
            closest_distance = None

            for item in pool:
                distance = abs(item["raw_objective"] - float(target))
                if closest_distance is None or distance < closest_distance:
                    closest_distance = distance
                    closest_item = item

            return closest_item

        def _sort_key(item: dict) -> float:
            return float(item["raw_objective"])

        lines.append(f"Funkcja: {problem.display_name}")
        lines.append(f"Tryb optymalizacji: {objective_mode}")
        lines.append(f"Liczba uruchomień: {engine_result.get('run_count', len(runs))}")
        lines.append(f"Łączny czas: {engine_result.get('elapsed', 0.0):.2f} s")
        lines.append("")

        if objective_mode == "min":
            lines.append(f"Znane minimum globalne: {problem.global_minimum_value:.7f}")
            if getattr(problem, "global_minimum_points", None):
                lines.append("Punkty minimum globalnego:")
                for point in problem.global_minimum_points:
                    lines.append(f"  - {point}")
            lines.append("")

        lines.append("Statystyki końcowe po wszystkich uruchomieniach (wartość funkcji celu)")
        lines.append(f"  Min: {_fmt_value(engine_result.get('min'))}")
        lines.append(f"  25%: {_fmt_value(engine_result.get('q1'))}")
        lines.append(f"  Mediana: {_fmt_value(engine_result.get('median'))}")
        lines.append(f"  75%: {_fmt_value(engine_result.get('q3'))}")
        lines.append(f"  Max: {_fmt_value(engine_result.get('max'))}")
        lines.append(f"  Średnia: {_fmt_value(engine_result.get('avg'))}")
        lines.append("")

        best_individuals_pool = _build_best_individuals_pool()

        if best_individuals_pool:
            sorted_pool = sorted(best_individuals_pool, key=_sort_key)

            if objective_mode == "min":
                best_item = sorted_pool[0]
                worst_item = sorted_pool[-1]
            else:
                best_item = sorted_pool[-1]
                worst_item = sorted_pool[0]

            median_target = engine_result.get("median")
            avg_target = engine_result.get("avg")

            median_item = _find_closest_individual_by_raw(best_individuals_pool, median_target)
            avg_item = _find_closest_individual_by_raw(best_individuals_pool, avg_target)

            if median_item is not None:
                lines.append("Mediana z najlepszych osobników uruchomień")
                lines.append(f"  Mediana wartości funkcji celu: {_fmt_value(median_target)}")
                lines.append(f"  Reprezentatywna wartość funkcji celu: {_fmt_value(median_item['raw_objective'])}")
                lines.append(f"  Fitness tego osobnika: {_fmt_value(median_item['fitness'])}")
                lines.append(f"  Uruchomienie: {median_item['run_index']}")
                lines.append(f"  Chromosom: {median_item['chromosome']}")
                lines.append(f"  Punkt: {_fmt_point(median_item['point'])}")
                lines.append("")

            if avg_item is not None:
                lines.append("Średnia z najlepszych osobników uruchomień")
                lines.append(f"  Średnia wartości funkcji celu: {_fmt_value(avg_target)}")
                lines.append(f"  Reprezentatywna wartość funkcji celu: {_fmt_value(avg_item['raw_objective'])}")
                lines.append(f"  Fitness tego osobnika: {_fmt_value(avg_item['fitness'])}")
                lines.append(f"  Uruchomienie: {avg_item['run_index']}")
                lines.append(f"  Chromosom: {avg_item['chromosome']}")
                lines.append(f"  Punkt: {_fmt_point(avg_item['point'])}")
                lines.append("")

            lines.append("Najlepszy osobnik z najlepszych osobników uruchomień")
            lines.append(f"  Wartość funkcji celu: {_fmt_value(best_item['raw_objective'])}")
            lines.append(f"  Fitness: {_fmt_value(best_item['fitness'])}")
            lines.append(f"  Uruchomienie: {best_item['run_index']}")
            lines.append(f"  Chromosom: {best_item['chromosome']}")
            lines.append(f"  Punkt: {_fmt_point(best_item['point'])}")
            lines.append("")

            lines.append("Najgorszy osobnik z najlepszych osobników uruchomień")
            lines.append(f"  Wartość funkcji celu: {_fmt_value(worst_item['raw_objective'])}")
            lines.append(f"  Fitness: {_fmt_value(worst_item['fitness'])}")
            lines.append(f"  Uruchomienie: {worst_item['run_index']}")
            lines.append(f"  Chromosom: {worst_item['chromosome']}")
            lines.append(f"  Punkt: {_fmt_point(worst_item['point'])}")


        lines = [f" {line}" if line else "" for line in lines]
        return "\n".join(lines)

    def _on_save(self) -> None:
        if not self.last_pipeline_result:
            messagebox.showerror("Błąd", "Brak wyników do zapisania.")
            return

        try:
            engine_result = self.last_pipeline_result.get("engine_result", {})
            if not engine_result:
                messagebox.showerror("Błąd", "Brak danych engine_result do zapisania.")
                return

            saved_dir = save_run_results(engine_result, format_type="all")

            self.run_panel.set_status(f"Ukończono. Wyniki zapisano do: {saved_dir}")
            messagebox.showinfo(
                "Zapisano",
                f"Pomyślnie wyeksportowano wyniki do formatu CSV i JSON.\nFolder:\n{saved_dir}",
            )
        except Exception as e:
            messagebox.showerror("Błąd zapisu", f"Wystąpił błąd podczas zapisu:\n{e}")

    def _on_close(self) -> None:
        try:
            plt.close("all")
        except Exception:
            pass

        try:
            self.root.quit()
        except Exception:
            pass

        try:
            self.root.destroy()
        except Exception:
            pass
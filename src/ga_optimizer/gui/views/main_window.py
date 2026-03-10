# main_window.py
# Główne okno aplikacji. Na Start składamy config z GUI, walidujemy go
# i przekazujemy dalej do warstwy pipeline.

from tkinter import messagebox, ttk

from ga_optimizer.config.validators import build_config_from_payload
from ga_optimizer.gui.state.view_model import ViewModel
from ga_optimizer.gui.views.config_panel import ConfigPanel
from ga_optimizer.gui.views.plots_panel import PlotsPanel
from ga_optimizer.gui.views.results_panel import ResultsPanel
from ga_optimizer.gui.views.run_panel import RunPanel
from ga_optimizer.pipeline.pipeline import run_pipeline


class MainWindow:
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
        self.plots_panel = None
        self.results_panel = None

        # Ostatni poprawnie zwalidowany config.
        self.last_validated_config = None

        # Ostatni wynik pipeline.
        self.last_pipeline_result = None

    def build(self) -> None:
        # Buduje całe okno aplikacji.
        self._configure_root()
        self._build_layout()
        self._build_header()
        self._build_panels()

    def _configure_root(self) -> None:
        # Ustawia podstawowe parametry okna.
        self.root.title("GA Optimizer")
        self.root.geometry("1600x900")
        self.root.minsize(1400, 800)
        # self.root.state("zoomed")

    def _build_layout(self) -> None:
        # Tworzy główny układ okna: nagłówek + ciało.
        self.main_frame = ttk.Frame(self.root, padding=12)
        self.main_frame.pack(fill="both", expand=True)

        self.header_frame = ttk.Frame(self.main_frame)
        self.header_frame.pack(fill="x", pady=(0, 10))

        self.body_frame = ttk.Frame(self.main_frame)
        self.body_frame.pack(fill="both", expand=True)

        # Konfiguruje siatkę dla sekcji głównej.
        self.body_frame.columnconfigure(0, weight=0)
        self.body_frame.columnconfigure(1, weight=1)
        self.body_frame.rowconfigure(0, weight=1)

        # Lewa kolumna ma stałą szerokość i zawiera konfigurację.
        self.left_frame = ttk.Frame(self.body_frame, width=620)
        self.left_frame.grid(row=0, column=0, sticky="nsw", padx=(0, 12))
        self.left_frame.grid_propagate(False)

        # Prawa kolumna zajmuje resztę przestrzeni.
        self.right_frame = ttk.Frame(self.body_frame)
        self.right_frame.grid(row=0, column=1, sticky="nsew")
        self.right_frame.columnconfigure(0, weight=1)
        self.right_frame.rowconfigure(0, weight=0)
        self.right_frame.rowconfigure(1, weight=1)
        self.right_frame.rowconfigure(2, weight=0)

    def _build_header(self) -> None:
        # Buduje pasek nagłówka okna.
        ttk.Label(self.header_frame, text="Algorytm genetyczny - GUI", style="Header.TLabel").pack(side="left")

    def _build_panels(self) -> None:
        # Buduje panel konfiguracji po lewej stronie.
        self.config_panel = ConfigPanel(self.left_frame, self.vm)
        self.config_panel.build()
        self.config_panel.frame.pack(fill="both", expand=True)

        # Buduje panel sterowania uruchomieniem.
        self.run_panel = RunPanel(self.right_frame, on_start=self._on_start, on_save=self._on_save)
        self.run_panel.build()
        self.run_panel.frame.grid(row=0, column=0, sticky="ew", pady=(0, 10))

        # Buduje panel wykresów / historii.
        self.plots_panel = PlotsPanel(self.right_frame)
        self.plots_panel.build()
        self.plots_panel.frame.grid(row=1, column=0, sticky="nsew", pady=(0, 10))

        # Buduje panel wyników końcowych.
        self.results_panel = ResultsPanel(self.right_frame)
        self.results_panel.build()
        self.results_panel.frame.grid(row=2, column=0, sticky="ew")

    def _on_start(self) -> None:
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
            self.run_panel.enable_save(False)
            self.run_panel.set_status("Błąd walidacji konfiguracji.")
            return

        # Zapamiętuje ostatni poprawny config.
        self.last_validated_config = config

        # Czyści oznaczenia błędów po poprawnej walidacji.
        self.config_panel.clear_validation_errors()

        # Przekazuje sterowanie do warstwy pipeline.
        self.run_panel.set_progress(10)
        self.run_panel.enable_save(False)
        self.run_panel.set_status("Walidacja zakończona. Uruchamianie pipeline ...")

        pipeline_result = run_pipeline(config)
        self.last_pipeline_result = pipeline_result

        # Aktualizuje GUI po wykonaniu pipeline.
        self.run_panel.set_progress(100)
        self.run_panel.enable_save(True)
        self.run_panel.set_status(pipeline_result["message"])

        engine_result = pipeline_result.get("engine_result", {})

        self.results_panel.set_termination_reason(
            "Konfiguracja zwalidowana i przekazana do pipeline / engine placeholder."
        )
        self.results_panel.set_summary(
            best=engine_result.get("best", "-"),
            avg=engine_result.get("avg", "-"),
            worst=engine_result.get("worst", "-"),
            elapsed=engine_result.get("elapsed", "-"),
        )

    def _on_save(self) -> None:
        # Placeholder pod zapis wyników.
        self.run_panel.set_status("Zapisano (placeholder)")
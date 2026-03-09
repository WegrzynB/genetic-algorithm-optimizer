# main_window.py
# Definiuje główne okno aplikacji i układ nadrzędny interfejsu

from tkinter import messagebox, ttk

from ga_optimizer.gui.state.view_model import ViewModel
from ga_optimizer.gui.views.config_panel import ConfigPanel
from ga_optimizer.gui.views.run_panel import RunPanel
from ga_optimizer.gui.views.plots_panel import PlotsPanel
from ga_optimizer.gui.views.results_panel import ResultsPanel


class MainWindow:
    def __init__(self, root):
        # Przechowuje obiekt okna głównego oraz wspólny model stanu GUI
        self.root = root
        self.vm = ViewModel(root)

        # Główne kontenery layoutu
        self.main_frame = None
        self.header_frame = None
        self.body_frame = None

        # Kolumny: lewa (konfiguracja) i prawa (wyniki/wykresy/sterowanie)
        self.left_frame = None
        self.right_frame = None

        # Panele GUI
        self.config_panel = None
        self.run_panel = None
        self.plots_panel = None
        self.results_panel = None

    def build(self) -> None:
        # Buduje całe okno: ustawienia, layout, nagłówek oraz panele
        self._configure_root()
        self._build_layout()
        self._build_header()
        self._build_panels()

    def _configure_root(self) -> None:
        # Ustawia tytuł i podstawowe rozmiary okna
        self.root.title("GA Optimizer")
        self.root.geometry("1600x900")
        self.root.minsize(1400, 800)
        self.root.state("zoomed")

    def _build_layout(self) -> None:
        # Kontener główny (padding) oraz podział na nagłówek i ciało
        self.main_frame = ttk.Frame(self.root, padding=12)
        self.main_frame.pack(fill="both", expand=True)

        self.header_frame = ttk.Frame(self.main_frame)
        self.header_frame.pack(fill="x", pady=(0, 10))

        self.body_frame = ttk.Frame(self.main_frame)
        self.body_frame.pack(fill="both", expand=True)

        # Układ siatki: kolumna 0 (lewa) stała, kolumna 1 (prawa) rozciągliwa
        self.body_frame.columnconfigure(0, weight=0)
        self.body_frame.columnconfigure(1, weight=1)
        self.body_frame.rowconfigure(0, weight=1)

        # Lewy panel (konfiguracja) ma stałą szerokość i nie dopasowuje się do zawartości
        self.left_frame = ttk.Frame(self.body_frame, width=620)
        self.left_frame.grid(row=0, column=0, sticky="nsw", padx=(0, 12))
        self.left_frame.grid_propagate(False)

        # Prawy panel wypełnia resztę przestrzeni
        self.right_frame = ttk.Frame(self.body_frame)
        self.right_frame.grid(row=0, column=1, sticky="nsew")
        self.right_frame.columnconfigure(0, weight=1)
        self.right_frame.rowconfigure(0, weight=0)
        self.right_frame.rowconfigure(1, weight=1)
        self.right_frame.rowconfigure(2, weight=0)

    def _build_header(self) -> None:
        # Nagłówek okna (tytuł interfejsu)
        ttk.Label(self.header_frame, text="Algorytm genetyczny - GUI", style="Header.TLabel").pack(side="left")

    def _build_panels(self) -> None:
        # Panel konfiguracji po lewej stronie
        self.config_panel = ConfigPanel(self.left_frame, self.vm)
        self.config_panel.build()
        self.config_panel.frame.pack(fill="both", expand=True)

        # Panel sterowania uruchomieniem (góra prawej strony)
        self.run_panel = RunPanel(self.right_frame, on_start=self._on_start, on_save=self._on_save)
        self.run_panel.build()
        self.run_panel.frame.grid(row=0, column=0, sticky="ew", pady=(0, 10))

        # Panel wykresu/historii (środek prawej strony)
        self.plots_panel = PlotsPanel(self.right_frame)
        self.plots_panel.build()
        self.plots_panel.frame.grid(row=1, column=0, sticky="nsew", pady=(0, 10))

        # Panel wyników końcowych i tabeli najlepszych osobników (dół prawej strony)
        self.results_panel = ResultsPanel(self.right_frame)
        self.results_panel.build()
        self.results_panel.frame.grid(row=2, column=0, sticky="ew")

    def _on_start(self) -> None:
        # Najpierw uruchamiamy walidację formularza.
        # Jeśli są błędy, nie przechodzimy dalej do właściwego startu algorytmu.
        errors = self.vm.validate_all()

        if errors:
            self.config_panel.show_validation_errors(errors)

            error_text = "\n".join(f"- {message}" for message in errors.values())
            messagebox.showerror(
                "Błędne dane wejściowe",
                f"Popraw pola formularza przed uruchomieniem algorytmu:\n\n{error_text}",
            )

            self.run_panel.set_progress(0)
            self.run_panel.enable_save(False)
            self.run_panel.set_status("Błąd walidacji formularza - popraw zaznaczone pola.")
            return

        # Jeśli walidacja przeszła, czyścimy stare oznaczenia błędów
        # i wykonujemy placeholder dalszego przebiegu.
        self.config_panel.clear_validation_errors()

        # Placeholder: tutaj docelowo uruchomiony zostanie silnik GA i aktualizacja UI
        self.run_panel.set_status("Uruchomiono (placeholder)")
        self.run_panel.set_progress(35)
        self.run_panel.enable_save(True)
        self.results_panel.set_termination_reason("Zakończenie: (placeholder) Epoki / Epsilon")
        self.results_panel.set_summary(best="-", avg="-", worst="-", elapsed="-")

    def _on_save(self) -> None:
        # Placeholder: tutaj docelowo zapis wyników do pliku/bazy
        self.run_panel.set_status("Zapisano (placeholder)")
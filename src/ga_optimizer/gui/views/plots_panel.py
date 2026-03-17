# plots_panel.py

from __future__ import annotations

from tkinter import ttk

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk

from ga_optimizer.visualization.show_charts import get_all_figures


class PlotsPanel:
    def __init__(self, parent):
        self.parent = parent

        self.frame = None
        self.placeholder_label = None
        self.notebook = None

        self._figures = {}
        self._canvases = []
        self._toolbars = []

    def build(self) -> None:
        self.frame = ttk.Frame(self.parent)
        self.frame.grid(row=0, column=0, sticky="nsew")

        self.parent.columnconfigure(0, weight=1)
        self.parent.rowconfigure(0, weight=1)

        self.frame.columnconfigure(0, weight=1)
        self.frame.rowconfigure(0, weight=1)

        self.placeholder_label = ttk.Label(
            self.frame,
            text="Tutaj będą wykresy i wizualizacje wyników.",
            anchor="center",
            justify="center",
        )
        self.placeholder_label.grid(row=0, column=0, sticky="nsew")

    def set_plots(self, engine_result: dict, input_dict: dict) -> None:
        self.reset()

        figures = get_all_figures(engine_result=engine_result, input_dict=input_dict)
        self._figures = figures

        if not figures:
            self.placeholder_label = ttk.Label(
                self.frame,
                text="Brak danych do wygenerowania wykresów.",
                anchor="center",
                justify="center",
            )
            self.placeholder_label.grid(row=0, column=0, sticky="nsew")
            return

        self.notebook = ttk.Notebook(self.frame)
        self.notebook.grid(row=0, column=0, sticky="nsew")

        for plot_key, figure in figures.items():
            tab = ttk.Frame(self.notebook, padding=8)
            tab.columnconfigure(0, weight=1)
            tab.rowconfigure(0, weight=1)

            canvas_container = ttk.Frame(tab)
            canvas_container.grid(row=0, column=0, sticky="nsew")
            canvas_container.columnconfigure(0, weight=1)
            canvas_container.rowconfigure(0, weight=1)

            canvas = FigureCanvasTkAgg(figure, master=canvas_container)
            canvas_widget = canvas.get_tk_widget()
            canvas_widget.grid(row=0, column=0, sticky="nsew")
            canvas.draw()

            toolbar = NavigationToolbar2Tk(canvas, tab, pack_toolbar=False)
            toolbar.update()
            toolbar.grid(row=1, column=0, sticky="ew", pady=(6, 0))

            self._canvases.append(canvas)
            self._toolbars.append(toolbar)

            self.notebook.add(tab, text=self._label_for_plot(plot_key))

    def reset(self) -> None:
        for canvas in self._canvases:
            try:
                canvas.get_tk_widget().destroy()
            except Exception:
                pass

        for toolbar in self._toolbars:
            try:
                toolbar.destroy()
            except Exception:
                pass

        self._canvases.clear()
        self._toolbars.clear()

        if self.notebook is not None:
            self.notebook.destroy()
            self.notebook = None

        if self.placeholder_label is not None:
            self.placeholder_label.destroy()
            self.placeholder_label = None

        for figure in self._figures.values():
            try:
                figure.clf()
            except Exception:
                pass

        self._figures = {}

    @staticmethod
    def _label_for_plot(plot_key: str) -> str:
        labels = {
            "convergence": "Zbieżność",
            "distribution": "Rozkład fitness",
            "function_1d": "Funkcja 1D + trajektoria",
            "function_2d_contour": "Rzut 2D + trajektoria",
            "function_2d_surface": "Powierzchnia 3D + trajektoria",
        }
        return labels.get(plot_key, plot_key.replace("_", " ").title())
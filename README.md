# GA Optimizer

Aplikacja w języku Python implementująca **algorytm genetyczny (GA)** do optymalizacji (minimalizacji lub maksymalizacji) funkcji wielu zmiennych. Projekt zawiera interfejs graficzny (Tkinter), zautomatyzowany zapis wyników (JSON/CSV), generowanie wykresów (matplotlib/seaborn) oraz zestaw skryptów eksperymentalnych do benchmarkowania operatorów.

Projekt zrealizowany w ramach przedmiotu *Obliczenia Ewolucyjne*.

**Autorzy:** Kamil Jarkowski, Bartłomiej Węgrzyn, Krystian Węgrzyn, Paweł Węgrzyn

---

## Wymagania

- **Python:** 3.12+
- **Biblioteki:** `numpy`, `matplotlib`, `seaborn`, `pandas` (szczegóły w pliku `requirements.txt`).

*Uwaga: Operatory GA oraz cała logika algorytmu zostały zaimplementowane od zera, bez użycia gotowych frameworków ewolucyjnych.*

---

## Instalacja i uruchomienie

**1. Klonowanie repozytorium**
```bash
git clone [https://github.com/WegrzynB/genetic-algorithm-optimizer.git](https://github.com/WegrzynB/genetic-algorithm-optimizer.git)
cd genetic-algorithm-optimizer
```

**2. Utworzenie i aktywacja wirtualnego środowiska**

*Windows (PowerShell):*
```powershell
py -3.12 -m venv .venv
.venv\Scripts\Activate.ps1
```

*Linux / macOS:*
```bash
python3.12 -m venv .venv
source .venv/bin/activate
```

**3. Instalacja zależności**
```bash
pip install -r requirements.txt
```

---

## Korzystanie z aplikacji

Projekt oferuje dwa niezależne tryby pracy: interaktywny oraz zautomatyzowany (eksperymentalny).

### Tryb GUI (Interfejs graficzny)
Aby otworzyć okno aplikacji, w którym można ręcznie skonfigurować parametry i śledzić proces optymalizacji na żywo, uruchom:
```bash
python scripts/run_gui.py
```

### Tryb Eksperymentów (Benchmarki)
Tryb ten służy do masowego testowania operatorów i zbierania danych statystycznych.
1. Otwórz plik `src/ga_optimizer/experiments/experiment_config.py`.
2. Ustaw `ACTIVE_EXPERIMENT_NAME` na wybrany profil testowy, np.:
   - `"single_function_operator_search_default"` (testy dla jednej funkcji),
   - `"all_functions_global_default"` (testy dla wszystkich funkcji).
3. Uruchom skrypt:
```bash
python scripts/run_experiment.py
```
Wyniki, rankingi i raporty zostaną wygenerowane w folderze `data/output/tests/`.

---

## Zaimplementowane operatory GA

Algorytm pozwala na dowolne łączenie poniższych metod na etapie konfiguracji:

### Selekcja
* **Ruletka** (O(n log n))
* **SUS** (Stochastyczne Próbkowanie Uniwersalne) (O(n))
* **Turniejowa** oraz **Podwójny turniej**
* **Najlepsza (Best)** / **Najgorsza (Worst)**
* **Losowa (Unbiased)**

### Krzyżowanie
* **N-punktowe:** Jednopunktowe, Dwupunktowe, Trzypunktowe, Wielopunktowe
* **Zaawansowane:** Równomierne, Tasujące, Ziarniste, Segmentowe, Zredukowane, Niszczące, Większościowe
* **Dla wartości ciągłych:** Arytmetyczne

### Mutacja
* **Punktowa:** Jednopunktowa, Dwupunktowa, Krawędziowa
* **Strukturalna:** Zamiany (Swap), Tasowania (Scramble)
* **Zależna od prawdopodobieństwa:** Bitowa, Resetowania

*Projekt obsługuje również elitaryzm oraz inwersję w celu zachowania najlepszych rozwiązań i zwiększenia różnorodności populacji.*

---

## Funkcje testowe

Aplikacja zawiera bazę **21 znanych funkcji benchmarkowych** służących do oceny wydajności algorytmów optymalizacyjnych, w tym m.in.:
* **Funkcje jednomodalne:** Hypersphere, Hyperellipsoid.
* **Wielomodalne (z wieloma minimami lokalnymi):** Rastrigin, Ackley, Schwefel, Griewank.
* **Specyficzne / Zmodyfikowane:** Rosenbrock (wąska dolina), Michalewicz, Eggholder, Styblinski-Tang.

Każda funkcja posiada zdefiniowaną optymalną dziedzinę poszukiwań oraz znane minimum globalne.

---

## Struktura projektu

```text
ga_optimizer/
├── scripts/                    # Skrypty startowe (run_gui.py, run_experiment.py)
├── src/ga_optimizer/
│   ├── core/                   # Główna pętla algorytmu, populacja, osobniki
│   ├── operators/              # Logika metod selekcji, krzyżowania i mutacji
│   ├── problems/               # Definicje 21 funkcji testowych
│   ├── gui/                    # Widoki i stan interfejsu (Tkinter)
│   ├── experiments/            # System benchmarkowania i analizy danych
│   ├── visualization/          # Generowanie wykresów 2D/3D i histogramów
│   └── io/                     # Zapis wyników do plików CSV/JSON
├── data/output/                # Katalog docelowy na logi i wykresy z uruchomień
└── docs/                       # Dokumentacja architektury i opis algorytmów
```

---

## Wyniki i eksport danych

Po zakończeniu działania algorytmu aplikacja generuje:
- **Wykresy zbieżności:** (Najlepszy, średni i najgorszy osobnik na przestrzeni epok).
- **Wizualizacje przestrzenne:** Krajobraz funkcji testowej (rzut 2D i wykres 3D) z zaznaczoną trajektorią rozwiązań.
- **Histogramy:** Rozkład fitness w końcowej populacji.
- **Surowe dane:** Pliki `.json` i `.csv` z pełną historią epok, gotowe do zewnętrznej analizy.

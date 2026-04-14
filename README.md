# README.md
# GA Optimizer

Aplikacja w Pythonie implementująca *algorytm genetyczny (GA)* do optymalizacji (minimalizacji / maksymalizacji) funkcji wielu zmiennych. Projekt zawiera pełny interfejs graficzny (Tkinter), zapis wyników (JSON/CSV), wykresy (matplotlib) oraz zestaw skryptów eksperymentalnych do benchmarkowania operatorów.

Projekt realizowany w ramach przedmiotu *Obliczenia Ewolucyjne*.

*Autorzy:* Kamil Jarkowski, Bartłomiej Węgrzyn, Krystian Węgrzyn, Paweł Węgrzyn

---

## Wymagania

- Python 3.12+
- Git

Zależności Python: numpy, matplotlib, seaborn, pandas (patrz requirements.txt).  
Operatory GA oraz logika algorytmu zaimplementowane od zera.

---

## Instalacja

*1. Klonowanie repozytorium*

git clone <URL_REPO>
cd <NAZWA_REPO>

*2. Wirtualne środowisko*

Windows (PowerShell):
py -3.12 -m venv .venv
.venv\Scripts\Activate.ps1

Windows (cmd):
cmd
py -3.12 -m venv .venv
.venv\Scripts\activate

Linux / macOS:
python3.12 -m venv .venv
source .venv/bin/activate

*3. Uruchomienie*

### GUI

python scripts/run_gui.py

Otwiera okno aplikacji. Z poziomu GUI można wybrać funkcję testową, skonfigurować wszystkie parametry algorytmu, uruchomić optymalizację i obejrzeć wyniki oraz wykresy.

### Eksperymenty (benchmarki)

1. Otwórz src/ga_optimizer/experiments/experiment_config.py
2. Ustaw ACTIVE_EXPERIMENT_NAME na jeden z presetów:
   - "single_function_operator_search_default" — szukanie najlepszych operatorów dla jednej funkcji
   - "random_functions_default" — testy na losowo wybranych funkcjach
   - "all_functions_global_default" — testy na wszystkich funkcjach
3. Dla testów jednofunkcyjnych ustaw też TARGET_PROBLEM_NAME (np. "Rosenbrock")
4. Uruchom:
   
   python scripts/run_experiment.py
   
5. Wyniki trafiają do data/output/tests/ — zacznij od report.md

---

## Funkcje testowe

Aplikacja obsługuje 21 funkcji benchmarkowych. Każda funkcja ma zdefiniowany sugerowany zakres poszukiwań, znane minimum globalne oraz domyślną liczbę zmiennych.

| Funkcja | Zakres | Min. globalne | Charakterystyka |

| Hypersphere | [-5, 5] | f(0,0) = 0 | Gładki, jednomodalny — prosta do optymalizacji |
| Hyperellipsoid | [-65.536, 65.536] | f(0,0) = 0 | Eliptyczny krajobraz, jednomodalny |
| Rastrigin | [-5.12, 5.12] | f(0,0) = 0 | Silnie wielomodalna, regularna siatka minimów lokalnych |
| Rosenbrock | [-2.048, 2.048] | f(1,1) = 0 | Wąska dolina — wymaga dużej precyzji i liczby epok |
| Ackley | [-32.768, 32.768] | f(0,0) ≈ 0 | Wielomodalna z płaskim centrum, pułapka na GA |
| Schwefel | [-500, 500] | f(420.97,...) ≈ 0 | Minimum daleko od centrum dziedziny |
| Griewank | [-600, 600] | f(0,0) = 0 | Wielomodalna, ale regularnie ustrukturyzowana |
| Michalewicz | [0, π] | f(...) ≈ -1.80 | Ostre, wąskie minima — wymaga precyzji |
| De Jong 3 | [-3.8, 3.8] | f(-3.5,-3.5) = -8 | Schodkowa, nieciągła |
| De Jong 5 | [-65.536, 65.536] | f(...) ≈ 0.998 | Wielomodalna z wieloma równoważnymi minimami |
| Martin & Gaddy | [-20, 20] | f(5,5) = 0 | Dwie zmienne, stała liczba wymiarów |
| Goldstein-Price | [-2, 2] | f(0,-1) = 3 | Silnie wielomodalna, stała liczba wymiarów |
| Picheny G-P | [-2, 2] | f(0.5,0.25) ≈ -3.13 | Zmodyfikowana Goldstein-Price |
| McCormick | [-3, 4] | f(-0.547,-1.547) ≈ -1.91 | Niesymetryczna dziedzina |
| Himmelblau | [-5, 5] | f(3,2) = 0 | Cztery równoważne minima globalne |
| Styblinski-Tang | [-5, 5] | f(-2.9,...) ≈ -78.33 | Wielomodalna z wyraźnym minimum |
| Schaffer 2 | [-100, 100] | f(0,0) = 0 | Współśrodkowe fale, stała liczba wymiarów |
| Rana | [-515, 515] | f(-488.6,512) ≈ -511.73 | Nieregularny, fraktalopodobny krajobraz |
| Eggholder | [-515, 515] | f(512,404.25) ≈ -959.71 | Minimum przy granicy dziedziny |
| Easom | [-100, 100] | f(π,π) = -1 | Bardzo wąskie minimum w gładkim krajobrazie |
| Pits and Holes | [-20, 20] | f(-10,-10) ≈ -0.239 | Nieregularny krajobraz z wieloma lokalnymi minimami |

---

## Algorytm genetyczny — opis

GA to metaheurystyczna metoda optymalizacji inspirowana ewolucją biologiczną, opracowana przez Johna Hollanda w latach 70. XX wieku.

### Podstawowe pojęcia

- *Osobnik* — jedno potencjalne rozwiązanie problemu
- *Chromosom* — reprezentacja osobnika jako ciąg genów (binarny lub liczbowy)
- *Populacja* — zbiór N osobników, inicjalizowany losowo
- *Fitness* — ocena przystosowania osobnika na podstawie wartości funkcji celu

### Pętla algorytmu

1. Generacja populacji początkowej (losowej)
2. Ocena osobników — obliczenie f(x) i fitness
3. Selekcja — wybór rodziców do reprodukcji
4. Krzyżowanie — tworzenie potomstwa przez wymianę fragmentów chromosomów
5. Mutacja — losowe zmiany w chromosomach potomstwa
6. Inwersja (opcjonalnie) — odwrócenie fragmentu chromosomu
7. Elitaryzm — przeniesienie najlepszych osobników bez zmian
8. Nowa populacja zastępuje starą
9. Powrót do kroku 2 — przez zadaną liczbę epok

### Warunki zakończenia

- Osiągnięcie maksymalnej liczby epok
- Osiągnięcie zadanego progu wartości funkcji celu
- Brak poprawy między epokami poniżej zadanego progu

### Kodowanie

Chromosomy mogą być reprezentowane na dwa sposoby:
- *Liczbowo* — bezpośrednia reprezentacja wartości zmiennych z zadaną precyzją (np. 0.001)
- *Binarnie* — kodowanie z zadaną liczbą bitów na zmienną (np. 16 lub 32 bity)

---

## Operatory GA

### Selekcja

| Metoda | Opis | Złożoność |

| Ruletka | Prawdopodobieństwo wyboru proporcjonalne do fitness | O(n log n) |
| SUS (Stochastyczne Próbkowanie Uniwersalne) | Jeden obrót koła, równomierne próbkowanie | O(n) |
| Turniejowa | Losuje grupę k osobników, wybiera najlepszego | O(n) |
| Podwójny turniej | Dwa etapy turniejowe | O(n) |
| Najlepsza (Best) | Odcięcie — zachowuje tylko T% najlepszych | O(n log n) |
| Najgorsza (Worst) | Eliminuje kolejno najsłabszych osobników | O(n log n) |
| Losowa (Unbiased) | Brak ciśnienia selekcyjnego, czysto losowa | O(n) |

### Krzyżowanie

| Metoda | Opis |

| Jednopunktowe | Podział w jednym losowym punkcie, zamiana prawych części |
| Dwupunktowe | Podział w dwóch punktach, zamiana środkowego fragmentu |
| Trzypunktowe | Podział w trzech punktach, naprzemienny wybór fragmentów |
| Wielopunktowe | k losowych punktów, naprzemienny wybór fragmentów |
| Równomierne | Każdy gen losowo z jednego z rodziców (z prawdop. p) |
| Tasujące | Tasowanie kolejności genów przed jednopunktowym krzyżowaniem |
| Ziarniste | Podział na bloki (granule), losowy wybór rodzica dla każdego bloku |
| Segmentowe | Zamiana co drugiego segmentu o stałej długości |
| Arytmetyczne | Kombinacja liniowa: α·P1 + (1−α)·P2 |
| Zredukowane | Krzyżowanie tylko w miejscach różnic między rodzicami |
| Niszczące | Losowa zamiana podzbioru miejsc, gdzie rodzice się różnią |
| Większościowe | Kopiuj zgodne geny, losuj w miejscach różnic |

### Mutacja

| Metoda | Opis |

| Jednopunktowa | Zmiana jednego losowego genu |
| Dwupunktowa | Zmiana dwóch losowych genów |
| Krawędziowa | Modyfikacja genów na krańcach chromosomu |
| Bitowa | Niezależna zmiana każdego genu z prawdopodobieństwem p |
| Zamiany (Swap) | Zamiana miejscami dwóch losowych genów |
| Tasowania (Scramble) | Przetasowanie losowego fragmentu chromosomu |
| Resetowania | Losowy gen ustawiany na nową losową wartość |

### Inwersja i Elitaryzm

- *Inwersja* — odwrócenie losowego fragmentu chromosomu; zwiększa różnorodność bez zmiany wartości genów
- *Elitaryzm* — przeniesienie najlepszych osobników z pokolenia t do t+1 bez modyfikacji; zapobiega utracie najlepszych znalezionych rozwiązań

---

## Struktura projektu

ga_optimizer/
├── scripts/
│   ├── run_gui.py              # Uruchamianie GUI
│   └── run_experiment.py       # Uruchamianie eksperymentów
│
├── src/ga_optimizer/
│   ├── core/                   # Rdzeń GA: populacja, pętla epok, pipeline
│   ├── operators/              # Operatory GA i dispatchery
│   │   ├── crossover/          # 12 metod krzyżowania
│   │   ├── mutation/           # 7 metod mutacji
│   │   ├── selection/          # 7 metod selekcji
│   │   ├── dispatch/           # Dispatchery operatorów
│   │   ├── elitism.py
│   │   └── inversion.py
│   ├── config/                 # Schemat konfiguracji, presety, walidacja
│   ├── problems/               # Funkcje testowe i rejestr problemów
│   ├── gui/                    # Interfejs Tkinter (widoki, stan UI)
│   │   ├── views/              # Panele: konfiguracja, uruchomienie, wyniki, wykresy
│   │   └── state/              # ViewModel (stan GUI)
│   ├── experiments/            # Benchmarki i agregacja wyników
│   ├── visualization/          # Wykresy matplotlib/seaborn
│   ├── io/                     # Zapis wyników JSON/CSV
│   └── utils/                  # Helpery narzędziowe
│
├── data/output/                # Wyniki runów i eksperymentów (nie commitujemy)
│   ├── runs/                   # Wyniki pojedynczych uruchomień z GUI
│   └── tests/                  # Wyniki eksperymentów benchmarkowych
│
└── docs/
    ├── architecture/           # Opis architektury i zależności modułów
    ├── notes/                  # Notatki zespołu
    └── todo/                   # Plan i lista zadań

*Zasady zależności między modułami:*
- gui → może importować: config, core, problems, io, visualization, utils
- core → może importować: config, operators, problems, utils
- operators → może importować: utils (bez zależności od GUI ani core)
- experiments → może importować: config, core, problems, io, visualization, utils
- utils nie zależy od żadnych innych modułów domenowych

---

## Eksperymenty

Moduł experiments/ pozwala na systematyczne testowanie różnych kombinacji operatorów GA. Trzy tryby eksperymentów:

- **single_function_operator_search** — przeszukiwanie przestrzeni operatorów dla wybranej funkcji; wynik: ranking operatorów
- **random_functions** — testy na zestawie losowo wybranych funkcji; pozwala ocenić ogólność konfiguracji
- **all_functions_global** — testy na wszystkich 21 funkcjach; wynik: globalne zestawienie rankingowe

Wyniki każdego eksperymentu trafiają do data/output/tests/<nazwa_eksperymentu>/:
- report.md — czytelne podsumowanie tekstowe
- results.csv — surowe wyniki
- operator_ranking.csv — ranking operatorów
- summary.json — zagregowane metryki
- plots/ — wykresy rankingowe i porównawcze

---

## Wyniki i wizualizacja

Po każdym uruchomieniu algorytmu (z GUI lub eksperymentu) zapisywane są:

- full_results.json — pełne wyniki wszystkich runów
- full_history.csv — historia wartości best/avg/worst dla każdej epoki
- runs_summary.csv — podsumowanie statystyk końcowych

Generowane wykresy:
- *Zbieżność* — best / avg / worst w kolejnych epokach
- *Rozkład fitness* — histogram końcowy populacji
- *Rzut 2D* — krajobraz funkcji z trajektorią najlepszego osobnika
- *Powierzchnia 3D* — krajobraz funkcji z zaznaczonym optimum
- *Rankingi operatorów* — wykresy słupkowe i rankingowe z eksperymentów

Wyniki eksportowane są w formatach *JSON* i *CSV*, co umożliwia dalszą analizę poza aplikacją.

---

## Workflow git

# 1. Aktualizacja main
git checkout main
git pull origin main

# 2. Nowy branch na zmianę
git checkout -b feature/nazwa-tematu

# 3. Commit i push
git add .
git commit -m "Add: krótki opis zmiany"
git push -u origin feature/nazwa-tematu

# 4. Pull Request na GitHubie: feature/... → main
#    W opisie PR: co zrobiono + jak przetestować

---

## Zasady repozytorium

- *Nie commitujemy:* .venv/, __pycache__/, data/output/, plików IDE (.vscode/, .idea/)
- main zawsze musi być uruchamialny
- Każda większa zmiana przechodzi przez Pull Request
- Każdy PR powinien zawierać opis: co zrobiono i jak przetestować

---

## Dokumentacja

- docs/architecture/overview.md — architektura, moduły i zasady zależności
- docs/architecture/generic_algorithm_desc.md — szczegółowy opis algorytmu GA
- docs/architecture/selection_methods.md — opis i analiza metod selekcji
- docs/architecture/crossover_methods.md — opis metod krzyżowania
- docs/architecture/mutation_methods.md — opis metod mutacji
- docs/todo/plan.md — plan budowy projektu przez branche
- docs/notes/ — notatki zespołu
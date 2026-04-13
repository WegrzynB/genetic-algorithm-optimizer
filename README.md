# README.md

## GA Optimizer (Python + Tkinter)

Projekt implementuje algorytm genetyczny (GA) do optymalizacji (min/max) funkcji wielu zmiennych, z GUI w Tkinter, zapisem wyników i wykresami w matplotlib/seaborn. Operatory GA oraz logika są implementowane od zera (dopuszczalne: numpy, matplotlib, seaborn, pandas).


## Wymagania

- Python 3.12 (lub ustalona wersja w zespole)
- Git

## Instalacja

1) Klonowanie repo:
- `git clone <URL_REPO>`
- `cd <NAZWA_REPO>`

2) Wirtualne środowisko:

Windows (PowerShell):
- `py -3.12 -m venv .venv`
- `.venv\Scripts\Activate.ps1`

Windows (cmd):
- `py -3.12 -m venv .venv`
- `.venv\Scripts\activate`

Linux/macOS:
- `python3.12 -m venv .venv`
- `source .venv/bin/activate`

3) Instalacja zależności:
- `pip install -r requirements.txt`

## Uruchomienie GUI

- `python scripts/run_gui.py`


### Uruchomienie eksperymentów

1. Otwórz `src/ga_optimizer/experiments/experiment_config.py`
2. Ustaw `ACTIVE_EXPERIMENT_NAME` na wybrany preset:
    `"single_function_operator_search_default"` — szukanie operatorów dla jednej funkcji
    `"random_functions_default"` — testy na losowych funkcjach
    `"all_functions_global_default"` — testy na wszystkich funkcjach globalnie
3. Dla testów jednofunkcyjnych ustaw też `TARGET_PROBLEM_NAME` (np. `"Rosenbrock"`)
4. Uruchom: `python scripts/run_experiment.py`
5. Wyniki trafiają do `data/output/tests/` — zacznij od `report.md`


## Struktura projektu

Wypisanie struktury (Windows):
- `tree /F /A`

Główne katalogi:
- src/ga_optimizer/` — kod aplikacji
    `core/` — rdzeń GA (populacja, pętla epok, pipeline)
    `operators/` — operatory GA i dispatchery
    `config/` — schemat konfiguracji, presety, walidacja
    `problems/` — funkcje testowe i rejestr problemów
    `gui/` — interfejs Tkinter (widoki, stan UI)
    `experiments/` — skrypty benchmarkowe i agregacja wyników
    `visualization/` — wykresy matplotlib/seaborn
    `io/` — zapis wyników (JSON/CSV)
    `utils/` — helpery narzędziowe
    `scripts/` — skrypty uruchomieniowe (`run_gui.py`, `run_experiment.py`)
    `data/output/` — wyniki runów (nie commitujemy do repo)
    `docs/` — dokumentacja projektu


## Workflow git (skrót)

1) Aktualizacja main:
- `git checkout main`
- `git pull origin main`

2) Branch na zmianę:
- `git checkout -b feature/nazwa-tematu`

3) Commit i push:
- `git add .`
- `git commit -m "Add: krótki opis"`
- `git push -u origin feature/nazwa-tematu`

4) Pull Request na GitHubie:
- `feature/...` → `main`
- w PR wpisz: co zrobiono + jak przetestować

## Zasady repo

- Nie commitujemy: `.venv/`, `__pycache__/`, `data/output/`, plików IDE.
- `main` ma być zawsze uruchamialny.
- Każda większa zmiana idzie przez Pull Request.

## Dokumentacja

- `docs/architecture/overview.md` — architektura i zależności modułów
- `docs/todo/plan.md` — instrukcja budowy projektu przez branche
- `docs/notes/` — notatki zespołu

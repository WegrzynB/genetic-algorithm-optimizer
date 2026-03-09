# Plan budowy projektu przez branche (instrukcja krok po kroku)

Ten dokument opisuje **kolejność branchy**, co dokładnie na nich powstaje, jak to **uruchomić/sprawdzić** oraz kiedy można robić merge do `main`.

---

## Zasady ogólne (stosujemy zawsze)

- `main` ma się uruchamiać po każdym merge.
- Jeden branch = jeden spójny temat (mały zakres).
- Branch tworzymy zawsze z aktualnego `main`:
  - `git checkout main && git pull`
  - `git checkout -b feature/...`
- Po merge: aktualizujemy lokalny `main` i usuwamy lokalny branch.

---

## Krok 0 — `docs/plan.md` i porządek startowy

### Branch: `docs/plan-initial`
**Co robimy**
- Uzupełniamy `docs/architecture/overview.md` (krótko: moduły i zależności).
- Uzupełniamy `docs/todo/plan.md` (ten plik).
- Uzupełniamy `README.md` (instalacja, uruchomienie GUI).

**Jak testować**
- Brak kodu do uruchomienia; sprawdzić czy `README.md` ma polecenia i czy struktura repo się zgadza.

**Merge warunek**
- Dokumenty istnieją i są spójne z aktualną strukturą katalogów.

---

## Krok 1 — uruchamialny szkielet aplikacji

### Branch: `feature/app-entrypoint`
**Co robimy**
- `src/ga_optimizer/main.py` uruchamia GUI.
- `src/ga_optimizer/gui/app.py` tworzy `tk.Tk()` i startuje pętlę `mainloop()`.
- `src/ga_optimizer/gui/views/main_window.py` pokazuje minimalne okno (header + placeholder log).

**Jak testować**
- Z terminala w repo:
  - uruchom `python -m src.ga_optimizer.main` jeśli macie taki sposób, albo
  - uruchom `python -m ga_optimizer.main` jeśli `src` jest w `PYTHONPATH`, albo
  - uruchom `python scripts/run_gui.py`.
- Oczekiwane: okno się otwiera i nie ma błędów.

**Merge warunek**
- GUI startuje na czystym repo (po `pip install -r requirements.txt`).

---

## Krok 2 — GUI: layout i panele (bez logiki GA)

### Branch: `feature/gui-layout`
**Co robimy**
- W `main_window.py` układ docelowy:
  - lewy panel konfiguracji,
  - prawy panel wyników/logów,
  - panel wykresów (placeholder).
- Dodajemy podstawowe widoki:
  - `views/config_panel.py`
  - `views/run_panel.py`
  - `views/results_panel.py`
  - `views/plots_panel.py`
- Widoki nie wywołują GA, tylko prezentują UI.

**Jak testować**
- Uruchom GUI.
- Sprawdź: widoczne panele, pola da się edytować, przyciski klikają (na razie tylko logują do okna).

**Merge warunek**
- Brak importów z `core/operators` w warstwie widoku (na razie czysty GUI).

---

## Krok 3 — GUI: widgety i walidacja pól (lokalnie)

### Branch: `feature/gui-widgets-validation`
**Co robimy**
- W GUI:
  - w pola numeryczne jest zablokowana możliwość wpisywania innych wartości niż liczby, albo jest to jakoś dobrze i szybko weryfikowane,
  - błędy pokazujemy w messagebox po kliknięciu w "Start".

**Jak testować**
- Uruchom GUI.
- Wpisz błędne dane (np. tekst w polu liczbowym, wartości ujemne).
- Oczekiwane: pole sygnalizuje błąd lub status bar pokazuje komunikat; Start nie przechodzi dalej.

**Merge warunek**
- Złe dane są blokowane lub jednoznacznie sygnalizowane.

---

## Krok 4 — konfiguracja (jedno źródło prawdy)

### Branch: `feature/config-model`
**Co robimy**
- `config/defaults.py`: sensowne domyślne wartości.
- `config/schema.py`: struktura konfiguracji (pola, typy).
- `config/validators.py`: walidacja zakresów i zależności.
- `config/presets.py`: 2–3 presety (np. szybki/standard/dokładny).

**Jak testować**
- W Python REPL / krótkim skrypcie:
  - tworzysz config z defaultów,
  - podmieniasz kilka pól,
  - validator zwraca OK / błąd.
- Dodatkowo: GUI odpala walidację configu po kliknięciu Start (na razie bez uruchamiania GA).

**Merge warunek**
- Da się zbudować config z GUI i walidacja działa spójnie.

---

## Krok 5 — problemy i rejestr problemów (dla GUI)

### Branch: `feature/problems-registry`
**Co robimy**
- `problems/base_problem.py`: interfejs problemu (nazwa, bounds, evaluate()).
- `problems/registry.py`: rejestr dostępnych problemów.
- `problems/benchmark_functions/rosenbrock.py` + ewentualnie `sphere.py`, `rastrigin.py` (po jednym pliku na funkcję).

**Jak testować**
- Krótki test manualny:
  - import registry,
  - pobierz problem,
  - policz `evaluate()` dla przykładowego wektora.
- GUI:
  - combobox problemów ładuje listę z `registry` (bez GA).

**Merge warunek**
- GUI widzi listę problemów z rejestru i nie ma “hardcode” w combobox.

---

## Krok 6 — core: reprezentacje i dekodowanie (bez pętli epok)

### Branch: `feature/core-representation`
**Co robimy**
- `core/chromosome.py`: struktura genotypu (bity/geny).
- `core/encoding.py` i `core/decoding.py`: mapowanie genotyp → wartości zmiennych (z uwzględnieniem bounds).
- `core/individual.py`: osobnik (chromosom + cached fitness).
- `core/population.py`: lista osobników + inicjalizacja populacji.

**Jak testować**
- Skrypt w `scripts/` typu `scripts/run_experiment.py` (tymczasowo) lub mały snippet:
  - stwórz populację,
  - zdekoduj kilka osobników,
  - sprawdź, że wartości mieszczą się w bounds.
- Minimum test jednostkowy: `decoding` nigdy nie wychodzi poza zakres.

**Merge warunek**
- Reprezentacje działają bez engine i są deterministyczne przy ustawionym seed.

---

## Krok 7 — core: evaluator + fitness

### Branch: `feature/core-evaluator`
**Co robimy**
- `core/evaluator.py`: wyliczanie wartości funkcji celu dla osobnika.
- `core/fitness.py`: mapowanie min/max do fitness (np. unifikacja porządku).
- Wspólny format “wyniku osobnika”: raw objective i fitness.

**Jak testować**
- Manualnie:
  - problem z registry,
  - populacja,
  - evaluator liczy fitness,
  - porównaj kilka wartości (czy sensownie rośnie/maleje zgodnie z trybem min/max).
- Minimum test jednostkowy: min/max daje odwrócony porządek rankingowy.

**Merge warunek**
- Na tej warstwie nadal brak operatorów; działa sama ocena.

---

## Krok 8 — operators v1: kontrakt i selekcja (pierwsza)

### Branch: `feature/operators-selection-v1`
**Co robimy**
- Kontrakt funkcji selekcji (np. `select(population, k, rng, ...) -> list[Individual]`).
- Implementacje w `operators/selection/`:
  - `best.py`
  - `tournament.py`
  - `roulette.py` (jeśli fitness dodatni lub znormalizowany — ująć w kodzie).

**Jak testować**
- Testy:
  - `best` zawsze zwraca najlepszych,
  - `tournament` zwraca poprawną liczbę osobników,
  - `roulette` nie wywala błędów dla skrajnych przypadków.
- Manualnie:
  - uruchom selekcję na małej populacji o znanych fitness.

**Merge warunek**
- Selekcje działają na “gołych” populacjach i mają testy jednostkowe.

---

## Krok 9 — operators v1: krzyżowanie

### Branch: `feature/operators-crossover-v1`
**Co robimy**
- Kontrakt krzyżowania (np. `crossover(parent1, parent2, rng, ...) -> (child1, child2)`).
- Implementacje:
  - `one_point.py`
  - `two_point.py`
  - `uniform.py`
  - `granular.py` (jeśli macie w wymaganiach własny wariant).

**Jak testować**
- Testy:
  - dzieci mają identyczną długość chromosomu,
  - geny pochodzą tylko od rodziców,
  - brak out-of-range na punktach cięcia.
- Manualnie:
  - na krótkim chromosomie wydrukuj rodziców i dzieci.

**Merge warunek**
- Krzyżowanie jest czyste i nie zależy od engine.

---

## Krok 10 — operators v1: mutacje + inwersja + elitaryzm

### Branch: `feature/operators-mutation-v1`
**Co robimy**
- Mutacje:
  - `mutation/one_point.py`
  - `mutation/two_point.py`
  - `mutation/edge.py`
- `operators/inversion.py`
- `operators/elitism.py`

**Jak testować**
- Testy:
  - mutacja zmienia geny zgodnie z definicją i nie psuje długości,
  - inwersja odwraca fragment,
  - elitaryzm zawsze przenosi top-N.
- Manualnie:
  - na znanym chromosomie pokaż efekt mutacji/inwersji.

**Merge warunek**
- Operatory nie ingerują w GUI; działają na obiektach core.

---

## Krok 11 — core: lifecycle + engine (pętla epok)

### Branch: `feature/core-engine-loop`
**Co robimy**
- `core/lifecycle.py`: składanie operatorów w generację (select → crossover → mutation → inversion → elitism).
- `core/termination.py`: warunki stopu (liczba epok + opcjonalnie brak poprawy).
- `core/engine.py`: pętla epok, historia best/avg/worst, pomiar czasu.

**Jak testować**
- Skrypt `scripts/run_experiment.py`:
  - wybierz problem,
  - uruchom engine na małych parametrach,
  - wypisz best fitness i kilka punktów historii.
- Sprawdź:
  - engine zwraca wynik i historię,
  - wynik jest powtarzalny przy seed,
  - brak crashy na różnych operatorach.

**Merge warunek**
- Engine działa bez GUI i daje wynik na co najmniej jednym problemie.

---

## Krok 12 — IO: zapis runów

### Branch: `feature/io-results`
**Co robimy**
- `io/results_writer.py`, `io/json_export.py`, `io/csv_export.py`, `io/serializers.py`.
- Folder runa:
  - `data/output/runs/<timestamp>_<id>/config.json`
  - `metrics.json`
  - `history.csv`

**Jak testować**
- Po uruchomieniu `scripts/run_experiment.py`:
  - sprawdź, że folder runa powstał,
  - pliki mają sensowną zawartość,
  - `history.csv` ma tyle wierszy, ile epok.

**Merge warunek**
- Zapis jest deterministyczny i nie nadpisuje poprzednich runów.

---

## Krok 13 — visualization: wykres zbieżności + zapis

### Branch: `feature/visualization-convergence`
**Co robimy**
- `visualization/convergence_plots.py` generuje wykres best/avg/worst.
- Zapisuje wykres do folderu runa `plots/`.
- `visualization/plot_styles.py` trzyma wspólne ustawienia.

**Jak testować**
- Po runie:
  - w `plots/` jest PNG,
  - wykres ma podpisane osie i legendę,
  - wartości zgadzają się z `history.csv`.

**Merge warunek**
- Wykres powstaje bez udziału GUI (na danych z runa).

---

## Krok 14 — integracja GUI ↔ engine

### Branch: `feature/gui-run-integration`
**Co robimy**
- `gui/controllers/run_controller.py` buduje config, uruchamia engine i odbiera wynik.
- GUI:
  - Start uruchamia obliczenia,
  - Stop przerywa (na początek: flaga w engine sprawdzana co epokę),
  - Wynik trafia do `results_panel` i do logu.

**Jak testować**
- Z GUI:
  - ustaw parametry, Start,
  - obserwuj log (np. co N epok),
  - po zakończeniu widzisz best wynik i czas.
- Sprawdź, że UI nie zawiesza się (jeśli jest wątek/after, upewnić się że aktualizacja UI jest bezpieczna).

**Merge warunek**
- Użytkownik może wykonać pełny run z GUI i zobaczyć rezultat.

---

## Krok 15 — GUI: wykresy i przycisk “Zapisz”

### Branch: `feature/gui-results-and-plots`
**Co robimy**
- `results_panel` pokazuje best/avg/worst, czas, parametry runa.
- `plots_panel` pokazuje wykres (na początek: wczytany z PNG z folderu runa).
- Przycisk “Zapisz wynik” w GUI wywołuje `results_writer`.

**Jak testować**
- Z GUI: uruchom run, kliknij “Zapisz”, sprawdź folder runa i obraz wykresu.
- Upewnij się, że zapis nie blokuje UI (jeśli trzeba: zapis po zakończeniu runa).

**Merge warunek**
- Wyniki i wykresy są dostępne w GUI oraz zapisują się do `data/output`.

---

## Krok 16 — eksperymenty (opcjonalne, ale wspierają sprawozdanie)

### Branch: `feature/experiments-benchmark`
**Co robimy**
- `scripts/batch_benchmark.py` odpala serię runów dla listy konfiguracji (np. różne selekcje/mutacje/krzyżowania).
- `experiments/metrics.py` i `aggregations.py` tworzą podsumowanie (CSV/JSON).
- `visualization/comparison_plots.py` generuje wykresy porównawcze.

**Jak testować**
- Uruchom `python scripts/batch_benchmark.py`.
- Sprawdź:
  - powstało kilka folderów runów,
  - jest summary (np. `data/output/summaries/...`),
  - wykres porównawczy istnieje i ma sens.

**Merge warunek**
- Benchmark nie wymaga ręcznej edycji kodu (konfiguracje z pliku lub listy w skrypcie).

---

## Krok 17 — rozszerzenia operatorów (w dowolnej kolejności)

### Branch template: `feature/operators-<typ>-<nazwa>`
**Co robimy**
- Dodajemy nowe metody selekcji/krzyżowania/mutacji bez ruszania engine.
- Aktualizujemy mapowanie w config/presetach i widoczność w GUI.

**Jak testować**
- Test jednostkowy dla operatora.
- Run na małej konfiguracji, sprawdzenie że działa i nie psuje historii.

**Merge warunek**
- Operator jest wybieralny konfiguracją i ma test.

---

## Krok 18 — stabilizacja

### Branch: `refactor/stabilization`
**Co robimy**
- Porządki importów, spójne nazwy parametrów.
- Minimalne testy integracyjne:
  - uruchomienie engine na 2–3 problemach,
  - kilka konfiguracji operatorów.
- Upewnienie się, że `__pycache__` i outputy nie są w repo.

**Jak testować**
- `python scripts/run_gui.py`
- `python scripts/run_experiment.py`
- uruchomienie kilku runów i sprawdzenie folderów output.

**Merge warunek**
- `main` uruchamia GUI i wykonuje run bez ręcznych poprawek.
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

## Krok 0 — `docs/plan.md` i porządek startowy (Ukończono)

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

## Krok 1 — uruchamialny szkielet aplikacji (Ukończono)

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

## Krok 2 — GUI: layout i panele (bez logiki GA) (Ukończono)

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

## Krok 3 — GUI: widgety i walidacja pól (lokalnie) (Ukończono)

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

## Krok 4 — model konfiguracji i katalog funkcji (jedno źródło prawdy) (Ukończono)

### Branch: `feature/config-model`

**Co robimy**
- Przenosimy specyfikacje pól i domyślne wartości z GUI do `config/`.
- Dodajemy:
  - `config/schema.py` — struktura konfiguracji, specyfikacje pól i osobne stałe dla parametrów selekcji / krzyżowania / mutacji,
  - `config/defaults.py` — budowanie domyślnego configu,
  - `config/validators.py` — składanie configu z GUI i walidacja.
- `config/presets.py` na razie pomijamy.
- Dodajemy w `problems/` katalog funkcji testowych jako jedyne źródło informacji o funkcjach dostępnych w GUI.
- GUI ma tylko trzymać `tk.Variable`, budować formularz z configu i składać config po kliknięciu `Start`.
- Po wyborze funkcji GUI automatycznie podmienia dedykowany zakres i domyślną liczbę zmiennych; jeśli funkcja ma stałą liczbę zmiennych, pole jest blokowane.
- Parametry metod mają działać automatycznie na podstawie aktualnie wybranej metody selekcji / krzyżowania / mutacji.
- Poprawiamy też scroll notebooka, żeby działał nad całym obszarem zakładki, także nad `Entry`, `Combobox` itd.

**Jak testować**
- W REPL:
  - tworzysz config z `build_default_config()`,
  - zmieniasz kilka pól,
  - uruchamiasz validator i dostajesz `OK` albo listę błędów.
- W GUI:
  - wybierasz funkcję,
  - sprawdzasz automatyczną zmianę zakresu i liczby zmiennych,
  - klikasz `Start` i GUI waliduje już złożony config.

**Merge warunek**
- GUI potrafi złożyć spójny config z jednego źródła prawdy, a walidacja działa tak samo dla GUI i dla kodu.

---

## Krok 5 — pula problemów i przygotowanie pod dalszy pipeline (Ukończono)

### Branch: `feature/problem-pool-pipeline-ready`

**Co robimy**
- Rozszerzamy pulę problemów w `src/ga_optimizer/problems/`.
- Porządkujemy warstwę problemów tak, żeby była gotowa do użycia przez dalsze moduły projektu.
- Dodajemy / porządkujemy:
  - plik z implementacjami funkcji problemowych,
  - katalog / rejestr problemów dostępnych w aplikacji,
  - wspólny sposób pobierania problemu po nazwie,
  - placeholdery funkcji i klas, które będą później wywoływane przez dalsze etapy programu.
- Przygotowujemy przepływ tak, żeby po kliknięciu `Start` aplikacja nie kończyła się tylko na walidacji, ale wywoływała już kolejną funkcję w pipeline.
- Na tym etapie ta dalsza funkcja może być jeszcze placeholderem, ale ma już mieć poprawny podpis, argumenty i typ zwracanych danych.
- Nowe problemy dodajemy już tylko przez warstwę `problems/`, bez hardcode w GUI.
- Robimy to tak, żeby kolejne kroki mogły działać już na jednym, spójnym modelu problemu.

**Jak testować**
- W konsoli / prostym skrypcie:
  - pobierz problem z rejestru,
  - wywołaj jego funkcję dla przykładowego wektora,
  - wypisz wynik przez `print()`.
- Sprawdź też:
  - czy rejestr zwraca listę dostępnych problemów,
  - czy da się pobrać pojedynczy problem po nazwie,
  - czy placeholder dalszego etapu przyjmuje config/problem i zwraca obiekt w oczekiwanym formacie.
- W GUI:
  - wybierz problem,
  - kliknij `Start`,
  - sprawdź, czy po walidacji wywoływana jest już kolejna funkcja, a nie tylko sam placeholder statusu.

**Merge warunek**
- Problemy są ładowane z jednej warstwy `problems/`.
- GUI nie trzyma listy problemów na sztywno.
- Po kliknięciu `Start` przepływ przechodzi o krok dalej i wywołuje przygotowaną funkcję pipeline, nawet jeśli jej logika jest jeszcze tymczasowa.

---

## Krok 6 — core: reprezentacje i dekodowanie (bez pętli epok) (Ukończono)

### Branch: `feature/core-representation`
**Co robimy**
- `core/chromosome.py`: struktura genotypu (bity/geny).
- `core/encoding.py` i `core/decoding.py`: mapowanie genotyp → wartości zmiennych (z uwzględnieniem bounds).
- `core/individual.py`: osobnik (chromosom + cached fitness).
- `core/population.py`: lista osobników + inicjalizacja populacji.
- Przygotowujemy te moduły jako samodzielną warstwę logiki, jeszcze bez integracji z GUI.

**Jak testować**
- W prostym skrypcie albo w konsoli:
  - stwórz populację,
  - zdekoduj kilka osobników,
  - wypisz wyniki przez `print()`,
  - sprawdź, że wartości mieszczą się w bounds.
- Minimum:
  - dekodowanie nigdy nie wychodzi poza zakres,
  - wynik jest powtarzalny przy ustawionym seed.

**Merge warunek**
- Reprezentacje działają bez engine i bez GUI.
- Moduły mają czytelny kontrakt i nadają się do użycia w kolejnych krokach.

---

## Krok 7 — core: evaluator + fitness

### Branch: `feature/core-evaluator`
**Co robimy**
- `core/evaluator.py`: wyliczanie wartości funkcji celu dla osobnika.
- `core/fitness.py`: mapowanie min/max do fitness.
- Ustalamy wspólny format wyniku osobnika: raw objective i fitness.
- Spinamy evaluator z aktualną warstwą problemów z `problems/`.

**Jak testować**
- W konsoli / prostym skrypcie:
  - pobierz problem,
  - przygotuj przykładowe wektory lub osobniki,
  - policz objective i fitness,
  - wypisz wyniki przez `print()`.
- Sprawdź ręcznie:
  - czy ranking ma sens,
  - czy min/max działa zgodnie z oczekiwaniem.

**Merge warunek**
- Działa sama ocena osobników.
- Warstwa oceny jest niezależna od GUI i operatorów.

---

## Krok 8 — operators v1: kontrakt i selekcja

### Branch: `feature/operators-selection-v1`
**Co robimy**
- Definiujemy kontrakt funkcji selekcji.
- Implementacje w `operators/selection/`:
  - `best.py`
  - `tournament.py`
  - `roulette.py`
- Robimy to tak, żeby selekcja działała na aktualnych obiektach core i dało się ją później łatwo podpiąć do lifecycle.

**Jak testować**
- W konsoli / prostym skrypcie:
  - przygotuj małą populację o znanych fitness,
  - uruchom każdą metodę selekcji,
  - wypisz wyniki przez `print()`.
- Sprawdź ręcznie:
  - `best` zwraca najlepszych,
  - `tournament` zwraca poprawną liczbę osobników,
  - `roulette` działa dla prostych przypadków i się nie wywala.

**Merge warunek**
- Selekcje działają na “gołych” populacjach.
- Każda metoda ma spójne wejście i wyjście.

---

## Krok 9 — operators v1: krzyżowanie

### Branch: `feature/operators-crossover-v1`
**Co robimy**
- Definiujemy kontrakt krzyżowania.
- Implementacje:
  - `one_point.py`
  - `two_point.py`
  - `uniform.py`
  - `granular.py`
- Przygotowujemy operator tak, żeby zwracał poprawne dzieci i dawał się później wpiąć w lifecycle bez przeróbek kontraktu.

**Jak testować**
- W konsoli / prostym skrypcie:
  - przygotuj krótkie chromosomy rodziców,
  - wykonaj krzyżowanie,
  - wypisz rodziców i dzieci przez `print()`.
- Sprawdź ręcznie:
  - dzieci mają poprawną długość,
  - geny pochodzą od rodziców,
  - nie ma błędów na punktach cięcia.

**Merge warunek**
- Krzyżowanie działa samodzielnie.
- Implementacje nie zależą od engine ani GUI.

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
- Domykamy podstawowy zestaw operatorów potrzebny do złożenia pełnego przebiegu generacji.

**Jak testować**
- W konsoli / prostym skrypcie:
  - uruchom mutację i inwersję na znanym chromosomie,
  - wypisz wynik przed i po przez `print()`,
  - sprawdź elitaryzm na małej populacji.
- Sprawdź ręcznie:
  - długość chromosomu się nie psuje,
  - inwersja odwraca właściwy fragment,
  - elitaryzm przenosi najlepszych.

**Merge warunek**
- Operatory działają na obiektach core.
- Warstwa operatorów jest gotowa do spięcia w lifecycle.

---

## Krok 11 — core: lifecycle + engine (pętla epok)

### Branch: `feature/core-engine-loop`
**Co robimy**
- `core/lifecycle.py`: składanie operatorów w generację (select → crossover → mutation → inversion → elitism).
- `core/termination.py`: warunki stopu.
- `core/engine.py`: pętla epok, historia best/avg/worst, pomiar czasu.
- Składamy w końcu działający pipeline obliczeń, ale jeszcze bez pełnej integracji GUI.

**Jak testować**
- W skrypcie lub konsoli:
  - wybierz problem,
  - uruchom engine na małych parametrach,
  - wypisz kilka epok i końcowy wynik przez `print()`.
- Sprawdź:
  - engine zwraca wynik i historię,
  - wynik jest powtarzalny przy seed,
  - brak crashy na różnych operatorach.

**Merge warunek**
- Engine działa bez GUI.
- Da się wykonać pełny run na co najmniej jednym problemie.

---

## Krok 12 — IO: zapis runów

### Branch: `feature/io-results`
**Co robimy**
- `io/results_writer.py`, `io/json_export.py`, `io/csv_export.py`, `io/serializers.py`.
- Folder runa:
  - `data/output/runs/<timestamp>_<id>/config.json`
  - `metrics.json`
  - `history.csv`
- Przygotowujemy trwały zapis wyników tak, żeby później GUI tylko korzystało z gotowej warstwy IO.

**Jak testować**
- Po uruchomieniu prostego runa:
  - wypisz ścieżkę zapisu przez `print()`,
  - sprawdź, że folder runa powstał,
  - sprawdź zawartość plików.
- Minimum:
  - `history.csv` ma tyle wierszy, ile epok,
  - zapis nie nadpisuje poprzednich wyników.

**Merge warunek**
- Zapis działa niezależnie od GUI.
- Format plików jest spójny i gotowy do dalszego użycia.

---

## Krok 13 — visualization: wykres zbieżności + zapis

### Branch: `feature/visualization-convergence`
**Co robimy**
- `visualization/convergence_plots.py` generuje wykres best/avg/worst.
- Zapisuje wykres do folderu runa `plots/`.
- `visualization/plot_styles.py` trzyma wspólne ustawienia.
- Przygotowujemy wizualizację jako osobną warstwę nad zapisanymi danymi.

**Jak testować**
- Po runie:
  - wypisz lokalizację wykresu przez `print()`,
  - sprawdź, że PNG istnieje,
  - porównaj dane z `history.csv`.
- Minimum:
  - wykres ma sensowne osie, legendę i wartości zgodne z historią.

**Merge warunek**
- Wykres powstaje bez udziału GUI.
- Moduł działa na danych z runa lub historii zwróconej przez engine.

---

## Krok 14 — integracja GUI ↔ engine

### Branch: `feature/gui-run-integration`
**Co robimy**
- `gui/controllers/run_controller.py` buduje config, uruchamia engine i odbiera wynik.
- GUI:
  - Start uruchamia obliczenia,
  - Stop przerywa,
  - wynik trafia do `results_panel` i do logu.
- Na tym etapie dopiero spinamy gotową logikę z interfejsem.

**Jak testować**
- Najpierw upewnij się, że sam engine działa poprawnie poza GUI.
- Potem z GUI:
  - ustaw parametry,
  - kliknij Start,
  - obserwuj komunikaty i końcowy wynik.
- Sprawdź:
  - czy przepływ od GUI do engine działa,
  - czy wynik wraca do GUI,
  - czy UI nie zawiesza się.

**Merge warunek**
- Użytkownik może wykonać pełny run z GUI.
- GUI korzysta z gotowych modułów logiki, a nie zawiera ich kopii.

---

## Krok 15 — GUI: wyniki, wykresy i przycisk “Zapisz”

### Branch: `feature/gui-results-and-plots`
**Co robimy**
- `results_panel` pokazuje best/avg/worst, czas, parametry runa.
- `plots_panel` pokazuje wykres.
- Przycisk “Zapisz wynik” w GUI wywołuje warstwę `io`.
- Domykamy prezentację wyników w GUI na bazie wcześniej przygotowanej logiki, IO i wizualizacji.

**Jak testować**
- Najpierw sprawdź dane i zapis po stronie logiki / plików.
- Potem z GUI:
  - uruchom run,
  - kliknij “Zapisz”,
  - sprawdź folder runa i obraz wykresu.
- Sprawdź:
  - czy GUI poprawnie pokazuje wyniki,
  - czy wykres odpowiada historii runa,
  - czy zapis działa bez ręcznych poprawek.

**Merge warunek**
- Wyniki i wykresy są dostępne w GUI.
- GUI korzysta z gotowych danych i zapisuje je do `data/output`.

---

## Krok 16 — eksperymenty i porównania konfiguracji

### Branch: `feature/experiments-benchmark`
**Co robimy**
- `scripts/batch_benchmark.py` odpala serię runów dla listy konfiguracji.
- `experiments/metrics.py` i `aggregations.py` zbierają i agregują wyniki.
- `visualization/comparison_plots.py` generuje wykresy porównawcze.
- Przygotowujemy tę warstwę tak, żeby dało się łatwo porównywać operatory, ustawienia i problemy bez ręcznego grzebania w kodzie.

**Jak testować**
- Uruchom `python scripts/batch_benchmark.py`.
- Sprawdź:
  - czy powstało kilka folderów runów,
  - czy zapisują się podsumowania,
  - czy da się wypisać zagregowane wyniki przez `print()`,
  - czy wykres porównawczy istnieje i ma sens.
- Na tym etapie nie trzeba jeszcze spinać tego z GUI.

**Merge warunek**
- Benchmark działa z poziomu skryptu.
- Da się uruchomić serię eksperymentów bez ręcznej edycji logiki wewnątrz modułów.

---

## Krok 17 — rozszerzenia operatorów i problemów

### Branch template: `feature/extensions-<obszar>-<nazwa>`
**Co robimy**
- Dodajemy nowe metody selekcji / krzyżowania / mutacji albo nowe problemy.
- Aktualizujemy odpowiednie mapowania w configu i rejestrach.
- Trzymamy się istniejących kontraktów, żeby nowe elementy dało się podpiąć bez przerabiania engine.
- Jeśli trzeba, uzupełniamy też warstwę eksperymentów i konfiguracji o nowe opcje.

**Jak testować**
- W konsoli / prostym skrypcie:
  - uruchom nowy operator albo nowy problem,
  - wypisz wyniki przez `print()`,
  - sprawdź, że działa z aktualnym pipeline.
- Potem zrób mały run na jednej konfiguracji i sprawdź, czy historia i wynik wyglądają sensownie.

**Merge warunek**
- Nowy element jest wybieralny z konfiguracji.
- Nie psuje istniejącego pipeline i działa w ramach obecnych kontraktów.

---

## Krok 18 — stabilizacja i porządki końcowe

### Branch: `refactor/stabilization`
**Co robimy**
- Porządki importów, nazw, komentarzy i zależności między modułami.
- Usuwamy zbędne fragmenty tymczasowe i placeholdery, które nie są już potrzebne.
- Sprawdzamy spójność warstw:
  - `config`,
  - `problems`,
  - `core`,
  - `operators`,
  - `io`,
  - `visualization`,
  - `gui`.
- Upewniamy się, że `__pycache__`, outputy i śmieci robocze nie trafiają do repo.

**Jak testować**
- Uruchom:
  - `python scripts/run_gui.py`
  - `python scripts/run_experiment.py`
  - `python scripts/batch_benchmark.py`
- Sprawdź:
  - czy pełny run działa,
  - czy zapis wyników działa,
  - czy benchmark działa,
  - czy GUI korzysta z tej samej logiki co skrypty.

**Merge warunek**
- `main` uruchamia GUI i wykonuje pełny run bez ręcznych poprawek.
- Projekt jest spójny, a przepływ od configu do wyniku działa end-to-end.


                                  **NOWA WERSJA**

# Krok 7 — ocena osobników (objective + fitness)

### Branch: `feature/core-evaluation`

### Co robimy
1. Tworzymy moduł odpowiedzialny za **liczenie wartości funkcji celu i fitnessu**.
2. Dodajemy pliki:
   core/evaluator.py
   core/fitness.py

 **evaluator.py:**
  - przyjmuje osobnika
  - dekoduje jego chromosom
  - wywołuje funkcję problemu

 **fitness.py:**
  - zamienia wartość funkcji celu na fitness
  - obsługuje:
    - minimalizację
    - maksymalizację

Po tym kroku każdy osobnik ma:
  - objective_value
  - fitness

### Testy (czy działa)
W prostym skrypcie:
  1. pobierz problem z `problems/`
  2. stwórz osobnika
  3. zdekoduj chromosom
  4. policz objective
  5. policz fitness
  6. wypisz wynik przez `print()`

Sprawdź:
- czy wynik funkcji jest poprawny
- czy ranking fitness działa

### Merge warunek:
 - evaluator działa bez GUI
 - fitness jest poprawnie liczony

---

# Krok 8 — selekcja osobników

### Branch: `feature/operators-selection`

### Co robimy:
1. Dodajemy operatory selekcji.
   Nowy katalog:
   operators/selection/
   - best.py
   - tournament.py
   - roulette.py

2. Implementujemy:
 - Best selection (best.py) - zwraca najlepszych osobników
 - Tournament selection (tournament.py) -losuje kilka osobników i wybiera najlepszego
 - Roulette selection (roulette.py) - prawdopodobieństwo wyboru zależy od fitness

### Jak testować
W skrypcie:
1. stwórz populację o znanych fitness
2. uruchom selekcję
3. wypisz wybranych osobników

Sprawdź:
 - czy `best` zwraca najlepszych
 - czy `tournament` działa poprawnie
 - czy `roulette` nie powoduje błędów

### Merge warunek
 - każda metoda działa
 - wszystkie mają ten sam kontrakt wejścia/wyjścia

---

# Krok 9 — krzyżowanie

### Branch: `feature/operators-crossover`

### Co robimy
1. Dodajemy operatory krzyżowania:
   operators/crossover/
   - one_point.py
   - two_point.py
   - uniform.py
   - granular.py

 Każdy operator działa tak:
	 rodzic1 + rodzic2
		       ↓
  dziecko1 + dziecko2

### Jak testować
W skrypcie:
1. stwórz dwóch rodziców
2. wykonaj crossover
3. wypisz rodziców i dzieci

Sprawdź:
- długość chromosomu
- czy geny pochodzą od rodziców

### Merge warunek
- krzyżowanie działa bez engine
- nie zmienia długości chromosomu

---

# Krok 10 — mutacja + inwersja + elitaryzm

### Branch: `feature/operators-mutation`

### Co robimy
1. Dodajemy operatory modyfikujące chromosom:

  mutation/
  - one_point.py
  - two_point.py
  - edge.py

  operators/
  - inversion.py
  - elitism.py

 Mutacja: losowa zmiana genów.
 Inwersja: odwrócenie fragmentu chromosomu.
 Elitaryzm: przeniesienie najlepszych osobników do następnej generacji.

### Jak testować
W skrypcie:
1. stwórz chromosom
2. wykonaj mutację
3. wykonaj inwersję
4. wypisz przed i po

Sprawdź:
- długość chromosomu się nie zmienia
- elitaryzm zachowuje najlepszych

### Merge warunek:
operatory działają na obiektach `core`

---

# Krok 11 — lifecycle generacji

### Branch: `feature/core-lifecycle`

### Co robimy
1. Tworzymy logikę **jednej generacji algorytmu**.
   Plik: core/lifecycle.py

  Przepływ generacji:
      populacja
      ↓
      selekcja
      ↓
      krzyżowanie
      ↓
      mutacja
      ↓
      inwersja
      ↓
      elitaryzm
      ↓
      nowa populacja

To jest **jedna epoka GA**.

### Jak testować
W skrypcie:

1. stwórz populację
2. wykonaj lifecycle
3. wypisz nową populację

### Merge warunek
- generacja działa
- populacja nie ulega uszkodzeniu

---

# Krok 12 — engine (pętla epok)

### Branch: `feature/core-engine`

### Co robimy
1. Dodajemy główny silnik algorytmu.
   Plik: core/engine.py
 Engine wykonuje:

	inicjalizacja populacji
	          ↓
        for epoch:
        lifecycle
        evaluator
        zapis historii
	          ↓
	      return wynik

  Historia zawiera:
  - best
  - avg
  - worst

### Jak testować
1. Uruchomić mały run:
    population = 20
    epochs = 30
2. Wypisać:
best fitness

### Merge warunek
- engine działa
- zwraca historię

---

# Krok 13 — zapis wyników

### Branch: `feature/io-results`

### Co robimy
1. Dodajemy zapis runów.
  - Nowy folder: io/
  - Pliki:

	  results_writer.py
	  json_export.py
	  csv_export.py

  Struktura zapisu: data/output/runs/ run_2026_01/
  - config.json
  - metrics.json
  - history.csv

### Jak testować
Po runie:
- sprawdzić czy folder powstał
- sprawdzić czy pliki istnieją

### Merge warunek
- run zapisuje pliki

---

# Krok 14 — wykres zbieżności

### Branch: `feature/visualization`

### Co robimy
1. Dodajemy wykresy.
 - visualization/convergence_plot.py

Wykres przedstawia:
 - best
 - avg
 - worst

Zapis wykresu: plots/convergence.png

### Jak testować
Po runie sprawdzić czy powstał plik PNG.

### Merge warunek
- wykres się generuje

---

# Krok 15 — integracja GUI z engine

### Branch: `feature/gui-engine-integration`

### Co robimy
1. GUI zaczyna uruchamiać algorytm.
  
  Przepływ:
     GUI
      ↓
    config
      ↓
    engine
      ↓
    wynik

Controller: gui/controllers/run_controller.py

### Jak testować
W GUI:
1. ustaw parametry
2. kliknij **Start**

Sprawdzić:
- czy algorytm się uruchamia
- czy wynik wraca do GUI

### Merge warunek
- można wykonać pełny run z GUI

---

# Krok 16 — wyniki w GUI

### Branch: `feature/gui-results`

### Co robimy
GUI pokazuje:
 - best
 - avg
 - worst
 - czas
 - wykres.

Panele:
- results_panel
- plots_panel

### Jak testować
Uruchomić run w GUI i sprawdzić czy dane się pojawiają.

### Merge warunek
- GUI poprawnie pokazuje wyniki

---

# Krok 17 — eksperymenty

### Branch: `feature/experiments`

### Co robimy
1. Dodajemy skrypt do wielu runów.
  - scripts/batch_experiment.py

  Skrypt może uruchamiać np.:
  - 3 problemy
  - 5 konfiguracji
  - 10 powtórzeń

### Jak testować
Uruchomić skrypt i sprawdzić czy powstało wiele runów.

### Merge warunek
- można uruchomić benchmark

---

# Krok 18 — stabilizacja projektu

### Branch: `refactor/stabilization`

### Co robimy

1. Końcowe porządki:
  - poprawa importów
  - poprawa nazw
  - usunięcie debugów
  - aktualizacja README
  - aktualizacja `.gitignore`

2. Sprawdzamy działanie:
  - GUI
  - engine
  - benchmark

### Jak testować
1. Uruchomić:
  - python scripts/run_gui.py
  - python scripts/run_experiment.py
  - python scripts/batch_experiment.py

### Merge warunek
Projekt działa **end-to-end**:
GUI → run → zapis → wykres → wyniki
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

## Krok 0 — `docs/plan.md` i porządek startowy [Bartek] (UKOŃCZONO)

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

## Krok 1 — uruchamialny szkielet aplikacji [Bartek] (UKOŃCZONO)

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

## Krok 2 — GUI: layout i panele (bez logiki GA) [Bartek] (UKOŃCZONO)

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

## Krok 3 — GUI: widgety i walidacja pól (lokalnie) [Bartek] (UKOŃCZONO)

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

## Krok 4 — model konfiguracji i katalog funkcji (jedno źródło prawdy) [Bartek] (UKOŃCZONO)

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

## Krok 5 — pula problemów i przygotowanie pod dalszy pipeline [Bartek, Krystian] (UKOŃCZONO)

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

## Krok 6 — core: reprezentacje i dekodowanie (bez pętli epok) [Paweł] (UKOŃCZONO)

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

# Krok 7 — ocena osobników (objective + fitness) [Kamil] (UKOŃCZONO)

### Branch: `feature/core-evaluation`

### Co robimy
1. Tworzymy moduł odpowiedzialny za **liczenie wartości funkcji celu i fitnessu**.
2. Dodajemy pliki:
   `core/evaluator.py`
   `core/fitness.py`

 **evaluator.py**:
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

# Krok 7.5 — całkowita poprawa kodu, żeby to było czytelne i jakkolwiek użyteczne [Bartek] (UKOŃCZONO)

### Branch: `feature/core-basic-fixes`

### Jak jest obecnie zmieniony kod i jaki jest plan
  - `pipeline/pipeline.py` tworzy słownik odpowiednich parametrów i odpala silnik w `core/engine.py` podając mu ten właśnie słownik (zamiast całego obiektu GAConfig, bo w nim był by problem z dojściem do konkretnych parametrów np. selekcji)
  - `core/engine.py` ma utworzyć populację startową i iterować po epokach, każda jedna epoka jest w `core/lifecycle.py`
  - `core/lifecycle.py` odpowiada za wszystkie zmiany w danej epoce w populacji

### Co robimy

1. Po pierwsze skupmy się na populacji. Skoro tworzymy klasę populacji, to najlepiej byłoby w niej trzymać podstawowe info o niej oraz metody pozwalające na dekodowanie i enkodowanie chromosomów (tym samym możemy usunąć tamte pliki).
2. Skoro tworzymy klasę evaluator, to w niej też możemy wykonywać wszystkie potrzebne operacje, bez konieczności śmiecenia kodem (oczywiście to też można wrzucić do klasy z populacją, ale możemy się wstrzymać). To oczywiście też w jednej klasie w jednym pliku.
3. Dorobię odpowiednie funkcje, które będą odpowiednio dla metody (selekcja itp.) przekierowywać do odpowiedniego pliku i funkcji w `core/lifecycle.py`.
4. Od Kroku 12 trzeba będzie edytować plan (nawet na kroki przed 7, żeby tam dać, że dodajemy mini integracje w engine i lifecycle i ją rozszerzamy)

### Populacja
  Niech klasa zawiera w sobie info o chromosomach (bity, liczba zmiennych, precyzja, chromosomy itp), dekodowanych wartościach itp. Niech posiada metodę, która ją generuje i raz to wykonujemy na początku, metodę zmieniającą chromosomy i aktualizującą odpowiednie rzeczy (też może metodę aktualizującą populację po zmianach wynikających z jakiś operacji, np selekcji).
  Czyli na początku generujemy populację odpowiednią metodą i działamy sobie na chromosomach, zmieniając je, potem aktualizujemy te wszystkie pozostałe rzeczy.


### Ewaluacja
  Niech ta klasa zawiera przy jej budowaniu info o tym jaka jest funkcja, problem itp. i niech robi swoje. Niech ma wbudowane metody wyliczające odpowiednie rzeczy i też żeby w jednej linijce już sobie wszystko wyliczać.
  Nie chcę usuwać tego co już napisałem, ale najlepiej byłoby to też umieścić w klasie populacji.

---

# Krok 8 — selekcja osobników [Kamil]

### Branch: `feature/operators-selection`

### Co robimy

1. Dodaj katalog `operators/selection/`.
2. Implementujemy **różne rodzaje selekcji**.
(Tutaj dodałem metody z wykładu: najgorszych, neutralna tj. beztendencyjna, podwójna turniejowa, stochastyczny dobór uniwersalny. Można jeszcze dodać: stochastyczny dobór resztowy, selekcja Boltzmana.)
Selekcja zwraca listę osobników, którzy będą użyci jako rodzice w następnym etapie algorytmu.

**Jak testować**
- Stwórz populację o znanych fitnessach
- Wykonaj selekcję
- Sprawdź, czy działa

**Merge warunek**
- Selekcja działa poprawnie
- Kontrakt wejścia/wyjścia spójny

---

# Krok 9 — krzyżowanie [Krystian]

### Branch: `feature/operators-crossover`

### Co robimy
1. Dodaj katalog `operators/crossover/`.
2. Implementujemy **różne rodzaje krzyżowań**:
   - losowany punkt podziału chromosomu
   - wymiana fragmentów między rodzicami
   - zachowana długość chromosomu

### Jak testować
1. stwórz dwóch rodziców
2. Wykonaj krzyżowanie
3. Sprawdź, czy długość chromosomu się nie zmienia i geny dzieci pochodzą od rodziców

**Merge warunek**
 - Krzyżowanie działa
  Długość chromosomu dzieci = rodziców

---

# Krok 10 — mutacja [Paweł]

### Branch: `feature/operators-mutation`

### Co robimy
1. Dodaj katalog `operators/mutation/`.
2. Implementujemy **różne rodzaje mutacji**:
   - losowo zmieniany geny w chromosomie
   - wprowadza różnorodność genetyczną

### Jak testować
1. stwórz chromosom
2. wykonaj mutację
3. wypisz chromosom przed i po mutacji

Sprawdź:
- czy długość chromosomu się nie zmienia
- czy przynajmniej jeden gen może się zmienić

### Merge warunek
- mutacja działa poprawnie
- długość chromosomu nie ulega zmianie

---

# Krok 11 - operatory inwersji i elitaryzm:
### Branch: `feature/operators-inversion-elitism`

**Co robimy**
1. Dodaj pliki:
   - `operators/inversion.py` — odwraca fragment chromosomu
   - `operators/elitism.py` — przenosi najlepszych osobników do następnej generacji 
  
**Jak testować**
- Stwórz populację
- Zastosuj inwersję i elitaryzm
- Sprawdź zmiany w chromosomach i zachowanie najlepszych osobników

**Merge warunek**
- Operatory działają poprawnie
- Zachowana spójność populacji

---

# Krok 12 — poprawki w gui, spowodowane wymaganiami powyższych implementacji [Bartek]
  Zajmę się tym


---

# Krok 13 — zapis wyników

### Branch: `feature/io-results`

### Co robimy
1. Dodajemy zapis runów.
  - Nowy folder: io/
  - Pliki:
	  `results_writer.py`
	  `json_export.py`
	  `csv_export.py`

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
 - `visualization/convergence_plot.py`

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
  
  Przepływ: `GUI → config → engine → wynik`

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

# Krok 17 — Eksperymenty / batch runy

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
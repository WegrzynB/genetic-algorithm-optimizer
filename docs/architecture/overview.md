# docs/architecture/overview.md

## Cel projektu
Aplikacja w Pythonie z GUI w Tkinter realizująca optymalizację (min/max) funkcji wielu zmiennych metodą algorytmu genetycznego, z możliwością konfiguracji operatorów, zapisu wyników oraz generowania wykresów.

## Moduły i odpowiedzialności

- `ga_optimizer/gui/` — interfejs Tkinter (widoki, kontrolery, widgety, stan UI).
- `ga_optimizer/config/` — domyślne ustawienia, presety i walidacja konfiguracji runa.
- `ga_optimizer/core/` — rdzeń algorytmu GA (osobnik, populacja, kodowanie/dekodowanie, evaluator, pętla epok).
- `ga_optimizer/operators/` — operatory GA (selekcja, krzyżowanie, mutacje, inwersja, elitaryzm).
- `ga_optimizer/problems/` — definicje problemów i funkcji testowych + rejestr wyboru w GUI.
- `ga_optimizer/io/` — zapis/odczyt wyników (JSON/CSV), organizacja folderów runów.
- `ga_optimizer/visualization/` — wykresy (zbieżność, porównania) generowane w matplotlib.
- `ga_optimizer/experiments/` — uruchamianie serii runów i agregacje wyników (skrypty/benchmarki).
- `ga_optimizer/utils/` — narzędzia pomocnicze (czas, losowość, ścieżki, logowanie).

## Zależności między modułami (zasady importów)

- `gui` może importować: `config`, `core`, `problems`, `io`, `visualization`, `utils`.
- `core` może importować: `config`, `operators`, `problems`, `utils`, `types`.
- `operators` mogą importować: `utils`, `types` (i ewentualnie elementy `core` tylko jeśli kontrakt tego wymaga, ale bez zależności od GUI).
- `problems` mogą importować: `utils`, `types` (bez zależności od GUI).
- `io` może importować: `config`, `utils`, `types` (oraz struktury wyników z `core`, jeśli to konieczne).
- `visualization` może importować: `utils` i formaty danych wynikowych (np. historię epok).
- `experiments` może importować: `config`, `core`, `problems`, `io`, `visualization`, `utils`.
- `utils` i `types` nie zależą od innych modułów domenowych.

## Przepływ działania (wysoki poziom)

1. Użytkownik wybiera problem i parametry w `gui`.
2. `gui` buduje konfigurację i uruchamia walidację z `config`.
3. `core/engine` uruchamia algorytm GA, korzystając z `operators` i `problems`.
4. Wyniki (best/avg/worst + historia) trafiają do `gui` oraz do `io` (zapis).
5. `visualization` generuje wykresy na podstawie historii, a `io` zapisuje je do folderu runa.

## Konwencje projektu

- Każdy operator (selekcja/krzyżowanie/mutacja) jest w osobnym pliku.
- Każdy problem testowy (funkcja) jest w osobnym pliku w `problems/benchmark_functions`.
- Wyniki runów zapisujemy w `data/output/runs/<timestamp>_<id>/` razem z `config.json`, `metrics.json`, `history.csv` i wykresami w `plots/`.
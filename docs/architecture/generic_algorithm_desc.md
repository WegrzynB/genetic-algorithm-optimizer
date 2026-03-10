# Algorytm genetyczny (Genetic Algorithm — GA)

Algorytm genetyczny (GA) to metaheurystyczna metoda optymalizacji inspirowana procesami ewolucji biologicznej. Został opracowany przez **Johna Hollanda w latach 70. XX wieku**. GA należy do klasy **algorytmów ewolucyjnych** i jest stosowany do rozwiązywania problemów, dla których klasyczne metody numeryczne są trudne lub niemożliwe do zastosowania.

Celem algorytmu genetycznego jest **znalezienie rozwiązania, które minimalizuje lub maksymalizuje funkcję celu**, poprzez iteracyjną optymalizację populacji rozwiązań.

## 1. Podstawowe pojęcia

### Osobnik (Individual)

Podstawowym elementem GA jest **osobnik**, który reprezentuje jedno potencjalne rozwiązanie problemu.

### Chromosom (Chromosome)

Każdy osobnik zapisany jest w postaci **chromosomu**, który składa się z genów: 
**chromosom = (g1, g2, g3, ..., gn):**
- `g_i` – pojedynczy gen, reprezentujący wartość zmiennej decyzyjnej
- `n` – długość chromosomu (liczba zmiennych problemu)

Chromosom może być reprezentowany binarnie, liczbowo lub mieszanie tych sposobów, w zależności od problemu.

### Populacja (Population)

Populacja to zbiór `N` osobników:
**P = {x1, x2, x3, ..., xN}**
- `N` – liczba osobników w populacji
- `x_i` – pojedynczy osobnik

Populacja początkowa jest generowana **losowo**, w określonym zakresie wartości zmiennych.

## 2. Ocena osobników

Każdy osobnik oceniany jest przy pomocy **funkcji celu** `f(x)`:
**f(x) → wartość funkcji celu**
- `x` – wektor zmiennych decyzyjnych osobnika
- `f(x)` – wartość funkcji celu (minimalizowana lub maksymalizowana)

Na podstawie wartości funkcji celu obliczana jest **fitness**, która określa przystosowanie osobnika do dalszej reprodukcji:
- Fitness wysoki → większa szansa na reprodukcję
- Fitness niski → mniejsza szansa na reprodukcję


## 3. Selekcja osobników

Selekcja wybiera osobniki do stworzenia następnej generacji. Osobniki o wyższym przystosowaniu mają większą szansę na reprodukcję.

### Metody selekcji
1. **Best Selection** – wybiera najlepszych osobników z całej populacji.
2. **Turniejowa (Tournament Selection)** – losuje grupę osobników i wybiera najlepszego z grupy.
3. **Ruletkowa (Roulette Selection)** – prawdopodobieństwo wyboru proporcjonalne do fitness osobnika.

## 4. Krzyżowanie (Crossover)
Krzyżowanie łączy chromosomy rodziców w celu wygenerowania potomstwa.

### Popularne metody:

1. **Jednopunktowe (One-Point Crossover)**
   - Chromosomy rodziców przecinane są w jednym punkcie
   - Fragmenty wymieniane między rodzicami

2. **Dwupunktowe (Two-Point Crossover)**
   - Chromosomy przecinane w dwóch punktach
   - Środkowe fragmenty wymieniane między rodzicami

3. **Równomierne (Uniform Crossover)**
   - Każdy gen potomka losowo wybierany od jednego z rodziców

4. **Granularne (Granular Crossover)**
    - Chromosom dzielony jest na małe segmenty (granule)
    - Segmenty są losowo wymieniane między rodzicami
    - Zachowuje lokalne wzorce genetyczne, poprawiając eksplorację przestrzeni rozwiązań

## 5. Mutacja (Mutation)
Mutacja losowo zmienia jeden lub kilka genów w chromosomie. Celem jest wprowadzenie różnorodności genetycznej i uniknięcie lokalnych minimów.

## Popularne metody:

1. **Jednopunktowa (One-Point Mutation)**
    - Losowo wybierany jest pojedynczy gen i jego wartość zostaje zmieniona

2. **Dwupunktowa (Two-Point Mutation)**
    - Losowo wybierane są dwa geny i ich wartości są zmieniane

3. **Krawędziowa (Edge Mutation)**
    - Zmiana genów na krańcach chromosomu (pierwszy lub ostatni gen)
    - Pomaga w szybkiej eksploracji przestrzeni w obszarach granicznych

4. **Mutacja binarna**
    - Typowa dla chromosomów binarnych:
        0 → 1
        1 → 0
        
## 6. Inwersja (Inversion)
Inwersja odwraca fragment chromosomu:
    (1,0,0,1,1) → (1,1,0,0,1)

Umożliwia zachowanie różnorodności przy zachowaniu istniejących genów.

## 7. Elitaryzm (Elitism)
Elitaryzm przenosi najlepsze osobniki z poprzedniej populacji do nowej **bez zmian**.
Dzięki temu najlepsze znalezione rozwiązania nie zostają utracone.


## 8. Pętla algorytmu genetycznego — krok po kroku
1. **Generacja populacji początkowej**
   - Losowe stworzenie `N` osobników w zadanym zakresie zmiennych

2. **Ocena osobników**
   - Obliczenie funkcji celu `f(x)` dla każdego osobnika
   - Obliczenie fitness

3. **Selekcja osobników**
   - Wybór osobników do reprodukcji (np. ruletka, turniej)

4. **Krzyżowanie**
   - Tworzenie nowych osobników przez wymianę fragmentów chromosomów rodziców

5. **Mutacja**
   - Wprowadzenie losowych zmian w chromosomach dzieci

6. **Inwersja (opcjonalnie)**
   - Odwracanie fragmentów chromosomów w populacji

7. **Elitaryzm**
   - Przeniesienie najlepszych osobników do nowej populacji

8. **Utworzenie nowej populacji**
   - Populacja nowej generacji zastępuje starą

9. **Powtarzanie procesu**
   - Iteracja przez określoną liczbę epok lub do spełnienia warunku stopu

## 9. Warunki zakończenia algorytmu
Algorytm może zakończyć działanie, gdy:

- osiągnięto maksymalną liczbę epok,
- osiągnięto zadany próg wartości funkcji celu,
- poprawa wyników między epokami jest mniejsza niż zadany próg.

## 10. Opis aplikacji
Zaimplementowana aplikacja umożliwia:
- wybór funkcji testowej,
- konfigurację parametrów GA (liczba zmiennych, populacja, epoki, operatorzy),
- uruchomienie algorytmu,
- wizualizację procesu optymalizacji (best/avg/worst),
- zapis wyników i historii runów.

### Moduły aplikacji
- **GUI** – interfejs użytkownika
- **core** – implementacja algorytmu
- **operators** – selekcja, krzyżowanie, mutacja, inwersja, elitaryzm
- **problems** – funkcje testowe
- **io** – zapis wyników w JSON/CSV
- **visualization** – generowanie wykresów zbieżności

## 11. Wizualizacja wyników
Podczas działania algorytmu zapisywane są wartości:

- **best** – najlepszy osobnik w populacji
- **avg** – średnia fitness populacji
- **worst** – najgorszy osobnik

Na podstawie tych danych generowane są wykresy zbieżności GA.

## 12. Podsumowanie
Algorytmy genetyczne są skuteczną metodą optymalizacji, szczególnie w problemach nieliniowych lub z wieloma lokalnymi minimami.

**Kluczowe zalety:**
- efektywne przeszukiwanie przestrzeni rozwiązań,
- modularna struktura operatorów,
- możliwość eksperymentowania z różnymi metodami selekcji, krzyżowania i mutacji.

Zaimplementowana aplikacja w Pythonie umożliwia **eksperymenty, analizę i wizualizację procesu optymalizacji GA**, a modularna architektura pozwala na łatwe rozszerzanie funkcjonalności.

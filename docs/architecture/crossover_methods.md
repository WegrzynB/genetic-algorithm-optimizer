# Metody krzyżowania w algorytmie genetycznym

Krzyżowanie (crossover) jest jednym z podstawowych operatorów algorytmu genetycznego.  
Polega na **łączeniu materiału genetycznego dwóch chromosomów rodzicielskich w celu utworzenia nowych chromosomów potomnych**.

Celem krzyżowania jest:

- przekazywanie dobrych cech między osobnikami,
- eksploracja nowych obszarów przestrzeni rozwiązań,
- zwiększenie różnorodności populacji.

Krzyżowanie wykonywane jest z określonym **prawdopodobieństwem `p`**.

W projekcie dostępne są następujące metody krzyżowania:

---

# 1. Krzyżowanie jednopunktowe

## Opis

Krzyżowanie jednopunktowe polega na **wybraniu jednego punktu podziału chromosomu**, a następnie wymianie fragmentów chromosomów pomiędzy rodzicami.

Algorytm:

1. Losowany jest punkt krzyżowania w zakresie `[1, długość-1]`.
2. Chromosomy rodziców dzielone są na dwie części.
3. Fragmenty za punktem krzyżowania są zamieniane między rodzicami.
4. Powstaje dwóch potomków.


## Przykład

RODZIC 1  
[0 1 0 | 1 1 0 0 1]

RODZIC 2  
[1 0 1 | 0 0 1 1 0]

POTOMKOWIE  

[0 1 0 | 0 0 1 1 0]  
[1 0 1 | 1 1 0 0 1]

## Cechy

- bardzo popularna metoda krzyżowania
- prosta implementacja
- zachowuje duże fragmenty chromosomów

---

# 2. Krzyżowanie dwupunktowe

## Opis
Krzyżowanie dwupunktowe polega na **wybraniu dwóch punktów podziału chromosomu** i wymianie fragmentu znajdującego się pomiędzy nimi.

Algorytm:
1. Losowane są dwa punkty krzyżowania `point1` i `point2`.
2. Chromosomy dzielone są na trzy fragmenty.
3. Fragment znajdujący się między punktami jest wymieniany między rodzicami.

Schemat:

```
P1: [A | B | C]
P2: [D | E | F]

Potomkowie:
[C1] = A + E + C
[C2] = D + B + F
```

# 3. Krzyżowanie trzypunktowe

## Opis

Krzyżowanie trzypunktowe polega na **wybraniu trzech punktów podziału chromosomu** i naprzemiennym pobieraniu fragmentów od rodziców.

Algorytm:

1. Losowane są trzy punkty krzyżowania.
2. Chromosomy dzielone są na cztery fragmenty.
3. Fragmenty są naprzemiennie pobierane od rodziców.

Schemat:

P1 | P2 | P1 | P2

czyli:

```
child1 = P1[0:p1] + P2[p1:p2] + P1[p2:p3] + P2[p3:]
child2 = P2[0:p1] + P1[p1:p2] + P2[p2:p3] + P1[p3:]
```


# 4. Krzyżowanie wielopunktowe

## Opis
Krzyżowanie wielopunktowe polega na **wybraniu wielu punktów podziału chromosomu**, które dzielą chromosom na fragmenty.
Fragmenty są następnie **naprzemiennie pobierane od rodziców**, zaczynając od pierwszego rodzica.

Algorytm:

1. Losowanych jest `k` punktów krzyżowania.
2. Chromosom dzielony jest na `k+1` fragmentów.
3. Fragmenty są naprzemiennie kopiowane od rodziców.

Schemat:

```
P1 | P2 | P1 | P2 | ...
```



# 5. Krzyżowanie równomierne

## Opis

Krzyżowanie równomierne polega na **losowej zamianie genów między rodzicami z określonym prawdopodobieństwem**.

Algorytm:
1. Dla każdego genu losowana jest liczba z zakresu `[0,1]`.
2. Jeśli wartość jest mniejsza niż parametr `p`, geny rodziców są zamieniane miejscami.
3. Jeśli nie – geny pozostają bez zmian.

Schemat:

```
if random < p:
    swap genów
```

Cechy:
- wysoka losowość
- duża różnorodność potomstwa
- może niszczyć dobre fragmenty chromosomów



# 6. Krzyżowanie tasujące

## Opis

Krzyżowanie tasujące polega na **losowym przetasowaniu kolejności genów przed wykonaniem krzyżowania**, aby zmniejszyć wpływ pozycji genu w chromosomie.

Algorytm:

1. Generowana jest losowa permutacja indeksów genów.
2. Chromosomy rodziców są tasowane według tej permutacji.
3. Wykonywane jest jednopunktowe krzyżowanie.
4. Następnie przywracana jest pierwotna kolejność genów.

Cechy:
- zmniejsza zależność od pozycji genu
- zwiększa eksplorację przestrzeni rozwiązań



# 7. Krzyżowanie ziarniste

## Opis
Krzyżowanie ziarniste polega na **podziale chromosomu na małe fragmenty (granule)** o ustalonej wielkości i losowym wyborze rodzica dla każdego fragmentu.

Algorytm:
1. Chromosom dzielony jest na fragmenty o długości `granularity`.
2. Dla każdego fragmentu losowany jest rodzic.
3. Cały fragment kopiowany jest od wybranego rodzica.

Schemat:

```
[blok] -> wybierz parent1 lub parent2
```

Cechy:
- operuje na blokach genów
- umożliwia kontrolę wielkości wymienianych fragmentów
- zwiększa różnorodność populacji



# 8. Krzyżowanie segmentowe

## Opis

Krzyżowanie segmentowe polega na **zamianie segmentów chromosomu o ustalonej długości w regularnych odstępach**.

Algorytm:
1. Chromosom dzielony jest na segmenty o długości `segment_length`.
2. Co drugi segment jest zamieniany między rodzicami.
3. Pozostałe segmenty pozostają bez zmian.

Schemat:

```
swap | keep | swap | keep | ...
```

Cechy:

- kontroluje wielkość wymienianych fragmentów
- zachowuje część struktury chromosomu
---


# 9. Krzyżowanie arytmetyczne

## Opis
Krzyżowanie arytmetyczne polega na **obliczeniu wartości genu potomka jako kombinacji liniowej genów rodziców**.

Algorytm:

1. Wybierany jest parametr `α`.
2. Nowy gen obliczany jest według wzoru:
child = alpha * parent1 + (1 - alpha) * parent2
3. Wynik jest konwertowany do liczby całkowitej.

W przypadku chromosomów binarnych powoduje to często **zaokrąglenie wartości do 0 lub 1**.

Cechy:
- często stosowane w optymalizacji ciągłej
- tworzy rozwiązania pośrednie
- przy reprezentacji binarnej może powodować utratę różnorodności

---

# 10. Krzyżowanie zredukowane

## Opis

Krzyżowanie zredukowane polega na **wykonaniu krzyżowania tylko w miejscach, w których geny rodziców się różnią**.

Algorytm:

1. Wyznaczane są pozycje, na których geny rodziców są różne.
2. Punkt krzyżowania wybierany jest tylko spośród tych pozycji.
3. Wykonywane jest standardowe jednopunktowe krzyżowanie.

Cechy:
- ogranicza niepotrzebne zmiany
- zachowuje wspólne fragmenty chromosomów


# 11. Krzyżowanie niszczące

## Opis

Krzyżowanie niszczące polega na **losowej zamianie części genów między rodzicami tylko w miejscach, gdzie geny się różnią**.

Algorytm:

1. Wyznaczane są pozycje różniących się genów.
2. Losowo wybierana jest część tych pozycji.
3. Na wybranych pozycjach geny są zamieniane między rodzicami.

Cechy:
- zwiększa różnorodność populacji
- modyfikuje tylko różniące się geny
- nie zawsze wykonuje pełne mieszanie chromosomów


# 12. Krzyżowanie większościowe

## Opis

Krzyżowanie większościowe polega na **porównaniu genów dwóch rodziców i losowym wyborze genu w przypadku różnicy**.

Algorytm:

1. Jeśli geny rodziców są takie same – potomkowie dziedziczą tę samą wartość.
2. Jeśli geny się różnią:

   - losowo wybierany jest jeden z genów,
   - pierwszy potomek otrzymuje wybraną wartość,
   - drugi potomek otrzymuje wartość przeciwną.

Schemat:
```
jeśli P1 == P2 → kopiuj
jeśli P1 != P2 → losuj gen
```

Cechy:
- utrzymuje część różnorodności
- generuje komplementarne potomstwo


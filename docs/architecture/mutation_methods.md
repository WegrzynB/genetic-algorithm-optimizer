# Metody mutacji w algorytmie genetycznym

Mutacja jest operatorem algorytmu genetycznego odpowiedzialnym za **wprowadzanie różnorodności genetycznej w populacji**.
Polega na **losowej modyfikacji genów chromosomu** z określonym prawdopodobieństwem.

Mutacje zapobiegają:

- przedwczesnej zbieżności algorytmu,
- utknięciu w lokalnym optimum,
- utracie różnorodności populacji.

W projekcie dostępne są następujące metody mutacji:

# 1. Mutacja jednopunktowa

## Opis

Mutacja jednopunktowa polega na **losowej zmianie jednego genu w chromosomie**.

Algorytm:

1. Z prawdopodobieństwem `p` wybierany jest chromosom do mutacji.
2. Losowany jest indeks genu.
3. Wartość genu zostaje zmieniona.

Dla chromosomu binarnego oznacza to:

0 → 1
1 → 0

## Przykład

PRZED
[0 1 0 1 1 0 0 1]

Losujemy gen nr 3

PO
[0 1 0 0 1 0 0 1]

## Cechy

- bardzo mała zmiana w chromosomie
- stabilna eksploracja przestrzeni rozwiązań
- często używana w prostych implementacjach GA


# 2. Mutacja dwupunktowa

## Opis

Mutacja dwupunktowa polega na **zmianie dwóch losowo wybranych genów chromosomu**.

Algorytm:

1. Z prawdopodobieństwem `p` wykonywana jest mutacja.
2. Losowane są dwa indeksy genów.
3. Oba geny zostają zmienione.

## Przykład

PRZED
[0 1 0 1 1 0 0 1]

Mutujemy gen 2 i 6

PO
[0 0 0 1 1 0 1 1]

## Cechy

- większa zmiana niż mutacja jednopunktowa
- zwiększa różnorodność populacji
- może przyspieszać eksplorację przestrzeni rozwiązań


# 3. Mutacja krawędziowa

## Opis

Mutacja krawędziowa modyfikuje **geny znajdujące się na krańcach chromosomu**.

W zależności od trybu mogą zostać zmienione:

- pierwszy gen
- ostatni gen
- oba jednocześnie

## Przykład

PRZED
[0 1 0 1 1 0 0 1]

PO
[1 1 0 1 1 0 0 0]

## Cechy

- modyfikuje tylko skrajne geny
- zachowuje większość struktury chromosomu
- przydatna przy reprezentacjach gdzie krańce mają znaczenie


# 4. Mutacja bitowa

## Opis

Mutacja bitowa jest **najbardziej klasyczną mutacją stosowaną w algorytmach genetycznych** dla chromosomów binarnych.

Każdy gen chromosomu może zostać zmieniony **z określonym prawdopodobieństwem `p`**.

## Przykład

PRZED
[0 1 0 1 1 0 0 1]

PO
[0 0 0 1 0 0 0 1]

## Cechy

- standardowa mutacja GA
- pozwala na zmiany wielu genów jednocześnie
- zapewnia dobrą eksplorację przestrzeni rozwiązań


# 5. Mutacja zamiany

## Opis

Mutacja zamiany polega na **zamianie miejscami dwóch losowo wybranych genów**.

Algorytm:

1. Losowane są dwa indeksy genów.
2. Wartości genów zostają zamienione miejscami.

## Przykład

PRZED
[0 1 0 1 1 0 0 1]

Zamiana genów 1 i 6

PO
[0 0 0 1 1 0 1 1]

## Cechy

- zmienia strukturę chromosomu
- często stosowana w problemach permutacyjnych
- zachowuje liczbę wystąpień wartości


# 6. Mutacja tasowania

## Opis

Mutacja tasowania polega na **losowym przetasowaniu fragmentu chromosomu**.

Algorytm:

1. Losowany jest fragment chromosomu.
2. Geny w tym fragmencie są losowo mieszane.

## Przykład

PRZED
[0 1 0 1 1 0 0 1]

Fragment 2-6

PO
[0 1 1 0 0 1 0 1]

## Cechy

- wprowadza dużą losowość
- pozwala eksplorować nowe kombinacje genów
- zachowuje wartości genów


# 7. Mutacja resetowania

## Opis

Mutacja resetowania polega na **ustawieniu wybranego genu na nową losową wartość**.

W przypadku chromosomu binarnego gen zostaje ustawiony na 0 lub 1.

## Przykład

PRZED
[0 1 0 1 1 0 0 1]

Reset genu 4

PO
[0 1 0 1 0 0 0 1]

## Cechy

- wprowadza losowość do chromosomu
- pozwala na powrót do wcześniej utraconych wartości
- podobna do mutacji bitowej, ale działa na pojedynczym genie

# Metody selekcji osobników w algorytmie genetycznym.

## Równanie dynamiki populacji
Każda metoda selekcji w algorytmach genetycznych sprowadza się do manipulowania proporcjami poszczególnych klas osobników w kolejnych pokoleniach. Podstawowym narzędziem analitycznym jest tutaj równanie narodzin, życia i śmierci. Zakładając synchroniczne zmiany w czasie (pokolenie po pokoleniu), równanie przyjmuje postać:

$$m_{i,t+1}=m_{i,t}+m_{i,t,b}-m_{i,t,d}$$

gdzie $m$ to liczba osobników, indeks $i$ oznacza klasę osobników o tej samej wartości funkcji celu $f_i$, $t$ to indeks czasu, $b$ oznacza osobniki narodzone, a $d$ – umierające.

Dla wygody analizy operuje się na proporcjach ($P$), dzieląc liczbę osobników przez rozmiar populacji:

$$P_{i,t+1}=P_{i,t}+P_{i,t,b}-P_{i,t,d}$$

W standardowym modelu nienakładających się pokoleń (gdzie całe stare pokolenie wymiera), cała dynamika opiera się na narodzinach: $P_{i,t+1}=P_{i,t,b}$.

## Metody selekcji

### Selekcja neutralna (beztendencyjna / losowa)

W tym skrajnym przypadku selekcji, prawdopodobieństwo wyboru każdego z osobników jest dokładnie takie samo i nie zależy od wartości funkcji dopasowania (przystosowania). Prawdopodobieństwo to wynosi:

$$p_{i} = \frac{1}{N}$$

gdzie $N$ to całkowity rozmiar populacji. Ponieważ każdy osobnik ma identyczną szansę na reprodukcję, wartość oczekiwana proporcji danej klasy w kolejnym pokoleniu pozostaje niezmieniona ($P_{i,t+1} = P_{i,t}$). Metoda ta nie wywiera żadnego ciśnienia selekcyjnego, a wszelkie zmiany w proporcjach populacji w praktyce wynikają wyłącznie ze zjawiska dryfu stochastycznego (dryfu genetycznego).

### Reprodukcja proporcjonalna (Ruletka, Stochastyczne Próbkowanie Uniwersalne (SUS))

Prawdopodobieństwo wyboru osobnika z $i$-tej klasy w $t$-tym pokoleniu zależy od jego przystosowania w stosunku do sumy przystosowania całej populacji:

$$p_{i,t}=\frac{f_{i}}{\sum_{j=1}^{k}m_{j,t}f_{j}}$$

Z tego wynika równanie różnicowe dla proporcji danej klasy w nowym pokoleniu:

$$P_{i,t+1}=P_{i,t}\frac{f_{i}}{\overline{f}_{t}}$$

gdzie $\overline{f}_{t}$ to średnia wartość funkcji dla obecnego pokolenia. Co ważne, autorzy pracy cytowanej podają dokładne rozwiązanie tego równania na dowolne pokolenie $t$ w przód:

$$P_{i,t}=\frac{f_{i}^{t}P_{i,0}}{\sum_{j}f_{j}^{t}P_{j,0}}$$

### Selekcja rankingowa

Zamiast bazować na wartościach $f_i$, populacja jest sortowana od najlepszego do najgorszego osobnika. Analiza matematyczna opiera się na kumulatywnej funkcji przypisania $\beta(x)$. Dla najpopularniejszego, liniowego rankingu, równanie różnicowe przyjmuje postać równania logistycznego:

$$P_{i,t+1}=P_{i,t}[c_{0}-(c_{0}-1)P_{i,t}]$$

gdzie parametry $c_0$ i $c_1$ definiują nachylenie funkcji przypisania (przy czym $c_0 \ge c_1$).

### Selekcja turniejowa (Turniej i Podwójny Turniej)

Dla turnieju binarnego ($s=2$) z prawdopodobieństwem wyboru lepszego osobnika równym $p$, równanie proporcji ma postać:

$$P_{i,t+1}=2pP_{i,t}-(2p-1)P_{i,t}^{2}$$

Kluczowy wniosek (z publikacji): selekcja turniejowa binarna i selekcja rankingowa liniowa są matematycznie identyczne w wartości oczekiwanej, jeśli podstawimy $c_0 = 2p$.

Dla większych turniejów (o rozmiarze $s$) łatwiej badać losowanie osobników najgorszych (oznaczmy ich proporcję jako $Q$). Kopia osobnika z najgorszej grupy powstanie tylko wtedy, gdy wszyscy $s$ wybrani uczestnicy będą z tej samej słabej grupy:

$$Q_{i,t+1}=Q_{i,t}^{s}$$

Z tego wyprowadza się dokładne rozwiązanie dla najlepszych ($P_i = 1 - Q_i$):

$$P_{i,t}=1-(1-P_{i,0})^{s^{t}}$$

### Selekcja najlepszych

Metoda ta opiera się na odcięciu i odrzuceniu gorszej części populacji. Pod kątem analitycznym formalizuje się ją poprzez aparat funkcji przypisania $\alpha(x)$ opisany w ogólnych modelach porządkowych. W przeciwieństwie do selekcji rankingowej funkcja $\alpha(x)$ przyjmuje tutaj postać skokową. Przy zdefiniowaniu progu odcięcia na poziomie $T$ ułamka najlepszych osobników, proporcja dla klas znajdujących się poniżej tego progu w pokoleniu $t+1$ wyniesie z definicji zero, co drastycznie zwiększa presję selekcyjną.

### Selekcja najgorszych

Metoda polegająca na sukcesywnym eliminowaniu osobników najsłabszych wymaga wykorzystania pełnego modelu dynamiki obejmującego człon śmierci z fundamentalnego równania $P_{i,t+1}=P_{i,t}+P_{i,t,b}-P_{i,t,d}$. W przeciwieństwie do standardowego modelu pokoleniowego śmierć jest tutaj ściśle deterministyczna i celowana: osobniki z najgorszej grupy tracą swoją proporcję w populacji, ustępując miejsca na nowo narodzone osobniki z grup lepszych. Osobniki o najlepszym przystosowaniu nie podlegają operacji usunięcia ($d = 0$), dopóki całkowicie nie zdominują struktury populacji.


## Złożoność obliczeniowa

Kryterium wydajności algorytmicznej (złożoność czasowa) poszczególnych metod selekcji wygląda następująco:
* Selekcja neutralna (losowa): Wybór pojedynczego osobnika to operacja w czasie $O(1)$. Powtórzenie tego procesu dla całej populacji wielkości $N$ (lub $n$) daje optymalną złożoność liniową $O(n)$.
* Ruletka: Przy standardowym wyszukiwaniu liniowym algorytm działa w czasie $O(n^2)$. Przy użyciu wyszukiwania binarnego czas ten można zredukować do $O(n \log n)$.
* Stochastic Universal Selection (SUS): Wymaga tylko jednego obrotu koła i działa w optymalnym czasie $O(n)$.
* Selekcja rankingowa: Ze względu na konieczność posortowania całej populacji, jej złożoność to $O(n \log n)$.
* Selekcja turniejowa: Wybór stałej liczby osobników i ich porównanie zajmuje czas stały, co przy wypełnianiu całej populacji daje doskonałą złożoność $O(n)$. Co więcej, jest to metoda najłatwiejsza do zrównoleglenia, ponieważ nie wymaga globalnych informacji o populacji.
* Selekcja najlepszych: Złożoność to $O(n \log n)$, co jest uwarunkowane koniecznością wstępnego posortowania puli osobników przed zastosowaniem progu odcięcia.
* Selekcja najgorszych: Ciągłe wyszukiwanie i przesuwanie elementów podczas utrzymywania porządku listy przy narodzinach i śmierci osobników zajmuje $O(\log n)$ na jedną iterację, co w przeliczeniu na kompletne pokolenie zachowuje złożoność całkowitą $O(n \log n)$ 

## Bibliografia:
1. Goldberg, D. E., & Deb, K. (1991). A Comparative Analysis of Selection Schemes Used in Genetic Algorithms. W: G. J. E. Rawlins (Red.), Foundations of Genetic Algorithms. San Mateo, CA: Morgan Kaufmann Publishers.

2. Książek, W. (2026). Obliczenia ewolucyjne. Wykład 2. Biologiczna inspiracja algorytmów genetycznych. Klasyczny algorytm genetyczny [Materiały z wykładu]. Wydział Informatyki i Matematyki, Katedra Informatyki, Politechnika Krakowska, Kraków.

To szybka, bieżąca lista zadań do wykonania i statusów (np. TODO / IN PROGRESS / DONE). Trzymacie tu krótkie, operacyjne punkty, które często się zmieniają (w przeciwieństwie do plan.md, który jest bardziej “strategiczny”). Dobrze sprawdza się jako “jedna kartka” do codziennego ogarniania pracy.


Kroki dodawania nowych metod operatorów:
1. Wpisanie odpowiedniej metody, wraz z jej parametrami do `src/ga_optimizer/config/method_xxx.py` (UWAGA: na samej górze jest stała `XXX_METHOD_LABELS`, należy do niej wpisać klucz metody, wraz z jej tłumaczeniem, które wyświetli się w interfejsie),
2. Wpisanie odpowiedniej metody w `src/ga_optimizer/operators/xxx/metoda.py`,
3. Dopisanie tej metody do pliku dispatch `src/ga_optimizer/operators/dispatch/dispatch_xxx.py` w match dla danego case
4. Testowanie

Każda z tych funkcji ma na wejściu mieć chromosomy (oraz `config_dict`) i zwracać chromosomy w takiej samej formie.
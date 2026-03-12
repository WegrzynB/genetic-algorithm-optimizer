To szybka, bieżąca lista zadań do wykonania i statusów (np. TODO / IN PROGRESS / DONE). Trzymacie tu krótkie, operacyjne punkty, które często się zmieniają (w przeciwieństwie do plan.md, który jest bardziej “strategiczny”). Dobrze sprawdza się jako “jedna kartka” do codziennego ogarniania pracy.


Kroki dodawania nowych metod operatorów:
1. Wpisanie odpowiedniej metody, wraz z jej parametrami do `src/fa_optimizer/config/metchod_xxx.py`,
2. Wpisanie odpowiedniej metody w `src/fa_optimizer/operators/xxx/metoda.py`,
3. Dopisanie tej metody do pliku dispatch `src/fa_optimizer/operators/dispatch/dispatch_xxx.py` w match dla danego case
4. Testowanie

Każda z tych funkcji ma na wejściu mieć chromosomy (oraz `config_dict`) i zwracać chromosomy w takiej samej formie.
# Zadanie 5 - Wartość czasowa opcji i gwarancji

W tym zadaniu zbudujesz model do obliczania **wartości czasowej opcji i gwarancji (TVOG)** na podstawie scenariuszy stochastycznych.

Modelowany produkt to **ubezpieczenie na dożycie z gwarantowaną sumą ubezpieczenia**.

Jak działa ten produkt?
- ubezpieczony wpłaca składki co roku,
- składki są inwestowane w fundusz inwestycyjny,
- jeśli ubezpieczony dożyje do końca umowy, otrzyma większą z dwóch wartości: wartość funduszu lub gwarantowaną sumę.

Dla uproszczenia przyjmujemy okresy roczne i pomijamy ryzyko śmierci. Skupiamy się tylko na ryzyku inwestycyjnym.

## 1 Utworzenie modelu

Na początek utwórz nowy model o nazwie `zadanie_5`.

W powłoce Pythona wpisz:

```python
from cashflower import create_model
create_model("zadanie_5")
```

## 2 Dane wejściowe

### 2.1 Dane ubezpieczeniowe (model point set)

W pliku `input.py` przygotuj dane dotyczące ubezpieczenia. Utwórz model point set o nazwie `policy`, który będzie zawierał:

- `premium` – roczna składka wpłacana na początku każdego roku: 9 000 zł
- `guaranteed_benefit` – gwarantowana wypłata w przypadku dożycia: 100 000 zł
- `term` – czas trwania umowy: 5 lat

Uzupełnij poniższy szkielet kodu:

```python
from cashflower import ModelPointSet
import pandas as pd

policy = ModelPointSet(data=pd.DataFrame({
    "premium": [_____],
    "guaranteed_benefit": [_____],
    "term": [_____],
}))
```

**Zadanie:**
Uzupełnij brakujące wartości zgodnie z danymi ubezpieczeniowymi.

### 2.2 Scenariusze stochastyczne

Model będzie wykorzystywał zestaw **losowych scenariuszy stóp zwrotu z inwestycji**.

Każdy scenariusz powinien zawierać:
- `scenario` – numer scenariusza,
- `t` – numer roku (od 1 do 5),
- `rate` – roczna stopa zwrotu w danym roku.

Załóż, że stopa zwrotu ma rozkład normalny ze średnią 4% i odchyleniem standardowym 10%.

Wygeneruj 1000 scenariuszy po 5 lat każdy. Skorzystaj z poniższego kodu:

```python
import pandas as pd
import numpy as np

n_scenarios = 1000
n_years = 5

stochastic_scenarios = pd.DataFrame({
    "scenario": np.repeat(np.arange(1, n_scenarios + 1), n_years),
    "t": list(range(1, n_years + 1)) * n_scenarios,
    "rate": np.random.normal(loc=0.04, scale=0.10, size=n_scenarios * n_years),
})
```
**Zadanie:**
Wygeneruj tabelę `stochastic_scenarios` zgodnie z powyższym kodem.

### 2.3 Stopa procentowa

Wartość czasowa gwarancji zależy od przyjętej stopy dyskonta. Załóż, że roczna techniczna stopa procentowa wynosi 3%.

Zapisz ją jako zmienną skalarną `interest_rate` w pliku `input.py`:

```python
interest_rate = 0.03
```

**Zadanie:**
Uzupełnij wartość stopy procentowej jako ułamek dziesiętny.

## 3 Ustawienia

W pliku `settings.py` ustaw parametry związane z liczbą scenariuszy i długością projekcji.

- `NUM_STOCHASTIC_SCENARIOS` – liczba scenariuszy: 1000
- `T_MAX_CALCULATION` – maksymalna liczba okresów do obliczeń: 5
- `T_MAX_OUTPUT` – maksymalna liczba okresów do wyświetlenia w wynikach: 5

Dla uproszczenia oraz przyspieszenia obliczeń, w tym zadaniu przyjmujemy 5-letni horyzont czasowy.

Uzupełnij słownik `settings`:

```python
# settings.py
settings = {
    "NUM_STOCHASTIC_SCENARIOS": _____,
    "T_MAX_CALCULATION": _____,
    "T_MAX_OUTPUT": _____,
    # ...
}
```

**Zadanie:**
Wstaw odpowiednie wartości zgodnie z opisem powyżej.










## 4 Model

### 4.1 Import zmiennych

Na początek zaimportuj dane wejściowe do pliku `model.py`.

W tym modelu będziesz korzystać z:
- danych polisy (`policy`),
- stopy procentowej (`interest_rate`),
- scenariuszy stochastycznych (`stochastic_scenarios`).

Uzupełnij kod:
```python
# model.py
from input import _____, _____, _____
```

**Zadanie:**
Uzupełnij nazwy zmiennych zgodnie z tymi, które przygotowałeś/aś w `input.py`.

### 4.2 Stopa zwrotu funduszu inwestycyjnego

Zdefiniuj zmienną stochastyczną `investment_return(t, stoch)`, która zwraca roczną stopę zwrotu z funduszu w danym scenariuszu.

Załóż:
- jeśli `t == 0`, to zwrot wynosi 0,
- jeśli `t` przekracza długość umowy (`term`), także zwracamy 0,
- w przeciwnym razie pobieramy wartość z tabeli `stochastic_scenarios`.

Uzupełnij funkcję:
```python
@variable()
def investment_return(t, stoch):
    if t == 0 or t > policy.get("_____"):
        return 0
    return stochastic_scenarios.loc[(stoch, t), "_____"]
```

**Zadanie:**
- Wstaw odpowiednią nazwę atrybutu z długością polisy (`term`).
- Wstaw nazwę kolumny z wartością stopy zwrotu (`rate`).

### 4.3 Wartość funduszu

Zmienna `fund_value(t, stoch)` pokazuje, ile wart jest fundusz inwestycyjny w danym roku `t` i scenariuszu `stoch`.

Założenia:
- w roku `t = 0` fundusz równa się pierwszej składce,
- w kolejnych latach rośnie zgodnie z przypisaną stopą zwrotu,
- składka jest wpłacana na początku roku.

Uzupełnij kod:

```python
@variable()
def fund_value(t, stoch):
    if t == 0:
        return policy.get("premium")
    elif t < policy.get("term"):
        return fund_value(t - 1, stoch) * (1 + investment_return(t, stoch)) + policy.get("_____")
    else:
        return fund_value(t - 1, stoch) * (1 + _____)
```

**Zadanie:**
- W pierwszej instrukcji `return`: uzupełnij nazwę atrybutu z wysokością składki,
- W drugiej: wpisz wywołanie funkcji `investment_return(t, stoch)`.

### 4.4 Różnica do gwarancji 

Na koniec trwania polisy ubezpieczyciel wypłaca klientowi większą z dwóch wartości: wartość funduszu albo gwarantowaną sumę. Jeżeli fundusz jest mniejszy, ubezpieczyciel musi dopłacić różnicę.

Zmienna `shortfall(t, stoch)` powinna:
- zwracać różnicę między gwarantowaną sumą a funduszem, jeśli fundusz jest niższy,
- zwracać 0 w przeciwnym wypadku..

Uzupełnij kod:
```python
@variable()
def shortfall(t, stoch):
    if t == policy.get("term"):
        return max(0, _____ - _____)
    return 0
```
**Zadanie:**
Uzupełnij wzór na różnicę: gwarantowana suma minus wartość funduszu.




### 4.5 Wartość czasowa opcji i gwarancji

Zmienna `tvog(t, stoch)` oblicza bieżącą wartość przewidywanej dopłaty ubezpieczyciela, czyli wartość opcji gwarantowanej wypłaty.

Założenia:
- W ostatnim roku TVOG to po prostu shortfall,
- W wcześniejszych latach – to zdyskontowana wartość TVOG z roku następnego.

Uzupełnij kod:

```python
@variable()
def tvog(t, stoch):
    if t == policy.get("term"):
        return shortfall(t, stoch)
    return _____ * (1 / (1 + interest_rate))
```

**Zadanie:**
Wpisz, jaka zmienna reprezentuje wartość z kolejnego roku.

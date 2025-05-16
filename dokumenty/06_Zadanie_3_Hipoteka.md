# Zadanie 3 - kredyt hipoteczny

W tym zadaniu zbudujesz prosty model spłaty **kredytu hipotecznego**.

Model będzie oparty na typowym kredycie z równą miesięczną ratą (tzw. kredycie annuitetowym).  

W modelu krok po kroku:

- obliczysz miesięczną stopę procentową na podstawie rocznej,
- wyznaczysz wysokość miesięcznej raty,
- rozdzielisz ratę na część odsetkową i kapitałową,
- policzysz saldo zadłużenia w każdym miesiącu.

## 1. Utworzenie modelu

Twoim pierwszym krokiem jest utworzenie nowego modelu.

W tym celu:
1. Otwórz powłokę Python.
2. Skorzystaj z poniższej komendy, aby utworzyć model o nazwie `zadanie_3`:

```python
from cashflower import create_model
create_model("zadanie_3")
```

## 2. Dane wejściowe

W tej części przygotujesz dane wejściowe: parametry kredytu (czyli tzw. model point set).

### 2.1 Parametry kredytu (model point set)

W pliku `input.py` zdefiniuj zbiór danych dla jednego kredytu. Nazwij go `mortgage`.

Kredyt ma następujące parametry:

- początkowa kwota kredytu: 100 000 zł (`loan`),
- roczna stopa procentowa: 10 % (`yearly_interest_rate`),
- okres kredytowania: 360 miesięcy (`term`).

Uzupełnij poniższy szkielet kodu:

```python
# input.py
from cashflower import ModelPointSet
import pandas as pd

mortgage = ModelPointSet(data=pd.DataFrame({
    "loan": [_____],
    "yearly_interest_rate": [_____],
    "term": [_____],
}))
```
**Zadanie:** 
Uzupełnij brakujące wartości zgodnie z opisanymi parametrami.

## 3. Model

W tej części zbudujesz krok po kroku zmienne modelowe do obliczenia rat, odsetek i salda kredytu.

### 3.1 Import danych

Na początku zaimportuj dane z pliku `input.py`. Otwórz `model.py` i uzupełnij import:

```python
# model.py
from input import _____
```

**Zadanie:** 
Uzupełnij nazwę zmiennej zawierającej dane kredytu.

### 3.2 Miesięczna stopa procentowa

Na podstawie rocznej stopy procentowej z model point setu oblicz miesięczną stopę procentową. Zmienna `interest_rate()` nie zależy od czasu.

Uzupełnij kod:

```python
from cashflower import variable

@variable()
def interest_rate():
    return mortgage.get("_____") / _____
```

**Zadanie:**
- Wstaw nazwę atrybutu z roczną stopą procentową,
- Podziel ją przez liczbę miesięcy w roku.

### 3.3 Rata miesięczna

Oblicz miesięczną ratę kredytu `payment()` na podstawie wzoru na annuitet:

$$  P = \frac{ L }{  \frac{1 - v^n}{j} } $$

gdzie

$$ v = \frac{1}{1+j} $$


Pamiętaj:
- `L` to kwota kredytu,
- `j` to miesięczna stopa procentowa (`interest_rate()`),
- `n` to liczba miesięcy (`mortgage.get("term")`).

Uzupełnij kod:

```python
@variable()
def payment():
    L = mortgage.get("_____")
    j = interest_rate()
    n = mortgage.get("_____")
    v = 1 / (1 + j)
    return L / ((_____) / _____)
```
**Zadanie:**
- Uzupełnij nazwy atrybutów `loan` i `term`,
- Uzupełnij wzór: jaka wartość powinna znaleźć się w liczniku i w mianowniku?


### 3.4 Odsetki

Odsetki naliczane w miesiącu `t` są równe saldu kredytu z poprzedniego miesiąca (`balance(t-1)` - tej zmiennej jeszcze nie mamy) pomnożonemu przez miesięczną stopę procentową.

Dla `t = 0` odsetki wynoszą 0 (jest to początek kredytu).

Uzupełnij kod funkcji:

```python
@variable()
def interest(t):
    if t == 0:
        return 0
    return _____ * _____
```

**Zadanie:**

Uzupełnij wzór na odsetki.


### 3.5 Spłata kapitału

Część raty, która spłaca kapitał (czyli zmniejsza saldo kredytu), to różnica między całkowitą ratą (`payment`) a częścią odsetkową (`interest`).

Uzupełnij kod funkcji:

```python
@variable()
def principal(t):
    return _____ - _____
```

**Zadanie:**
Wstaw odpowiednie zmienne:
- jedna to stała miesięczna rata,
- druga to odsetki w miesiącu `t`.

### 3.6 Pozostałe saldo kredytu

Zmienna `balance(t)` określa saldo pozostałego długu w danym miesiącu:

- dla `t = 0` saldo równa się początkowemu kredytowi,
- później maleje o spłacony kapitał.

```python
@variable()
def balance(t):
    if t == 0:
        return mortgage.get("_____")
    return balance(t - 1) - principal(t)
```

**Zadanie:**
Uzupełnij nazwę atrybutu określającego początkowy kredyt.


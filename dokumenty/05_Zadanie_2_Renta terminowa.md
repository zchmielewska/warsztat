# Zadanie 2 - renta terminowa

W tym zadaniu zbudujesz prosty model aktuarialny służący do wyznaczenia **bieżącej wartości aktuarialnej** renty terminowej.

Renta terminowa to umowa, w której ubezpieczyciel zobowiązuje się wypłacać cykliczne świadczenia (np. co miesiąc) przez określony czas – pod warunkiem, że ubezpieczony żyje.

W modelu zakładamy:
- miesięczne wypłaty świadczenia (np. 2 000 zł),
- stałe miesięczne prawdopodobieństwo zgonu,
- brak kosztów, prowizji i reasekuracji (czyli liczymy wartość netto),
- stałą stopę procentową (oprocentowanie techniczne).

## **1 Utworzenie modelu**

Twoim zadanTwoim pierwszym krokiem jest utworzenie nowego modelu.

W tym celu:
1. Otwórz powłokę Python.
2. Skorzystaj z poniższej komendy, aby utworzyć model o nazwie `zadanie_2`:

```python
from cashflower import create_model
create_model("zadanie_2")
```

## **2 Dane wejściowe**

W tej części przygotujesz dane wejściowe: dane ubezpieczeniowe (tzw. model point set) oraz założenie dotyczące stopy procentowej.

### **2.1 Dane ubezpieczeniowe (model point set)**

W pliku `input.py` przygotuj dane dotyczące ubezpieczonych. Skorzystaj z klasy `ModelPointSet` i przygotuj dane w formie tabeli (`DataFrame`). Nazwij swój model point set `policy`.

Dodaj dane dla dwóch osób:
- osoba 1: świadczenie 2 000 zł, miesięczne prawdopodobieństwo zgonu 0.004, długość renty 120 miesięcy,
- osoba 2: świadczenie 3 000 zł, miesięczne prawdopodobieństwo zgonu 0.005, długość renty 48 miesięcy.

Uzupełnij kod:

```python
# input.py

from cashflower import ModelPointSet
import pandas as pd

policy = ModelPointSet(data=pd.DataFrame({
    "id": [1, 2],
    "benefit": [_____, _____],
    "mortality_rate": [_____, _____],
    "remaining_term": [_____, _____],
}))
```
**Zadanie:** 
Uzupełnij brakujące wartości zgodnie z danymi ubezpieczonych.

### **2.2 Założenia rynkowe**

Załóż, że miesięczna stopa procentowa wynosi 0.3%. Zapisz ją jako zmienną skalarną `interest_rate`. Umieść ją w tym samym pliku `input.py`.

```python
# input.py

interest_rate = _____
```

**Zadanie:** 
Uzupełnij wartość stopy procentowej jako ułamek dziesiętny.

## 3. Model

W tej części utworzysz zmienne potrzebne do obliczenia bieżącej wartości aktuarialnej renty.

###  3.1 Import danych

Na początek zaimportuj dane wejściowe z pliku `input.py`. Otwórz plik `model.py`.

Znajdziesz tam przykładową zmienną, możesz ją zakomentować lub usunąć, aby mieć czysty plik.

Zaimportuj dane:
- `policy` – dane polisowe,
- `interest_rate` – stopa procentowa.

Uzupełnij poniższy kod:

```python
# model.py
from input import _____, _____
```
**Zadanie:**
Wstaw odpowiednie nazwy zmiennych, które przygotowałeś/aś w `input.py`.

### 3.2 Prawdopodobieństwo przeżycia `t` miesięcy

Utwórz zmienną `survival_rate(t)`, która będzie wyznaczać prawdopodobieństwo przeżycia `t` miesięcy od początku trwania renty.

Skorzystaj ze wzoru rekurencyjnego:

$$
\begin{align*}
\text{survival\_rate(t)} = {}_tp_x = {}_{t-1}p_x \cdot (1-q_{x+t-1})
\end{align*}
$$

Załóż, że:
- dla `t=0` przeżywalność wynosi 1,
- prawdopodobieństwo zgonu miesięczne jest stałe i równe `policy.get("mortality_rate")`.

Uzupełnij funkcję poniżej:

```python
@variable()
def survival_rate(t):
    if t == 0:
        return 1
    else:
        q = policy.get("_____")
        return survival_rate(t - 1) * (1 - _____)
```

**Zadanie:**
- Uzupełnij nazwę atrybutu zawierającego miesięczne prawdopodobieństwo zgonu.
- Zastanów się, jak wyrazić prawdopodobieństwo przeżycia t miesięcy.

### 3.3. Oczekiwane świadczenie

Zdefiniuj zmienną`expected_benefit(t)` – oczekiwaną wartość świadczenia wypłacanego w miesiącu `t`.

Skorzystaj ze wzoru:

$$
\begin{align*}
\text{expected\_benefit(t)} = B \cdot {}_{t}p_x
\end{align*}
$$

Pamiętaj, że:

- dla `t = 0` oraz po zakończeniu okresu renty świadczenie wynosi 0,
- $B$ to `policy.get("benefit")`,
- długość trwania renty to `policy.get("remaining_term")`.

Uzupełnij poniższy kod:

```python
@variable()
def expected_benefit(t):
    if t == 0 or t > policy.get("_____"):
        return 0
    else:
        B = policy.get("_____")
        return B * _____
```

**Zadanie:**
- Uzupełnij nazwę atrybutu `remaining_term` i `benefit`,
- Wstaw odpowiednią zmienną dla przeżywalności `t` okresów.

### 3.4 Bieżąca wartość aktuarialna

Oblicz bieżącą wartość aktuarialną renty, czyli sumę zdyskontowanych oczekiwanych świadczeń.

Zastosuj podejście rekurencyjne:

$$ \text{actuarial\_present\_value(t)} = \text{expected\_benefit(t)} + \text{actuarial\_present\_value(t+1)} \cdot v $$

gdzie:

- $v = \frac{1}{1+i}$,
- $i$ to miesięczna stopa procentowa (`interest_rate`),
- dla maksymalnego `t` wartość równa się `expected_benefit(t)`.

Uzupełnij kod poniżej:

```python
from settings import settings

@variable()
def actuarial_present_value(t):
    if t == settings["_____"]:
        return _____
    else:
        v = 1 / (1 + _____)
        return _____ + v * _____
```

**Zadanie:**
- Uzupełnij nazwę parametru `T_MAX_CALCULATION` z pliku `settings.py`,
- Wstaw odpowiednie zmienne: `expected_benefit`, `interest_rate`, `actuarial_present_value`.


## 4. Struktura wyników 

### 4.1. Wyniki indywidualne

Aby uzyskać wyniki osobno dla każdego ubezpieczonego, w pliku `settings.py` ustaw:

```python
# setting.py
settings = {
    "GROUP_BY": "id",
    # ...
}
```


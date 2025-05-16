# Zadanie 1 - terminowe ubezpieczenie na życie

W tym zadaniu zbudujesz prosty model aktuarialny służący do wyznaczenia **składki  jednorazowej netto** dla terminowego ubezpieczenia na życie.

Terminowe ubezpieczenie na życie to umowa, w której ubezpieczyciel zobowiązuje się wypłacić świadczenie w przypadku śmierci ubezpieczonego w określonym czasie trwania ochrony (np. przez 36 miesięcy). Jeśli ubezpieczony przeżyje cały okres ubezpieczenia, świadczenie nie jest wypłacane, a ochrona wygasa.

W modelu zakładamy:
- wypłatę świadczenia w wysokości 100 000 zł w przypadku zgonu w trakcie trwania polisy,
- stałe miesięczne prawdopodobieństwo zgonu,
- brak kosztów, prowizji i reasekuracji (czyli liczymy składkę netto),
- stałą stopę procentową (oprocentowanie techniczne).

## 1 Utworzenie modelu

Twoim pierwszym krokiem jest utworzenie nowego modelu.

W tym celu:
1. Otwórz powłokę Python.
2. Skorzystaj z poniższej komendy, aby utworzyć nowy model o nazwie `zadanie_1`:

```python
from cashflower import create_model
create_model("zadanie_1")
```

## 2 Dane wejściowe

W tej części przygotujesz dane wejściowe: dane ubezpieczeniowe (tzw. model point set) oraz założenie dotyczące stopy procentowej.

### 2.1 Dane ubezpieczeniowe (model point set)

W pliku `input.py` przygotuj dane dotyczące ubezpieczonego. Skorzystaj z klasy `ModelPointSet` i przygotuj dane w formie tabeli (`DataFrame`). Nazwij swój model point set `policy`.

Polisa powinna zawierać następujące atrybuty:
- suma ubezpieczenia: 100 000 zł (`sum_assured`),
- miesięczne prawdopodobieństwo zgonu: 0.003 (`mortality_rate`),
- pozostały czas trwania umowy: 36 miesięcy (`remaining_term`).

Poniżej znajdziesz szkielet kodu z miejscami do uzupełnienia:

```python
# input.py

from cashflower import ModelPointSet
import pandas as pd

policy = ModelPointSet(data=pd.DataFrame({
    "sum_assured": [ _____ ],
    "mortality_rate": [ _____ ],
    "remaining_term": [ _____ ],
}))
```
**Zadanie:** uzupełnij brakujące wartości zgodnie z założeniami.

### 2.2 Założenia rynkowe

Załóż, że miesięczna stopa procentowa wynosi 0.5%. Zapisz ją jako zmienną skalarną `interest_rate`. Umieść ją w tym samym pliku `input.py`.

```python
# input.py

interest_rate = _____
```

** Zadanie:** Uzupełnij wartość stopy procentowej jako ułamek dziesiętny.

## 3 Model

W tej części stworzysz zmienne modelowe potrzebne do obliczenia składki jednorazowej netto.

### 3.1 Import danych

Na początek zaimportuj dane wejściowe z pliku `input.py`. Otwórz plik `model.py`.

Znajdziesz tam przykładową zmienną, możesz ją zakomentować lub usunąć, aby mieć czysty plik.

Zaimportuj dane:
- `policy` – dane polisy,
- `interest_rate` – stopa procentowa.

Uzupełnij poniższy kod:

```python
# model.py
from input import _____, _____
```


### 3.2 Prawdopodobieństwo przeżycia `t` miesięcy

Utwórz zmienną `survival_rate(t)`, która będzie wyznaczać prawdopodobieństwo przeżycia `t` miesięcy od początku trwania umowy.

Posłuż się zależnością rekurencyjną:

$$
\begin{align*}
\text{survival\_rate(t)} = {}_tp_x = {}_{t-1}p_x \cdot (1-q_{x+t-1})
\end{align*}
$$

Załóż, że:

- dla `t=0` przeżywalność  wynosi `1`,
- prawdopodobieństwo zgonu miesięczne jest stałe i równe `policy.get("mortality_rate")`.

Uzupełnij funkcję poniżej:

```python 
@variable()
def survival_rate(t):
    if t == 0:
        return 1
    else:
        q = policy.get("_____")
        return survival_rate(t - 1) * (_____ )
```

**Zadanie:**
- Uzupełnij nazwę atrybutu zawierającego miesięczne prawdopodobieństwo zgonu.
- Zastanów się, jak wyrazić prawdopodobieństwo przeżycia `t` miesięcy.

### 3.3 Oczekiwane świadczenie

Zdefiniuj zmienną expected_benefit(t) – oczekiwaną wartość świadczenia wypłacanego w momencie zgonu w miesiącu t.

Skorzystaj ze wzoru:

$$
\begin{align*}
\text{expected\_benefit(t)} = B \cdot {}_{t-1}p_x \cdot q_{x+t-1}
\end{align*}
$$

Pamiętaj, że:

- dla `t = 0` oraz po zakończeniu okresu ubezpieczenia świadczenie wynosi 0,
- $B$ to`policy.get("sum_assured")`,
- długość trwania polisy to `policy.get("remaining_term")`.

Uzupełnij poniższy kod:

```python
@variable()
def expected_benefit(t):
    if t == 0 or t > policy.get("_____"):
        return 0
    else:
        B = policy.get("_____")
        q = policy.get("_____")
        return B * _____ * q

```
**Zadanie:**
- Uzupełnij brakujące nazwy atrybutów (`remaining_term`, `sum_assured`, `mortality_rate`).
- Uzupełnij część wzoru, która odpowiada za prawdopodobieństwo przeżycia do miesiąca `t-1`.




### 3.4 Składka jednorazowa netto

Oblicz wartość składki jednorazowej netto, czyli bieżącej wartości oczekiwanych świadczeń.

Zastosuj podejście rekurencyjne:

$$ \text{net\_single\_premium(t)} = \text{expected\_benefit(t)} + \text{net\_single\_premium(t+1)} \cdot v $$

gdzie:

- $ v = \frac{1}{1+i} $,

- $ i $ to miesięczna stopa procentowa (`interest_rate`),
- dla ostatniego miesiąca (maksymalne `t`) składka to oczekiwane świadczenie.

Pamiętaj, że maksymalna wartość `t` jest ustawiona w `settings.py` jako `T_MAX_CALCULATION`.

Uzupełnij poniższy kod:

```python
from settings import settings

@variable()
def net_single_premium(t):
    if t == settings["_____"]:
        return _____
    else:
        v = 1 / (1 + _____)
        return _____ + v * _____
```

**Zadanie:**
- Uzupełnij nazwę parametru z `settings.py`, który określa maksymalne `t`,
- Wstaw odpowiednie zmienne do obliczenia składki (np. `expected_benefit`, `net_single_premium`, `interest_rate`).

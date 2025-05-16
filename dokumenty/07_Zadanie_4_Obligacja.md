# Zadanie 4 - obligacja kuponowa

W tym zadaniu zbudujesz model **obligacji kuponowej** i obliczysz jej wartość bieżącą na dany moment. Będziemy modelować prostą obligację z rocznymi kuponami, wypłacanymi co 12 miesięcy.

Dowiesz się, jak:
- określić momenty płatności kuponów i nominału,
- wyznaczyć wartość bieżącą przepływów pieniężnych,
- przetestować model w scenariuszach stresowych – z wyższą i niższą stopą procentową.

## 1 Utworzenie modelu

Pierwszym krokiem jest utworzenie nowego modelu o nazwie zadanie_4.

Otwórz powłokę Python i użyj poniższej komendy:

```python
from cashflower import create_model
create_model("zadanie_4")
```

## 2 Dane wejściowe

W tej części przygotujesz dane wejściowe dla modelu:

- datę wyceny (w planie biegów),
- parametry obligacji (model point set),
- stopę procentową.

### 2.1 Plan biegów (runplan)

Model będzie uruchamiany na dzień 31 grudnia 2024. Dodaj dane wyceny do planu biegów (`runplan`) – to tam trzymamy informacje dotyczące danej wersji modelu (np. datę wyceny lub wariant stresowy).

Uzupełnij poniższy kod w pliku `input.py`:

```python
from cashflower import ModelPointSet, Runplan
import pandas as pd

runplan = Runplan(data=pd.DataFrame({
    "version": [1],
    "valuation_year": [_____],
    "valuation_month": [_____], 
}))
```

**Zadanie:**
Ustaw rok i miesiąc wyceny zgodnie z treścią zadania. Zapisz miesiąc jako liczbę.

### 2.2 Parametry obligacji (model point set)

Utwórz model point set o nazwie `bond`, który zawiera dane jednej obligacji:

- nominał: 1 000 zł (`nominal`),
- roczna stopa kuponowa: 3% (`coupon_rate`),
- czas trwania: 120 miesięcy (`term`),
- data emisji: czerwiec 2024 (`issue_year`, `issue_month`).

Uzupełnij szkielet kodu:

```python
bond = ModelPointSet(data=pd.DataFrame({
    "nominal": [_____],
    "coupon_rate": [_____],
    "term": [_____],
    "issue_year": [_____],
    "issue_month": [_____],
}))
```

**Zadanie:**
Wstaw brakujące wartości zgodnie z opisem obligacji.


## 2.3 Stopa procentowa

Dodaj zmienną `base_interest_rate`, która zawiera miesięczną stopę procentową: 0.2%.

W pliku `input.py` dopisz:

```python
base_interest_rate = _____
```

**Zadanie:**
Uzupełnij wartość jako ułamek dziesiętny.

## 3 Model

W tej części zbudujesz zmienne potrzebne do wyznaczenia przepływów pieniężnych i ich wartości bieżącej.

### 3.1 Import danych

Na początku zaimportuj dane wejściowe z pliku `input.py`.

Uzupełnij kod w `model.py`:

```python
from input import _____, _____, _____
```

**Zadanie:**
Zaimportuj trzy zmienne:
- plan biegów,
- model point set obligacji,
- bazową stopę procentową.


### 3.2 Ostatni miesiąc obligacji (`t_end`)

Oblicz, ile miesięcy zostało do końca życia obligacji (czyli ile miesięcy jeszcze pozostało do momentu wykupu, licząc od daty wyceny).

Aby to zrobić:
- określ, ile miesięcy minęło od emisji obligacji do daty wyceny (`months_elapsed`),
- odejmij tę wartość od całkowitego czasu trwania obligacji (`term`).

Uzupełnij funkcję:

```python
@variable()
def t_end():
    months_elapsed = (runplan.get("_____") - bond.get("_____")) * 12 + (runplan.get("_____") - bond.get("_____"))
    return bond.get("_____") - months_elapsed
```
**Zadanie:**

Uzupełnij brakujące atrybuty:
- rok i miesiąc wyceny (`valuation_year`, `valuation_month`),
- rok i miesiąc emisji (`issue_year`, `issue_month`),
- czas trwania (`term`).


### 3.3 Miesiąc kalendarzowy

Zamodeluj zmienną `calendar_month(t)`, która wskazuje miesiąc kalendarzowy dla każdego okresu t.

Założenia:
- W miesiącu wyceny wartość kalendarzowa to `valuation_month`,
- W kolejnych miesiącach zwiększamy tę wartość o 1,
- Gdy osiągniemy 12, zaczynamy od 1 (czyli: po grudniu następuje styczeń).

Uzupełnij kod funkcji:

```python
@variable()
def calendar_month(t):
    if t == 0:
        return runplan.get("_____")
    elif calendar_month(t - 1) == _____:
        return _____
    else:
        return calendar_month(t - 1) + 1
```

**Zadanie**:
Uzupełnij:
- nazwę atrybutu z miesiącem wyceny,
- sprawdzany miesiąc końca roku (`12`),
- wartość miesiąca początkowego (`1`).



### 3.4 Kupon

Obligacja wypłaca kupon raz w roku – zawsze w tym samym miesiącu, w którym została wyemitowana. W naszym przykładzie jest to czerwiec, bo `issue_month = 6`.

Wartość kuponu to iloczyn:
- nominału (`nominal`)
- oraz stopy kuponowej (`coupon_rate`).

Kupon wypłacany jest tylko:
- jeśli bieżący miesiąc (`calendar_month`) jest równy `issue_month`,
- i jeśli nie minął jeszcze koniec okresu (`t <= t_end()`).

Uzupełnij kod:

```python
@variable()
def coupon(t):
    if calendar_month(t) == bond.get("_____") and t <= t_end():
        return bond.get("_____") * bond.get("_____")
    else:
        return 0
```

**Zadanie:**
Wstaw:
- nazwę atrybutu z miesiącem emisji,
- nazwę atrybutu z nominałem,
- nazwę atrybutu ze stopą kuponową.


### 3.5 Wypłata nominału

Na koniec życia obligacji wypłacany jest nominał.

Uzupełnij funkcję:

Podpowiedź:

```python
@variable()
def nominal_value(t):
    if t == t_end():
        return bond.get("_____")
    return 0
```

**Zadanie:**
Wstaw nazwę atrybutu z wartością nominału.




### 3.6 Wartość bieżąca

Wartość bieżąca to suma zdyskontowanych przyszłych przepływów pieniężnych.
- Dla ostatniego okresu: `coupon` + `nominal_value`,
- W pozostałych: ta sama suma plus wartość bieżąca przyszłego okresu, zdyskontowana miesięczną stopą procentową.

W ostatnim miesiącu (`T_MAX_CALCULATION`) nie ma już kolejnych okresów, więc bierzemy tylko kupon i nominał.

Uzupełnij kod funkcji:

```python
from settings import settings

@variable()
def present_value(t):
    if t == settings["_____"]:
        return coupon(t) + nominal_value(t)
    v = 1 / (1 + base_interest_rate)
    return coupon(t) + nominal_value(t) + v * _____
```

**Zadanie:**
- Wstaw nazwę ustawienia z `settings.py`, która określa ostatni miesiąc,
- Wstaw wywołanie zmiennej z wartością bieżącą kolejnego okresu.







## 4 Scenariusze stresowe

Wartość bieżąca obligacji zależy od przyjętej stopy procentowej. Sprawdź, jak zmienia się wycena obligacji w trzech scenariuszach:

- scenariusz bazowy – bez zmian stopy,
- scenariusz wzrostu stopy procentowej,
- scenariusz spadku stopy procentowej.

### 4.1 Wersje w planie biegów

Dodaj kolumnę `stress` do planu biegów i dopisz dwie nowe wersje:
- wersja 1 - scenariusz bazowy (`stress = 0` ),
- wersja 2 - stopa wzrasta o 10% (`stress = 0.1`),
- wersja 3 - stopa maleje o 10% (`stress = -0.1`).

Uzupełnij poniższy kod:

```python
runplan = Runplan(data=pd.DataFrame({
    "version": [1, _____, _____],
    "valuation_year": [2024, 2024, 2024],
    "valuation_month": [12, 12, 12],
    "stress": [0, _____, _____]
}))
```

**Zadanie:**
Wstaw odpowiednie numery wersji (`2`, `3`) i wartości stresu (`0.1`, `-0.1`).

### 4.2 Zmienna dla stopy procentowej

Zamiast używać `base_interest_rate` bezpośrednio, utwórz nową zmienną `interest_rate()`, która modyfikuje stopę procentową zgodnie ze scenariuszem.

```python
@variable()
def interest_rate():
    return base_interest_rate * (1 + runplan.get("_____"))
```

**Zadanie:**
Wstaw nazwę atrybutu zawierającego stres w planie biegów.

### 4.3 Aktualizacja zmiennej `present_value`

Zmień kod funkcji `present_value`, tak aby korzystała z nowej zmiennej `interest_rate()` zamiast `base_interest_rate`.

```python
@variable()
def present_value(t):
    if t == settings["T_MAX_CALCULATION"]:
        return coupon(t) + nominal_value(t)
    v = 1 / (1 + interest_rate())
    return coupon(t) + nominal_value(t) + v * present_value(t + 1)
```

**Zadanie:**
Nie musisz nic dopisywać – upewnij się tylko, że korzystasz ze zmiennej `interest_rate()` (a nie z bazowej stopy `base_interest_rate`).

### 4.4 Uruchamianie wersji w terminalu

Uruchom różne wersje modelu, aby zobaczyć wpływ stresu na wartość obligacji.

```bash
cd zadanie_4

python run.py             # wersja 1 (domyślna)
python run.py --version 2
python run.py --version 3

```

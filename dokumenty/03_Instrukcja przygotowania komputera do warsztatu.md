# Przygotowanie komputera do warsztatu z modelowania aktuarialnego w Pythonie

**Drogi Uczestniku!**
Przed warsztatem proszę przejdź przez poniższe instrukcje z odpowiednim wyprzedzeniem – dzięki temu będziemy mogli wcześniej rozwiązać ewentualne trudności.

Jeśli napotkasz jakikolwiek problem, śmiało napisz do mnie – najlepiej od razu dołączając zrzut ekranu pokazujący, co poszło nie tak. Mój adres e-mail to: zchmielewska@gmail.com.

## 01. Wstęp

Już wkrótce weźmiesz udział w warsztacie z modelowania aktuarialnego w Pythonie. Żeby maksymalnie wykorzystać czas zajęć, warto wcześniej przygotować swój komputer.

Najlepiej korzystać z komputera osobistego, a nie służbowego – firmowe urządzenia często mają ograniczenia w instalacji nowych programów i tylko administrator może wprowadzać zmiany. Do udziału w warsztacie wystarczy zwykły komputer o przeciętnych parametrach.

Potrzebne nam będą:  
– Python (wraz z pakietem `cashflower`)  
– środowisko programistyczne (IDE), np. PyCharm

Za chwilę pokażę, jak je zainstalować krok po kroku.

## 02.  Instalacja Pythona

Aby zainstalować Pythona, wejdź na stronę [python.org](https://www.python.org). Następnie przejdź do sekcji "Downloads" i wybierz wersję odpowiednią dla Twojego systemu operacyjnego (zwykle "Windows").  
Wybierz stabilną wersję Pythona, np. "3.12.10".

![01](C:\Users\admin\Desktop\kaszflołek\02_Print screens\01.PNG)

Po pobraniu pliku instalacyjnego, uruchom go. 

![02](C:\Users\admin\Desktop\kaszflołek\02_Print screens\02.PNG)

W trakcie instalacji zaznacz opcję „Add python.exe to PATH”. Następnie kliknij „Install Now”.

<img src="C:\Users\admin\Desktop\kaszflołek\02_Print screens\03.PNG" alt="03" width="600" />

Aby upewnić się, że Python został zainstalowany poprawnie, otwórz **Windows PowerShell** i wpisz:

```bash
python --version
```
![04](C:\Users\admin\Desktop\kaszflołek\02_Print screens\04.PNG)

Powinna pojawić się informacja o zainstalowanej wersji Pythona, np. „3.12.10”.

## 03.  Instalacja IDE (PyCharm)

IDE (Integrated Development Environment) to środowisko programistyczne, które ułatwia pisanie kodu. Podczas warsztatu będę korzystać z **PyCharm**, więc zachęcam, abyś również go zainstalował/a. PyCharm dostępny jest w wersji płatnej i darmowej, a nam wystarczy wersja bezpłatna.

Aby zainstalować PyCharm, wejdź na stronę [JetBrains](https://www.jetbrains.com/pycharm/download/) i kliknij „Download”.  

![05](C:\Users\admin\Desktop\kaszflołek\02_Print screens\05.PNG)

Po pobraniu pliku uruchom instalator.

<img src="C:\Users\admin\Desktop\kaszflołek\02_Print screens\06.PNG" alt="06" width="600" />

Podczas instalacji, zaznacz opcje zgodnie z preferencjami. Jeśli chcesz, możesz dodać PyCharm do menu kontekstowego systemu, co ułatwi późniejsze uruchamianie programu.

<img src="C:\Users\admin\Desktop\kaszflołek\02_Print screens\07.PNG" alt="07" width="600"/>

## 04.  Utworzenie projektu

1. Włącz PyCharm i wybierz **New Project**.

<img src="C:\Users\admin\Desktop\kaszflołek\02_Print screens\08.PNG" alt="08" width="800"/>

2. Wybierz folder, w którym ma znajdować się projekt. Python 3.12 powinien automatycznie się podlinkować.

<img src="C:\Users\admin\Desktop\kaszflołek\02_Print screens\09.PNG" alt="09" width="800" />

3. Kliknij symbol terminala „>\_” po lewej stronie, aby otworzyć okienko terminala. Wpisz:

```bash
pip install cashflower
```

Narzędzie `pip` zainstaluje pakiet `cashflower`, który będziemy wykorzystywać do budowania modeli cash flowowych. Po chwili proces instalacji powinien się zakończyć.

![10](C:\Users\admin\Desktop\kaszflołek\02_Print screens\10.PNG)

4. Następnie kliknij ikonę Pythona po lewej na dole, aby otworzyć powłokę Pythonową. Wpisz:

```python
from cashflower import create_model
```

Zaimportujesz funkcję `create_model` z biblioteki `cashflower`.

5. Wywołaj funkcję, wpisując nazwę swojego modelu:

```python
create_model(„moj_model”)
```

![11](C:\Users\admin\Desktop\kaszflołek\02_Print screens\11.PNG)

6. W drzewie projektu pojawi się nowy folder o nazwie modelu. Jeśli folder się nie pojawi, kliknij prawym przyciskiem myszy nazwę projektu i wybierz **Reload from Disk**.

![12](C:\Users\admin\Desktop\kaszflołek\02_Print screens\12.PNG)

7. Otwórz skrypt `run.py` i kliknij zielony trójkącik, aby uruchomić program. Powinien pojawić się nowy folder output z plikiem CSV.

![13](C:\Users\admin\Desktop\kaszflołek\02_Print screens\13.PNG)

**Gratulacje!** Twój pierwszy model został uruchomiony. Jesteś gotów na warsztat! 😊

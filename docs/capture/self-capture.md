# Samodzielne wykonywanie materiału

Samodzielny capture jest pełnoprawnym scenariuszem projektu. Dokumentacja rozróżnia dwa workflow: `moving_camera`, w którym osoba pozostaje nieruchoma, oraz `rotating_subject`, w którym kamera pozostaje nieruchoma, a osoba wykonuje kontrolowany obrót między zdjęciami.

Drugi wariant jest konieczny wtedy, gdy fotografowana osoba wykonuje całą sesję samodzielnie i nie może bezpiecznie przestawiać aparatu wokół siebie przy każdym ujęciu.

## Wariant A: kamera zmienia pozycję

Jest to wariant najbardziej zbliżony do klasycznej fotogrametrii statycznej.

1. Zaznacz pozycje stóp oraz kierunek patrzenia.
2. Ustaw aparat na statywie z pilotem lub timerem.
3. Po każdym zdjęciu przesuń aparat o 10-15° wokół osoby.
4. Zachowuj tę samą wysokość dla jednego pierścienia zdjęć.
5. Wykonaj osobne pierścienie dla wysokości klatki, barków i głowy.
6. Powtarzaj A-pose możliwie identycznie.

Ten workflow pozostaje preferowany, jeżeli dostępna jest druga osoba lub zautomatyzowany ruch kamery.

## Wariant B: osoba obraca się przed nieruchomą kamerą

Ten wariant jest oficjalnie wspierany przez Avatar Studio jako `rotating_subject`. Nie należy jednak traktować go jak zwykłej fotogrametrii nieruchomej sceny. Solve musi być prowadzony jako rekonstrukcja obiektu pierwszoplanowego, z ograniczeniem wpływu tła.

### Stanowisko

- aparat na stabilnym statywie;
- ręczny tryb ekspozycji i zablokowany focus;
- jednolite, matowe tło możliwe do łatwej segmentacji;
- równomierne miękkie światło, bez zmieniających się cieni na tle;
- na podłodze centralny punkt obrotu oraz oznaczenia kąta;
- dwa znaczniki ustawienia stóp;
- znacznik kierunku głowy lub wzroku;
- opcjonalna obrotowa platforma o małej wysokości, jeżeli jest stabilna i bezpieczna.

Nie należy umieszczać markerów fotogrametrycznych na nieruchomym tle i następnie używać ich do estymacji pozy kamery. W tym wariancie tło nie reprezentuje obracającego się obiektu.

## Geometria obrotu

Baseline dla całej sylwetki:

- krok główny: 10°;
- 36 pozycji na pełne 360°;
- minimum akceptowalne: 24 pozycje po 15°;
- profil wysokiej jakości: 48 pozycji po 7,5°;
- po zatrzymaniu odczekaj 2 s przed wykonaniem zdjęcia;
- po zmianie ustawienia stóp odczekaj 3 s.

Jeżeli rejestrowane są trzy wysokości aparatu, docelowa seria ma 72-108 zdjęć. Nie trzeba wykonywać wszystkich wysokości w jednej nieprzerwanej sekwencji.

## Obrót ciała

Najlepszy wariant to obrót całej osoby razem ze stopami, a nie skręcanie tułowia względem nieruchomych nóg.

1. Utrzymaj A-pose.
2. Wykonaj krok obrotowy całym ciałem.
3. Ustaw obie stopy zgodnie z oznaczeniem kolejnego kąta.
4. Ustaw miednicę, mostek i głowę w jednej osi.
5. Sprawdź położenie dłoni względem ud i tułowia.
6. Dopiero wtedy wykonaj zdjęcie.

Skręcanie wyłącznie tułowia powoduje zmianę anatomii między klatkami i jest zabronione dla serii rekonstrukcyjnej.

## Stabilizacja pozy

Dopuszczalny dryf między sąsiednimi zdjęciami powinien być mniejszy niż:

- głowa: 1°;
- łokcie: około 10 mm względem tułowia;
- dłonie: około 15 mm;
- miednica względem osi obrotu: około 10 mm;
- zmiana wysokości barków: około 10 mm.

Są to progi praktyczne do kontroli serii, a nie dokładność samej rekonstrukcji.

## Włosy i ubranie

Największym źródłem błędów w `rotating_subject` jest ruch wtórny.

- długie włosy należy tymczasowo ustabilizować tak, aby nie zmieniały układu między zdjęciami;
- luźna odzież nie może swobodnie falować;
- nie wykonuj zdjęcia bezpośrednio po gwałtownym obrocie;
- oddychaj spokojnie i wykonuj zdjęcia w podobnej fazie oddechu;
- nie zmieniaj napięcia mięśni ani ułożenia dłoni.

Właściwy wygląd włosów i ubrań zbiera się dodatkowo jako referencję, jeżeli ich stabilizacja była konieczna podczas rekonstrukcji geometrii ciała.

## Segmentacja i solve

Dla `rotating_subject` wymagane jest ograniczenie tła przed rekonstrukcją.

Preferowana procedura:

1. wyznacz maskę osoby dla każdego zdjęcia;
2. poszerz maskę o 3-8 px przy rozdzielczości około 4K, aby nie ucinać krawędzi włosów i sylwetki;
3. usuń z procesu matching cechy należące wyłącznie do nieruchomego tła;
4. sprawdź, czy rekonstrukcja zachowuje wspólny układ obiektu;
5. odrzuć zdjęcia z wyraźną zmianą pozy lub poruszeniem;
6. przeskaluj wynik na podstawie rzeczywistych pomiarów antropometrycznych.

Jeżeli wybrane narzędzie nie obsługuje dobrze rekonstrukcji obracającego się obiektu, dozwolone jest wykonanie części solve w narzędziu object-centric lub użycie masek i późniejsze połączenie segmentów w Blenderze.

## Automatyzacja zdjęć

Najpraktyczniejszy samodzielny workflow używa interwałometru, pilota Bluetooth, zegarka albo aplikacji aparatu z opóźnieniem.

Baseline:

- timer po wyzwoleniu: 3 s;
- opóźnienie po zajęciu pozy: minimum 2 s;
- ręczna ekspozycja;
- ręczny albo zablokowany AF;
- stały balans bieli;
- brak HDR i portrait mode;
- brak automatycznej zmiany obiektywu w telefonie.

## Kontrola jakości podczas sesji

Co 6 zdjęć, czyli około 60° dla kroku 10°, wykonaj kontrolę:

- ostrości twarzy i krawędzi sylwetki;
- położenia dłoni;
- wysokości barków;
- ustawienia stóp;
- braku zmiany ekspozycji;
- braku ruchu włosów i ubrania.

Po pełnym obrocie wykonaj szybki podgląd sekwencji jako animację. Nagły skok konturu oznacza błąd pozy i konieczność powtórzenia fragmentu.

## Tryb hybrydowy

Dla jednej osoby wykonującej zdjęcia samodzielnie zalecany jest tryb hybrydowy:

1. sylwetka 360° przez `rotating_subject`;
2. twarz i dłonie jako osobne serie przy nieruchomym ciele i zmianie położenia kamery lub statywu;
3. dokładne pomiary do nadania skali;
4. osobne referencje włosów, zarostu, ubrań i okularów.

Daje to lepszą jakość obszarów krytycznych bez rezygnowania z praktycznego wariantu obracającej się osoby.

## Czego nie robić

Nie obracaj się płynnie podczas pojedynczej serii zdjęć. Nie ekstraktuj klatek z filmu jako domyślnej metody. Nie skręcaj tułowia przy nieruchomych stopach. Nie zmieniaj ogniskowej, zoomu, ekspozycji ani oświetlenia w ramach jednej serii.

## Definition of Done

Wariant jest zapisany w manifeście jako `moving_camera` albo `rotating_subject`.

Dla `rotating_subject` wymagane są:

- opis kroku kątowego;
- sposób segmentacji tła;
- potwierdzenie stabilnej pozy;
- co najmniej jeden pełny obrót 360°;
- kontrola ciągłości sylwetki;
- nadanie skali z pomiarów rzeczywistych;
- odnotowanie odrzuconych klatek.

Szczegółowa procedura wariantu obracającej się osoby znajduje się również w [dedykowanym przewodniku](rotating-subject-capture.md).

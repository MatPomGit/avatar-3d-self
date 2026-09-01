# Kalibracja aparatu i kontrola jakości zdjęć

Kalibracja aparatu służy do opisania matematycznej relacji między sceną 3D a obrazem 2D. Fotogrametria może estymować część tych parametrów automatycznie, ale kontrolowana kalibracja zmniejsza ryzyko, że zniekształcenia obiektywu zostaną błędnie zinterpretowane jako geometria twarzy lub sylwetki.

## Parametry wewnętrzne aparatu

Parametry wewnętrzne (camera intrinsics) opisują między innymi ogniskową w pikselach, położenie punktu głównego oraz zniekształcenie obiektywu. Nie należy ręcznie przepisywać ich z odpowiednika ogniskowej dla pełnej klatki, ponieważ są to inne wielkości.

W praktyce:

- stała ogniskowa i stała rozdzielczość ułatwiają kalibrację;
- zmiana zoomu w połowie sesji tworzy nowy profil aparatu;
- cyfrowa stabilizacja obrazu może zmieniać efektywny kadr i powinna być wyłączona, jeśli urządzenie na to pozwala.

## Zniekształcenie promieniowe

Zniekształcenie promieniowe (radial distortion) wygina proste linie przede wszystkim przy brzegach kadru. Dodatnia lub ujemna korekcja może odpowiadać charakterowi beczkowemu albo poduszkowemu.

Jeżeli zniekształcenie jest niedoszacowane, kontur głowy i kończyn może być systematycznie wygięty. Jeżeli jest nadmiernie skorygowane, obraz zostaje rozciągnięty przy krawędziach.

Dlatego podczas capture twarzy i ciała preferujemy środkową część pola widzenia oraz umiarkowaną ogniskową zamiast szerokiego kąta.

## Wzorzec kalibracyjny

Do niezależnej kalibracji można użyć płaskiego wzorca szachownicowego lub innego wzorca o znanej geometrii. Powinien on być fotografowany:

- centralnie;
- blisko każdego narożnika kadru;
- pod kilkoma kątami;
- w co najmniej dwóch odległościach.

Typowa seria 15-30 ostrych zdjęć jest wystarczająca do kontroli stabilności modelu obiektywu. Większa liczba zdjęć nie kompensuje złej ostrości ani zbyt podobnych ujęć.

## Błąd reprojekcji

**Błąd reprojekcji (reprojection error)** mierzy odległość między obserwowanym punktem na zdjęciu a pozycją przewidywaną przez model 3D i parametry kamery. Mniejsza wartość zwykle oznacza lepszą zgodność modelu, ale bardzo niski wynik nie gwarantuje poprawnej geometrii, jeśli dopasowano niewłaściwy model do błędnych danych.

Praktyczna interpretacja dla rekonstrukcji wysokiej jakości:

- poniżej 0,5 px: bardzo dobry wynik;
- 0,5-1,0 px: zwykle dobry;
- 1,0-2,0 px: wymaga kontroli źródła błędów;
- powyżej 2,0 px: sygnał ostrzegawczy dla sesji statycznej.

Nie jest to uniwersalny próg dla każdego algorytmu. Należy równocześnie oglądać rozkład błędów i wynikową geometrię.

## Ostrość

Zdjęcie może mieć poprawną ekspozycję i nadal być bezużyteczne przez poruszenie lub nietrafioną ostrość. Kontrolę wykonujemy w powiększeniu 100%.

Dla twarzy sprawdzamy przede wszystkim:

- rzęsy;
- krawędzie tęczówki;
- pojedyncze włosy brody;
- krawędź ust;
- detal skóry.

Jeżeli te elementy są rozmyte na kilku kolejnych klatkach, należy powtórzyć sektor sesji.

## Ekspozycja

W serii rekonstrukcyjnej ważniejsza jest spójność niż estetyczny wygląd pojedynczego zdjęcia. Histogram nie powinien wskazywać rozległego obcięcia jasnych partii skóry. Niewielkie lokalne prześwietlenie punktowego refleksu jest mniej szkodliwe niż duże obszary bez informacji.

## Balans bieli

Stały balans bieli (white balance) zapewnia porównywalny kolor między zdjęciami. Automatyczny balans bieli może zmienić temperaturę barwową po obrocie osoby i utrudnić tworzenie spójnej tekstury.

Dla sesji rekonstrukcyjnej ustawiamy balans ręcznie lub blokujemy wartość automatycznie wyznaczoną przed rozpoczęciem serii.

## Kontrola przed właściwą sesją

Przed wykonaniem pełnej serii należy zrobić 8-12 zdjęć testowych obejmujących środek i skrajne kąty planowanej sekwencji. Dopiero po sprawdzeniu ostrości, ekspozycji i stabilności parametrów rozpoczynamy właściwy capture.

## Definition of Done

Kalibracja i kontrola jakości zaliczają etap, jeśli:

- ogniskowa, rozdzielczość i tryb aparatu są stałe w serii;
- wyłączono niepożądane dynamiczne przetwarzanie obrazu;
- błąd reprojekcji nie wykazuje systematycznych anomalii;
- klatki są ostre w skali 100%;
- balans bieli jest stabilny;
- profil aparatu i ustawienia sesji są zapisane w manifeście capture.

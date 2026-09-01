# COLMAP

COLMAP jest narzędziem do rekonstrukcji z ruchu kamery (Structure from Motion, SfM) i wielowidokowej rekonstrukcji stereo (Multi-View Stereo, MVS). W Avatar Studio służy do obliczania położenia kamer, rzadkiej geometrii sceny oraz, w odpowiednim wariancie, gęstej chmury punktów. Nie jest zależnością pakietu Python i nie powinien być uruchamiany jako duże zadanie obliczeniowe w CI.

## Co zmienia wybór trybu rekonstrukcji

W projekcie istnieją dwa różne warianty pozyskiwania zdjęć:

1. kamera porusza się wokół nieruchomej osoby;
2. osoba obraca się przed nieruchomą kamerą.

Pierwszy wariant jest zgodny z klasycznym założeniem SfM: scena jest statyczna, a zmienia się położenie kamery. Drugi wariant jest rekonstrukcją obiektocentryczną (object-centric reconstruction). W tym przypadku nie wolno bezrefleksyjnie interpretować pozycji oszacowanych przez COLMAP jako rzeczywistego ruchu kamery w świecie. Maski pierwszego planu i późniejsza normalizacja układu odniesienia są wtedy obowiązkowymi elementami potoku.

## Baza danych

COLMAP zapisuje wykryte punkty charakterystyczne, dopasowania i parametry kamer w bazie danych SQLite. Jest to artefakt pośredni, który należy zachować razem z konfiguracją sesji.

Nie kopiuj bazy danych między sesjami, jeśli zmieniły się obrazy, nazwy plików, rozdzielczość albo parametry aparatu.

## Model kamery

**Model kamery (camera model)** opisuje sposób rzutowania punktów 3D na obraz oraz parametry zniekształceń obiektywu. Zbyt prosty model może pozostawić systematyczne błędy na krawędziach kadru, natomiast zbyt złożony model przy małej liczbie danych może przeuczyć kalibrację.

Dla sesji wykonanej tym samym aparatem, tą samą rozdzielczością i stałą ogniskową preferuj współdzielenie parametrów wewnętrznych aparatu (camera intrinsics), zamiast niezależnego estymowania ich dla każdego zdjęcia.

Jeżeli kalibracja została wykonana wcześniej i jest wiarygodna, zachowaj ją jako punkt odniesienia. Nie poprawiaj automatycznie dobrze skalibrowanego aparatu tylko dlatego, że optymalizator potrafi zmienić większą liczbę parametrów.

## Ekstrakcja punktów charakterystycznych

**Ekstrakcja punktów charakterystycznych (feature extraction)** wyszukuje lokalne fragmenty obrazu, które można później rozpoznać w innych zdjęciach. Więcej punktów zwiększa szansę na dopasowanie trudnych obszarów, ale zwiększa czas i pamięć oraz może wprowadzać więcej punktów z tła.

Dla awatara problematyczne są:

- gładkie fragmenty skóry;
- jednolite ubrania;
- odbicia na okularach;
- włosy i broda zmieniające lokalny wygląd;
- poruszające się dłonie;
- tło widoczne pomiędzy kończynami.

Dlatego jakość sesji zdjęciowej jest ważniejsza niż maksymalne zwiększanie liczby cech.

## Dopasowanie cech

**Dopasowanie cech (feature matching)** łączy punkty charakterystyczne znalezione na różnych zdjęciach. Dla niewielkiej, uporządkowanej sesji dookoła człowieka można stosować dopasowanie wyczerpujące (exhaustive matching). W bardzo dużych zbiorach rośnie ono kosztowo wraz z liczbą par obrazów, więc należy rozważyć strategię sekwencyjną lub inną opartą na strukturze sesji.

Przy 36 zdjęciach jedna wysokość daje 630 nieuporządkowanych par obrazów. Przy 108 zdjęciach liczba par rośnie do 5778. Nie oznacza to automatycznie, że każdą parę należy porównywać w identyczny sposób.

## Rekonstrukcja rzadka

**Rekonstrukcja rzadka (sparse reconstruction)** wyznacza położenia kamer i trójwymiarowe punkty na podstawie zgodnych obserwacji w wielu zdjęciach. Jej głównym celem w Avatar Studio jest ocena, czy geometria sesji jest spójna, zanim uruchomiona zostanie kosztowna rekonstrukcja gęsta.

Sprawdź:

- ile zdjęć zostało zarejestrowanych w modelu;
- czy nie powstało kilka niezależnych modeli;
- rozkład punktów wokół osoby;
- błędy reprojekcji;
- odstające pozycje kamer;
- zgodność kierunku i skali po późniejszym wyrównaniu.

Jeżeli duża część zdjęć nie została zarejestrowana, nie przechodź od razu do MVS. Najpierw popraw problem w dopasowaniu, maskach albo materiale wejściowym.

## Błąd reprojekcji

**Błąd reprojekcji (reprojection error)** jest odległością na obrazie pomiędzy obserwowanym punktem a rzutem odpowiadającego mu punktu 3D. Jest zwykle wyrażany w pikselach. Niższa wartość oznacza lepszą zgodność modelu z obserwacjami, ale sama średnia nie mówi, czy błędy są równomierne.

Punkt startowy do diagnostyki sesji statycznej:

- poniżej 0,5 px: bardzo dobra zgodność;
- 0,5-1,0 px: zwykle dobra;
- 1,0-2,0 px: wymaga sprawdzenia rozkładu błędów;
- powyżej 2,0 px: sygnał ostrzegawczy.

Dla osoby obracającej się przed kamerą interpretacja jest trudniejsza, ponieważ założenie statycznej sceny jest naruszone przez resztkowe ruchy ciała. Progi nie są wtedy samodzielnym kryterium akceptacji.

## Maski

**Maska pierwszego planu (foreground mask)** wskazuje obszar obrazu należący do rekonstruowanej osoby. W wariancie osoby obracającej się przed kamerą maski są wymagane, ponieważ tło jest statyczne i inaczej może zdominować dopasowanie cech.

Przy rozdzielczości około 4K punkt startowy dla rozszerzenia maski poza sylwetkę wynosi 3-8 px. Zbyt mały margines odcina włosy i krawędzie odzieży. Zbyt duży wprowadza fragmenty tła.

Maskę zawsze kontroluj na włosach, palcach, przestrzeniach pomiędzy kończynami i przy oprawkach okularów.

## Gęsta rekonstrukcja

Po poprawnej rekonstrukcji rzadkiej typowy przepływ MVS jest następujący:

```text
image_undistorter
    ↓
patch_match_stereo
    ↓
stereo_fusion
    ↓
poisson_mesher lub delaunay_mesher
```

`image_undistorter` przygotowuje obrazy i parametry kamer dla gęstego etapu. `patch_match_stereo` wyznacza mapy głębokości i normalnych, a `stereo_fusion` łączy je w kolorową chmurę punktów. Siatka utworzona później nie jest jeszcze produkcyjną topologią awatara.

## Wykorzystanie GPU

Rekonstrukcja gęsta może zużywać dużo pamięci GPU. Zwiększenie rozdzielczości wejścia zwiększa szczegółowość, ale również koszt pamięci i czasu. Nie traktuj awarii z braku pamięci jako powodu do trwałego zmniejszenia jakości całego projektu. Najpierw sprawdź możliwość podziału zadania, parametry MVS i rozdzielczość roboczą.

## Windows

Sprawdzenie instalacji:

```powershell
colmap.exe -h
```

Przykładowa struktura prywatnego workspace:

```text
D:\AvatarStudio\projects\self-avatar\capture\
D:\AvatarStudio\projects\self-avatar\colmap\database.db
D:\AvatarStudio\projects\self-avatar\colmap\sparse\
D:\AvatarStudio\projects\self-avatar\colmap\dense\
```

Nie zapisuj bazy danych, zdjęć ani gęstych rekonstrukcji w publicznym repozytorium.

## Linux

Sprawdzenie:

```bash
colmap -h
which colmap
```

Przykładowa struktura:

```text
/home/<user>/AvatarStudio/projects/self-avatar/capture/
/home/<user>/AvatarStudio/projects/self-avatar/colmap/database.db
/home/<user>/AvatarStudio/projects/self-avatar/colmap/sparse/
/home/<user>/AvatarStudio/projects/self-avatar/colmap/dense/
```

## Raport sesji

Raport powinien zapisywać co najmniej:

- wersję COLMAP;
- system operacyjny i GPU;
- identyfikator manifestu zdjęć;
- SHA-256 listy obrazów lub manifestu;
- model kamery;
- ustawienia parametrów wewnętrznych aparatu;
- strategię dopasowania;
- liczbę zdjęć wejściowych i zarejestrowanych;
- liczbę modeli rzadkich;
- liczbę punktów 3D;
- statystyki błędu reprojekcji;
- informację o maskach;
- parametry etapu gęstego;
- nazwy i hashe artefaktów wynikowych.

## Osoba obracająca się przed kamerą

W tym wariancie:

1. tło musi być wyłączone z dopasowania przez maski;
2. osoba zatrzymuje się przed każdym zdjęciem;
3. obrazy dzieli się na sektory, jeśli pełna rekonstrukcja jest niestabilna;
4. wynik wyrównuje się do obiektocentrycznego układu odniesienia;
5. skala jest nadawana z rzeczywistych pomiarów, a nie z pozornych pozycji kamer;
6. dryf pozy ciała jest osobnym źródłem błędu i musi być oceniany wizualnie.

Nie należy opisywać tego wariantu jako klasycznego nieruchomego obiektu fotografowanego przez poruszającą się kamerę.

## Definition of Done

Etap COLMAP jest zaliczony, jeśli:

- wejściowe obrazy i maski są jednoznacznie powiązane z manifestem;
- parametry aparatu są zapisane;
- rekonstrukcja rzadka jest spójna i diagnostycznie zaakceptowana;
- nie ma niewyjaśnionych grup niezarejestrowanych zdjęć;
- raport zawiera statystyki błędów i wersje narzędzi;
- wynik gęsty ma zachowany ślad pochodzenia;
- wariant osoby obracającej się przed kamerą nie jest interpretowany jak klasyczny ruch kamery;
- żaden prywatny materiał zdjęciowy nie trafia do publicznego repozytorium.

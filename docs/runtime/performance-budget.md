# Budżet wydajności

Budżet wydajności (performance budget) określa, ile czasu obliczeniowego i pamięci może zużyć awatar, aby całe środowisko czasu rzeczywistego nadal osiągało wymagany poziom płynności. Nie jest to jedna liczba dotycząca wyłącznie liczby trójkątów. Koszt postaci składa się z geometrii, deformacji skóry, kształtów deformacyjnych twarzy, materiałów, włosów, tekstur, animacji i logiki sterującej.

## Czas pojedynczej klatki

Czas pojedynczej klatki (frame time) to czas dostępny na przygotowanie jednego obrazu. Jest odwrotnością liczby klatek na sekundę:

`frame_time_ms = 1000 / FPS`

Przykładowo:

| Cel | Dostępny czas na klatkę |
| ---: | ---: |
| 30 FPS | 33,33 ms |
| 60 FPS | 16,67 ms |
| 90 FPS | 11,11 ms |
| 120 FPS | 8,33 ms |

Zwiększenie docelowej liczby klatek na sekundę zmniejsza czas dostępny na każdą klatkę. Model, który działa stabilnie w 60 FPS, nie musi spełniać wymagań 90 FPS używanych np. w części zastosowań XR.

## Budżet demonstratora desktopowego

Dla pierwszego demonstratora PC przyjmujemy 60 FPS, czyli 16,67 ms na klatkę. Awatar nie powinien zużywać całego tego czasu.

Początkowy budżet produkcyjny:

| Składnik | Wartość docelowa |
| --- | ---: |
| animacja ciała i twarzy na CPU | <= 2,0 ms |
| renderowanie całej postaci na GPU | <= 8,0 ms |
| pozostała scena, logika i margines | >= 6,67 ms |

Wartości te są punktem startowym, a nie gwarancją dla każdego sprzętu.

## Percentyle czasu klatki

Średnia liczba FPS może ukrywać krótkie, ale widoczne przycięcia. Dlatego analizujemy percentyle czasu klatki.

- mediana opisuje typowe zachowanie;
- 95. percentyl pokazuje gorsze 5% klatek;
- 99. percentyl pokazuje rzadkie, ale zauważalne skoki.

Dla profilu 60 FPS przyjmujemy:

- mediana <= 16,67 ms;
- 95. percentyl <= 20 ms;
- 99. percentyl <= 33,3 ms;
- brak powtarzalnych skoków powyżej 50 ms.

Jeżeli średnia wynosi 60 FPS, ale 99. percentyl przekracza 50-80 ms, użytkownik będzie odczuwał nieregularne zacięcia mimo poprawnej średniej.

## Wywołania rysowania

Wywołanie rysowania (draw call) to polecenie wysyłane do procesora graficznego w celu narysowania określonej partii geometrii z konkretnym stanem materiału. Duża liczba osobnych materiałów i siatek zwiększa liczbę takich wywołań.

Nie istnieje jedna uniwersalna bezpieczna liczba. Dla awatara należy jednak mierzyć ją osobno i unikać sztucznego mnożenia slotów materiałowych. Przykładowo rozdzielenie skóry twarzy na dziesięć materiałów tylko z powodów organizacyjnych jest gorsze niż kilka logicznych materiałów o jasno określonej funkcji.

## Pamięć tekstur

Rezydentność tekstur (texture residency) oznacza, jaka część tekstur znajduje się aktualnie w pamięci procesora graficznego. Tekstura 8K nie zawsze musi być w całości obecna w pamięci, jeżeli silnik używa strumieniowania i niższych poziomów łańcucha mipmap.

W praktyce należy zapisywać:

- rozmiar tekstur na dysku;
- przybliżony koszt w pamięci GPU;
- najwyższy aktywny poziom mipmap;
- zachowanie po szybkim zbliżeniu kamery do twarzy.

Jeżeli po zbliżeniu twarz przez kilka sekund jest wyraźnie rozmyta, budżet pamięci lub konfiguracja strumieniowania może być zbyt agresywna.

## Koszt kształtów deformacyjnych

Sama liczba kształtów deformacyjnych nie opisuje pełnego kosztu. Ważne jest również, ile z nich jest ocenianych jednocześnie oraz ile wierzchołków zmieniają.

Dla twarzy zachowujemy pełny zestaw w LOD0, ale mierzymy:

- liczbę wszystkich kształtów;
- liczbę aktywnych jednocześnie;
- koszt ich oceny;
- koszt kształtów korekcyjnych;
- wpływ na pamięć.

## Włosy

System włosów może być jednym z najdroższych elementów postaci. Profil wydajności zapisuje oddzielnie koszt:

- włosów renderowanych jako pasma;
- płaszczyzn z teksturą włosów;
- cieni włosów;
- ruchu wtórnego;
- kolizji.

Jeżeli wyłączenie cieni włosów daje dużą poprawę czasu GPU, nie należy automatycznie pozostawiać ich wyłączonych. Najpierw trzeba ocenić, czy można obniżyć ich jakość bez zmiany sylwetki i odbioru twarzy.

## Procedura pomiarowa

Benchmark musi obejmować co najmniej:

1. neutralną pozę;
2. animację bezczynności;
3. pełną mimikę;
4. mowę z ruchem ust;
5. szybki obrót głowy;
6. przejście przez poziomy szczegółowości;
7. zbliżenie twarzy;
8. co najmniej 60 s ciągłego działania.

Dla problemów pamięci wykonujemy dodatkowo test 5-minutowy.

## Windows

Raport zapisuje wersję Windows, GPU, wersję sterownika, CPU, pamięć RAM, wersję silnika, backend renderera, rozdzielczość i ustawienia jakości.

## Linux

Raport zapisuje dystrybucję, wersję jądra, GPU, wersję sterownika, CPU, pamięć RAM, wersję silnika i backend renderera. Wyników Windows i Linux nie łączymy w jeden rekord.

## Kryterium zaliczenia

Profil wydajności jest zaliczony, jeśli:

- osiąga docelową liczbę FPS bez regularnych skoków czasu klatki;
- nie wykazuje narastającego zużycia pamięci;
- przełączanie poziomów szczegółowości nie powoduje skoków większych niż wynikające z samej zmiany jakości;
- koszt postaci jest oddzielony od kosztu całej sceny;
- test można powtórzyć na tej samej konfiguracji.
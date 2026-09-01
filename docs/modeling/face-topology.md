# Topologia twarzy

Topologia twarzy opisuje sposób rozmieszczenia wierzchołków, krawędzi i ścian siatki. W przypadku twarzy jej zadaniem nie jest wyłącznie odwzorowanie kształtu spoczynkowego. Musi także przewidywać kierunki deformacji podczas mrugania, mowy i ekspresji.

## Przepływ krawędzi

**Przepływ krawędzi (edge flow)** to układ kolejnych pętli krawędzi prowadzących przez siatkę. Dobry przepływ krawędzi prowadzi geometrię zgodnie z kierunkami deformacji skóry i struktur anatomicznych.

Zbyt rzadki przepływ powoduje kanciaste deformacje i utratę objętości. Zbyt gęsty może utrudniać rigowanie, zwiększać koszt kształtów deformacyjnych i utrwalać niepotrzebny szum rekonstrukcji.

## Gęstość geometrii

Nie ustalamy jednej absolutnej liczby wielokątów dla twarzy. Gęstość powinna być najwyższa tam, gdzie:

- zmienia się krzywizna powierzchni,
- występują duże deformacje,
- wymagane jest domknięcie powierzchni,
- obszar ma duże znaczenie percepcyjne.

W praktyce więcej geometrii wymaga okolica powiek, ust, skrzydeł nosa i bruzdy nosowo-wargowej niż płaska część czoła.

## Powieki

Powieki wymagają koncentrycznych pętli wokół oka. Ich geometria musi umożliwiać pełne domknięcie bez przenikania przez gałkę oczną.

Zalecenia:

- zachowaj ciągłą pętlę górnej i dolnej powieki,
- utrzymuj równomierną gęstość przy brzegu powieki,
- nie umieszczaj biegunów topologicznych bezpośrednio na linii brzegu powieki,
- zapewnij dodatkową geometrię w zewnętrznym i wewnętrznym kąciku oka.

Przy pełnym mrugnięciu nie powinien powstawać widoczny otwór między powiekami większy niż około 0,5 mm w skali modelu, chyba że referencja wskazuje inaczej.

## Usta

Wokół ust stosuj kilka koncentrycznych pętli. Muszą obsługiwać:

- pełne domknięcie warg,
- rozciągnięcie boczne,
- wysunięcie,
- zaokrąglenie,
- asymetrię lewa/prawa,
- unoszenie i opuszczanie kącików.

**Czerwień wargowa (vermilion)** powinna mieć geometrię pozwalającą zachować objętość przy kompresji. Zbyt mała liczba pętli powoduje spłaszczanie warg przy `mouthPucker` i `mouthFunnel`.

## Bruzda nosowo-wargowa

**Bruzda nosowo-wargowa (nasolabial fold)** jest dynamiczną strukturą biegnącą od okolicy skrzydła nosa w stronę kącika ust. Nie należy modelować jej jako głębokiego, stałego rowka. W neutralnej twarzy może być subtelna, a podczas uśmiechu staje się wyraźniejsza.

Topologia powinna pozwalać na lokalne zagęszczenie i zmianę krzywizny bez „złamania” policzka.

## Nos

Skrzydła nosa, podstawa nosa i okolica nozdrzy powinny mieć własny kontrolowany przepływ krawędzi. Przy ekspresjach takich jak `noseSneer` geometria nie może ciągnąć całej bocznej ściany nosa jako jednego bloku.

## Żuchwa i podbródek

Otwarcie żuchwy nie jest zwykłym obrotem dolnej części siatki. Tkanki policzka i podbródka zmieniają objętość, a dolna warga przemieszcza się inaczej niż broda.

Topologia powinna zapewniać:

- ciągłość od dolnej wargi do brody,
- dodatkowe pętle w bruździe wargowo-bródkowej,
- płynne przejście żuchwy w szyję.

## Bieguny topologiczne

**Biegun topologiczny (topological pole)** to wierzchołek, w którym zbiega się liczba krawędzi inna niż typowe cztery dla regularnej siatki czworokątów. Bieguny są potrzebne do przekierowywania przepływu, ale nie powinny znajdować się w miejscach o największej deformacji.

Dobre miejsca to względnie spokojne obszary czoła lub bocznej części policzka. Złe miejsca to brzeg powieki, kącik ust i środek bruzdy nosowo-wargowej.

## Testy przed rigowaniem

Przed tworzeniem pełnego układu twarzy wykonaj tymczasowe deformacje:

- `jawOpen` 0,25 / 0,5 / 1,0,
- `mouthSmileLeft/Right`,
- `mouthFrownLeft/Right`,
- `mouthPucker`,
- `mouthFunnel`,
- `eyeBlinkLeft/Right`,
- `eyeWideLeft/Right`,
- `browDownLeft/Right`.

Sprawdzaj nie tylko kształt końcowy, ale także wartości pośrednie. Siatka, która wygląda dobrze przy 0 i 1, może nadal dawać nienaturalne zapadanie przy 0,4-0,6.

## Kryteria akceptacji

Topologia jest gotowa, gdy:

- mrugnięcie zamyka oko bez zapadania powieki,
- usta mogą osiągnąć pełne domknięcie,
- policzek zachowuje objętość podczas uśmiechu,
- skrzydła nosa mogą deformować się lokalnie,
- otwarcie żuchwy nie tworzy ostrej granicy deformacji,
- asymetryczne ekspresje nie powodują skręcenia całej twarzy.
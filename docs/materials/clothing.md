# Materiały ubrań

Ubranie wpływa na podobieństwo postaci nie tylko przez kolor i krój. Materiał określa sposób odbijania światła, widoczność splotu, grubość krawędzi, zachowanie fałd oraz to, jak tkanina reaguje na ruch. Dlatego geometria ubrania, jego materiał i ruch wtórny muszą być projektowane razem.

## Chropowatość powierzchni

**Chropowatość (roughness)** opisuje, jak bardzo mikroskopijne nierówności powierzchni rozpraszają odbicie. Niska wartość daje wąskie i wyraźne odbicia, a wysoka rozmywa refleks.

Przykładowe wartości początkowe dla modelu GGX:

| Materiał | Wartość niska | Typowa | Wysoka | Efekt praktyczny |
| --- | ---: | ---: | ---: | --- |
| lakierowane tworzywo | 0,18 | 0,28 | 0,40 | od połysku do półmatu |
| skóra licowa | 0,28 | 0,38 | 0,55 | od nowej/polerowanej do zużytej |
| denim | 0,50 | 0,62 | 0,75 | matowa, wyraźnie włóknista powierzchnia |
| bawełna | 0,55 | 0,68 | 0,80 | szeroki, miękki refleks |
| wełna | 0,65 | 0,78 | 0,90 | bardzo rozproszone odbicie |

Są to wartości startowe, nie uniwersalne stałe. Jeżeli bawełna wygląda jak plastik, chropowatość jest zwykle za niska albo mapa normalnych jest zbyt słaba. Jeżeli skóra traci charakterystyczny połysk i wygląda jak kreda, wartość jest prawdopodobnie zbyt wysoka.

## Splot i mikrogeometria

**Mapa normalnych (normal map)** zmienia kierunek lokalnej normalnej powierzchni bez dodawania rzeczywistej geometrii. Dla ubrań służy przede wszystkim do odwzorowania włókien, splotu i drobnych zagnieceń.

Należy rozdzielić:

- detal splotu o skali poniżej kilku milimetrów, zwykle w mapie normalnych;
- fałdy średniej skali, które mogą pochodzić z mapy normalnych lub mapy przemieszczeń (displacement map);
- duże fałdy, które powinny być częścią geometrii albo deformacji ubrania.

Zbyt mocna mapa normalnych powoduje efekt „rzeźbionej” tkaniny. Zbyt słaba sprawia, że ubranie wygląda jak gładka folia.

## Grubość tkaniny

W miejscach widocznych z boku ubranie powinno mieć rzeczywistą grubość. Dla typowych ubrań codziennych można przyjąć orientacyjnie:

- cienka koszulka: 0,4-0,8 mm;
- koszula: 0,5-1,0 mm;
- denim: 0,8-1,5 mm;
- bluza: 1,5-3,0 mm;
- kurtka wielowarstwowa: lokalnie kilka milimetrów i więcej.

Wartość za mała daje papierowe krawędzie. Zbyt duża zmienia sylwetkę i zwiększa ryzyko kolizji z ciałem.

## Barwa bazowa

**Barwa bazowa (Base Color)** powinna zawierać rzeczywisty kolor materiału bez wypalonych cieni i odbić. W tkaninie można zachować lokalne różnice koloru wynikające z włókien, przetarć, szwów i zużycia.

Nie należy usuwać cech rozpoznawalnych konkretnego ubrania, jeżeli jest ono częścią docelowego wyglądu awatara.

## Metaliczność

**Metaliczność (metallic)** dla włókien, skóry naturalnej i tworzyw wynosi `0`. Wartość `1` stosujemy tylko dla rzeczywistych odsłoniętych metali, np. metalowego zamka lub sprzączki. Nie używamy metaliczności do sztucznego zwiększania połysku tkaniny.

## Rozwinięcie UV i gęstość tekseli

Ubrania mają niezależne rozwinięcie UV (UV unwrapping). Szwy UV powinny w miarę możliwości pokrywać się z rzeczywistymi szwami konstrukcyjnymi ubrania.

Typowa gęstość tekseli (texel density) dla wersji wzorcowej wynosi 8-16 px/cm. Elementy blisko twarzy, np. kołnierz, mogą otrzymać 16-24 px/cm, jeśli często występują w zbliżeniu.

## Ruch i materiał

Materiał należy oceniać także w animacji. Ta sama tekstura może wyglądać poprawnie w pozycji neutralnej, a źle po zgięciu łokcia lub biodra, jeśli splot rozciąga się razem z siatką w nienaturalny sposób.

Dla tkanin rozciągliwych dopuszczalna jest widoczna deformacja splotu. Dla sztywnych materiałów, takich jak gruby denim lub skóra, nadmierne rozciągnięcie tekstury jest błędem.

## Walidacja

Ubranie zalicza etap materiałowy, jeśli:

- typ włókna jest rozpoznawalny w neutralnym oświetleniu;
- chropowatość nie jest jednolita bez uzasadnienia;
- splot ma prawidłową skalę względem ciała;
- krawędzie mają wiarygodną grubość;
- metaliczność jest stosowana wyłącznie dla metalu;
- brak widocznego rozciągania tekstur w typowym zakresie ruchu;
- materiał pozostaje wiarygodny w świetle frontalnym, bocznym i pod światło.

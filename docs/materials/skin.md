# Skóra

Skóra jest materiałem wielowarstwowym. Fotorealizm wymaga równoczesnego odwzorowania pigmentacji, mikrogeometrii, odbicia powierzchniowego oraz rozpraszania podpowierzchniowego (Subsurface Scattering, SSS). Sama wysokiej jakości barwa bazowa (Base Color) i mapa normalnych (normal map) nie wystarczają do uzyskania wiarygodnej skóry w ruchu i zmiennym oświetleniu.

Terminologia jest zgodna ze [słownikiem terminologicznym](../project/terminology.md).

## Kanoniczny zestaw map

Minimalny zestaw produkcyjny:

- barwa bazowa (Base Color) lub albedo;
- mapa normalnych skali makro (macro normal map);
- mapa normalnych skali mikro (micro normal map);
- mapa chropowatości (roughness map);
- mapa okluzji otoczenia (Ambient Occlusion map, AO), tylko gdy używa jej środowisko docelowe (target environment);
- mapa przemieszczeń (displacement map) lub mapa wysokości (height map) dla LOD0 i wersji wzorcowej (master asset);
- maska rozpraszania podpowierzchniowego (SSS mask);
- opcjonalna mapa zagłębień (cavity map);
- opcjonalne mapy zmarszczek dynamicznych (dynamic wrinkle maps).

Barwa bazowa (Base Color) nie może zawierać wypalonych cieni, refleksów ani składowej odbicia zwierciadlanego (specular reflection).

## Parametry fizyczne i wartości bazowe renderera

Skóra jest dielektrykiem:

- metaliczność (metallic): `0`;
- współczynnik załamania światła powierzchni (Index of Refraction, IOR): około `1.40`;
- odpowiadający współczynnik odbicia Fresnela dla padania prostopadłego (normal-incidence Fresnel reflectance, F0): około `0.028`;
- w silnikach bez jawnego parametru IOR używamy poprawnego modelu odbicia dielektryka, a nie sztucznie zwiększonej metaliczności (metallic).

Chropowatość (roughness) jest parametrem modelu materiałowego, a nie uniwersalną stałą fizyczną. Dla modelu mikrofaset GGX przyjmujemy jako punkt startowy:

| Region | Chropowatość bazowa (roughness) | Typowy zakres strojenia |
| --- | ---: | ---: |
| czoło | 0.38 | 0.30-0.48 |
| nos i strefa T | 0.34 | 0.26-0.44 |
| policzki | 0.48 | 0.38-0.60 |
| okolice oczu | 0.52 | 0.42-0.64 |
| szyja | 0.50 | 0.40-0.62 |
| uszy | 0.46 | 0.36-0.58 |
| skórna część ust | 0.40 | 0.30-0.52 |

Wartości stroimy względem rzeczywistej osoby, referencyjnego oświetlenia i konkretnej implementacji dwukierunkowej funkcji rozkładu odbicia (Bidirectional Reflectance Distribution Function, BRDF).

## Rozpraszanie podpowierzchniowe

Rozpraszanie podpowierzchniowe (Subsurface Scattering, SSS) jest obowiązkowe w profilu fotorealistycznym. Bez niego skóra ma tendencję do wyglądu suchego, plastikowego lub kredowego.

Dla renderera obsługującego fizyczną skalę przyjmujemy orientacyjny efektywny promień rozpraszania (effective scattering radius):

- kanał czerwony R: `1.2 mm`;
- kanał zielony G: `0.55 mm`;
- kanał niebieski B: `0.25 mm`.

Są to wartości startowe, a nie pomiar konkretnej skóry. W silnikach używających znormalizowanego promienia rozpraszania podpowierzchniowego (normalized subsurface radius) zachowujemy proporcję kanałów i kalibrujemy amplitudę na podstawie referencji.

Priorytetowe obszary oceny:

- krawędzie uszu przy oświetleniu od tyłu (backlight);
- skrzydełka nosa;
- policzki;
- dolna część żuchwy;
- palce.

Zbyt duży promień rozpraszania (scattering radius) daje efekt wosku. Zbyt mały pozostawia zbyt twardą składową rozproszoną (diffuse component).

## Mikrogeometria

Rozdzielamy trzy pasma częstotliwości przestrzennej:

1. **skala makro (macro scale)**: bruzdy, większe fałdy i relief około 1-20 mm;
2. **skala pośrednia (meso scale)**: drobne zmarszczki i struktura 0,2-2 mm;
3. **skala mikro (micro scale)**: pory i bardzo drobna tekstura poniżej około 0,5 mm.

Nie próbujemy reprezentować wszystkich pasm jedną mapą normalnych (normal map).

Siła mapy normalnych skali mikro (micro normal strength) powinna być taka, aby pory były czytelne w zbliżeniu 1:1, ale praktycznie znikały przy średnim planie. Jeśli pory dominują twarz w standardowym ujęciu, amplituda jest zbyt duża.

## Barwa skóry

Albedo powinno zachować lokalne różnice: czerwień policzków i nosa, subtelne żyłki, przebarwienia, okolice zarostu, pieprzyki, blizny oraz różnice między twarzą, szyją, uszami i dłońmi.

Nie wolno automatycznie wyrównywać barwy skóry w sposób usuwający cechy identyfikujące osobę.

## Zmarszczki dynamiczne

Dla twarzy LOD0 zalecane są mapy zmarszczek dynamicznych (dynamic wrinkle maps) lub korekcyjne mapy normalnych i przemieszczeń (corrective normal/displacement maps), sterowane grupami FACS/ARKit.

Minimalny zestaw dynamiczny:

- czoło przy `browInnerUp` i `browOuterUp`;
- okolica gładzizny czoła (glabella) przy `browDown`;
- kurze łapki przy `eyeSquint`;
- bruzda nosowo-wargowa (nasolabial fold) przy `mouthSmile` i `cheekSquint`;
- okolice ust przy kanałach pucker/funnel.

Dynamiczny detal nie może pojawiać się skokowo. Wagi wygładzamy tą samą warstwą czasową co układ sterowania twarzą (facial rig).

## Rozdzielczość tekstur

Wartości bazowe dla wersji wzorcowej (master asset):

- twarz: minimum 4K, preferowane 8K, jeżeli źródła rzeczywiście zawierają taki detal;
- ciało: 4K na kafel w systemie kafli tekstur UDIM (UDIM texture tiling);
- dłonie: efektywnie minimum 2K na dłoń, preferowane 4K dla zbliżeń;
- mapa normalnych skali mikro (micro normal map) może być kafelkowana niezależnie od albedo.

Środowisko czasu rzeczywistego (runtime environment) może używać niższych poziomów łańcucha mipmap (mipmap chain) i poziomów szczegółowości (LOD), ale wersja wzorcowa pozostaje niezmieniona.

## Walidacja

Materiał skóry zalicza etap, jeśli:

- barwa bazowa (Base Color) nie zawiera refleksów ani wypalonych cieni;
- metaliczność (metallic) jest równa zero;
- chropowatość (roughness) ma lokalną zmienność;
- rozpraszanie podpowierzchniowe (SSS) jest widoczne, ale nie daje woskowego wyglądu;
- pory nie są przeskalowane;
- odcień twarzy i szyi jest spójny;
- charakterystyczne cechy osoby nie zostały wygładzone;
- materiał pozostaje wiarygodny w świetle przednim (front light), bocznym (side light) i tylnym (backlight).
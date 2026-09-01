# Skóra

Skóra jest materiałem wielowarstwowym. Fotorealizm wymaga równoczesnego odwzorowania pigmentacji, mikrogeometrii, refleksu powierzchniowego oraz subsurface scattering. Samo wysokiej jakości albedo i normal map nie wystarczają do uzyskania wiarygodnej skóry w ruchu i zmiennym oświetleniu.

## Kanoniczny zestaw map

Minimalny zestaw produkcyjny:

- Base Color / Albedo;
- Normal macro;
- Normal micro;
- Roughness;
- Ambient Occlusion tylko tam, gdzie target workflow go wykorzystuje;
- Displacement lub Height dla LOD0/offline master;
- maska SSS/scatter;
- opcjonalna cavity/wrinkle mask;
- opcjonalne mapy dynamicznych zmarszczek.

Base Color nie może zawierać wypalonych cieni, highlightów ani specular reflection.

## Parametry fizyczne i baseline renderera

Skóra jest dielektrykiem:

- `metallic = 0`;
- baseline IOR powierzchni: około `1.40`;
- odpowiadający temu Fresnel F0: około `0.028`;
- dla rendererów bez jawnego IOR należy korzystać z ich dielektrycznego modelu specular zamiast sztucznie zwiększać metalness.

Roughness jest parametrem workflow, nie uniwersalną stałą fizyczną. Dla GGX jako punkt startowy przyjmujemy:

| Region | Baseline roughness | Typowy zakres strojenia |
| --- | ---: | ---: |
| czoło | 0.38 | 0.30-0.48 |
| nos / T-zone | 0.34 | 0.26-0.44 |
| policzki | 0.48 | 0.38-0.60 |
| okolice oczu | 0.52 | 0.42-0.64 |
| szyja | 0.50 | 0.40-0.62 |
| uszy | 0.46 | 0.36-0.58 |
| usta, część skórna | 0.40 | 0.30-0.52 |

Wartości trzeba stroić względem rzeczywistej osoby, warunków referencyjnego oświetlenia i konkretnej implementacji BRDF.

## Subsurface scattering

SSS jest obowiązkowy w profilu fotorealistycznym. Bez niego skóra ma tendencję do wyglądu suchego, plastikowego lub kredowego.

Jako baseline dla efektywnego promienia rozpraszania w rendererze obsługującym fizyczną skalę przyjmujemy orientacyjnie:

- R: `1.2 mm`;
- G: `0.55 mm`;
- B: `0.25 mm`.

Są to wartości startowe, a nie pomiar konkretnej skóry. W rendererach używających znormalizowanego `subsurface radius` należy zachować proporcję kanałów i skalibrować amplitudę wizualnie na podstawie referencji.

Priorytetowe obszary oceny:

- krawędzie uszu przy świetle zza postaci;
- skrzydełka nosa;
- policzki;
- dolna część żuchwy;
- palce.

Zbyt duży radius daje efekt wosku. Zbyt mały pozostawia twardy, syntetyczny diffuse.

## Mikrogeometria

Rozdzielamy trzy pasma częstotliwości:

1. **macro**: bruzdy, większe fałdy i relief około 1-20 mm;
2. **meso**: drobne zmarszczki i struktura 0,2-2 mm;
3. **micro**: pory i bardzo drobna tekstura poniżej około 0,5 mm.

Nie należy próbować reprezentować wszystkich częstotliwości jedną normal mapą.

Baseline siły mikro-normal powinien być taki, aby pory były czytelne w zbliżeniu 1:1, ale praktycznie znikały przy średnim planie. Jeśli pory pozostają dominującym elementem twarzy przy standardowym ujęciu, amplituda jest za wysoka.

## Kolor skóry

Albedo powinno zachować lokalne różnice:

- czerwień policzków i nosa;
- subtelne żyłki;
- przebarwienia;
- okolice zarostu;
- pieprzyki, blizny i charakterystyczne cechy;
- różnice między twarzą, szyją, uszami i dłońmi.

Nie wolno automatycznie wyrównywać koloru skóry w sposób usuwający cechy identyfikujące osobę.

## Dynamiczne zmarszczki

Dla LOD0 twarzy zalecane są wrinkle maps lub corrective normal/displacement sterowane grupami FACS/ARKit. Minimalny zestaw dynamiczny:

- czoło przy `browInnerUp`/`browOuterUp`;
- glabella przy `browDown`;
- kurze łapki przy `eyeSquint`;
- nasolabial fold przy `mouthSmile`/`cheekSquint`;
- okolice ust przy pucker/funnel.

Dynamiczny detal nie może pojawiać się skokowo. Wagi należy wygładzać tą samą warstwą czasową co facial rig.

## Rozdzielczość

Baseline master:

- twarz: 4K minimum, 8K master jeśli źródła na to pozwalają;
- ciało: 4K na UDIM;
- dłonie: minimum efektywnie 2K na dłoń, preferowane 4K w zbliżeniach;
- micro normal może być kafelkowany i niezależny od albedo.

Runtime może używać niższych mip/LOD, ale master pozostaje niezmieniony.

## Walidacja

Materiał skóry zalicza etap, jeśli:

- nie zawiera highlightów ani cieni w Base Color;
- metalness jest zerowy;
- roughness ma lokalną zmienność;
- SSS jest widoczny, ale nie powoduje woskowego wyglądu;
- pory nie są przeskalowane;
- odcień twarzy i szyi jest spójny;
- charakterystyczne cechy osoby nie zostały wygładzone;
- materiał pozostaje wiarygodny w świetle frontalnym, bocznym i backlight.

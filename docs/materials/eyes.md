# Materiały i geometria oczu

Realistyczne oko należy traktować jako wielowarstwowy układ optyczny. Jedna tekstura na kuli nie zapewnia poprawnego odbicia, załamania światła (refraction) ani paralaksy (parallax) tęczówki.

Terminologia materiałowa jest zgodna ze [słownikiem terminologicznym](../project/terminology.md).

## Wymiary bazowe

| Parametr | Wartość bazowa | Zakres strojenia |
| --- | ---: | ---: |
| średnica gałki ocznej | 24.0 mm | 23-25 mm |
| średnica widocznej tęczówki | 11.8 mm | 11-12.5 mm |
| średnica źrenicy w stanie neutralnym | 3.5 mm | 2-5 mm |
| dynamiczny zakres średnicy źrenicy | 2-8 mm | zależny od światła |
| współczynnik załamania światła rogówki (Index of Refraction, IOR) | 1.376 | 1.37-1.38 |
| współczynnik załamania światła cieczy łzowej (Index of Refraction, IOR) | 1.336 | 1.33-1.34 |

Wymiary osoby referencyjnej mają pierwszeństwo przed wartościami bazowymi.

## Warstwy

Minimalnie rozdzielamy:

1. gałkę oczną i twardówkę;
2. tęczówkę z rzeczywistym lub realizowanym przez program cieniujący (shader) zagłębieniem;
3. źrenicę;
4. przezroczystą rogówkę;
5. menisk łzowy na styku powieki i oka.

Wysokiej jakości poziom szczegółowości LOD0 może dodatkowo zawierać geometrię rąbka rogówki (limbus) i subtelne nierówności powierzchni oka.

## Rogówka

Rogówka powinna mieć własną wypukłość i punkt obrotu zgodny z gałką oczną. Nie należy symulować jej wyłącznie mapą normalnych (normal map).

Wartości bazowe:

- współczynnik załamania światła (Index of Refraction, IOR): `1.376`;
- chropowatość powierzchni optycznej (roughness): `0.01-0.04` w modelu mikrofaset GGX;
- metaliczność (metallic): `0`;
- załamanie światła (refraction) aktywne, jeśli środowisko docelowe (target environment) je obsługuje;
- w środowisku bez załamania światła stosujemy kontrolowaną paralaksę tęczówki (iris parallax), zamiast płaskiej tekstury.

## Twardówka

Twardówka nie jest czysto biała. Powinna zawierać lekko ciepły odcień, delikatne żyłki, subtelną zmienność chropowatości (roughness) oraz niewielkie rozpraszanie podpowierzchniowe (Subsurface Scattering, SSS) lub transmisję światła (translucency), jeśli model cieniowania (shading model) to obsługuje.

Wartość bazowa chropowatości (roughness) twardówki: `0.35-0.50`. Żyłki nie mogą być kontrastowe w średnim planie.

## Tęczówka

Tęczówka wymaga rzeczywistej lub realizowanej przez program cieniujący (shader) głębi.

Zalecenia:

- radialna mikrostruktura;
- niezależna barwa bazowa (Base Color) i detal;
- ciemniejszy pierścień rąbkowy (limbal ring);
- brak refleksu zapisanego na stałe w teksturze;
- rozszerzanie źrenicy (pupil dilation) nie może skalować całej tęczówki.

Jeżeli używana jest paralaksa (parallax), przesunięcie wizualne powinno odpowiadać zagłębieniu około `0.4-0.8 mm`.

## Źrenica

W neutralnym oświetleniu przyjmujemy około `3.5 mm` średnicy. Środowisko czasu rzeczywistego (runtime environment) może modulować ją w zakresie `2-8 mm`.

Dynamika źrenicy jest znacznie wolniejsza niż sakkada (saccade). Przyjmujemy:

- zwężanie po wzroście luminancji: stała czasowa (time constant) około `0.6 s`;
- rozszerzanie po spadku luminancji: około `1.2 s`;
- brak losowego pulsowania bez uzasadnienia fizjologicznego.

Jeżeli środowisko docelowe (target environment) nie dostarcza informacji o luminancji sceny, źrenica pozostaje na wartości profilu zamiast wykonywać losowe zmiany.

## Menisk łzowy

Menisk łzowy ma duży wpływ na fotorealizm zbliżenia.

Wartości bazowe:

- cienki pas geometrii przy dolnej powiece;
- chropowatość (roughness): `0.01-0.03`;
- współczynnik załamania światła (Index of Refraction, IOR): około `1.336`;
- brak przesadnej grubości;
- ciągłość w kącikach oka.

## Powieki i kontakt z gałką

Materiał oka musi być walidowany razem z geometrią powiek.

Wymagania:

- brak szczeliny między powieką a okiem;
- brak penetracji rogówki podczas mrugnięcia (blink);
- poprawne śledzenie powieki za ruchem oka (eyelid follow);
- zachowany kontakt rzęs z powieką;
- poprawne zachowanie spojrzenia w górę, dół i na boki.

## Kryteria ukończenia

Oko zalicza etap, jeśli:

- ma niezależną rogówkę i tęczówkę;
- refleks pochodzi z powierzchni rogówki, a nie z tekstury;
- twardówka nie jest czysto biała;
- średnica i położenie tęczówki odpowiadają referencji;
- źrenica ma poprawną skalę;
- menisk łzowy jest widoczny tylko w odpowiednim zbliżeniu;
- nie występuje penetracja powiek;
- oba oczy zachowują ten sam model optyczny.
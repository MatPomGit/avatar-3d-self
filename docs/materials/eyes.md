# Materiały i geometria oczu

Realistyczne oko należy traktować jako układ optyczny kilku warstw. Jedna tekstura na kuli nie zapewnia poprawnych refleksów, refrakcji ani parallax tęczówki.

## Wymiary bazowe

Dla dorosłego oka przyjmujemy jako punkt startowy:

| Parametr | Baseline | Zakres strojenia |
| --- | ---: | ---: |
| średnica gałki ocznej | 24.0 mm | 23-25 mm |
| średnica widocznej tęczówki | 11.8 mm | 11-12.5 mm |
| źrenica neutralna | 3.5 mm | 2-5 mm |
| zakres dynamiczny źrenicy | 2-8 mm | zależny od światła |
| IOR rogówki | 1.376 | 1.37-1.38 |
| IOR cieczy/łez | 1.336 | 1.33-1.34 |

Wymiary osoby referencyjnej mają pierwszeństwo przed baseline.

## Warstwy

Minimalnie rozdziel:

1. gałkę oczną/twardówkę;
2. tęczówkę z fizycznym lub shaderowym zagłębieniem;
3. źrenicę;
4. przezroczystą rogówkę;
5. menisk łzowy na styku powieki i oka.

Wysokiej jakości LOD0 może dodatkowo zawierać geometrię limbusu i subtelne nierówności powierzchni oka.

## Rogówka

Rogówka powinna mieć własną wypukłość i punkt obrotu zgodny z gałką oczną. Nie należy symulować jej wyłącznie normal mapą.

Baseline:

- `IOR = 1.376`;
- roughness optycznej powierzchni: `0.01-0.04` w workflow GGX;
- metalness = 0;
- refrakcja aktywna, jeśli target engine ją obsługuje;
- w środowisku bez refrakcji należy użyć kontrolowanego parallax tęczówki zamiast płaskiej tekstury.

## Twardówka

Twardówka nie jest czysto biała.

Powinna zawierać:

- lekko ciepły odcień;
- delikatne żyłki;
- subtelną zmienność roughness;
- minimalne SSS/translucency, jeśli renderer to obsługuje.

Baseline roughness twardówki: `0.35-0.50`. Żyłki nie mogą być kontrastowe w średnim planie.

## Tęczówka

Tęczówka wymaga rzeczywistej lub shaderowej głębi.

Zalecenia:

- radialna mikrostruktura;
- niezależny kolor bazowy i detal;
- ciemniejszy limbal ring;
- brak płaskiego highlightu należącego do tekstury;
- pupil dilation nie może skalować całej tęczówki.

Jeżeli używany jest parallax, przesunięcie wizualne powinno odpowiadać zagłębieniu około `0.4-0.8 mm`.

## Źrenica

W neutralnym oświetleniu baseline to około `3.5 mm` średnicy. Runtime może modulować ją w zakresie `2-8 mm`.

Dynamika źrenicy jest znacznie wolniejsza niż sakkada. W projekcie przyjmujemy:

- zwężanie po wzroście światła: time constant około `0.6 s`;
- rozszerzanie po spadku światła: około `1.2 s`;
- bez pulsowania proceduralnego bez uzasadnienia.

Jeżeli target nie ma informacji o luminancji sceny, źrenica pozostaje na wartości profilu zamiast wykonywać losowe zmiany.

## Menisk łzowy

Menisk łzowy ma duży wpływ na fotorealizm zbliżenia.

Baseline:

- cienki pas geometrii przy dolnej powiece;
- roughness `0.01-0.03`;
- IOR około `1.336`;
- brak przesadnej grubości;
- ciągłość w kącikach oka.

## Powieki i kontakt z gałką

Materiał oka musi być walidowany razem z geometrią powiek.

Wymagania:

- brak szczeliny między powieką a okiem;
- brak penetracji rogówki podczas blink;
- poprawny eyelid follow;
- zachowany kontakt rzęs z powieką;
- poprawne zachowanie spojrzenia w górę, dół i na boki.

## Definition of Done

Oko zalicza etap, jeśli:

- ma niezależną rogówkę i tęczówkę;
- refleks pochodzi z powierzchni rogówki, nie z tekstury;
- twardówka nie jest czysto biała;
- średnica i położenie tęczówki odpowiadają referencji;
- źrenica ma poprawną skalę;
- menisk łzowy jest widoczny tylko w zbliżeniu;
- nie ma penetracji powiek;
- oba oczy zachowują ten sam model optyczny.

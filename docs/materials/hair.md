# Włosy i zarost

Włosy, broda, wąsy, brwi i rzęsy są osobnymi systemami o różnych długościach, kierunkach wzrostu i wymaganiach runtime. Nie należy traktować ich jako jednego materiału.

## Reprezentacja

Dozwolone są trzy strategie:

- groom strands;
- hair cards;
- hybryda, np. groom dla LOD0 i cards dla dalszych LOD.

Wybór jest dokonywany per element, nie globalnie dla całej postaci.

## Parametry włosa

Jako punkt startowy dla włosów głowy przyjmujemy:

| Parametr | Baseline | Zakres |
| --- | ---: | ---: |
| średnica włosa | 70 µm | 50-100 µm |
| losowa zmiana średnicy | ±12% | 5-20% |
| losowa zmiana długości | ±4% | 2-8% |
| losowa zmiana kierunku | 2° | 0.5-5° |
| roughness longitudinal | 0.28 | 0.20-0.40 |
| roughness azimuthal | 0.45 | 0.35-0.60 |

Jeżeli shader nie obsługuje anizotropowego modelu włosa, należy użyć rozwiązania docelowego silnika zamiast próbować kopiować te parametry bezpośrednio do klasycznego GGX.

## Gęstość

Rzeczywista liczba włosów na głowie jest duża, ale renderowany groom nie musi odwzorowywać każdego włosa 1:1.

Baseline LOD0:

- 800-1500 guides;
- około 60k-120k render strands dla fryzury o średniej gęstości;
- children/interpolation zależnie od DCC;
- clumping wieloskalowy, minimum dwa poziomy;
- pojedyncze flyaways: około 0.5-2% widocznych włosów.

Wartości są budżetem produkcyjnym i należy je zmniejszać w runtime zgodnie z profilem wydajności.

## Linia włosów

Linia włosów jest jednym z silnych elementów podobieństwa twarzy.

Wymagania:

- przebieg linii włosów zgodny z referencją;
- naturalne przejście gęstości przy skroniach i czole;
- brak idealnie równej granicy groomu;
- osobne krótkie baby hairs przy krawędzi, jeśli są obecne na referencji.

## Broda i wąsy

Broda o widocznej objętości nie może być zastąpiona wyłącznie teksturą skóry.

Baseline:

- strand diameter 60-100 µm;
- większa losowość kierunku niż dla włosów głowy;
- clumping słabszy niż dla fryzury;
- osobne grupy: broda, wąsy, bokobrody;
- kolor musi zawierać naturalne lokalne różnice.

Dla bardzo krótkiego zarostu można stosować hybrydę: tekstura/normal + krótkie strands w obszarach silnego profilu.

## Brwi

Brwi wymagają osobnego groomu albo cards.

- kierunek rośnie od przyśrodkowego ku bocznemu;
- gęstość nie może być jednolita;
- pojedyncze włoski wystają poza główny kontur;
- brwi muszą deformować się razem z brow rig bez ślizgania po skórze.

## Rzęsy

Rzęsy są częścią mechaniki powieki.

Baseline długości:

- górne: 7-10 mm;
- dolne: 4-7 mm;
- większa gęstość w środkowo-bocznej części górnej powieki;
- brak idealnej symetrii L/R.

Rzęsy muszą przejść pełny test blink bez penetracji rogówki.

## Długie włosy

Długie włosy wymagają ruchu wtórnego. Zalecany jest podział na sekcje funkcjonalne:

- przód lewy/prawy;
- skronie;
- tył centralny;
- tył lewy/prawy;
- opcjonalne pasma boczne.

Każda sekcja może być sterowana łańcuchem kości, groom dynamics albo hybrydą. Root włosa pozostaje stabilnie związany ze skalpem.

## Kolizje

Dla symulacji używamy uproszczonych colliderów:

- czaszka;
- szyja;
- barki;
- klatka;
- górna część pleców.

Minimalna odległość bezpieczeństwa od powierzchni kolizji: baseline 2-4 mm w LOD0. Nie należy zwiększać jej tak mocno, aby fryzura zaczęła „unosić się” nad ciałem.

## LOD

Rekomendowany profil:

| LOD | Render strands / cards | Dynamika |
| --- | --- | --- |
| LOD0 | 100% | pełna |
| LOD1 | 55-65% | uproszczona |
| LOD2 | 25-35% | tylko główne pasma |
| LOD3 | cards / 10-15% | wyłączona |

## Definition of Done

System włosów i zarostu zalicza etap, jeśli:

- linia włosów odpowiada referencji;
- broda ma właściwą objętość;
- brwi i rzęsy są osobnymi elementami;
- nie występuje widoczny scalp pop-through;
- groom nie przenika przez głowę i ubranie w standardowym zakresie ruchu;
- LOD nie zmienia radykalnie sylwetki fryzury;
- ruch wtórny długich włosów jest stabilny i nie oscyluje bez tłumienia.

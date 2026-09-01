# Włosy i zarost

Włosy, broda, wąsy, brwi i rzęsy są osobnymi systemami o różnych długościach, kierunkach wzrostu i wymaganiach środowiska czasu rzeczywistego (runtime environment). Nie należy traktować ich jako jednego materiału.

Terminologia jest zgodna ze [słownikiem terminologicznym](../project/terminology.md).

## Sposób reprezentacji

Dozwolone są trzy strategie:

- system włosów oparty na pojedynczych pasmach (strand-based groom);
- płaszczyzny z teksturą włosów (hair cards);
- rozwiązanie hybrydowe, np. system włosów (groom) dla LOD0 i płaszczyzny z teksturą włosów (hair cards) dla dalszych poziomów szczegółowości (Levels of Detail, LOD).

Wybór jest dokonywany osobno dla każdego elementu fryzury i zarostu.

## Parametry włosa

Jako punkt startowy dla włosów głowy przyjmujemy:

| Parametr | Wartość bazowa | Zakres |
| --- | ---: | ---: |
| średnica włosa | 70 µm | 50-100 µm |
| losowa zmiana średnicy | ±12% | 5-20% |
| losowa zmiana długości | ±4% | 2-8% |
| losowa zmiana kierunku | 2° | 0.5-5° |
| chropowatość wzdłużna (longitudinal roughness) | 0.28 | 0.20-0.40 |
| chropowatość azymutalna (azimuthal roughness) | 0.45 | 0.35-0.60 |

Jeżeli program cieniujący (shader) nie obsługuje anizotropowego modelu odbicia włosa (anisotropic hair shading model), należy użyć rozwiązania przewidzianego przez środowisko docelowe (target environment), zamiast kopiować wartości do klasycznego modelu GGX.

## Gęstość i prowadnice

Rzeczywista liczba włosów na głowie jest duża, ale system włosów (groom) nie musi odwzorowywać każdego włosa 1:1.

Wartości bazowe dla LOD0:

- 800-1500 prowadnic włosów (guide strands);
- około 60 000-120 000 włosów renderowanych (render strands) dla fryzury o średniej gęstości;
- interpolacja włosów potomnych (child strand interpolation) zależnie od programu DCC;
- grupowanie pasm (clumping) co najmniej na dwóch skalach;
- pojedyncze odstające włosy (flyaway hairs): około 0,5-2% widocznych włosów.

Są to budżety produkcyjne. W środowisku czasu rzeczywistego (runtime environment) należy je zmniejszać zgodnie z profilem wydajności.

## Linia włosów

Linia włosów (hairline) jest jednym z silnych elementów podobieństwa twarzy.

Wymagania:

- przebieg linii włosów zgodny z referencją;
- naturalne przejście gęstości przy skroniach i czole;
- brak idealnie równej granicy systemu włosów (groom);
- osobne krótkie włosy przy krawędzi (baby hairs), jeśli występują w materiale referencyjnym.

## Broda i wąsy

Broda o widocznej objętości nie może być zastąpiona wyłącznie teksturą skóry.

Wartości bazowe:

- średnica włosa zarostu (strand diameter): 60-100 µm;
- większa losowość kierunku niż dla włosów głowy;
- słabsze grupowanie pasm (clumping) niż dla fryzury;
- osobne grupy: broda, wąsy i bokobrody;
- barwa musi zawierać naturalne lokalne różnice.

Dla bardzo krótkiego zarostu można stosować rozwiązanie hybrydowe: teksturę i mapę normalnych (normal map) uzupełnione krótkimi włosami renderowanymi (render strands) w obszarach istotnych dla sylwetki twarzy.

## Brwi

Brwi wymagają osobnego systemu włosów (groom) albo płaszczyzn z teksturą włosów (hair cards).

- kierunek włosków zmienia się od części przyśrodkowej ku bocznej;
- gęstość nie może być jednolita;
- pojedyncze włoski powinny wychodzić poza główny kontur;
- brwi muszą deformować się razem z układem sterowania brwiami (brow rig) bez ślizgania po skórze.

## Rzęsy

Rzęsy są częścią mechaniki powieki.

Wartości bazowe długości:

- górne: 7-10 mm;
- dolne: 4-7 mm;
- większa gęstość w środkowo-bocznej części górnej powieki;
- brak idealnej symetrii lewej i prawej strony.

Rzęsy muszą przejść pełny test mrugnięcia (blink test) bez penetracji rogówki.

## Długie włosy

Długie włosy wymagają ruchu wtórnego (secondary motion). Zalecany jest podział na sekcje funkcjonalne: przód lewy/prawy, skronie, tył centralny, tył lewy/prawy i opcjonalne pasma boczne.

Każda sekcja może być sterowana łańcuchem kości, dynamiką systemu włosów (groom dynamics) albo rozwiązaniem hybrydowym. Nasada włosa (hair root) pozostaje stabilnie związana ze skórą głowy (scalp).

## Kolizje

Do symulacji używamy uproszczonych brył kolizyjnych (collision volumes) dla czaszki, szyi, barków, klatki piersiowej i górnej części pleców.

Minimalny margines kolizji (collision margin) dla LOD0: 2-4 mm. Nie należy zwiększać go tak mocno, aby fryzura zaczęła unosić się nad ciałem.

## Poziomy szczegółowości

| Poziom szczegółowości (LOD) | Włosy renderowane / płaszczyzny włosów | Dynamika |
| --- | --- | --- |
| LOD0 | 100% | pełna |
| LOD1 | 55-65% | uproszczona |
| LOD2 | 25-35% | tylko główne pasma |
| LOD3 | płaszczyzny z teksturą włosów (hair cards) lub 10-15% pasm | wyłączona |

## Kryteria ukończenia

System włosów i zarostu zalicza etap, jeśli:

- linia włosów odpowiada referencji;
- broda ma właściwą objętość;
- brwi i rzęsy są osobnymi elementami;
- nie występuje prześwitywanie skóry głowy (scalp pop-through);
- system włosów nie przenika przez głowę ani ubranie w standardowym zakresie ruchu;
- zmiana poziomu szczegółowości (LOD transition) nie zmienia radykalnie sylwetki fryzury;
- ruch wtórny (secondary motion) długich włosów jest stabilny i nie oscyluje bez tłumienia.
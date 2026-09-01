# System kodowania ruchów twarzy FACS

System kodowania ruchów twarzy (Facial Action Coding System, FACS) opisuje obserwowalne ruchy twarzy za pomocą jednostek działania mięśniowego (Action Units, AU). W Avatar Studio FACS jest warstwą interpretacji anatomicznej i semantycznej. Nie jest listą gotowych emocji.

## Action Unit

Jednostka działania mięśniowego opisuje charakterystyczny ruch regionu twarzy, np. uniesienie wewnętrznej części brwi lub uniesienie kącika ust. Natężenie można zapisywać jakościowo lub mapować do wartości liczbowej 0-1 na potrzeby systemu animacji.

Wartość 0 oznacza brak aktywacji, około 0,2-0,4 subtelną ekspresję, 0,5-0,7 wyraźną, a 0,8-1,0 bardzo silną. W naturalnej rozmowie większość aktywacji nie powinna stale dochodzić do 1.

## Najważniejsze jednostki dla Avatar Studio

| AU | Znaczenie praktyczne | Przykładowe kanały |
| --- | --- | --- |
| AU1 | uniesienie wewnętrznej części brwi | `browInnerUp` |
| AU2 | uniesienie zewnętrznej części brwi | `browOuterUpLeft/Right` |
| AU4 | opuszczenie i zbliżenie brwi | `browDownLeft/Right` |
| AU5 | uniesienie górnej powieki | `eyeWideLeft/Right` |
| AU6 | uniesienie policzka | `cheekSquintLeft/Right` |
| AU7 | napięcie powiek | `eyeSquintLeft/Right` |
| AU9 | zmarszczenie nosa | `noseSneerLeft/Right` |
| AU10 | uniesienie górnej wargi | `mouthUpperUpLeft/Right` |
| AU12 | uniesienie kącika ust | `mouthSmileLeft/Right` |
| AU15 | opuszczenie kącika ust | `mouthFrownLeft/Right` |
| AU17 | uniesienie brody | komponent dolnej wargi/brody |
| AU18 | wysunięcie i ściągnięcie warg | `mouthPucker` |
| AU20 | rozciągnięcie warg | `mouthStretchLeft/Right` |
| AU25 | rozwarcie warg | zależne od `jawOpen` i ust |
| AU26 | opuszczenie żuchwy | `jawOpen` |

Mapowanie nie jest relacją 1:1. Jeden kanał ARKit może wspierać kilka AU, a jedna AU może wymagać kilku deformacji wewnętrznych.

## Intensywność i czas

FACS opisuje rodzaj ruchu, natomiast animacja potrzebuje także przebiegu czasowego. Dla ekspresji twarzy używamy faz:

- czas narastania (onset time);
- faza maksymalnego nasilenia (apex);
- czas wygaszania (offset time).

Dla subtelnej ekspresji konwersacyjnej punktem startowym może być około 200-400 ms narastania, 300-1000 ms utrzymania i 250-600 ms wygaszania. Krótsze czasy dają wrażenie reakcji gwałtownej, dłuższe bardziej spokojnej.

## Emocje jako kombinacje

Nie zapisujemy reguły `radość = smile`. Przykładowa naturalna radość może łączyć AU6 i AU12 z różnym natężeniem oraz niewielką asymetrią. Złość może łączyć AU4, AU5/7, napięcie ust i ruch żuchwy.

## Asymetria

Asymetria 5-12% między stronami jest często bardziej naturalna niż idealna symetria, ale nie jest obowiązkową stałą. Powinna wynikać z materiału referencyjnego lub z subtelnego proceduralnego zróżnicowania.

## Walidacja FACS

Dla każdej kluczowej AU sprawdź:

- czy porusza właściwy region;
- czy nie aktywuje błędnych sąsiednich obszarów;
- czy działa przy 0,25, 0,5, 0,75 i 1,0;
- czy można ją łączyć z innymi AU;
- czy kombinacja zachowuje objętość twarzy.

## Definition of Done

FACS jest zatwierdzony, gdy mapping AU do wewnętrznych deformacji jest udokumentowany, kluczowe AU można testować niezależnie, a presety emocji są zbudowane jako kombinacje AU, nie jako pojedyncze kształty.
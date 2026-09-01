# Walidacja podobieństwa

Podobieństwo jest miarą zgodności awatara z konkretną osobą referencyjną. Nie jest tym samym co ogólny realizm. Twarz może być fotorealistyczna, a jednocześnie nie przypominać właściwej osoby.

## Zasada rozdzielenia ocen

Walidację wykonuj osobno dla:

1. geometrii,
2. materiałów,
3. włosów i zarostu,
4. okularów i akcesoriów,
5. mimiki,
6. ruchu.

Jeżeli wszystkie warstwy ocenia się jednocześnie, atrakcyjne oświetlenie lub dobra tekstura mogą maskować błędy geometrii.

## Punkty charakterystyczne

**Punkt charakterystyczny twarzy (facial landmark)** to dobrze identyfikowalny punkt anatomiczny lub wizualny, np. środek źrenicy, kącik oka, skrzydło nosa lub kącik ust.

Punkty służą do pomiaru różnic między modelem a zdjęciem po dopasowaniu kamery.

### Zalecany zestaw ręczny

- środki źrenic,
- wewnętrzne i zewnętrzne kąciki oczu,
- najwyższe punkty brwi,
- skrzydła nosa,
- czubek nosa,
- kąciki ust,
- środek górnej i dolnej wargi,
- dolny punkt brody,
- kąty żuchwy,
- górne i dolne punkty uszu.

## Błąd położenia punktu

Dla punktu `i` można obliczyć błąd ekranowy:

`e_i = sqrt((x_model - x_ref)^2 + (y_model - y_ref)^2)`

Aby wynik był porównywalny między rozdzielczościami, normalizuj go przez szerokość twarzy w pikselach:

`e_norm = e_i / face_width_px`.

Praktyczny punkt startowy:

- poniżej 0,5% szerokości twarzy: bardzo dobra zgodność,
- 0,5-1,0%: zwykle akceptowalna,
- 1-2%: widoczna różnica wymagająca oceny,
- powyżej 2%: zwykle istotny błąd w obszarze kluczowym.

Nie traktuj tych wartości jako normy biologicznej. Są progiem produkcyjnym dla kontroli własnego modelu.

## Sylwetka

**Błąd sylwetki (silhouette error)** opisuje różnicę między obrysem modelu a obrysem osoby na zdjęciu. Jest szczególnie przydatny dla profilu nosa, czoła, ust, brody, czaszki i całego ciała.

Najpierw oceniaj obrys bez tekstur. W profilu różnica 2-4 mm w projekcji nosa lub brody może być wyraźnie widoczna, nawet gdy ujęcie frontalne wygląda poprawnie.

## Kamery walidacyjne

Używaj co najmniej:

- widoku frontalnego,
- lewego profilu,
- prawego profilu,
- 3/4 z lewej,
- 3/4 z prawej.

Dla ciała dodaj przód, tył i oba profile.

Nie zmieniaj ogniskowej tylko po to, aby model „lepiej pasował”. Najpierw dopasuj parametry kamery do referencji.

## Priorytety percepcyjne

Największą wagę nadaj:

1. oczom i oczodołom,
2. relacji nosa, ust i brody,
3. sylwetce czaszki,
4. żuchwie,
5. linii włosów,
6. zarostowi,
7. uszom,
8. okularom,
9. proporcjom ciała.

## Walidacja neutralnej twarzy

Neutralna twarz jest wzorcem geometrii. Sprawdź:

- brak przypadkowego uśmiechu lub napięcia brwi,
- naturalny kontakt warg,
- rzeczywiste asymetrie,
- ilość widocznej twardówki,
- położenie powiek względem tęczówki,
- pozycję żuchwy.

## Walidacja ekspresji

Podobieństwo musi utrzymywać się także podczas ekspresji. Porównaj co najmniej:

- lekki i szeroki uśmiech,
- uniesienie brwi,
- zmarszczenie brwi,
- mocne zamknięcie oczu,
- otwarcie ust,
- wysunięcie i zaokrąglenie warg.

Awatar, który przypomina osobę tylko w neutralnej pozie, nie spełnia celu projektu.

## Procedura akceptacji

1. Wyłącz postprocessing.
2. Użyj neutralnego światła studyjnego.
3. Dopasuj kamerę do referencji.
4. Porównaj geometrię bez tekstur.
5. Zapisz błędy punktów charakterystycznych.
6. Oceń sylwetkę.
7. Włącz materiały i sprawdź, czy nie zmieniają percepcji kształtu.
8. Włącz włosy, zarost i okulary.
9. Powtórz test dla ekspresji.
10. Zapisz zestaw obrazów przed/po.

## Kryterium zaliczenia

Nie zatwierdzaj modelu na podstawie jednego atrakcyjnego renderu. Podobieństwo musi być stabilne w wielu kątach, przy neutralnym świetle i przy podstawowych ekspresjach.
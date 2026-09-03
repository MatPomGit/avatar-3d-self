# 09. Włosy i zarost

System włosów (groom) opisuje fryzurę za pomocą prowadnic włosów (guide strands), z których powstają włosy renderowane. W środowisku czasu rzeczywistego może zostać zachowany jako groom, zamieniony na płaszczyzny z teksturą włosów (hair cards) albo połączony w rozwiązanie hybrydowe. Najpierw zatwierdza się kierunek wzrostu i sylwetkę, a dopiero potem zwiększa gęstość.

## Wymagania wstępne

- zatwierdzona topologia oraz skala głowy; zmiana indeksów wierzchołków po przypięciu groomu wymaga migracji;
- referencje linii włosów, przedziałka, wirów, boków, tyłu głowy, brody, wąsów i brwi;
- wybrana reprezentacja docelowa oraz budżet geometrii, pamięci, draw calls i symulacji dla każdego LOD;
- zatwierdzone UV skóry głowy i atlasów włosów, jeżeli powstają hair cards;
- rig głowy i żuchwy oraz dostępne bryły kolizyjne szyi, barków i ubrania.

### Sprawdzenie wymagań

1. Porównaj wersję i sumę kontrolną siatki głowy z manifestem. **Oczekiwany wynik:** scalp można przypiąć bez przemapowania wierzchołków.
2. Ułóż referencje według widoku i zaznacz obszary bez pokrycia. **Oczekiwany wynik:** kierunek wzrostu każdego widocznego regionu ma źródło albo jawnie oznaczone założenie.
3. Otwórz profil środowiska docelowego. **Oczekiwany wynik:** wiadomo, czy każdy LOD używa groomu, hair cards czy mesha oraz jaki ma budżet.
4. Odtwórz testowy ruch głowy i żuchwy z proxy kolizyjnymi. **Oczekiwany wynik:** układ współrzędnych, animacja i kolizje działają przed budową fryzury.

## Input

- wersja wzorcowa głowy, rig i materiały skóry;
- prywatne referencje włosów i zarostu przechowywane poza publicznym repozytorium;
- profil reprezentacji, materiału, LOD, kolizji i eksportu;
- zatwierdzone budżety wydajnościowe.

## Process

1. **Zbuduj skórę głowy (scalp).** Wyodrębnij czystą, nieprzecinającą głowy powierzchnię obejmującą obszar wzrostu; dodaj osobne powierzchnie dla brwi i zarostu, gdy wymaga tego narzędzie. **Oczekiwany wynik:** powierzchnie poruszają się z głową i nie wystają spod linii włosów.
2. **Zaznacz regiony prowadnic.** Podziel fryzurę na linię włosów, skronie, boki, tył, koronę, przedziałek i wiry zgodnie ze zmianami kierunku. **Oczekiwany wynik:** mapa regionów nie ma przypadkowych luk ani nakładania identyfikatorów.
3. **Rozmieść prowadnice.** Zacznij od granic i pasm definiujących sylwetkę, następnie dodaj przepływ wewnętrzny; nasady prowadź zgodnie z kierunkiem wzrostu. **Oczekiwany wynik:** rzadki podgląd już odtwarza przedziałek, wiry i ogólną bryłę.
4. **Ustaw gęstość.** Steruj nią maską, zachowując naturalne przejście linii włosów i świadome przerzedzenia. **Oczekiwany wynik:** scalp nie prześwituje przypadkowo, a hairline nie przypomina ostrej czapki.
5. **Dodaj grupowanie pasm (clumping).** Najpierw grupy główne, potem subtelne grupy wtórne; nie używaj clumpingu do naprawiania złych prowadnic. **Oczekiwany wynik:** fryzura ma czytelny rytm bez mokrych, jednakowych kolców.
6. **Ustaw szerokość i profil pasm.** Zwężaj włos od nasady ku końcówce i oceniaj szerokość w pikselach z docelowej kamery. **Oczekiwany wynik:** końcówki nie są tępe, a pasma nie znikają ani nie migoczą.
7. **Zbuduj reprezentację czasu rzeczywistego.** Dla hair cards układaj płaszczyzny warstwami od masy wewnętrznej do konturu; dla groomu redukuj prowadnice i włosy zgodnie z profilem. **Oczekiwany wynik:** reprezentacja zachowuje rozdzielenie pasm oraz przepuszczalność bez nadmiernego overdraw.
8. **Zbuduj zarost.** Rozdziel brodę, wąsy, brwi i ewentualny meszek; dopasuj kierunek do anatomii i ruchu żuchwy. Krótki zarost może łączyć geometrię z maską skóry, lecz nie powinien istnieć wyłącznie jako namalowany ciemny obszar w zbliżeniu. **Oczekiwany wynik:** nasady pozostają związane z twarzą, a wargi i nozdrza są czyste.
9. **Przygotuj poziomy szczegółowości (Level of Detail, LOD).** Redukuj włosy, karty, szerokość i symulację stopniowo; zachowaj hairline i pasma definiujące kontur najdłużej. **Oczekiwany wynik:** każdy LOD mieści się w budżecie i nie zmienia gwałtownie objętości.
10. **Dodaj kolizje i opcjonalną dynamikę.** Użyj uproszczonych proxy głowy, szyi, uszu, barków i ubrania; symuluj tylko pasma o zauważalnym ruchu wtórnym. **Oczekiwany wynik:** ruch nie eksploduje, a włosy nie przechodzą przez ciało w animacji testowej.
11. **Wykonaj test sylwetki.** Oglądaj nieruchomą czarną sylwetkę na jasnym tle z przodu, boków, tyłu i góry, następnie włącz światło oraz ruch. **Oczekiwany wynik:** kształt zgadza się z referencją bez polegania na kolorze i połysku.

## Parametry liczbowe

Parametry generatorów nie są przenośne jeden do jednego. Poniższe znormalizowane wartości należy zapisać razem z liczbą wynikowych włosów lub kart, aby wynik był odtwarzalny.

**Gęstość (density)** określa liczbę włosów renderowanych na obszar albo znormalizowany mnożnik maski. Większa wypełnia fryzurę, ale zwiększa pamięć, overdraw i koszt symulacji. **Przykładowe wartości mnożnika:** 0,25 (niska, dalszy LOD), 0,6 (typowa reprezentacja czasu rzeczywistego), 1,0 (wysoka/master). Za mała odsłania scalp i rozrywa bryłę, za duża tworzy nieprzezroczysty hełm oraz przekracza budżet. Liczbę wynikową zawsze raportuj.

**Siła clumpingu** opisuje, jak mocno włosy zbiegają się ku osi grupy. Wzrost daje większe, czytelniejsze pasma. **Przykładowe wartości znormalizowane:** 0,15 (niska, włosy puszyste), 0,45 (typowa), 0,8 (wysoka, włosy mokre lub stylizowane). Zbyt mała daje jednorodny puch, zbyt duża — ostre kolce i puste szczeliny. Wynik zależy również od liczby clumpów, dlatego oba ustawienia zapisuj w manifeście.

**Szerokość pasma** jest średnicą renderowanego włosa albo wizualną szerokością pasma na karcie. Większa poprawia stabilność z daleka, lecz pogrubia fryzurę. **Przykładowe wartości dla pojedynczego włosa:** 40 µm (niska), 70 µm (typowa), 110 µm (wysoka); hair cards ocenia się dodatkowo w pikselach kamery. Za mała szerokość migocze lub znika, za duża przypomina drut i zatyka prześwity. Stosuj zwężenie końcówki zamiast jednej szerokości na całej długości.

**Liczba włosów lub kart na LOD** bezpośrednio steruje kosztem i jakością. Więcej elementów poprawia rozdzielenie pasm, ale obciąża GPU. **Przykładowy mnożnik względem LOD0:** 1,0 (wysoki), 0,5 (typowy LOD pośredni), 0,2 (niski/daleki). To nie jest uniwersalny budżet: profil musi podać liczby absolutne. Nadmierna redukcja zmienia kontur, a zbyt mała nie daje mierzalnego zysku wydajności.

**Odstęp kolizyjny** to minimalna odległość włosa od proxy. Większy ogranicza penetracje, ale sprawia, że fryzura unosi się nad ciałem. **Przykładowe wartości przy skali w metrach:** 1 mm (niska), 3 mm (typowa), 8 mm (wysoka dla grubego ubrania). Za mały daje clipping, za duży widoczną szczelinę. Dobierz go do szerokości pasma, dokładności solvera i ruchu.

## Editable output

Kanoniczny `hair_master_vNNN` zachowuje scalp, regiony, prowadnice, maski density, hierarchię clumpingu, parametry szerokości, osobne warstwy zarostu, materiały, ustawienia LOD oraz proxy i parametry dynamiki. Wygenerowane hair cards nie mogą być jedynym źródłem fryzury.

### Zapis edytowalnego mastera

1. Zapisz prowadnice przed generowaniem oraz reguły lub ustawienia generowania każdego regionu.
2. Zachowaj osobno źródła atlasu, scalp, groom głowy, brwi, brody i wąsów.
3. Zapisz nową wersję `hair_master_vNNN` wraz z wersją głowy, rigu i profilu wydajnościowego.
4. Otwórz kopię, przelicz groom i porównaj liczby elementów, obwiednię oraz sumy kontrolne eksportowalnych map.

## Derived output

- zoptymalizowane groomy, hair cards lub siatki dla każdego LOD;
- atlasy koloru, opacity, normalnych i parametrów modelu włosa;
- proxy kolizyjne oraz opcjonalne dane symulacji;
- render testu sylwetki, animacja ruchu i raport budżetu.

### Eksport artefaktów pochodnych

1. Wygeneruj każdy LOD wyłącznie z zatwierdzonego mastera i nazwij go zgodnie z profilem.
2. Wyeksportuj transformacje nasad, wiązanie, materiały i proxy w formacie obsługiwanym przez środowisko docelowe.
3. Zaimportuj do czystej sceny, sprawdź skalę, kolejność przezroczystości i model anizotropowego odbicia włosa.
4. Zapisz liczby włosów/kart, pamięć, czas renderowania, wynik animacji oraz porównanie sylwetek LOD.

## Validation

- zgodność hairline, przedziałka, wirów, objętości i zarostu z referencją;
- test sylwetki z wymaganych kierunków, bez materiału i z materiałem;
- pomiar budżetu każdego LOD oraz przejść LOD w ruchu kamery;
- animacja głowy, szyi i żuchwy z kolizjami oraz opcjonalną symulacją;
- kontrola scalp, sortowania przezroczystości, migotania i overdraw w środowisku docelowym.

| Objaw | Możliwa przyczyna | Naprawa |
| --- | --- | --- |
| Fryzura wygląda jak czapka | Jednolita density lub zbyt szerokie pasma | Zróżnicuj maskę, zwęź końcówki i otwórz prześwity. |
| Scalp prześwituje przypadkowo | Za niska density albo luka między regionami | Napraw maskę i przepływ prowadnic, nie tylko przyciemniaj skórę. |
| Mokre, ostre kolce | Za silny clumping | Zmniejsz siłę i dodaj clumpy wtórne o różnej skali. |
| Kontur przeskakuje przy zmianie LOD | Usunięto prowadnice sylwetki lub zła histereza | Zachowaj pasma konturu i dostrój progi przejścia w profilu. |
| Pasma migoczą z daleka | Zbyt cienkie włosy lub niestabilna alfa | Dostosuj szerokość LOD i filtrowanie atlasu. |
| Włosy wchodzą w bark | Brak proxy lub za mały odstęp | Popraw proxy, margines i wagi dynamiki. |
| Broda odkleja się od żuchwy | Błędne wiązanie nasad | Przypnij scalp zarostu do właściwej deformacji twarzy. |

## Failure conditions

Przejście dalej jest zablokowane, jeśli:

- scalp lub nasady odklejają się po deformacji albo zależą od niezatwierdzonej topologii;
- hairline, kierunki regionów, sylwetka lub geometria zarostu nie zgadzają się z referencją;
- którykolwiek LOD przekracza budżet albo powoduje widoczny skok sylwetki;
- występują trwałe penetracje, eksplozje symulacji, migotanie lub krytyczne błędy sortowania;
- eksportu nie można odtworzyć z mastera i manifestu parametrów.

## Definition of Done

Etap jest ukończony, gdy wersjonowany master odtwarza groom i zarost, wszystkie LOD mieszczą się w budżecie oraz zachowują hairline i sylwetkę, a import docelowy przechodzi test materiału, przejść LOD, kolizji i ruchu bez krytycznego clippingu, migotania lub odklejenia nasad.

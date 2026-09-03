# 08. Oczy

Oko jest układem współosiowych warstw, a nie jedną pomalowaną kulą. Osobna twardówka (sclera), tęczówka (iris), rogówka (cornea) i linia wilgotna powieki (wetline) pozwalają zachować głębię, załamanie światła oraz kontakt powiek z gałką.

## Wymagania wstępne

- zatwierdzona głowa z symetrią lub udokumentowaną asymetrią, powiekami i workiem spojówkowym;
- zdjęcia oczu na wprost i pod kątem, bez zmiany skali oraz z widoczną granicą rogówki;
- scena w skali rzeczywistej, znana oś patrzenia i przyjęta konwencja pivotów;
- model cieniowania obsługujący przezroczystość lub załamanie światła i profil eksportu;
- podstawowy rig oka i sterowanie mrugnięciem (blink), jeśli etap rigowania już istnieje.

### Sprawdzenie wymagań

1. Zmierz znany odcinek modelu i porównaj z jednostkami sceny. **Oczekiwany wynik:** skala jest rzeczywista i nie wymaga korekty przy eksporcie.
2. Obejrzyj referencje pod kątem paralaksy oraz odbić zasłaniających krawędź tęczówki. **Oczekiwany wynik:** co najmniej jeden widok pozwala wiarygodnie oszacować kulę.
3. Wyświetl lokalne osie głowy i kości oczu. **Oczekiwany wynik:** dodatni kierunek patrzenia i oś pionowa są zapisane w profilu.
4. Wykonaj test materiału przezroczystej kuli w docelowym rendererze. **Oczekiwany wynik:** wiadomo, czy renderer obsługuje fizyczne refraction, czy wymaga przybliżenia.

## Input

- wersja wzorcowa retopologizowanej głowy;
- skalibrowane referencje oczu i pomiary twarzy;
- profil materiału oka, rigowania i eksportu;
- zatwierdzone nazwy elementów lewego i prawego oka.

## Process

1. **Wyznacz środek gałki.** Dopasuj okrąg do widocznej granicy rogówki w kilku widokach, zbuduj pomocniczą sferę i iteracyjnie dopasuj ją do powierzchni powiek. Nie wyznaczaj środka tylko z jednego zdjęcia perspektywicznego. **Oczekiwany wynik:** pomocnicza sfera pozostaje współosiowa z okiem we wszystkich widokach.
2. **Wyznacz promień.** Skaluj sferę do referencji i anatomii, po czym zapisz promień w jednostkach sceny. **Oczekiwany wynik:** przednia powierzchnia oka podpiera powieki bez deformowania sfery.
3. **Ustaw pivot i osie.** Umieść pivot dokładnie w wyznaczonym środku, zastosuj transformacje i skieruj lokalną oś patrzenia zgodnie z profilem. **Oczekiwany wynik:** obrót nie powoduje zataczania okręgu ani translacji oka.
4. **Zbuduj twardówkę.** Zachowaj kulistą geometrię i subtelną zmienność barwy; nie maluj stałego cienia powiek. **Oczekiwany wynik:** twardówka jest czytelna bez kredowej bieli i przesadnych naczynek.
5. **Zbuduj tęczówkę i źrenicę.** Osadź tęczówkę pod powierzchnią rogówki, zachowaj limbus oraz radialny detal, a skalę źrenicy kontroluj parametrem lub wariantem materiału. **Oczekiwany wynik:** tęczówka ma głębię i nie wygląda jak nadruk na kuli.
6. **Zbuduj rogówkę.** Uformuj gładką wypukłość, przypisz fizyczny współczynnik załamania i oddziel roughness od twardówki. **Oczekiwany wynik:** highlight przesuwa się ciągle, a tęczówka nie ulega nienaturalnemu powiększeniu.
7. **Zbuduj wetline.** Dodaj cienką, ciągłą geometrię lub rozwiązanie materiałowe przy brzegu obu powiek, bez zamykania kanalika łzowego przypadkową bryłą. **Oczekiwany wynik:** refleks łączy optycznie gałkę z powieką, ale nie tworzy szklanego pierścienia.
8. **Dopasuj powieki do kuli.** Przesuwaj powieki i ich topologię, a nie spłaszczaj oka; zachowaj równy kontakt oraz mięsisty brzeg. **Oczekiwany wynik:** w pozycji neutralnej nie ma szczeliny ani penetracji.
9. **Skonfiguruj śledzenie i blink.** Dopasuj górną i dolną powiekę do ruchu oka, a następnie wykonaj pełne domknięcie ze spotkaniem brzegów, nie ich przenikaniem. **Oczekiwany wynik:** źrenica nie prześwituje w pełnym blinku, a objętość powiek jest zachowana.
10. **Sprawdź zakres spojrzenia.** Przetestuj skrajne kierunki osobno i razem z eyelid follow oraz blink. **Oczekiwany wynik:** brak przecięć rogówki, wetline i powiek, a pivot pozostaje stabilny.

## Parametry liczbowe

**Promień gałki ocznej** opisuje rozmiar sfery podpierającej powieki. Większy wypycha powieki i zmniejsza miejsce w oczodole, mniejszy tworzy zapadnięcie. **Przykładowe wartości dla dorosłej postaci:** 11 mm (niska), 12 mm (typowa), 13 mm (wysoka). To punkt startowy, nie diagnoza anatomiczna; wybór musi wynikać z referencji i skali modelu. Za mały promień daje szczeliny i płaskie powieki, za duży — wytrzeszcz i penetracje.

**Współczynnik załamania światła (Index of Refraction, IOR)** mówi, jak silnie rogówka zmienia kierunek światła. Wyższy wzmacnia załamanie i zmienia odbicie Fresnela. **Przykładowe wartości:** 1,33 (niska, przybliżenie warstwy wodnej), 1,376–1,38 (typowa rogówka), 1,45 (wysoka, zwykle niefizyczna dla oka). Zbyt niski spłaszcza tęczówkę, zbyt wysoki nadmiernie ją przesuwa lub powiększa. Gdy renderer upraszcza transmisję, wartość wizualną należy opisać w profilu, zamiast udawać zgodność fizyczną.

**Roughness rogówki** steruje szerokością i ostrością odbicia na jej mikrostrukturze. Wyższa rozmywa refleks, niższa daje ostry blik. **Przykładowe wartości:** 0,02 (niska), 0,05 (typowa), 0,12 (wysoka), w skali 0–1 popularnego modelu perceptual roughness. Niska pasuje do mokrej, gładkiej powierzchni; wyższa może służyć stylizacji. Zero daje niestabilny, idealnie lustrzany blik, a zbyt wysoka wartość wygląda jak matowy plastik. Roughness twardówki powinien być kalibrowany osobno.

**Zakres spojrzenia** jest kątem obrotu od pozycji neutralnej. Większy zakres daje ekspresję, ale zwiększa ryzyko penetracji. **Przykładowe wartości testowe:** 20° (niska), 30° (typowa w poziomie), 40° (wysoka/skrajna); pion zwykle wymaga mniejszego limitu i dopasowania do postaci. Zbyt mały wygląda sztywno, zbyt duży odsłania nienaturalną ilość twardówki albo przecina powiekę. Każdy limit musi pochodzić z walidacji, nie z samej tabeli.

**Domknięcie blinku** opisuje znormalizowaną wagę sterownika. **Przykładowe wartości:** 0,0 (otwarte), 0,5 (pośrednie), 1,0 (pełne). Zwiększenie przesuwa powieki ku kontaktowi. Przy 1,0 brak styku pozostawia szczelinę, a nadmierna korekta powoduje penetrację; nie używaj wartości ponad 1,0 do naprawiania złego kształtu.

## Editable output

Kanoniczny `eyes_master_vNNN` zawiera osobne warstwy sclera, iris/pupil, cornea i wetline, geometrię pomocniczą pomiaru, pivoty, materiały, UV, limity spojrzenia oraz edytowalne kształty blink i eyelid follow.

### Zapis edytowalnego mastera

1. Zachowaj sferę pomiarową, zapisane środki i promienie dla obu oczu oraz notatkę o metodzie dopasowania.
2. Zastosuj skalę geometrii, ale nie zamrażaj błędnej orientacji pivotu; sprawdź osie po ponownym otwarciu.
3. Zapisz nową wersję `eyes_master_vNNN` z odwołaniem do wersji głowy i profilu renderera.
4. Otwórz kopię mastera, porusz obojgiem oczu i uruchom blink, aby wykryć utracone więzy lub tekstury.

## Derived output

- siatki i materiały oka w formacie wymiany;
- tekstury twardówki, tęczówki, masek i opcjonalnych przybliżeń refraction;
- animacja testowa spojrzenia i blinku;
- raport środka, promienia, osi, IOR, roughness, limitów oraz walidacji.

### Eksport artefaktów pochodnych

1. Powiel master i zastosuj wyłącznie operacje wymagane przez profil, np. triangulację lub łączenie materiałów.
2. Eksportuj z zachowaniem pivotów, osi, skali, nazw i osobnych warstw wymaganych przez renderer.
3. Zaimportuj do czystej sceny docelowej i odtwórz materiał; nie oceniaj tylko podglądu DCC.
4. Uruchom animację testową, zapisz raport i render z neutralnego światła.

## Validation

- pomiar środka, promienia i zgodności pivotu po eksporcie;
- obrót każdego oka wokół wszystkich osi bez translacji;
- kontrola ciągłości refleksu na cornea i wetline oraz głębi iris;
- pełny blink w neutralnym i skrajnych kierunkach spojrzenia;
- porównanie z referencją na wprost, z profilu i w ujęciu trzy czwarte.

| Objaw | Możliwa przyczyna | Naprawa |
| --- | --- | --- |
| Oko zatacza okrąg | Pivot nie leży w środku gałki | Ponownie dopasuj sferę i przenieś pivot przed rigowaniem. |
| Tęczówka wygląda jak naklejka | Brak osobnej cornea lub głębokości iris | Rozdziel warstwy i zweryfikuj refraction w rendererze. |
| Tęczówka jest nadmiernie powiększona | Za wysoki IOR albo zła grubość cornea | Przywróć wartość fizyczną i skalibruj geometrię. |
| Szklany pierścień przy powiece | Wetline jest za gruba lub zbyt lustrzana | Zwęź geometrię i zwiększ roughness. |
| Źrenica prześwituje podczas blinku | Kształt powieki nie domyka się | Popraw kształt blink, zachowując kontakt brzegów. |
| Przecięcie przy spojrzeniu w górę | Brak eyelid follow lub zbyt szeroki limit | Dodaj korektę powieki i ustaw zwalidowany limit. |
| Oczy wyglądają na zezujące | Niespójne osie lub punkt fiksacji | Ujednolić osie i testować wspólny cel spojrzenia. |

## Failure conditions

Przejście dalej jest zablokowane, jeśli:

- środek, promień, osie lub skala nie są zapisane albo pivot powoduje translację przy obrocie;
- brakuje którejkolwiek wymaganej warstwy bez udokumentowanego odpowiednika w docelowym shaderze;
- refraction, roughness lub głębia tęczówki nie przechodzą testu w docelowym rendererze;
- powieki, cornea lub wetline przecinają się w blinku albo zatwierdzonym zakresie spojrzenia;
- eksport nie zachowuje nazw, pivotów, materiałów lub animacji testowej.

## Definition of Done

Etap jest ukończony, gdy `eyes_master_vNNN` zachowuje pomiary i warstwy, eksport obraca oczy wokół poprawnych pivotów, materiały dają wiarygodną głębię i odbicia, a neutralna pozycja, pełny blink oraz cały zatwierdzony zakres spojrzenia przechodzą bez szczelin i penetracji.

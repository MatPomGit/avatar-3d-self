# 07. Materiały PBR

Ten etap przenosi szczegół z siatki wysokiej rozdzielczości i zdjęć na materiały zgodne z modelem metaliczności i chropowatości (metallic-roughness workflow). Podane wartości są punktami startowymi: wynik należy oceniać w skali rzeczywistej i w docelowym modelu cieniowania.

## Wymagania wstępne

- zatwierdzona siatka niskiej i wysokiej rozdzielczości w tej samej skali oraz przestrzeni obiektu;
- zatwierdzone UV, bez nakładania wysp poza świadomie współdzielonymi fragmentami, oraz manifest kafli UDIM;
- zdjęcia referencyjne z profilem barwnym albo udokumentowaną transformacją do roboczej przestrzeni barw;
- zatwierdzony profil eksportu wskazujący konwencję mapy normalnych, kanały, format i model cieniowania środowiska docelowego;
- scena testowa z neutralnym światłem, szarą kartą i kulami referencyjnymi.

### Sprawdzenie wymagań

1. Nałóż teksturę kontrolną UV i sprawdź szwy, nakładanie oraz jednakową gęstość tekseli. **Oczekiwany wynik:** wzór nie rozciąga się, a manifest odpowiada użytym kaflom.
2. Porównaj transformaty obu siatek i obwiednie po ich nałożeniu. **Oczekiwany wynik:** powierzchnie pokrywają się bez ręcznego przesunięcia, obrotu ani zmiany skali.
3. Otwórz profil eksportu i wykonaj bake próbnego detalu kierunkowego. **Oczekiwany wynik:** wiadomo, czy kanał zielony mapy normalnych jest `+Y` czy `-Y`, i próbka nie jest wklęsła zamiast wypukłej.
4. Odczytaj metadane zdjęć i dokument zarządzania barwą. **Oczekiwany wynik:** każde źródło ma znaną przestrzeń wejściową; plik bez profilu zostaje oznaczony do ręcznej kalibracji.

## Input

- wersje wzorcowe siatki high-poly, retopologii i UV;
- skalibrowane zdjęcia oraz maski regionów skóry, ust, oczu i włosów;
- profil materiału i eksportu środowiska docelowego;
- nazwa wydania i numer wersji `vNNN`.

## Process

1. **Zamroź stan wejścia.** Zapisz identyfikatory wersji siatek, UV, profilu barwnego i eksportowego w notatce materiału. **Oczekiwany wynik:** bake można jednoznacznie odtworzyć.
2. **Zbuduj klatkę wypalania (bake cage).** Powiel siatkę low-poly, odsuń ją wzdłuż normalnych i ręcznie popraw okolice nozdrzy, uszu, ust oraz powiek; klatka ma objąć high-poly bez chwytania sąsiednich powierzchni. **Oczekiwany wynik:** podgląd promieni nie przecina high-poly i nie przechodzi na przeciwległe fragmenty.
3. **Wykonaj bake testowy.** Wypal identyfikatory materiałów, mapę normalnych w przestrzeni stycznej (tangent space), AO i mapę przemieszczeń na małej rozdzielczości. Triangulacja, normalne wierzchołków i baza styczna muszą być takie same podczas bake'u i eksportu. **Oczekiwany wynik:** brak przekoszeń, fal i odwróconych detali.
4. **Ustal rozdzielczość i margines.** Dobierz je z budżetu gęstości tekseli i najmniejszego poziomu mipmap, a następnie wykonaj bake produkcyjny. **Oczekiwany wynik:** detal twarzy jest czytelny, a dylatacja wypełnia otoczenie każdej wyspy.
5. **Zbuduj barwę bazową (Base Color).** Skalibruj zdjęcia, wyrównaj ekspozycję i usuń światło: cienie kierunkowe, blik, AO oraz przebarwienia od otoczenia. Zachowaj rzeczywistą zmienność pigmentu. **Oczekiwany wynik:** Base Color wygląda płasko w trybie bez oświetlenia i nie ma namalowanego bliku ani cienia nosa.
6. **Zbuduj kanały danych.** Przygotuj `Normal`, `Roughness`, `Metallic`, AO oraz, jeżeli profil tego wymaga, `Displacement`, maski rozpraszania podpowierzchniowego (Subsurface Scattering, SSS) i `Opacity`. **Oczekiwany wynik:** każdy kanał ma udokumentowane znaczenie, zakres i wartość domyślną poza wyspami.
7. **Przypisz przestrzenie barw.** Base Color odczytuj zgodnie z profilem projektu, zwykle jako sRGB; mapy normalnych, roughness, metallic, AO, displacement i maski odczytuj jako dane liniowe (`Non-Color`). **Oczekiwany wynik:** renderer nie stosuje funkcji sRGB do danych technicznych.
8. **Spakuj kanały tylko według profilu.** Zapisz kolejność, np. `R=AO`, `G=Roughness`, `B=Metallic`, i nie umieszczaj mapy normalnych w takim pakiecie. **Oczekiwany wynik:** podgląd pojedynczych kanałów zgadza się z manifestem.
9. **Skonfiguruj materiał skóry.** Dopasuj roughness, normal detail i SSS najpierw w skali rzeczywistej, bez kompensowania złej Base Color. **Oczekiwany wynik:** skóra zachowuje pory i miękkość, ale nie wygląda jak plastik ani wosk.
10. **Wykonaj test neutralnego oświetlenia.** Obejrzyj twarz bez korekcji artystycznej: w równomiernym świetle frontalnym, bocznym oraz po obrocie światła wokół nieruchomego modelu. **Oczekiwany wynik:** detal obraca się ze światłem, szwy nie ujawniają się, a na Base Color nie pozostaje „drugie”, nieruchome światło.

## Parametry liczbowe

**Rozdzielczość tekstury** określa liczbę tekseli na kafel i ilość zapisanego detalu. Wyższa zwiększa ostrość, pamięć oraz czas bake'u; niższa może zatrzeć pory. **Przykładowe wartości:** 2K (niska, dalszy LOD), 4K (typowa dla głowy czasu rzeczywistego), 8K (wysoka, zbliżenie lub master). Wybieraj ją z gęstości tekseli i budżetu, nie dla maskowania złego UV. Zbyt niska daje piksele i miękkie pory, zbyt wysoka nie poprawia obrazu, lecz zwiększa pamięć i migotanie mikrodetalu.

**Margines wypalania (bake padding)** rozszerza kolor poza wyspy UV. Większy chroni szwy w mipmapach, lecz może zalać sąsiednią wyspę. **Przykładowe wartości dla 4K:** 8 px (niska), 16 px (typowa), 32 px (wysoka); dla innej rozdzielczości skaluj proporcjonalnie. Mały margines ujawnia ciemne szwy z oddali, a zbyt duży powoduje przecieki koloru. Odstęp między wyspami musi pomieścić dylatację obu sąsiadów.

**Odsunięcie klatki** to odległość powierzchni cage od low-poly, mierzona w jednostkach sceny. Większa obejmuje odleglejszy high-poly, ale łatwiej chwyta obce powierzchnie. **Przykładowe wartości przy scenie w metrach:** 0,5 mm (niska), 2 mm (typowa), 5 mm (wysoka i tylko lokalnie). Wartość dobiera się do maksymalnej różnicy powierzchni. Za mała daje brakujące promienie i plamy, za duża — projekcje rzęs, warg lub przeciwległej strony nosa.

**Próbki bake'u** ograniczają szum map liczonych promieniami. Więcej próbek wygładza AO kosztem czasu. **Przykładowe wartości:** 16 (niska, test), 64 (typowa), 256 (wysoka, final). Za mało daje ziarnistość; bardzo wysoka wartość wydłuża bake bez widocznej poprawy. Pozostałe wartości, takie jak intensywność SSS czy skala displacement, zależą od konkretnego modelu cieniowania i muszą być zapisane w profilu wraz z analogicznym testem wartości niskiej, typowej i wysokiej.

## Editable output

Kanonicznym wynikiem jest wersjonowany plik sceny lub projektu tekstur `materials_master_vNNN` zawierający warstwy źródłowe, niedestrukcyjne maski, cage, ustawienia bake'u, przypisania przestrzeni barw, materiał oraz manifest zależności. Spłaszczone tekstury nie zastępują mastera.

### Zapis edytowalnego mastera

1. Usuń nieużywane testy, ale zachowaj źródła, maski i historię ustawień potrzebną do ponownego bake'u.
2. Zapisz względne odwołania do publicznych zasobów; prywatne zdjęcia pozostaw poza repozytorium i zanotuj ich kontrolne identyfikatory.
3. Zapisz atomowo nową wersję `materials_master_vNNN`, otwórz ją ponownie i sprawdź brakujące zależności.
4. Dołącz manifest z wersją siatek, UV, konwencją tangent space, rozdzielczością, paddingiem, kanałami i przestrzeniami barw.

## Derived output

- tekstury `BaseColor`, `Normal`, `Roughness`, `Metallic` i AO;
- opcjonalne `Displacement`, maski SSS i `Opacity`;
- pakiety kanałów zgodne z profilem środowiska docelowego;
- miniatury kanałów, render neutralnego światła i raport walidacji.

### Eksport artefaktów pochodnych

1. Eksportuj z mastera, bez ręcznego poprawiania plików wynikowych.
2. Zastosuj format, głębię bitową, konwencję normalnych i układ kanałów z profilu.
3. Zaimportuj komplet do czystego materiału w środowisku docelowym i zapisz log importu.
4. Wygeneruj render kontrolny i sumy kontrolne plików; każdy ponowny eksport może nadpisać wyłącznie artefakty pochodne tej wersji.

## Validation

- porównanie sylwetki i detalu low-poly z high-poly przy świetle przesuwanym po powierzchni;
- kontrola każdego kanału osobno, w tym pustych obszarów i szwów UV;
- test wypukłości kierunkowego detalu po imporcie do środowiska docelowego;
- test Base Color w trybie bez oświetlenia oraz test materiału w neutralnym świetle frontalnym i bocznym;
- kontrola mipmap z kilku odległości i zgodności manifestu z plikami.

| Objaw | Możliwa przyczyna | Naprawa |
| --- | --- | --- |
| Ciemne szwy z oddali | Za mały padding lub brak dylatacji | Zwiększ margines, odsuń wyspy i wykonaj bake ponownie. |
| Wgłębienia wyglądają jak wypukłości | Odwrócony kanał zielony mapy normalnych | Ustaw zgodną konwencję `+Y`/`-Y` i ponownie wyeksportuj. |
| Smugi z nosa na policzku | Cage chwyta sąsiednią powierzchnię | Popraw cage lokalnie i ogranicz odległość promieni. |
| Cień pozostaje podczas obrotu światła | Oświetlenie zapisane w Base Color | Ponownie usuń składową oświetlenia ze zdjęć. |
| Skóra wygląda jak plastik | Za niska roughness lub zbyt słaby mikrodetal | Skoryguj roughness na podstawie referencji; nie przyciemniaj Base Color. |
| Skóra wygląda jak wosk | Zbyt szerokie lub silne SSS | Zmniejsz promień/intensywność w profilu i sprawdź skalę sceny. |
| Kanał roughness ma zły kontrast | Błędnie odczytano go jako sRGB | Ustaw kanał jako dane liniowe i przeimportuj. |

## Failure conditions

Przejście dalej jest zablokowane, jeśli występuje choć jeden z warunków:

- bake zawiera chybną projekcję, brakujące promienie, odwrócone normalne lub widoczne szwy;
- konwencja tangent space, przestrzeń barw albo układ kanałów nie są udokumentowane i potwierdzone po imporcie;
- Base Color zawiera rozpoznawalne światło kierunkowe, blik albo wypalone cienie;
- materiał nie przechodzi testu neutralnego oświetlenia lub mipmap;
- nie można odtworzyć eksportu z wersjonowanego mastera albo brakuje raportu zależności.

## Definition of Done

Etap jest ukończony, gdy master otwiera się bez brakujących zależności, bake jest powtarzalny, wszystkie kanały i przestrzenie barw są zgodne z profilem, a zaimportowany materiał przechodzi kontrolę kanałów, szwów, mipmap i neutralnego światła bez efektu plastiku, wosku ani utrwalonego oświetlenia.

# 10. Ubrania

Ubranie jest osobnym, edytowalnym zasobem z własną konstrukcją, UV, materiałem i deformacją. Powinno wynikać z wykroju (sewing pattern) albo kontrolowanej bryły bazowej, a nie być jedynie odsuniętą kopią ciała. Symulacja jest opcjonalna; poprawny skinning i stabilna sylwetka pozostają wymagane także bez niej.

## Wymagania wstępne

- zatwierdzone ciało w pozycji spoczynkowej, skali rzeczywistej i stabilnej topologii;
- zatwierdzony szkielet, pozycja wiązania i zestaw animacji lub poz skrajnych;
- zdjęcia ubrania z przodu, tyłu i boków, wymiary oraz informacje o rodzaju tkaniny;
- budżet geometrii, materiałów, tekstur, kości i opcjonalnej symulacji;
- profil eksportu oraz collision proxies ciała albo możliwość ich utworzenia.

### Sprawdzenie wymagań

1. Porównaj identyfikator ciała i szkieletu z manifestem rigu. **Oczekiwany wynik:** pozycja wiązania i hierarchia kości są zgodne z eksportem docelowym.
2. Zmierz wzrost postaci i charakterystyczny wymiar ubrania. **Oczekiwany wynik:** scena i referencje używają jawnych jednostek.
3. Uruchom zestaw poz skrajnych na samym ciele. **Oczekiwany wynik:** animacje testowe są poprawne i obejmują stawy zasłaniane przez ubranie.
4. Otwórz profil budżetu oraz materiału. **Oczekiwany wynik:** znane są limity i wymagane kanały dla każdego elementu garderoby.

## Input

- wersja wzorcowa ciała, szkielet, bind pose i zestaw poz skrajnych;
- referencje, wymiary, opis konstrukcji oraz właściwości wizualne materiału;
- profile UV/PBR, skinningu, kolizji, LOD, symulacji i eksportu;
- numer wersji `vNNN` każdego elementu garderoby.

## Process

1. **Wybierz źródło konstrukcji.** Dla odzieży szytej odtwórz płaskie części wykroju i linie zszycia; dla elementu formowanego zbuduj czystą bryłę bazową z udokumentowanym odstępem od ciała. **Oczekiwany wynik:** każdy panel lub fragment bryły odpowiada widocznemu elementowi konstrukcyjnemu.
2. **Dopasuj sylwetkę w rest pose.** Ustal długość, obwody, luz i punkty podparcia bez kopiowania lokalnych nierówności ciała. **Oczekiwany wynik:** ubranie zachowuje charakter kroju i nie przecina neutralnego ciała.
3. **Nadaj grubość.** Stosuj rzeczywistą podwójną powierzchnię tam, gdzie widać krawędź, a uproszczenie shaderowe tylko zgodnie z profilem. **Oczekiwany wynik:** mankiety, kołnierze i brzegi mają wiarygodny przekrój bez podwójnych powierzchni.
4. **Zbuduj szwy i detale konstrukcyjne.** Umieść linie szycia, zakładki, lamówki, guziki oraz zamki zgodnie z wykrojem; drobne detale przenieś do map, jeśli geometria przekracza budżet. **Oczekiwany wynik:** szwy łączą właściwe panele i nie pływają po powierzchni.
5. **Wykonaj retopologię i UV.** Prowadź pętle zgodnie z fałdami i stawami, rozcinaj UV w miejscach konstrukcyjnych, wyrównaj gęstość tekseli i orientację splotu. **Oczekiwany wynik:** wzór tkaniny ma stałą skalę, a szwy UV są ukryte lub ciągłe wizualnie.
6. **Zbuduj materiały.** Oddziel Base Color od oświetlenia, przygotuj normalne włókien, roughness, AO i opcjonalną opacity; różne tkaniny otrzymują osobne, uzasadnione regiony materiałowe. **Oczekiwany wynik:** materiał komunikuje splot i masę bez namalowanych fałd oświetleniowych.
7. **Przenieś wagi wpływu kości (skin weights).** Skopiuj bazowe wagi z najbliższej powierzchni ciała, znormalizuj je i usuń wpływy niezgodne z konstrukcją ubrania. **Oczekiwany wynik:** ubranie podąża za szkieletem bez opóźnienia i zapadania między kośćmi.
8. **Dodaj korekty stawów.** Popraw barki, łokcie, nadgarstki, biodra, kolana i krok za pomocą wag, geometrii lub wersjonowanych kształtów korekcyjnych. **Oczekiwany wynik:** zgięcia zachowują objętość i nie rozciągają szwów jak guma.
9. **Zbuduj collision proxies.** Przygotuj proste, gładkie bryły ciała i warstw odzieży; ustal kolejność kolizji dla zestawów wielowarstwowych. **Oczekiwany wynik:** proxy pokrywają obszary kontaktu bez drobnych wklęśnięć destabilizujących solver.
10. **Skonfiguruj opcjonalną symulację.** Zaznacz obszary przytwierdzone i ruchome, przypisz parametry z pomiaru lub presetu tkaniny oraz zapisz cache tylko jako artefakt pochodny. **Oczekiwany wynik:** element wraca do stabilnego stanu, nie rozciąga się bez ograniczenia i nie eksploduje.
11. **Uruchom zestaw poz skrajnych.** Sprawdź co najmniej uniesienie oraz skrzyżowanie ramion, pełne zgięcie łokci i kolan, skręt tułowia, głęboki siad, szeroki krok i skrajne pochylenie. **Oczekiwany wynik:** nie ma krytycznej penetracji, odwrócenia ścian ani utraty objętości.
12. **Przygotuj LOD.** Redukuj niewidoczne warstwy i drobne detale, zachowując kontur, szwy konstrukcyjne oraz zgodność skinningu. **Oczekiwany wynik:** przejścia nie zmieniają kroju ani nie odsłaniają ciała.

## Parametry liczbowe

**Grubość** jest odległością między zewnętrzną i wewnętrzną powierzchnią materiału. Zwiększenie wzmacnia krawędzie i sztywność wizualną, zmniejszenie daje delikatną tkaninę. **Przykładowe wartości:** 0,3 mm (niska, cienka koszulka), 1 mm (typowa tkanina), 3 mm (wysoka, gruby materiał). Dobieraj ją do referencji i rzeczywistej skali. Za mała daje papierową, znikającą krawędź; za duża — tapicerowany wygląd i kolizje warstw.

**Luz konstrukcyjny** to różnica obwodu ubrania i ciała w danym przekroju. Większy zmienia dopasowanie i umożliwia fałdy. **Przykładowe wartości względne:** 1% (niska, ubranie dopasowane), 6% (typowa), 15% (wysoka, luźny krój). To punkty startowe zależne od fasonu i rozciągliwości. Za mały luz powoduje naprężenie i penetracje, za duży niekontrolowane fałdy oraz błędną sylwetkę.

**Margines kolizji** oddziela symulowaną powierzchnię od proxy. Większy ogranicza penetrację kosztem widocznej szczeliny. **Przykładowe wartości:** 2 mm (niska), 5 mm (typowa), 10 mm (wysoka dla grubej odzieży lub szybkiego ruchu). Za mały daje clipping i drgania, za duży sprawia, że ubranie lewituje. Dla warstw marginesy i kolejność rozwiązywania muszą być spójne.

**Sztywność zginania** opisuje opór tkaniny przed zmianą krzywizny; jednostka i skala zależą od solvera. Wyższa daje szerokie fałdy, niższa drobne. **Przykładowe wartości znormalizowanego presetu:** 0,1 (niska, miękka tkanina), 0,5 (typowa), 0,9 (wysoka, sztywny materiał). Za mała tworzy szum drobnych fałd i niestabilność, za duża zachowuje się jak blacha. Zapisuj nazwę i wersję solvera, bo liczby nie są przenośne.

**Kroki jakości symulacji** określają liczbę podkroków lub iteracji w klatce. Więcej zwiększa stabilność i koszt. **Przykładowe wartości:** 2 (niska, podgląd), 6 (typowa), 12 (wysoka, szybki ruch lub finalny cache). Za mało daje tunelowanie, rozciąganie i eksplozje; zbyt dużo wydłuża obliczenia bez widocznej korzyści. Jeśli solver rozdziela substeps i iterations, raportuj obie liczby i przetestuj każdą osobno.

## Editable output

Kanoniczny `clothing_<item>_master_vNNN` zawiera wykrój lub bryłę bazową, siatkę produkcyjną, konstrukcję szwów, grubość, UV, źródła materiałów, skin weights, kształty korekcyjne, LOD, collision proxies i ustawienia opcjonalnej symulacji. Cache i eksport nie zastępują mastera.

### Zapis edytowalnego mastera

1. Zachowaj osobno wzór/bryłę źródłową, siatkę produkcyjną, materiały, rigowanie i symulację.
2. Usuń tymczasowe cache, a wymagane wyniki oznacz jako artefakty pochodne możliwe do regeneracji.
3. Zapisz nową wersję `clothing_<item>_master_vNNN` z wersją ciała, szkieletu, bind pose i profilu solvera.
4. Otwórz kopię, odbuduj zależności i uruchom neutralną oraz jedną skrajną pozę przed zatwierdzeniem.

## Derived output

- siatki garderoby i materiały dla każdego LOD;
- tekstury PBR i spakowane kanały zgodne z profilem;
- collision proxies, opcjonalne cache symulacji i kształty wymagane przez środowisko docelowe;
- animacja zestawu poz skrajnych oraz raport penetracji i budżetu.

### Eksport artefaktów pochodnych

1. Powiel master i zastosuj operacje profilu, nie niszcząc źródła: triangulację, redukcję LOD lub bake symulacji.
2. Eksportuj w skali i osiach projektu z zachowaniem szkieletu, bind pose, wag, materiałów i nazw.
3. Zaimportuj do czystej sceny docelowej i ponownie przypisz profil materiału oraz kolizji.
4. Uruchom cały zestaw poz i opcjonalną symulację; zapisz raport, log importu i sumy kontrolne eksportów.

## Validation

- porównanie kroju, grubości, szwów, orientacji splotu i właściwości materiału z referencją;
- kontrola wag oraz zachowania objętości w bind pose i pełnym zestawie poz skrajnych;
- automatyczna lub wizualna kontrola penetracji ciała, odzieży i warstw odzieży;
- test stabilności opcjonalnej symulacji w spoczynku, szybkim ruchu i pętli animacji;
- pomiar budżetu i porównanie sylwetki wszystkich LOD w środowisku docelowym.

| Objaw | Możliwa przyczyna | Naprawa |
| --- | --- | --- |
| Materiał wygląda jak papier | Brak grubości lub zbyt ostry brzeg | Dodaj fizyczny przekrój w widocznych miejscach i popraw normalne. |
| Szew rozciąga się na łokciu | Złe wagi lub brak korekty stawu | Popraw skin weights i dodaj kształt korekcyjny. |
| Wzór obraca się między panelami | Niespójna orientacja UV | Obróć wyspy zgodnie z nitką tkaniny i wyrównaj skalę. |
| Ubranie lewituje | Za duży margines kolizji | Zmniejsz margines po sprawdzeniu stabilności solvera. |
| Symulacja eksploduje | Za mało kroków, nakładanie startowe lub złe jednostki | Usuń penetrację w klatce startowej, sprawdź skalę i zwiększ kroki. |
| Pachy lub krok zapadają się | Transfer wag z niewłaściwej powierzchni | Ręcznie popraw wagi i objętość w pozach skrajnych. |
| Ciało wychodzi przy zmianie LOD | Niezgodne LOD lub usunięta warstwa maskująca | Ujednolić redukcję, wagi i maskowanie ciała dla całego zestawu. |

## Failure conditions

Przejście dalej jest zablokowane, jeśli:

- ubranie nie ma edytowalnego wzoru lub bryły bazowej, własnych UV albo udokumentowanego materiału;
- skin weights, bind pose lub korekty stawów powodują krytyczne załamanie, rozciąganie szwów lub utratę objętości;
- w którejkolwiek wymaganej pozie występuje trwała penetracja widoczna z kamery produkcyjnej;
- opcjonalna symulacja jest niestabilna albo jej wyłączenie pozostawia nieakceptowalny wynik bazowy;
- LOD przekracza budżet, zmienia sylwetkę albo odsłania ciało;
- eksportu nie można powtórzyć z mastera i zapisanych profili.

## Definition of Done

Etap jest ukończony, gdy każdy element ma wersjonowany master z konstrukcją, UV, materiałem, wagami, korektami i kolizjami, wszystkie eksporty mieszczą się w budżecie, a neutralna poza, pełny zestaw poz skrajnych, przejścia LOD i opcjonalna symulacja przechodzą w środowisku docelowym bez krytycznych penetracji lub utraty sylwetki.

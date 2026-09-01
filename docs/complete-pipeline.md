# Instrukcja tworzenia awatara 3D

Dokument opisuje kolejność pracy. Nie przechodź do eksportu, dopóki etap poprzedni nie działa. Zawsze zachowuj edytowalny plik źródłowy sceny.

## 0. Załóż strukturę pracy

Utwórz osobne katalogi robocze dla: referencji, skanu, sceny źródłowej, retopologii, tekstur, rigu, animacji i eksportów. Nie zastępuj źródłowego pliku DCC eksportem FBX lub GLB.

Zdefiniuj jeden układ współrzędnych, skalę w centymetrach oraz nazwę wersji. Zapisuj tylko istotne etapy, na przykład `head_retopology_v01.blend`, a nie kopię po każdej drobnej zmianie.

## 1. Przygotuj referencje

1. Wykonaj zdjęcia twarzy z przodu, z obu profili i pod kątem 45 stopni. Zachowaj neutralny wyraz twarzy.
2. Wykonaj zdjęcia całej sylwetki z przodu, z boku i z tyłu. Stań prosto, z rękami lekko odsuniętymi od tułowia.
3. Zmierz wzrost, szerokość barków, długość ramion, obwód głowy oraz wymiary okularów.
4. Zrób dodatkowe zdjęcia oczu, zarostu, włosów, rzęs, ubrań i okularów w równym świetle.
5. Zachowaj materiały prywatnie. Do repozytorium dodawaj wyłącznie manifesty i zatwierdzone, nieobciążone prywatnością zasoby.

**Kontrola:** na referencjach są czytelne rysy twarzy, proporcje sylwetki, oprawki, zarost i charakter włosów.

## 2. Zbuduj lub zrekonstruuj główny mesh ciała

Główny mesh to jedna, animowana powierzchnia: głowa, szyja, tułów, ręce z dłońmi i palcami oraz nogi ze stopami. Nie modeluj w nim okularów, ubrań, gałek ocznych, rzęs, włosów ani brody.

1. Wykonaj rekonstrukcję ze zdjęć albo rozpocznij od bazowej siatki człowieka.
2. Dopasuj proporcje głowy, barków, klatki, ramion, dłoni, bioder i nóg do referencji.
3. Ustaw postać w neutralnej pozie A-pose lub T-pose. Pozę wybierz raz i utrzymaj we wszystkich etapach.
4. Zadbaj o zamkniętą, poprawną siatkę skóry. W głowie przygotuj otwór jamy ustnej oraz osobne miejsce na zęby i język.
5. Dodaj wystarczającą geometrię w stawach, ale nie zagęszczaj całego ciała bez potrzeby.

**Kontrola:** mesh ma poprawną skalę, nie ma dziur, odwróconych normalnych ani samoprzecięć.

## 3. Wykonaj retopologię pod animację

Retopologia ma umożliwiać ruch, a nie tylko dobrze wyglądać w spoczynku.

1. Prowadź pętle krawędzi wokół oczu, powiek, ust, żuchwy i policzków.
2. Dodaj pętle deformacji dla barków, łokci, nadgarstków, palców, bioder i kolan.
3. Przy palcach zachowaj wyraźne segmenty dla stawów. Każdy palec musi móc się zginać niezależnie.
4. Sprawdź siatkę w prostych pozach: zgięcie łokcia i kolana, uniesienie ręki, zamknięcie dłoni, otwarcie ust.
5. Dopiero po zaliczeniu testów przenieś detale ze skanu na normal map lub displacement.

**Kontrola:** ruch nie powoduje widocznego zapadania, ostrych fałd ani rozciągania twarzy.

## 4. Dodaj elementy przytwierdzone do ciała

Te elementy są osobnymi obiektami, ale podążają za ciałem lub głową.

### Oczy

1. Utwórz osobne gałki oczne: twardówkę, tęczówkę, źrenicę i rogówkę.
2. Ustaw ich środek w osi obrotu oka. Nie obracaj całej głowy, aby zmienić spojrzenie.
3. Dopasuj powieki do gałek ocznych, aby przy patrzeniu w górę i w dół nie przecinały oka.
4. Dodaj osobne kości lub kontrolery lewego i prawego oka.

### Rzęsy

1. Utwórz rzęsy jako osobne kępki, karty włosów albo groom przy górnej i dolnej powiece.
2. Podepnij je do powiek lub odpowiednich wierzchołków skóry.
3. Sprawdź mrugnięcie. Rzęsy nie mogą przenikać przez oko ani odrywać się od powieki.

### Włosy i broda

1. Włosy wykonaj jako groom, hair cards lub rozwiązanie mieszane, zależnie od środowiska docelowego.
2. Brodę i wąsy wykonaj osobno od mesha skóry. Unikaj zastępowania ich jedynie płaską teksturą.
3. Przytwierdź włosy do skóry głowy, a brodę i wąsy do twarzy. Ustaw naturalną linię włosów i kierunek wzrostu.
4. Jeśli włosy mają reagować na ruch, dodaj uproszczoną symulację dopiero po ukończeniu podstawowego rigu.

**Kontrola:** oczy obracają się niezależnie, powieki i rzęsy działają podczas mrugania, a włosy i broda pozostają na miejscu przy ruchu głowy.

## 5. Dodaj elementy dodatkowe

Elementy dodatkowe można wymieniać lub ukrywać bez zmiany głównego mesha.

### Ubrania

1. Modeluj każde ubranie jako osobny obiekt: koszulka, spodnie, buty i ewentualne dodatki.
2. Dopasuj ubranie do ciała w pozie bazowej, pozostawiając niewielki odstęp, aby uniknąć przenikania.
3. Przenieś wagi z ciała na ubranie, a następnie popraw ręcznie okolice barków, łokci, bioder i kolan.
4. Dodaj własne UV i materiały PBR. Nie używaj tekstur skóry jako tekstur ubrania.

### Okulary

1. Wykonaj oprawki i soczewki jako osobny model.
2. Umieść punkt mocowania przy nasadzie nosa lub na kości głowy.
3. Sprawdź, czy oprawki nie przenikają przez nos, brwi i rzęsy podczas mimiki.
4. Przygotuj materiał oprawek oraz przezroczysty materiał soczewek dla silnika docelowego.

**Kontrola:** ubranie deformuje się z ciałem, a okulary pozostają stabilne przy ruchu głowy i mimice.

## 6. Przygotuj UV i tekstury PBR

1. Rozłóż UV osobno dla skóry, oczu, włosów, brody, ubrań i okularów.
2. Dla każdego materiału przygotuj co najmniej Base Color, Normal i Roughness. Dodaj Metallic tylko tam, gdzie ma sens.
3. Dla skóry przygotuj AO oraz, gdy renderer obsługuje, parametry subsurface scattering.
4. Sprawdź mapy na modelu w świetle frontalnym i bocznym.

**Kontrola:** brak widocznych szwów, błędnych map i rozciągniętych detali.

## 7. Zbuduj rig ciała i dłoni

1. Utwórz szkielet z kością główną, miednicą, kręgosłupem, szyją i głową.
2. Dodaj kości dla obojczyków, ramion, przedramion, dłoni, nóg i stóp.
3. Dla każdej dłoni dodaj kości: nadgarstek, trzy segmenty dla każdego palca oraz odpowiednie segmenty kciuka.
4. Każdy palec ma mieć niezależny kontroler lub czytelne sterowanie FK. Dopuszczalny jest dodatkowy kontroler zbiorczy do zamykania dłoni.
5. Użyj IK dla rąk i nóg oraz FK tam, gdzie potrzebna jest precyzyjna poza.
6. Zrób skinning głównego mesha, a następnie przenieś i popraw wagi dla ubrań.

**Kontrola:** porusz każdy palec osobno, zaciśnij i otwórz dłoń, wykonaj zgięcie łokci, kolan, barków i stóp.

## 8. Zbuduj rig ust, szczęki i twarzy

1. Dodaj osobną żuchwę. Otwieranie ust musi wynikać z jej obrotu, a nie wyłącznie z przesuwania warg.
2. Dodaj zęby górne, zęby dolne i język jako osobne elementy. Dolne zęby oraz język podążają za żuchwą.
3. Utwórz kontrolery lub blend shapes dla warg, kącików ust, policzków, brwi i powiek.
4. Dodaj niezależne sterowanie oczami i mruganiem.
5. Przygotuj mapowanie zgodne z ARKit, FACS albo udokumentowaną konwersję między nimi.
6. Sprawdź otwarcie ust, uśmiech, zaciskanie warg, mrugnięcie, marszczenie brwi i spojrzenie w każdą stronę.

**Kontrola:** podczas otwierania ust porusza się żuchwa, dolne zęby i język; wargi nie rozrywają mesha.

## 9. Testuj ruch i popraw wagi

Wykonaj krótkie testy: chód, przysiad, uniesienie rąk, chwyt, wskazywanie palcem, mruganie, zmiana spojrzenia, otwieranie ust i kilka emocji. Popraw wagi tam, gdzie skóra lub ubranie zachowują się nienaturalnie.

Nie przechodź dalej, jeśli błąd jest widoczny w ruchu. Łatwiej poprawić rig i skinning przed animacją mowy niż po eksporcie.

## 10. Dodaj mowę i zachowanie

1. Wygeneruj audio za pomocą Piper.
2. Uzyskaj czas fonemów lub visemów.
3. Zamień visemy na kontrolery twarzy i ruch żuchwy.
4. Dodaj mruganie, spojrzenie, subtelny ruch głowy i prostą gestykulację.
5. Obejrzyj nagranie bez dźwięku i z dźwiękiem. W obu przypadkach mowa powinna wyglądać wiarygodnie.

## 11. Eksportuj i sprawdź w silniku

Eksportuj osobno edytowalny master oraz wersję docelową. Dołącz raport konwersji. W silniku sprawdź materiały, tekstury, szkielet, wagi, wszystkie palce, otwieranie ust, oczy, rzęsy, włosy, brodę, ubrania, okulary i animacje.

**Końcowa lista:**

- główny mesh ciała jest animowany;
- oczy są ruchome i niezależne;
- rzęsy, włosy i broda są osobnymi elementami przytwierdzonymi do ciała;
- ubrania i okulary są osobnymi elementami dodatkowymi;
- każdy palec obu dłoni porusza się niezależnie;
- usta otwierają się przez ruch żuchwy;
- postać przechodzi test mowy, mimiki i ruchu całego ciała.

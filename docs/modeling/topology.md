# Topologia produkcyjna

Topologia produkcyjna jest warstwą pośrednią pomiędzy rekonstrukcją/modelowaniem wysokiej rozdzielczości a riggingiem, UV, skinningiem, blend shapes i eksportem runtime. Jej celem nie jest mechaniczne zmniejszenie liczby wielokątów, lecz zaprojektowanie siatki, która zachowuje sylwetkę i istotne formy anatomiczne oraz deformuje się przewidywalnie.

## Pojęcia podstawowe

- **High-poly** – siatka źródłowa o wysokiej gęstości geometrii, pochodząca np. z fotogrametrii, skanu lub sculptingu. Przechowuje szczegóły powierzchni i stanowi referencję kształtu, ale zwykle nie nadaje się bezpośrednio do riggingu i pracy czasu rzeczywistego.
- **Low-poly** – zoptymalizowana siatka produkcyjna o kontrolowanej liczbie wielokątów. W tym projekcie termin nie oznacza stylistyki niskopoligonowej: model ma zachować fotorealistyczną sylwetkę, a detale high-poly są przenoszone m.in. przez mapy normalnych i displacement.
- **Siatka rozmaitościowa (manifold mesh)** – siatka opisująca poprawną powierzchnię, w której typowa krawędź powierzchni zamkniętej należy dokładnie do dwóch ścian, a lokalne sąsiedztwo wierzchołków nie tworzy rozgałęzień lub innych niejednoznaczności topologicznych. Elementy nierozmaitościowe wymagają naprawy przed zatwierdzeniem.
- **Przebieg krawędzi (edge flow)** – sposób prowadzenia kolejnych krawędzi i pętli względem anatomii, kierunku naprężeń oraz planowanych deformacji. Dobry edge flow pozwala zginać i skręcać ciało bez przypadkowych załamań powierzchni.
- **Biegun (pole)** – wierzchołek o walencji innej niż cztery w siatce quadów. Bieguny są normalnym narzędziem zmiany kierunku edge flow, lecz nie powinny być umieszczane w centrum silnej deformacji ani na kluczowej linii sylwetki, jeśli powodują pinching.
- **Pętla deformacyjna (deformation loop)** – pętla lub grupa pętli krawędzi zaprojektowana do kontrolowania kompresji, rozciągania i zachowania objętości podczas ruchu stawu. W praktyce pojedyncza linia krawędzi rzadko wystarcza: staw wymaga strefy deformacji.

## Wymagania ogólne

- Preferuj quady w obszarach deformacji; trójkąty stosuj tylko świadomie i poza krytycznymi strefami zgięcia.
- Usuń non-manifold geometry, wewnętrzne ściany, niezamierzone duplikaty i krawędzie zerowej długości.
- Dopasuj gęstość do funkcji. Staw wymaga większej kontroli niż płaska powierzchnia tułowia.
- Nie kompensuj błędnego edge flow samym zwiększaniem liczby polygonów.
- Utrzymuj czytelną ciągłość pętli między sąsiednimi segmentami ciała.
- Symetrię wykorzystuj jako narzędzie robocze, ale nie usuwaj charakterystycznej asymetrii osoby referencyjnej z finalnego kształtu.

## 1. Przygotowanie high-poly i sceny

### 1.1. Import i kontrola źródła

1. Zachowaj niezmodyfikowaną kopię siatki high-poly jako artefakt źródłowy.
2. Sprawdź kompletność skanu, orientację normalnych, dziury, fragmenty odłączone od ciała i artefakty rekonstrukcji.
3. Nie naprawiaj braków przez przypadkowe wygładzanie cech anatomicznych. W miejscach niepewnych korzystaj ze zdjęć referencyjnych.
4. Oddziel elementy, które docelowo będą osobnymi obiektami, np. okulary, oczy, ubrania czy włosy, jeśli zostały zeskanowane razem z ciałem.

### 1.2. Skala

Przed retopologią ustal jednostki sceny i rzeczywisty wzrost postaci. Zmierz co najmniej wysokość całkowitą oraz jeden dodatkowy wymiar kontrolny znany z rzeczywistości. Nie skaluj później niezależnie osi X/Y/Z w celu „poprawienia” proporcji.

Skala musi być stabilna przed riggingiem, ponieważ wpływa na położenie kości, parametry fizyki, odległości kamer, collision geometry i część procedur eksportowych.

### 1.3. Osie i układ współrzędnych

Ustal jeden kanoniczny układ projektu i udokumentuj konwersje wymagane przez DCC oraz silnik docelowy. Przed rozpoczęciem pracy:

1. ustaw postać pionowo;
2. ustaw płaszczyznę strzałkową na osi symetrii roboczej;
3. umieść stopy na wspólnej płaszczyźnie podłoża;
4. ustaw origin/root zgodnie z konwencją projektu;
5. zastosuj lub świadomie zachowaj transformacje obiektu tak, aby eksport nie wprowadzał ukrytej zmiany skali lub odbicia.

### 1.4. Symetria robocza

Retopologię ciała można rozpocząć na połowie modelu z modyfikatorem symetrii/mirror. Płaszczyzna odbicia musi przechodzić przez środek głowy, mostka, miednicy i przestrzeni między stopami. Wierzchołki osi środkowej powinny być scalane bez szczeliny i bez podwójnej geometrii.

Symetria jest narzędziem konstrukcyjnym. Po ustabilizowaniu topologii można odtworzyć rzeczywistą asymetrię kształtu przez projekcję na high-poly lub kontrolowaną korektę pozycji wierzchołków, nie zmieniając ich indeksacji.

### 1.5. Widoki referencyjne

Przygotuj co najmniej widok z przodu, z tyłu, z obu boków oraz ujęcia 3/4. Jeżeli fotografie mają istotną dystorsję perspektywiczną, nie traktuj ich jako ortograficznego wzorca proporcji. Ustaw referencje tak, aby punkty antropometryczne zgadzały się pomiędzy widokami: barki, łokcie, nadgarstki, kolce biodrowe, pachwiny, kolana, kostki i poziom podłoża.

Weryfikuj model jednocześnie względem high-poly i fotografii. Projekcja low-poly na błędny fragment skanu nie może mieć pierwszeństwa przed wiarygodną anatomią widoczną w materiałach referencyjnych.

## 2. Kolejność retopologii ciała

Zalecana kolejność ogranicza konieczność późniejszego przebudowywania połączeń:

1. **Tułów** – wyznacz linię środkową, klatkę piersiową, łuki żebrowe, talię, brzuch, grzbiet i obręcz miedniczną. Zbuduj duże, możliwie równomierne quady zgodne z kierunkiem deformacji.
2. **Obręcz barkowa** – poprowadź pętle z klatki przez mięsień naramienny do ramienia. Nie buduj ramienia jako cylindra doczepionego do płaskiej ściany tułowia.
3. **Pacha** – połącz przepływ klatki, pleców i ramienia, pozostawiając miejsce na kompresję przy opuszczaniu i przywodzeniu kończyny.
4. **Ramię i łokieć** – prowadź pętle wzdłuż osi kończyny, a przedramię przygotuj również na skręt pronacja/supinacja. Wokół łokcia zbuduj kontrolowaną strefę zgięcia.
5. **Nadgarstek** – przejdź do gęstości dłoni bez gwałtownego skoku rozdzielczości. Szczegóły dłoni opisano w `hands-and-feet.md`.
6. **Miednica i pośladki** – zaprojektuj ciągły przepływ między brzuchem, grzbietem, pośladkiem i pachwiną. Miednica nie powinna być prostym cylindrem rozdzielonym na dwie nogi.
7. **Pachwina i biodro** – utwórz strefę umożliwiającą zgięcie, odwiedzenie i rotację uda bez zapadania krocza i utraty objętości pośladka.
8. **Udo i kolano** – utrzymuj pętle zgodne z masą mięśniową i przygotuj kilka pierścieni deformacyjnych wokół kolana.
9. **Podudzie i kostka** – prowadź edge flow przez łydkę do kostek, zachowując ich asymetryczną anatomię i wystarczającą geometrię do zgięcia stawu skokowego.
10. **Stopa** – przejdź do topologii pięty, łuków i palców zgodnie z algorytmem w `hands-and-feet.md`.

Po każdym większym regionie sprawdź sylwetkę z wielu kierunków. Nie odkładaj korekty proporcji do końca retopologii.

## 3. Krytyczne strefy deformacji

### Bark

**Funkcja pętli:** otoczyć masę mięśnia naramiennego i rozprowadzić ruch ramienia na klatkę oraz łopatkę. Pętle powinny umożliwiać uniesienie i rotację ramienia bez ostrej granicy między barkiem a tułowiem.

**Objawy błędu:** zapadnięcie pachy, „odcięty” bark, ostre załamanie przy uniesieniu ręki, utrata objętości deltoidu, rozciągnięte quady na górnej powierzchni barku.

### Pacha

**Funkcja pętli:** zapewnić zapas geometrii do kompresji i rozciągania pomiędzy klatką, mięśniem piersiowym, plecami i ramieniem.

**Objawy błędu:** zlepienie powierzchni przy opuszczonej ręce, dziura lub głęboki pinching przy uniesieniu, nienaturalna błona między ramieniem a tułowiem albo silne rozciągnięcie tekstury.

### Łokieć

**Funkcja pętli:** utworzyć strefę zawiasową z kompresją po stronie zginaczy i zachowaniem objętości/kształtu wyrostka łokciowego po stronie grzbietowej.

**Objawy błędu:** „gumowa rurka”, ostry klin po wewnętrznej stronie, spłaszczenie łokcia, utrata objętości przy około 90–120° zgięcia lub spiralne załamania podczas skrętu przedramienia.

### Pachwina i biodro

**Funkcja pętli:** przenieść deformację pomiędzy miednicą, pośladkiem i udem podczas zgięcia, odwiedzenia oraz rotacji. Edge flow powinien pozostawiać geometrię na fałd pachwinowy bez przecinania go przypadkowymi biegunami.

**Objawy błędu:** zapadanie krocza, „przyklejenie” uda do miednicy, utrata objętości pośladka, ostry fałd przy zgięciu lub rozciąganie polygonów przy odwiedzeniu nogi.

### Kolano

**Funkcja pętli:** zachować przednią formę rzepki, zapewnić kompresję z tyłu kolana i płynne przejście uda w podudzie. Kilka pierścieni rozkłada deformację zamiast koncentrować ją na jednej krawędzi.

**Objawy błędu:** zgnieciona lub przesuwająca się rzepka, ostry klin w dole podkolanowym, utrata objętości, „gumowe” kolano albo przenikanie powierzchni przy głębokim zgięciu.

### Kostka

**Funkcja pętli:** zachować kostkę przyśrodkową i boczną oraz umożliwić zgięcie grzbietowe/podeszwowe bez deformowania pięty i śródstopia jak jednego miękkiego segmentu.

**Objawy błędu:** znikające kostki, załamanie siatki na przodzie stawu, zwężenie stawu podczas zgięcia, niekontrolowane obracanie pięty lub utrata płaskiego kontaktu stopy z podłożem.

## 4. Rozmieszczanie biegunów

Bieguny wykorzystuj do redukcji lub rozdzielenia pętli. Umieszczaj je na względnie stabilnych powierzchniach, gdzie nie przecinają głównej linii zgięcia i nie tworzą widocznego artefaktu na sylwetce. Szczególnie unikaj skupiania biegunów:

- w centrum pachy;
- na przedniej i tylnej linii zgięcia łokcia;
- w fałdzie pachwinowym;
- na rzepce i w dole podkolanowym;
- na przedniej linii zgięcia kostki.

Każdy biegun o walencji 5+ w strefie ruchomej powinien zostać sprawdzony w deformacji, a nie tylko w neutralnej pozie.

## 5. Testowy skinning przed topology freeze

Retopologia nie jest zatwierdzana wyłącznie na podstawie wyglądu siatki statycznej. Przed zamrożeniem wykonaj tymczasowy rig i testowy skinning. Nie musi to być finalny rig produkcyjny, ale osie stawów i długości segmentów muszą być anatomiccznie wiarygodne.

### Procedura

1. Utwórz minimalny szkielet: root/miednica, kręgosłup, obojczyki, ramiona, przedramiona, dłonie, uda, podudzia i stopy.
2. Ustaw centra rotacji na podstawie anatomii, nie na podstawie środka geometrycznego przekroju siatki.
3. Wykonaj początkowe automatyczne lub ręczne wagi.
4. Usuń oczywiste wpływy kości po przeciwnej stronie ciała i nielogiczne długozasięgowe weighty.
5. Przetestuj pojedyncze stawy, następnie pozy złożone.
6. Obserwuj jednocześnie objętość, sylwetkę, kompresję polygonów, rozciąganie i położenie biegunów.
7. Jeśli problem wynika z edge flow, popraw topologię zamiast maskować go ekstremalnymi wagami.
8. Powtórz test po każdej istotnej zmianie pętli.

### Minimalny zakres poz testowych

Przed topology freeze należy sprawdzić co najmniej:

- neutralną pozę referencyjną;
- ramiona w dół, około 45°, 90° oraz nad głową;
- odwiedzenie i przywiedzenie ramienia;
- rotację wewnętrzną i zewnętrzną barku;
- zgięcie łokcia: 0°, około 45°, 90°, 120° i możliwe maksimum;
- pronację i supinację przedramienia;
- zgięcie, wyprost i skręt tułowia;
- zgięcie biodra: neutralne, około 45°, 90° i głębokie;
- odwiedzenie oraz rotację uda;
- zgięcie kolana: 0°, około 45°, 90°, 120° i głębokie;
- zgięcie grzbietowe i podeszwowe stopy;
- pozycję stojącą, wykrok/przysiad oraz wspięcie na palce;
- co najmniej jedną asymetryczną pozę całego ciała łączącą skręt tułowia z różnym ustawieniem kończyn.

Testy dłoni i stóp należy dodatkowo wykonać zgodnie z `hands-and-feet.md`.

Ocena powinna obejmować zarówno skrajne pozy diagnostyczne, jak i zakres typowy dla naturalnej animacji. Ekstremalna poza może ujawnić problem, ale nie uzasadnia pogorszenia deformacji w najczęściej używanym zakresie ruchu.

## 6. Checklista błędów technicznych i naprawa

Przed zamrożeniem topologii sprawdź:

- [ ] **Non-manifold geometry** – zaznacz automatycznie elementy nierozmaitościowe; usuń wewnętrzne ściany, rozgałęzienia i niepoprawne połączenia, następnie ponów test.
- [ ] **Otwarte krawędzie w powierzchni, która ma być zamknięta** – zlokalizuj boundary edges i zamknij je kontrolowaną topologią, nie przypadkowym fill.
- [ ] **Zduplikowane wierzchołki/ściany** – scal wyłącznie elementy, które powinny być wspólne; sprawdź, czy operacja nie skleiła odrębnych powierzchni.
- [ ] **Odwrócone lub niespójne normalne** – przelicz orientację, a następnie ręcznie sprawdź regiony złożone.
- [ ] **Degeneraty i krawędzie zerowej długości** – usuń lub przebuduj lokalny patch.
- [ ] **N-gony w strefach deformacji** – przebuduj na przewidywalne quady/trójkąty przed skinningiem.
- [ ] **Długie, cienkie lub silnie skośne quady** – rozłóż wierzchołki zgodnie z krzywizną i kierunkiem deformacji.
- [ ] **Nagłe skoki gęstości** – redukuj pętle stopniowo, przenosząc bieguny do spokojniejszych regionów.
- [ ] **Biegun na linii zgięcia** – przekieruj edge flow i przesuń pole poza strefę maksymalnej kompresji.
- [ ] **Pinching** – sprawdź walencję, triangulację wynikową, odstępy między pętlami i wagi; przebuduj patch, jeśli artefakt jest topologiczny.
- [ ] **Utrata objętości stawu** – dodaj lub przesuń pętle podtrzymujące; dopiero potem koryguj skinning/corrective shapes.
- [ ] **Nierównomierne odstępy pętli** – zagęść strefę kompresji i pozostaw przestrzeń na rozciąganie, unikając przypadkowego skupienia krawędzi.
- [ ] **Niezamierzona asymetria topologiczna** – porównaj strony. Asymetria kształtu jest dozwolona, ale asymetria connectivity powinna być świadomą decyzją.
- [ ] **Interpenetracja w pozach testowych** – ustal, czy wynika z topologii, wag, osi stawu czy geometrii sąsiedniego elementu; napraw przyczynę, nie tylko konkretną pozę.
- [ ] **Zmiana sylwetki względem high-poly/referencji** – skoryguj położenie wierzchołków przez kontrolowaną projekcję i ręczne dopasowanie bez niszczenia edge flow.

Po naprawie błędu technicznego ponów walidację manifold oraz test skinningu obszaru. Naprawa nie jest zakończona, jeżeli jedynie przesunęła artefakt do sąsiedniej pozy.

## 7. Topology freeze

**Zamrożenie topologii (topology freeze)** jest formalnym punktem akceptacji, po którym connectivity siatki i indeksacja wierzchołków stają się kontraktem dla kolejnych etapów pipeline.

### Warunki zatwierdzenia

Topology freeze można ogłosić dopiero, gdy:

1. sylwetka i proporcje są zaakceptowane względem high-poly i fotografii;
2. siatka przechodzi kontrolę manifold i checklistę techniczną;
3. edge flow wszystkich głównych stawów został sprawdzony testowym skinningiem;
4. dłonie i stopy przeszły własne testy deformacji;
5. nie przewiduje się dodawania/usuwania wierzchołków w bazowym body mesh;
6. uzgodniono granice obiektów i miejsca połączeń z głową, oczami, ubraniem i innymi zależnymi elementami;
7. wersja bazowej siatki została zapisana jako jednoznacznie oznaczony, wersjonowany artefakt.

### Artefakt freeze

Zapisz co najmniej:

- wersję źródłową DCC;
- wyeksportowaną siatkę bazową w ustalonym formacie interoperacyjnym;
- liczbę wierzchołków, krawędzi i ścian;
- nazwę obiektu/mesha i wersję;
- informację o jednostkach, osiach i pozie bazowej;
- identyfikator commita/release lub inny trwały identyfikator wersji;
- raport/checklistę testów deformacji.

Od tego momentu dozwolone są korekty pozycji istniejących wierzchołków, o ile nie naruszają uzgodnionych zależności i są wersjonowane. Dodawanie, usuwanie, scalanie, dzielenie lub zmiana kolejności wierzchołków wymaga traktowania siatki jako nowej rewizji topologii.

## 8. Dlaczego vertex IDs są kontraktem

UV, skin weights, blend shapes/morph targets, corrective shapes, cache animacji i część narzędzi transferowych może odwoływać się do wierzchołków przez ich indeks. Dwie siatki mogą wyglądać identycznie i mieć tę samą liczbę wierzchołków, a mimo to być niezgodne, jeśli zmieniła się ich kolejność.

Zmiana **vertex IDs** po topology freeze może spowodować:

- przypisanie wag skinningu do niewłaściwych punktów;
- eksplozję lub deformację blend shapes;
- błędne mapowanie danych korekcyjnych i symetrii;
- utratę zgodności cache'y i eksportów;
- konieczność ponownego bake'u lub transferu zależnych danych;
- trudne do wykrycia błędy, gdy narzędzie nie zgłosi niezgodności, lecz zastosuje dane do złych indeksów.

Jeżeli zmiana connectivity po freeze jest nieunikniona, nie nadpisuj starego artefaktu. Utwórz nową wersję topologii, zachowaj poprzednią siatkę i przeprowadź jawną migrację: UV, skin weights, blend shapes/correctives oraz pozostałe dane zależne należy przetransferować i ponownie zwalidować. Po migracji cały zestaw testów deformacji musi zostać wykonany ponownie.

Topology freeze nie oznacza końca pracy nad wyglądem. Oznacza stabilizację struktury siatki, na której bezpiecznie mogą być budowane kosztowne zależności produkcyjne.
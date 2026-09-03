# Dłonie i stopy

Dłonie i stopy wymagają osobnej kontroli topologicznej. Są zbudowane z wielu krótkich segmentów, pracują w dużym zakresie ruchu i zawierają charakterystyczne punkty anatomiczne, których utrata szybko obniża realizm awatara. Topologię należy projektować pod rig i deformację, a nie tylko pod wygląd w pozie neutralnej.

## 1. Algorytm retopologii dłoni

### Krok 1. Ustal proporcje i punkty anatomiczne

1. Dopasuj obrys dłoni do high-poly i fotografii referencyjnych.
2. Oznacz nadgarstek, głowy kości śródręcza, stawy MCP, PIP i DIP oraz końce palców.
3. Nie zakładaj identycznych długości palców ani równych odcinków paliczków. Zachowaj proporcje konkretnej osoby.
4. Sprawdź długość każdego palca zarówno od strony grzbietowej, jak i dłoniowej; błona międzypalcowa optycznie zmienia miejsce, z którego palec wydaje się wyrastać.

### Krok 2. Zbuduj główną bryłę dłoni

1. Rozpocznij od możliwie prostego patcha obejmującego śródręcze.
2. Zachowaj klinowaty charakter dłoni zamiast modelować ją jako płaską deskę.
3. Uwzględnij łuk poprzeczny dłoni oraz podłużne zróżnicowanie wysokości głów kości śródręcza.
4. Pozostaw geometrię umożliwiającą „złożenie” dłoni podczas chwytu: strona łokciowa może zbliżać się do kciuka, a głowy śródręcza nie powinny pozostawać w jednej sztywnej płaszczyźnie.

### Krok 3. Rozmieść stawy MCP

Stawy **MCP (metacarpophalangeal)** tworzą podstawową linię zgięcia palców, ale ich osie nie powinny być reprezentowane jako jedna idealnie prosta poprzeczna krawędź. Rozmieść pętle zgodnie z rzeczywistym łukiem nasad palców.

Dla każdego MCP pozostaw strefę kilku pętli: centralną linię kontrolującą zgięcie oraz pętle wspierające po obu stronach. Muszą umożliwiać zarówno zgięcie, jak i niewielkie odwiedzenie/przywiedzenie palców.

### Krok 4. Zbuduj palce i proporcje paliczków

1. Prowadź każdy palec jako kontrolowany ciąg quadów od MCP do opuszki.
2. Zachowaj indywidualne długości paliczka bliższego, środkowego i dalszego zgodnie z referencją.
3. Nie umieszczaj PIP i DIP w geometrycznym środku segmentów „na oko”. Punkty zgięcia muszą odpowiadać anatomii i późniejszym osiom kości.
4. Zmieniaj przekrój palca wzdłuż długości; palec nie jest cylindrem o stałej średnicy.
5. Zachowaj objętość opuszki i miejsce na płytkę paznokciową.

### Krok 5. Pętle PIP i DIP

Dla **PIP (proximal interphalangeal)** i **DIP (distal interphalangeal)** zbuduj strefy deformacyjne pozwalające na kompresję od strony dłoniowej oraz rozciąganie od strony grzbietowej. Zbyt mała liczba pętli daje ostre zgięcie, natomiast nadmierne zagęszczenie bez funkcji utrudnia skinning.

W neutralnej pozie odstępy mogą być lekko nierównomierne, jeśli wynika to z planowanej kompresji. Oceniaj rozmieszczenie w zgięciu około 90°, nie tylko przy wyprostowanym palcu.

### Krok 6. Błona międzypalcowa

1. Nie łącz palców ostrym rowkiem sięgającym do MCP.
2. Zbuduj błonę międzypalcową jako powierzchnię przejściową pomiędzy sąsiednimi palcami.
3. Zapewnij geometrię umożliwiającą rozstawienie palców bez tworzenia cienkiego, nienaturalnego trójkąta.
4. Bieguny potrzebne do rozdzielenia edge flow umieszczaj poza centrum błony i poza głównymi liniami zgięcia.

### Krok 7. Podstawa kciuka

Kciuk wymaga osobnego przepływu topologii. Nie powinien być cylindrem doczepionym do boku dłoni.

1. Wyznacz masę kłębu kciuka.
2. Poprowadź pętle wokół podstawy kciuka tak, aby przenosiły deformację na śródręcze.
3. Zapewnij zakres dla opozycji, odwiedzenia, przywiedzenia i rotacji kciuka.
4. Sprawdź przestrzeń między kciukiem i palcem wskazującym w pinch oraz w szeroko otwartej dłoni.
5. Nie umieszczaj skupiska biegunów dokładnie w fałdzie podstawy kciuka.

### Krok 8. Łuki dłoni

Topologia musi wspierać co najmniej:

- łuk poprzeczny śródręcza;
- łuk związany z ustawieniem głów kości śródręcza;
- lokalną deformację kłębu kciuka i kłębika palca małego.

Podczas chwytu dłoń powinna zmieniać przekrój i tworzyć zagłębienie, zamiast zachowywać płaską powierzchnię.

### Krok 9. Pętle chwytu (grip loops)

Pętle chwytu to funkcjonalne pętle deformacyjne biegnące przez stronę dłoniową i okolice podstaw palców. Powinny wspierać fałdy powstające podczas zamykania dłoni oraz przenosić kompresję z MCP na środek dłoni.

Sprawdź je na pięści i chwycie cylindrycznym. Jeżeli po zamknięciu dłoni powierzchnia tworzy pojedynczy ostry rowek albo pozostaje zupełnie płaska, edge flow wymaga korekty.

### Krok 10. Paznokcie

Paznokcie powinny być kontrolowanym elementem geometrii, a nie przypadkowym szczegółem normal mapy, jeżeli mają być widoczne w zbliżeniach.

1. Zachowaj naturalną krzywiznę płytki paznokciowej.
2. Dopasuj jej szerokość i długość do referencji.
3. Nie zagłębiaj paznokcia jak otworu w palcu.
4. Utrzymuj wystarczającą geometrię wałów paznokciowych i opuszki.
5. Jeżeli paznokieć jest osobnym meshem, zapewnij stabilne dopasowanie do deformującego się paliczka dalszego i unikaj z-fightingu.

### Krok 11. Połączenie z nadgarstkiem

Stopniowo przejdź z gęstej topologii dłoni do przedramienia. Zachowaj czytelne formy kostne nadgarstka i nie redukuj wielu pętli w jednym skupisku biegunów na linii zgięcia. Połączenie musi wytrzymać zgięcie, wyprost oraz odchylenie promieniowe i łokciowe.

## 2. Algorytm retopologii stopy

### Krok 1. Ustal płaszczyznę kontaktu

1. Ustaw stopę względem rzeczywistej płaszczyzny podłoża.
2. Wyznacz punkty kontaktu: piętę, głowy śródstopia i obszary palców uczestniczące w podporze.
3. Nie spłaszczaj całej podeszwy do jednej płaszczyzny. Łuki stopy muszą pozostać czytelne.
4. Sprawdź obie stopy osobno; różnice kształtu mogą być rzeczywiste.

### Krok 2. Zbuduj piętę

Pięta powinna zachować objętość guza piętowego i miękkiej poduszki podporowej. Prowadź pętle wokół pięty tak, aby nie zapadała się przy plantarflexion ani przy wspięciu na palce.

Tylna część stopy musi przechodzić w okolicę ścięgna Achillesa bez ostrego przewężenia wynikającego wyłącznie z topologii.

### Krok 3. Odtwórz łuki stopy

Uwzględnij przede wszystkim łuk podłużny przyśrodkowy, niższy łuk boczny oraz łuk poprzeczny przodostopia. Nie modeluj ich jako dekoracyjnych wgłębień. Powinny wynikać z przestrzennej formy podeszwy i śródstopia.

Topologia ma umożliwiać niewielką zmianę tych łuków pod obciążeniem, jeżeli późniejszy rig lub corrective shapes będą to realizować.

### Krok 4. Śródstopie

1. Prowadź pętle wzdłuż głównych osi stopy, ale pozwól im rozchodzić się w kierunku pięciu promieni śródstopia.
2. Zachowaj rozszerzenie przodostopia względem środkowej części stopy.
3. Nie sprowadzaj całego śródstopia do jednego sztywnego bloku, jeśli awatar ma wspierać realistyczny toe-off.
4. Rozmieść redukcje pętli poza strefą intensywnego zginania u nasad palców.

### Krok 5. Nasady palców

Linia stawów MTP/nasad palców nie jest idealnie prosta. Zbuduj strefę deformacyjną umożliwiającą zgięcie palców podczas przetaczania stopy i wspięcia na palce.

Duży palec wymaga szczególnej kontroli, ponieważ przenosi znaczną część końcowej fazy podporu. Zachowaj jego objętość i możliwość wyprostu bez zapadania powierzchni u podstawy.

### Krok 6. Palce

Dostosuj liczbę segmentów do planowanego rigu. Jeżeli palce mają być animowane indywidualnie, każdy istotny staw musi otrzymać wystarczającą strefę deformacyjną. Nie zwiększaj jednak gęstości tylko dlatego, że high-poly zawiera drobne zmarszczki; detale powierzchni przenoś do PBR.

### Krok 7. Kostka i połączenie z podudziem

Zachowaj różnicę położenia kostki przyśrodkowej i bocznej. Pętle powinny rozprowadzać zgięcie stawu skokowego na podudzie i stopę bez przesuwania pięty jak miękkiego przedłużenia łydki.

Przednią strefę zgięcia pozostaw wystarczająco gęstą do dorsiflexion, lecz unikaj skupiska biegunów dokładnie w miejscu największej kompresji.

### Krok 8. Kontrola płaszczyzny podporu

W neutralnym staniu sprawdź stopę na płaskiej powierzchni bez penetracji. Wagi i topologia powinny umożliwiać zachowanie stabilnego kontaktu podczas przenoszenia ciężaru. Nie koryguj błędnego kształtu stopy przez przesuwanie samej płaszczyzny podłoża.

## 3. Testy deformacji dłoni i stóp

Testy wykonuj na tymczasowym rigu przed **zamrożeniem topologii (topology freeze)**. Każdy błąd najpierw sklasyfikuj jako problem topologii, osi stawu, skin weights lub brakującej korekty objętości. Nie próbuj naprawiać wszystkich problemów samym weight paintingiem.

### Test 1. Otwarta dłoń

**Procedura:** wyprostuj palce, następnie wykonaj ich umiarkowane odwiedzenie; kciuk ustaw od pozycji neutralnej do szerokiego odwiedzenia.

**Oczekiwany rezultat:** naturalny wachlarz palców, zachowany łuk MCP, płynna błona międzypalcowa, brak naprężonych trójkątów i brak zapadania podstawy kciuka.

**Korekta:** przesuń pętle błony, rozłóż bieguny poza strefą rozciągania, popraw orientację osi MCP lub dodaj geometrię tylko tam, gdzie rzeczywiście brakuje powierzchni do rozciągnięcia.

### Test 2. Pięść

**Procedura:** zegnij kolejno MCP, PIP i DIP do pełnej, naturalnej pięści; kciuk ułóż na zewnątrz palców zgodnie z naturalnym chwytem.

**Oczekiwany rezultat:** palce tworzą zwarty kształt bez przenikania, kostki MCP pozostają czytelne, strona dłoniowa kompresuje się w fałdy, a opuszki nie tracą objętości.

**Korekta:** przesuń pętle stawowe względem osi rotacji, zwiększ przestrzeń po stronie kompresji, popraw grip loops i wagi; przy utracie objętości rozważ corrective shape dopiero po potwierdzeniu poprawnej topologii.

### Test 3. Uszczypnięcie (pinch)

**Procedura:** zetknij opuszkę kciuka z opuszką palca wskazującego, następnie sprawdź wariant precyzyjny z niewielką przestrzenią między pozostałymi palcami.

**Oczekiwany rezultat:** opozycja kciuka przebiega po naturalnym łuku, przestrzeń między kciukiem a wskazującym nie zapada się, opuszki stykają się bez nienaturalnego spłaszczenia.

**Korekta:** popraw topologię i rig podstawy kciuka, zweryfikuj rotację kości kciuka oraz wagi kłębu; usuń bieguny powodujące pinching w pierwszej przestrzeni międzypalcowej.

### Test 4. Chwyt

**Procedura:** wykonaj chwyt cylindryczny na obiekcie o realistycznej średnicy oraz, opcjonalnie, chwyt większego obiektu.

**Oczekiwany rezultat:** palce owijają obiekt, dłoń tworzy zagłębienie, łuki śródręcza uczestniczą w chwycie, kciuk przeciwstawia się palcom, a kontakt nie wymaga penetracji geometrii.

**Korekta:** popraw grip loops, rozkład wag śródręcza i osie MCP; jeśli dłoń pozostaje płaska, dodaj kontrolę cup/palm arch w rigu lub corrective shape zamiast nadmiernie zginać same palce.

### Test 5. Zgięcie grzbietowe (dorsiflexion)

**Procedura:** unieś przodostopie w kierunku podudzia w realistycznym zakresie, utrzymując piętę jako punkt odniesienia.

**Oczekiwany rezultat:** kompresja pojawia się głównie z przodu kostki, pięta i łuki zachowują objętość, kostki pozostają rozpoznawalne, a siatka nie tworzy ostrego klina.

**Korekta:** przesuń pętle stawu skokowego, usuń pole z linii kompresji, skoryguj oś stawu i gradient wag. Jeżeli powierzchnia nadal traci objętość przy poprawnej topologii, zastosuj korektę zależną od pozy.

### Test 6. Zgięcie podeszwowe (plantarflexion)

**Procedura:** skieruj stopę w dół, kontrolując przejście od podudzia przez kostkę do pięty i śródstopia.

**Oczekiwany rezultat:** górna powierzchnia stawu rozciąga się płynnie, pięta nie zapada się, ścięgno Achillesa zachowuje czytelną formę, a stopa nie wygląda jak sztywno obrócony klocek połączony z łydką.

**Korekta:** popraw rozkład pętli z tyłu i po bokach kostki, gradient skin weights oraz położenie osi; przy lokalnym pinching przebuduj patch zamiast zwiększać smoothing wag.

### Test 7. Wspięcie na palce

**Procedura:** ustaw piętę nad podłożem, obciążając przodostopie i zginając stopę w okolicy nasad palców; sprawdź również duży palec.

**Oczekiwany rezultat:** przetoczenie odbywa się przez przodostopie, nasady palców zginają się po naturalnym łuku, duży palec zachowuje podporę, pięta unosi się bez utraty objętości, a płaszczyzna kontaktu pozostaje stabilna w obszarze podporowym.

**Korekta:** przesuń pętle MTP/nasad palców do rzeczywistej osi zgięcia, rozdziel wpływy kości stopy i palców, popraw geometrię pod głowami śródstopia. Jeśli przodostopie załamuje się na jednej krawędzi, poszerz strefę deformacyjną o dodatkowe pętle.

## 4. Kryterium akceptacji

Dłonie i stopy mogą zostać przekazane do topology freeze tylko wtedy, gdy wszystkie powyższe testy przechodzą bez krytycznego pinching, utraty objętości, interpenetracji wynikającej z topologii ani widocznego załamania sylwetki. Drobne problemy możliwe do rozwiązania przez skin weights lub corrective shapes należy zapisać jawnie jako zadania kolejnego etapu; nie wolno w ten sposób maskować błędnego edge flow.

Po topology freeze nie zmieniaj liczby ani kolejności wierzchołków bez uruchomienia procedury migracji opisanej w `topology.md`, ponieważ skinning, morph targets i inne dane mogą zależeć od stabilnych vertex IDs.
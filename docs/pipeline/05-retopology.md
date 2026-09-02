# 05. Retopologia

**Input:** zatwierdzony high-poly z etapu 04.  
**Editable output:** `avatar_body_retopo_vNNN.blend`.  
**Gate:** po akceptacji następuje topology freeze.

## Cel etapu

Retopologia zamienia nieregularną siatkę skanu w siatkę przeznaczoną do deformacji i animacji. Nie chodzi o minimalizację liczby polygonów za wszelką cenę. Priorytetem jest przewidywalny edge flow wokół stawów i twarzy, zachowanie sylwetki oraz możliwość późniejszego tworzenia blend shapes.

## Przygotowanie

1. Otwórz oczyszczony high-poly jako obiekt referencyjny.
2. Utwórz nowy mesh deformacyjny. Nie edytuj bezpośrednio high-poly.
3. Włącz snapping/shrinkwrap do powierzchni skanu.
4. Ustal docelową gęstość siatki dla wersji wzorcowej. LOD powstają później.
5. Zachowaj osobne obiekty dla oczu, zębów, języka, włosów, ubrań i okularów.

## Kolejność pracy

### 1. Tułów i główne proporcje

Najpierw zbuduj duże powierzchnie tułowia, miednicy, szyi i głowy. Kontroluj sylwetkę w widoku przód, bok i 3/4. Siatka ma przylegać do high-poly bez wygładzania charakterystycznych proporcji.

### 2. Twarz

Twarz wymaga pętli zgodnych z kierunkiem deformacji mięśniowej. Zbuduj co najmniej:

- koncentryczne pętle wokół ust;
- koncentryczne pętle wokół oczu;
- przepływ od skrzydełek nosa do bruzdy nosowo-wargowej;
- pętle wspierające policzek i kąciki ust;
- czytelny przepływ wzdłuż żuchwy;
- geometrię pozwalającą na niezależny ruch górnej i dolnej powieki.

Nie kończ twarzy na podstawie neutralnego wireframe'u. Już podczas retopologii testuj tymczasowe deformacje `jaw open`, `blink`, `smile`, `frown` i `cheek raise`.

### 3. Barki i pachy

Bark jest jednym z najtrudniejszych obszarów deformacji. Pętle powinny pozwalać na rotację ramienia bez zapadania klatki piersiowej i bez nadmiernego rozciągania pachy. Dodaj wystarczającą liczbę segmentów wokół deltoidu i łopatki.

### 4. Łokcie i kolana

Wokół stawu stosuj kilka pętli rozłożonych po obu stronach osi zgięcia. Przy pełnym zgięciu geometria po stronie wewnętrznej musi mieć miejsce na kompresję, a po stronie zewnętrznej na rozciągnięcie.

### 5. Nadgarstki i kostki

Unikaj pojedynczej pętli pełniącej rolę całego stawu. Nadgarstek i kostka wymagają rozłożenia rotacji na kilka segmentów, szczególnie gdy później będą używane twist bones.

### 6. Dłonie

Każdy palec powinien mieć osobne segmenty odpowiadające stawom. Zachowaj geometrię dla zgięcia MCP/PIP/DIP oraz opozycji kciuka. Nie upraszczaj kciuka do zwykłego palca obróconego pod kątem.

### 7. Stopy

Zachowaj geometrię pięty, śródstopia, nasady palców i dużego palca. Nawet jeżeli palce stóp nie będą niezależnie animowane w każdej scenie, ich topologia nie może tworzyć artefaktów podczas kontaktu stopy z podłożem.

## Gęstość siatki

Większa gęstość jest uzasadniona w regionach:

- powiek;
- ust;
- nosa;
- uszu;
- palców;
- barków;
- łokci i kolan.

Mniejsza gęstość wystarcza na dużych, mało deformujących się fragmentach tułowia. Zmiany gęstości wprowadzaj stopniowo, aby uniknąć długich cienkich quadów.

## Poles i triangles

Docelowa siatka deformacyjna powinna być głównie quadowa. Poles są dopuszczalne, ale nie umieszczaj ich bezpośrednio w najbardziej deformujących się częściach powieki, kącika ust, pachy czy zgięcia stawu. Triangles mogą być używane lokalnie po świadomej ocenie deformacji, ale nie powinny zastępować poprawnego edge flow.

## Test deformacji przed topology freeze

Utwórz prosty tymczasowy rig lub użyj deformatorów i sprawdź co najmniej:

1. `jaw open`;
2. pełny blink;
3. szeroki uśmiech;
4. shoulder raise;
5. arm abduction 90–120°;
6. elbow flexion około 130°;
7. pronation/supination przedramienia;
8. wrist flexion/extension;
9. pełną pięść;
10. squat;
11. knee flexion;
12. dorsiflexion stopy.

Jeżeli problem wymaga przesuwania dużej liczby vertexów przy każdej pozie, popraw edge flow przed topology freeze.

## Kontrola podobieństwa

Retopologia może nieświadomie zmienić twarz przez zbyt silny shrinkwrap, smoothing albo uśrednianie. Porównuj nowy mesh z high-poly i fotografiami. W szczególności sprawdź profil nosa, usta, żuchwę, uszy i asymetrię policzków.

## Topology freeze

Po zatwierdzeniu topologii:

1. zapisz wersję oznaczoną jako approved;
2. zapisz liczbę vertices i faces;
3. zapisz hash pliku;
4. nie dodawaj ani nie usuwaj vertexów bez jawnego otwarcia nowej rewizji topologii;
5. UV, skinning i blend shapes powinny odnosić się do tej samej wersji vertex order.

Zmiana topology po rozpoczęciu blend shapes zwykle unieważnia kolejne artefakty.

## Inspekcja w Avatar Studio

W etapie 05 wybierz **Run supported operation** i wskaż scenę `.blend`. Raport powinien pozwolić potwierdzić m.in. liczbę vertices, polygons i obecność oczekiwanych obiektów. Następnie zarejestruj zatwierdzoną scenę jako artefakt.

## Typowe błędy

### Siatka wygląda dobrze w A-pose, ale psuje się w ruchu

Retopologia była oceniana statycznie. Wróć do testów deformacji i dodaj lub przesuń pętle w kierunku zginania.

### Usta tracą objętość przy otwarciu szczęki

Pętle wokół ust i żuchwy są zbyt płytkie lub źle rozłożone. Sprawdź też geometrię wnętrza jamy ustnej.

### Powieka przecina oko

Edge flow powieki i jej grubość nie odpowiadają kulistej geometrii gałki ocznej. Popraw geometrię przed riggingiem.

### Bark zapada się przy podniesieniu ręki

Potrzebna jest lepsza topologia deltoidu/łopatki i później poprawny joint placement oraz corrective shapes. Nie próbuj rozwiązać całego problemu wyłącznie weight paintem.

## Validation

Sprawdź:

- zgodność vertex order zatwierdzonej wersji;
- brak przypadkowych n-gonów w krytycznych regionach;
- logiczne pętle twarzy;
- osobne i deformowalne palce;
- poprawne joint loops;
- zachowanie sylwetki i podobieństwa;
- przejście testowych póz bez krytycznych artefaktów.

## DoD

Topologia jest gotowa do UV, rigu i blend shapes, ma zatwierdzony vertex order, poprawny edge flow w obszarach deformacji i przeszła testy ruchu. Dopiero wtedy można wykonać topology freeze.

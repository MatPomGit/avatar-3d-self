# 16. Skinning

**Input:** zatwierdzona topologia, rig ciała, dłoni i twarzy oraz ubrania.  
**Editable output:** skin weights i corrective deformation setup.  
**Derived output:** raport deformacji i zestaw póz walidacyjnych.

## Cel etapu

Skinning wiąże siatkę z kośćmi. Poprawny skinning nie oznacza wyłącznie braku widocznych dziur. Powinien zachowywać objętość tkanek, poprawnie rozkładać skręt i zgięcie oraz współpracować z corrective shapes tam, gdzie sama interpolacja wag nie wystarcza.

## Przygotowanie

1. Upewnij się, że topologia i rig są zatwierdzone.
2. Nie zmieniaj joint placement w trakcie weight paintingu bez ponownego otwarcia etapu rigu.
3. Wykonaj kopię sceny przed automatycznym bindem.
4. Oddziel deform bones od control bones.
5. Przygotuj zestaw referencyjnych póz walidacyjnych.

## Procedura

### 1. Initial bind

Wykonaj automatyczny bind wyłącznie jako punkt startowy. Sprawdź, czy wszystkie vertices otrzymały wagę i czy nie ma nieoczekiwanych wpływów od odległych kości.

### 2. Ogranicz liczbę influences

Dostosuj liczbę wpływających kości do docelowego runtime. Typowy silnik czasu rzeczywistego ma limit influences per vertex. Nie redukuj ich mechanicznie bez sprawdzenia barków, dłoni, twarzy i obszarów twist.

### 3. Bark

Testuj arm abduction, forward raise i rotation. Zachowaj objętość deltoidu oraz naturalny ruch pachy. Jeżeli weight painting wymaga ekstremalnych wartości, sprawdź wcześniej joint placement i topologię.

### 4. Łokieć i kolano

Przy pełnym zgięciu powierzchnia wewnętrzna powinna się kompresować, a zewnętrzna rozciągać bez ostrego załamania. Rozłóż wpływ na kilka pętli siatki.

### 5. Twist

Sprawdź pronation/supination przedramienia i rotację uda. Twist powinien być rozłożony wzdłuż segmentu, a nie kumulowany w jednym pierścieniu vertexów.

### 6. Nadgarstek i dłoń

Testuj osobno każdy palec, opozycję kciuka, pełną pięść, chwyt cylindryczny i precyzyjny. Zwróć uwagę na webbing między palcami i zapadanie się nasady kciuka.

### 7. Biodra i pośladki

Testuj siad, squat i wysoki krok. Zachowaj objętość pośladków oraz stabilne połączenie uda z miednicą.

### 8. Szyja i żuchwa

Weighty szyi nie powinny powodować przesuwania szczęki ani klatki. Dolna część twarzy musi współpracować z facial rig i jaw bone bez podwójnej deformacji.

### 9. Ubrania

Ubrania mogą korzystać z transferu wag z ciała, ale wymagają osobnej korekty. Sprawdź penetrację ciała, szczególnie w pachach, biodrach, kolanach i przy siedzeniu.

### 10. Corrective shapes

Dodaj corrective shapes tylko tam, gdzie problem wynika z ograniczeń liniowego skinningu, a nie z błędnego rigu. Typowe regiony to bark, łokieć, biodro, kolano i nadgarstek.

Corrective shape powinien aktywować się deterministycznie na podstawie pozy lub kombinacji kości i nie zmieniać neutralnej sylwetki.

## Poses walidacyjne

Minimalny zestaw:

1. neutral A/T-pose;
2. ręce do góry;
3. ręka przez klatkę piersiową;
4. elbow 130°;
5. pronation i supination;
6. pełna pięść;
7. chwyt cylindryczny;
8. squat;
9. siad 90° biodra/kolana;
10. wysoki krok;
11. head yaw ±60°;
12. neck flexion/extension;
13. jaw open z ruchem szyi;
14. kombinacja ekspresji twarzy z ruchem głowy.

## Ocena objętości

Porównuj deformację nie tylko do neutralnego meshu, ale do oczekiwanej anatomii. Szczególnie kontroluj:

- objętość barku;
- przedramię podczas twist;
- pośladki w siadzie;
- łydkę i kolano przy zgięciu;
- nasadę kciuka;
- policzki i żuchwę podczas mowy.

## Normalizacja wag

Wagi powinny być znormalizowane zgodnie z wymaganiami silnika. Szukaj vertices bez wpływu lub z sumą wag niezgodną z kontraktem eksportowym. Przed finalnym eksportem usuń wpływy od kości kontrolnych, które nie są przeznaczone do deformacji.

## Inspekcja w Avatar Studio

Uruchom inspekcję sceny `.blend` z etapu 16 i zarejestruj scenę oraz raport deformacji. Obecna inspekcja automatyczna potwierdza obecność armature i podstawową strukturę sceny, ale wizualna ocena wag i corrective shapes nadal wymaga Blender/DCC.

## Typowe błędy

### Candy-wrapper twist

Skręt jest skupiony w jednym miejscu. Dodaj lub popraw twist bones i rozłóż weighty na długości kończyny.

### Zapadnięty bark

Najpierw sprawdź pozycję jointu i clavicle. Następnie popraw weights i dopiero na końcu dodaj corrective shape.

### Ubranie przenika ciało tylko w jednej pozie

Transfer wag był niewystarczający. Popraw lokalne weighty albo dodaj korektę odzieży dla krytycznej pozy.

### Dłoń wygląda dobrze w pięści, ale źle w chwycie precyzyjnym

Walidacja była zbyt wąska. Testuj kilka funkcjonalnych chwytów, nie tylko maksymalne zgięcie palców.

## Validation

Etap przechodzi, gdy:

- nie ma vertices bez wag;
- liczba influences spełnia budżet runtime;
- barki, biodra i stawy zachowują objętość;
- twist nie tworzy candy-wrapper artifacts;
- dłonie przechodzą zestaw funkcjonalnych chwytów;
- ubrania nie mają krytycznych penetracji;
- corrective shapes nie zmieniają neutralnej pozy;
- twarz i jaw nie otrzymują podwójnej deformacji.

## DoD

Skinning przechodzi pełny zestaw póz walidacyjnych bez krytycznych artefaktów. Raport deformacji, lista corrective shapes i zatwierdzona scena są zarejestrowane jako artefakty. Zmiana rigu lub topology po tym etapie unieważnia skinning i zależne animacje.

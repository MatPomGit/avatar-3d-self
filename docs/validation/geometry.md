# Walidacja geometrii

Walidujemy osobno high-poly scan, retopology master i eksport runtime. Progi zależą od etapu.

## Retopology master

Wymagania pass:

- brak non-manifold edges, poza jawnie udokumentowanymi otworami technicznymi;
- brak zerowych powierzchni trójkątów i zduplikowanych wierzchołków na szwach, które miały być spawane;
- brak odwróconych normalnych;
- brak niezamierzonych self-intersections w pozie bazowej;
- skala zgodna z pomiarem wysokości do ±0.5%;
- symetria nie jest wymagana i nie może nadpisywać rzeczywistej asymetrii osoby.

## Topologia deformacyjna

Co najmniej 3 ciągłe pętle deformacyjne wokół ust i oczu muszą zachować stabilność podczas podstawowych ekspresji, ale liczba pętli nie jest celem sama w sobie. Test praktyczny ma pierwszeństwo.

## Gęstość

Nie ustalamy globalnego limitu polygonów dla mastera. Raport zawiera vertices, faces, triangles, bounding box, liczbę UV sets, materiałów i shape keys. Runtime LOD posiada osobny budżet.

## UV

Sprawdzamy overlapping UV tylko w miejscach jawnie zaprojektowanych. Padding po bake powinien odpowiadać minimum 8 px w docelowej teksturze 4K, preferowane 16 px dla atlasów pod mipmapping.

## Raport

Każdy błąd otrzymuje `error`, `warning` albo `accepted_exception` z opisem przyczyny.
# LOD i skalowanie jakości

LOD redukuje koszt geometrii, materiałów, groomu, blend shapes i kości. Nie ograniczamy się do redukcji trójkątów.

## Baseline desktop

Dla pojedynczego bohatera na PC przyjmujemy następujący punkt startowy:

| Poziom | Ekran / dystans orientacyjny | Geometria względem LOD0 | Facial shapes | Hair |
| --- | --- | ---: | ---: | --- |
| LOD0 | close-up, głowa >300 px wysokości | 100% | pełny zestaw | pełny groom/cards |
| LOD1 | medium shot | 55% | 70-100% | uproszczony |
| LOD2 | full body | 25% | kluczowe 30-50% | cards / niższa gęstość |
| LOD3 | daleki plan | 10% | 0-20% | bardzo uproszczony |

Wartości procentowe są baseline, a nie absolutną liczbą polygonów. LOD0 jest wyznaczany przez jakość podobieństwa i target engine.

## Twarz

Przy redukcji zachowujemy pętle powiek, ust i sylwetkę nosa dłużej niż detale policzków. Normal map i tekstury mogą przenosić część mikrodetalu. W LOD2 można łączyć część shape keys, ale blink, jaw i podstawowy smile/frown pozostają.

## Skeleton LOD

Kości palców mogą zostać ograniczone w dalekim planie tylko wtedy, gdy dłonie zajmują mało pikseli. Jaw, eyes, head i podstawowe kości twarzy są zachowane dłużej, ponieważ błędy twarzy są percepcyjnie kosztowne.

## Hair LOD

Najpierw redukujemy gęstość groomu, następnie przechodzimy do cards/hybrid. Sylwetka fryzury ma pozostać stabilna między poziomami.

## Histereza

LOD nie może przełączać się przy pojedynczym progu. Stosujemy 10-15% histerezy odległości lub screen size i opcjonalny cross-fade 100-250 ms, jeśli silnik na to pozwala.

## Walidacja

Przejście LOD testujemy na wolnym dolly-in/out oraz obrocie postaci. Kryteria: brak wyraźnego poppingu sylwetki, oczu, fryzury i ekspresji.
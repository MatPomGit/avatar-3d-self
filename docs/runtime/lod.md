# Poziomy szczegółowości i skalowanie jakości

Poziom szczegółowości (Level of Detail, LOD) to wariant tego samego zasobu przeznaczony dla innej wielkości postaci na ekranie. Im mniejsza postać w kadrze, tym mniej detalu można zachować bez widocznej utraty jakości. Prawidłowy LOD redukuje koszt obliczeń tam, gdzie oko użytkownika nie jest w stanie wykorzystać dodatkowego szczegółu.

LOD nie oznacza wyłącznie redukcji liczby trójkątów. W cyfrowym człowieku redukcji mogą podlegać również włosy, tekstury, liczba kości, liczba aktywnych kształtów deformacyjnych, złożoność materiałów, cienie i ruch wtórny.

## Wielkość na ekranie zamiast samej odległości

Odległość od kamery jest łatwa do wykorzystania, ale nie zawsze jest najlepszym kryterium. Postać znajdująca się 2 m od kamery szerokokątnej może zajmować mniej ekranu niż postać z tej samej odległości przy długiej ogniskowej.

Dlatego decyzję LOD preferujemy opierać na wielkości obiektu na ekranie, np. wysokości głowy lub postaci w pikselach, jeśli środowisko docelowe to umożliwia.

## Profil desktopowy

Punkt startowy dla pojedynczego awatara wysokiej jakości:

| Poziom | Przykładowa sytuacja | Geometria względem LOD0 | Twarz | Włosy |
| --- | --- | ---: | --- | --- |
| LOD0 | zbliżenie, głowa >300 px | 100% | pełny zestaw | pełny system |
| LOD1 | plan średni | 50-60% | 70-100% kanałów | uproszczony |
| LOD2 | pełna sylwetka | 20-30% | kluczowe 30-50% | niższa gęstość / płaszczyzny |
| LOD3 | daleki plan | 8-15% | 0-20% | bardzo uproszczony |

Są to wartości startowe. Ostateczne progi wynikają z testu percepcyjnego i wydajnościowego.

## Co redukować najpóźniej

Twarz jest percepcyjnie bardziej wrażliwa niż wiele innych obszarów. Dlatego podczas redukcji geometrii najdłużej zachowujemy:

- sylwetkę nosa;
- kontur ust;
- pętle powiek;
- kąciki oczu;
- linię żuchwy;
- charakterystyczne fałdy i asymetrie wpływające na podobieństwo.

Mikrodetal skóry może wcześniej zostać przeniesiony do map normalnych niż geometria odpowiedzialna za sylwetkę.

## LOD twarzy

W LOD0 dostępny jest pełny kontrakt ARKit/FACS i kształty korekcyjne.

W LOD1 można ograniczyć część rzadko używanych korekt, ale mruganie, ruch oczu, żuchwa, uśmiech, marszczenie i główne ruchy ust pozostają pełne.

W LOD2 można łączyć część kanałów o podobnym efekcie wizualnym, ale podstawowa mowa musi pozostać czytelna.

W LOD3 animacja twarzy może zostać bardzo ograniczona, jeżeli twarz zajmuje tak mało pikseli, że pełne ekspresje nie są rozpoznawalne.

## LOD szkieletu

Redukcja szkieletu polega na ograniczeniu kości, których wpływ nie jest już widoczny. Kości palców mogą zostać usunięte wcześniej niż głowa, oczy i żuchwa.

Nie usuwamy kości wyłącznie dlatego, że ich udział w geometrii jest mały. Kość o małym obszarze wpływu może być kluczowa dla sylwetki lub mimiki.

## LOD włosów

Włosy redukujemy etapami:

1. zmniejszenie liczby włosów renderowanych;
2. zmniejszenie liczby prowadnic;
3. uproszczenie dynamiki;
4. przejście do płaszczyzn z teksturą włosów;
5. ograniczenie cieni i ruchu wtórnego w dalekim planie.

Najważniejszym kryterium jest zachowanie sylwetki fryzury. Jeżeli po przełączeniu LOD głowa wydaje się nagle węższa albo szersza, redukcja jest zbyt agresywna.

## Histereza

Histereza (hysteresis) oznacza użycie różnych progów dla przejścia na niższy i wyższy poziom jakości. Zapobiega to szybkiemu przełączaniu między dwoma LOD, gdy obiekt znajduje się dokładnie na granicy progu.

Dla wartości bazowej stosujemy różnicę 10-15%. Przykładowo, jeżeli przejście LOD0 -> LOD1 następuje przy 300 px wysokości głowy, powrót LOD1 -> LOD0 może nastąpić dopiero przy 330-345 px.

Zbyt mała histereza powoduje migotanie jakości. Zbyt duża sprawia, że postać zbyt długo pozostaje na niewłaściwym poziomie.

## Łagodne przejście

Jeżeli silnik wspiera łagodne przejście, można użyć krótkiego przenikania 100-250 ms. Nie powinno ono jednak maskować źle przygotowanych LOD. Duża różnica sylwetki będzie widoczna nawet przy długim przenikaniu.

## Walidacja

Test LOD wykonujemy przy:

- wolnym zbliżeniu kamery;
- wolnym oddaleniu;
- obrocie postaci;
- animacji twarzy;
- mowie;
- mocnym oświetleniu bocznym;
- zmianie fryzury w ruchu.

Etap zaliczamy, jeśli nie występuje czytelne przeskakiwanie sylwetki, oczu, fryzury, ubrania ani podstawowych ekspresji.
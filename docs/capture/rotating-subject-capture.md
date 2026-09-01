# Fotogrametria sylwetki z obracającą się osobą

Ten workflow jest przeznaczony dla sytuacji, w której jedna osoba wykonuje zdjęcia własnej sylwetki bez operatora kamery. Kamera pozostaje nieruchoma, a osoba wykonuje serię kontrolowanych obrotów.

Metoda jest praktyczna i wspierana w Avatar Studio, ale wymaga innego podejścia do matching i segmentacji niż klasyczna fotogrametria statycznej sceny.

## Cel

Uzyskać kompletną geometrię całej sylwetki 360° przy zachowaniu możliwie stałej anatomii między klatkami.

## Przygotowanie stanowiska

### Kamera

- statyw, bez przesunięć w czasie jednej serii;
- ogniskowa 50-70 mm equivalent dla pełnej klatki, baseline 55 mm;
- ręczna ekspozycja;
- czas 1/125 s lub krótszy;
- f/5.6-f/8, jeśli aparat pozwala;
- ISO możliwie niskie, zwykle 100-400;
- stały balans bieli;
- wyłączony HDR, portrait mode, upiększanie i automatyczna zmiana obiektywu.

### Tło

Najlepsze jest tło:

- jednolite;
- matowe;
- kontrastujące z ubraniem i włosami;
- bez ruchomych przedmiotów;
- oświetlone osobno i możliwie równomiernie.

Tło ma ułatwiać maskowanie, nie dostarczać punktów do rekonstrukcji.

### Podłoga

Na podłodze przygotuj:

- centralny punkt osi obrotu;
- okrąg lub wielokąt z pozycjami co 10°;
- znaczniki lewej i prawej stopy;
- linię kierunku patrzenia.

Jeżeli używasz platformy obrotowej, platforma musi być sztywna, stabilna i nie może zmieniać wysokości osoby.

## Liczba zdjęć

Profil domyślny:

| Profil | Krok | Liczba pozycji |
| --- | ---: | ---: |
| minimalny | 15° | 24 |
| standard | 10° | 36 |
| high quality | 7,5° | 48 |

Dla całego ciała zaleca się co najmniej dwa poziomy aparatu, a najlepiej trzy:

1. okolice miednicy/tułowia;
2. barki/klatka;
3. głowa lekko z góry.

W praktyce standardowa sesja zawiera 72-108 zdjęć.

## Procedura pojedynczego kroku

Dla każdego kąta:

1. obróć całe ciało razem ze stopami;
2. ustaw stopy na znacznikach;
3. wyprostuj kolana bez przeprostu;
4. ustaw miednicę nad środkiem stóp;
5. ustaw mostek i głowę w osi ciała;
6. przywróć A-pose;
7. sprawdź symetrię dłoni i odległość rąk od tułowia;
8. spójrz w ustalony punkt;
9. odczekaj 2 s;
10. wyzwól migawkę.

Nie wykonuj obrotu samym tułowiem.

## Kontrola pozy

Dopuszczalny praktyczny dryf względem sąsiedniej pozycji:

- miednica względem osi obrotu: <=10 mm;
- wysokość barków: <=10 mm;
- dłonie: <=15 mm;
- łokcie względem tułowia: <=10 mm;
- orientacja głowy: <=1°.

Jeżeli te wartości są regularnie przekraczane, trzeba zwiększyć opóźnienie przed zdjęciem lub uprościć pozę.

## Oddech

Pełne zatrzymywanie oddechu przez długą serię jest niewykonalne. Przyjmujemy kontrolowany naturalny oddech.

Najlepsza procedura:

1. spokojny wdech;
2. spokojny wydech;
3. zdjęcie pod koniec naturalnego wydechu, bez wymuszonego zapadania klatki.

Dzięki temu zmienność obwodu klatki jest mniejsza.

## Włosy

Długie lub ruchome włosy należy na czas rekonstrukcji sylwetki ustabilizować. Docelowa fryzura jest później rekonstruowana z osobnych referencji.

Dla krótkich włosów wystarczy unikać gwałtownych obrotów przed zdjęciem.

## Ubranie

Do rekonstrukcji anatomii używaj możliwie dopasowanej, matowej odzieży bez połysku i dużych fałd.

Jeżeli celem jest również geometria konkretnego ubrania, wykonaj drugą serię przeznaczoną wyłącznie dla ubrania.

## Maskowanie

Maskowanie osoby jest integralną częścią tego workflow.

Baseline dla 4K:

- maska binarna lub alpha;
- rozszerzenie krawędzi o 3-8 px;
- ręczna kontrola włosów, dłoni i przestrzeni między nogami;
- brak tła wewnątrz maski;
- maski przechowywane jako edytowalne artefakty.

Maska nie może wycinać drobnych części palców, uszu ani obrysu włosów.

## Matching i rekonstrukcja

Nie należy estymować ruchu kamery na podstawie nieruchomego pokoju. Rekonstrukcja ma być obiektocentryczna.

Praktyczna kolejność:

1. segmentacja foreground;
2. feature extraction wewnątrz maski;
3. matching pomiędzy sąsiednimi kątami;
4. rekonstrukcja lokalnych segmentów;
5. kontrola spójności sylwetki;
6. połączenie/cleanup;
7. skala z rzeczywistych pomiarów.

Jeśli pojedynczy solve 360° jest niestabilny, podziel serię na cztery sektory po około 90° i połącz je później na podstawie wspólnych fragmentów geometrii.

## Kontrola jakości po sesji

Utwórz szybki flipbook lub animację z kolejnych zdjęć. Szukaj:

- skoków pozycji dłoni;
- zmiany wysokości barków;
- rotacji głowy niezależnej od ciała;
- falowania ubrania;
- przesuwania włosów;
- różnic ekspozycji;
- nieostrych klatek.

Każdy wyraźny skok należy oznaczyć w manifeście i powtórzyć, jeśli to możliwe.

## Tryb awaryjny

Jeżeli nie można uzyskać pełnego solve:

- zachowaj serię jako referencję proporcji;
- zrekonstruuj przód, boki i tył jako niezależne fragmenty;
- użyj pomiarów antropometrycznych do kontroli skali;
- połącz geometrię ręcznie w Blenderze;
- retopologię wykonaj dopiero po zatwierdzeniu proporcji.

## Definition of Done

Workflow można uznać za zaliczony, gdy:

- jest pełne pokrycie 360°;
- krok kątowy jest zapisany w manifeście;
- maski foreground są kompletne;
- co najmniej 90% klatek jest ostre i użyteczne;
- nie ma dużych skoków pozy między sąsiednimi ujęciami;
- skala została nadana na podstawie co najmniej trzech rzeczywistych pomiarów;
- wynik pozwala wiarygodnie odtworzyć proporcje całej sylwetki.

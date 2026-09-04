# 02. Fotogrametria

**Input:** zatwierdzona seria zdjęć z etapu 01.  
**Editable output:** baza COLMAP, parametry kamer i sparse reconstruction.  
**Derived output:** sparse point cloud, raport jakości zdjęć, opcjonalny zestaw zdjęć po preprocessingu oraz raport operacji.

## Cel etapu

Celem nie jest jeszcze utworzenie gęstej siatki człowieka. Najpierw trzeba sprawdzić, czy zdjęcia tworzą spójny geometrycznie model kamer i punktów 3D. Ten etap odpowiada na pytanie: **czy zestaw zdjęć jest wystarczająco spójny, aby bezpiecznie przejść do dense reconstruction?**

Sparse reconstruction jest krytycznym punktem kontroli. Jeżeli model jest fragmentaryczny, dense reconstruction zwykle tylko zwiększy koszt obliczeń i utrwali wcześniejsze błędy.

## Przygotowanie

Przed uruchomieniem:

1. Upewnij się, że wszystkie zdjęcia pochodzą z jednej spójnej sesji i nie zostały przeskalowane.
2. Usuń jedynie pliki technicznie uszkodzone. Nie usuwaj zdjęć tylko dlatego, że wydają się mniej estetyczne.
3. Jeżeli używano jednej kamery i nie zmieniano obiektywu ani zoomu, traktuj serię jako `single camera`.
4. Nie mieszaj zdjęć twarzy i pełnego ciała wykonanych w skrajnie innych warunkach optycznych bez jawnego rozdzielenia sesji.
5. Dla osoby obracającej się przed nieruchomą kamerą przeczytaj również [Rotating-subject capture](../capture/rotating-subject-capture.md). Taki materiał jest trudniejszy niż klasyczna fotogrametria nieruchomego obiektu.

## Kontrola jakości partii zdjęć przed COLMAP

Przed uruchomieniem rekonstrukcji sparse należy wykonać automatyczną ocenę całej partii zdjęć. Avatar Studio zawiera moduł `photo_quality.py` oraz polecenie `scripts/photo_batch.py`, które analizują każde zdjęcie i relację pomiędzy kolejnymi ujęciami.

Wymagane są zależności `vision`:

```bash
pip install -e ".[vision]"
```

Analizę uruchamia się poleceniem:

```bash
python scripts/photo_batch.py analyze references/photos \
  --report reports/photo_quality_report.json
```

Raport obejmuje:

- ostrość ocenianą przez wariancję Laplasjanu;
- średnią luminancję i wykrywanie niedoświetlenia lub prześwietlenia;
- udział pikseli obciętych w cieniach i światłach;
- kontrast globalny;
- liczbę dopasowanych cech pomiędzy kolejnymi zdjęciami;
- udział dopasowań zgodnych z homografią RANSAC;
- syntetyczny `overlap_score` opisujący siłę pokrycia pomiędzy kolejnymi ujęciami;
- listę zdjęć sugerowanych do ponownego wykonania;
- listę par zdjęć o zbyt małym pokryciu.

### Interpretacja overlapu

Overlap nie jest liczony jako proste podobieństwo pikseli. Moduł wykrywa cechy ORB w dwóch sąsiednich zdjęciach, dopasowuje deskryptory, odrzuca niejednoznaczne dopasowania testem ilorazowym i następnie wykorzystuje RANSAC do oceny zgodności geometrycznej. Takie podejście jest bardziej odporne na zmianę punktu widzenia niż korelacja całych obrazów.

Niski overlap może oznaczać:

1. zbyt duży skok kątowy pomiędzy zdjęciami;
2. zbyt małą liczbę stabilnych cech powierzchni;
3. zmianę ekspozycji lub ostrości;
4. ruch osoby pomiędzy ujęciami;
5. zmianę kadru, ogniskowej albo dystansu;
6. refleksy na okularach, skórze lub ubraniu.

Jeżeli raport oznacza zdjęcie jako `insufficient_overlap_with_previous`, należy w pierwszej kolejności wykonać dodatkowe zdjęcie pomostowe pomiędzy wskazanymi pozycjami.

### Ocena rozmycia

Wariancja Laplasjanu jest metryką techniczną, a nie semantyczną oceną jakości fotografii. Niski wynik oznacza małą ilość energii wysokich częstotliwości, co często odpowiada motion blur albo defocus. Próg należy kalibrować dla konkretnego aparatu, rozdzielczości i sposobu kadrowania. Zdjęcia twarzy mogą wymagać wyższego progu niż zdjęcia całej sylwetki.

### Ocena światła

Raport nie ogranicza się do średniej jasności. Rejestruje również odsetek pikseli bardzo ciemnych i bardzo jasnych. Jest to istotne, ponieważ poprawna średnia luminancja może współistnieć z lokalnym clippingiem skóry, włosów albo ubrania.

Automatyczna analiza ma identyfikować fotografie wymagające inspekcji lub ponownego wykonania. Nie należy bezrefleksyjnie usuwać wszystkich zdjęć oznaczonych ostrzeżeniem.

## Preprocessing partii zdjęć

Avatar Studio może utworzyć osobny, pochodny zestaw zdjęć z ujednoliconą luminancją, poprawionym kontrastem albo usuniętym statycznym tłem. Oryginalne fotografie nie są nadpisywane.

Przykład:

```bash
python scripts/photo_batch.py preprocess references/photos work/photos_preprocessed \
  --normalize-lighting \
  --improve-contrast \
  --background references/background/empty_scene.jpg
```

Każda operacja zapisuje `preprocessing_report.json`, zawierający źródło, katalog wynikowy i listę zastosowanych transformacji.

### Normalizacja oświetlenia

Normalizacja działa na kanale luminancji w przestrzeni LAB. Dla całej partii obliczana jest mediana luminancji, a każde zdjęcie jest delikatnie dopasowywane do wspólnego poziomu odniesienia. Chromatyczność nie jest bezpośrednio skalowana.

Ta operacja może poprawić stabilność ekstrakcji cech przy umiarkowanych zmianach ekspozycji, ale nie zastępuje poprawnego oświetlenia podczas capture. Silne prześwietlenia i niedoświetlenia należy poprawić przez ponowne wykonanie zdjęcia.

### Poprawa kontrastu

Opcjonalna poprawa kontrastu wykorzystuje CLAHE na kanale luminancji. Parametry są celowo zachowawcze. Nadmierne wzmacnianie lokalnego kontrastu może wytworzyć sztuczne cechy i pogorszyć zgodność fotometryczną między zdjęciami.

Do rekonstrukcji należy porównać wynik na małej próbce i zachować możliwość powrotu do oryginałów.

### Usuwanie tła

Jeżeli dostępny jest osobny obraz pustego tła wykonany:

- z tej samej pozycji kamery;
- przy tej samej ogniskowej;
- z niezmienionym kadrem;
- przy możliwie takim samym oświetleniu;

moduł może utworzyć maskę pierwszego planu przez różnicowanie obrazu z fotografią tła. Wynik jest zapisywany jako PNG z kanałem alfa.

Metoda ta jest przeznaczona dla nieruchomej kamery i statycznego tła. Nie należy stosować jej do sesji, w której kamera przemieszcza się wokół osoby, ponieważ tło nie jest wtedy geometrycznie zgodne z kolejnymi zdjęciami.

### Zasada reprodukowalności

W repozytorium i workspace należy rozróżniać:

```text
references/photos/          # oryginały, read-only
reports/                    # raporty QA
work/photos_preprocessed/   # obrazy pochodne
```

Preprocessing nigdy nie powinien usuwać ani nadpisywać materiału źródłowego. W razie problemu z rekonstrukcją trzeba móc jednoznacznie ustalić, czy używano oryginałów czy konkretnej wersji danych pochodnych.

## Wykonanie w Avatar Studio

### Krok 1. Rozpocznij etap

W GUI wybierz **02 Photogrammetry** i kliknij **Start stage**. Przycisk operacji staje się dostępny, jeśli etap 01 został zaliczony.

### Krok 2. Uruchom rekonstrukcję sparse

Kliknij **Run supported operation** i wskaż katalog zdjęć.

Avatar Studio uruchamia kolejno:

```text
feature_extractor
    ↓
matcher
    ↓
mapper
```

Nie musisz wpisywać poleceń COLMAP ręcznie.

### Krok 3. Wybierz matcher

Dostępne warianty:

| Matcher | Kiedy używać | Ryzyko |
| --- | --- | --- |
| `exhaustive` | standardowa sesja 360° z dziesiątkami lub setkami zdjęć | wolniejszy, ale najbezpieczniejszy punkt startowy |
| `sequential` | uporządkowana sekwencja wideo lub zdjęć wykonywanych kolejno wokół osoby | może pominąć ważne połączenia między odległymi klatkami |
| `spatial` | materiał z wiarygodną informacją o pozycji kamer | zależy od jakości metadanych pozycji |

Dla pierwszego skanu osoby użyj zwykle `exhaustive`.

### Krok 4. Model kamery

Domyślnym modelem Avatar Studio jest `OPENCV`. Jest wystarczająco elastyczny dla typowych aparatów i smartfonów, ponieważ uwzględnia podstawowe zniekształcenia radialne i tangencjalne.

Jeżeli wszystkie fotografie wykonano tym samym urządzeniem bez zmiany ogniskowej, pozostaw tryb jednej kamery. Jeżeli ogniskowa lub urządzenie się zmieniały, trzeba traktować fotografie jako więcej niż jedną kamerę.

## Co powinno powstać

W prywatnym workspace pojawia się struktura zbliżona do:

```text
work/colmap/
├── database.db
└── sparse/
    └── 0/
        ├── cameras.bin
        ├── images.bin
        └── points3D.bin
```

Może powstać więcej niż jeden model (`0`, `1`, `2`...). Kilka rozłącznych modeli jest sygnałem, że COLMAP nie znalazł wystarczającej liczby połączeń pomiędzy grupami zdjęć.

Avatar Studio zapisuje dodatkowo raport JSON w `reports/` i rejestruje go jako artefakt etapu.

## Kontrola wyniku

### Liczba zarejestrowanych zdjęć

Najważniejszym pierwszym wskaźnikiem jest stosunek zdjęć zarejestrowanych do wszystkich wejściowych.

Przykład:

```text
96 zdjęć wejściowych
91 zarejestrowanych
registration ratio = 94,8%
```

Wysoki udział jest pożądany, ale nie wystarcza. Model może zarejestrować wiele zdjęć i nadal mieć słabe pokrycie uszu, brody lub dłoni.

### Błąd reprojekcji

Mean reprojection error opisuje średnią odległość pomiędzy obserwacją punktu na obrazie a rzutem odpowiadającego mu punktu 3D.

Orientacyjna interpretacja dla dobrze kontrolowanej sesji:

- `< 0,5 px` – bardzo dobry wynik;
- `0,5–1,0 px` – zwykle dobry;
- `1–2 px` – wymaga inspekcji;
- `> 2 px` – wyraźny sygnał problemu.

Nie traktuj tej liczby jako jedynej oceny jakości.

### Geometria kamer

Wizualnie sprawdź, czy kamery tworzą oczekiwany pierścień lub zestaw pierścieni wokół osoby. Podejrzane są:

- kamera umieszczona daleko poza pozostałymi;
- nagłe odwrócenie orientacji kamery;
- duża luka kątowa bez zdjęć;
- osobna grupa kamer bez połączenia z głównym modelem.

### Pokrycie ciała

Sprawdź szczególnie:

- uszy i boki głowy;
- spód nosa i brody;
- tył głowy;
- szyję;
- pachy;
- przestrzeń między ręką a tułowiem;
- dłonie i palce;
- wewnętrzną stronę nóg i stóp.

## Typowe błędy i naprawa

### Powstaje kilka sparse models

Najczęstsze przyczyny:

1. za mały overlap;
2. zmiana ekspozycji lub ostrości;
3. poruszenie osoby;
4. jednolite powierzchnie bez cech;
5. refleksy na okularach, skórze lub ubraniu.

Naprawa:

1. ustal, które grupy zdjęć zostały rozdzielone;
2. znajdź brakujący zakres kątowy;
3. jeżeli to możliwe, wykonaj dodatkowe fotografie pomostowe;
4. nie próbuj scalać modeli tylko transformacją 3D, jeśli brak im wspólnych obserwacji.

### Dużo zdjęć nie rejestruje się

Sprawdź ostrość, motion blur i overlap. W przypadku zdjęć prawidłowych spróbuj `exhaustive` zamiast `sequential`.

### Kamery mają chaotyczną geometrię

Najpierw podejrzewaj błędne dopasowania, ruch osoby albo nieprawidłowy model kamery. Nie przechodź do dense reconstruction.

### Model dobrze obejmuje tułów, ale słabo twarz

Twarz wymaga większej gęstości ujęć niż duże powierzchnie ubrania. Wykonaj osobną serię z mniejszym krokiem kątowym i większą skalą twarzy w kadrze.

## Praca ręczna w COLMAP

GUI Avatar Studio obsługuje podstawową rekonstrukcję sparse. Ręczne otwarcie projektu w COLMAP jest przydatne do zaawansowanej diagnostyki i wizualnej inspekcji kamer. Nie należy jednak ręcznie zmieniać plików w `work/colmap/` bez zachowania informacji o zmianie, jeżeli wynik ma pozostać reprodukowalny.

## Validation

Etap należy uznać za poprawny, gdy:

1. partia zdjęć została poddana kontroli technicznej;
2. fotografie oznaczone jako wymagające ponownego wykonania zostały przejrzane;
3. nie ma nieuzasadnionych luk overlapu pomiędzy kolejnymi ujęciami;
4. powstał co najmniej jeden sparse model;
5. większość zatwierdzonych zdjęć jest zarejestrowana;
6. trajektoria kamer jest geometrycznie sensowna;
7. nie ma dużych luk w krytycznych obszarach ciała;
8. błąd reprojekcji nie wskazuje na systematyczny problem;
9. konfiguracja i raport operacji zostały zapisane.

## DoD

Sparse reconstruction jest spójna, pokrycie jest wystarczające do dense reconstruction, raport jakości zdjęć i raport COLMAP znajdują się w projekcie, a wszystkie obrazy po preprocessingu są traktowane jako dane pochodne z zachowaniem oryginałów.

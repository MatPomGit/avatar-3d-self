# 02. Fotogrametria

**Input:** zatwierdzona seria zdjęć z etapu 01.  
**Editable output:** baza COLMAP, parametry kamer i sparse reconstruction.  
**Derived output:** sparse point cloud oraz raport operacji.

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

1. powstał co najmniej jeden sparse model;
2. większość zatwierdzonych zdjęć jest zarejestrowana;
3. trajektoria kamer jest geometrycznie sensowna;
4. nie ma dużych luk w krytycznych obszarach ciała;
5. błąd reprojekcji nie wskazuje na systematyczny problem;
6. konfiguracja i raport operacji zostały zapisane.

## DoD

Sparse reconstruction jest spójna, pokrycie jest wystarczające do dense reconstruction, raport znajduje się w projekcie, a niezaakceptowane anomalie nie są ukryte przez ręczne oznaczenie etapu jako zaliczony.

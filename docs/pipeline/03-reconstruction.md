# 03. Rekonstrukcja geometrii

**Input:** zatwierdzony sparse model z etapu 02 oraz oryginalne fotografie.  
**Editable output:** prywatny dense workspace COLMAP i wysokorozdzielcza geometria.  
**Derived output:** `fused.ply`, wynikowy mesh `.ply` oraz raport operacji.

## Cel etapu

Sparse reconstruction wyznacza głównie pozycje kamer i rzadką strukturę sceny. W tym etapie obliczane są mapy głębi dla zdjęć, następnie łączone w gęstą chmurę punktów i przekształcane w powierzchnię 3D.

Avatar Studio realizuje podstawową ścieżkę COLMAP:

```text
image undistortion
      ↓
PatchMatch stereo
      ↓
stereo fusion
      ↓
Poisson albo Delaunay meshing
```

Wynik tego etapu jest nadal skanem produkcyjnym high-poly. Nie jest jeszcze siatką gotową do rigu i animacji.

## Warunki wejściowe

Nie uruchamiaj dense reconstruction tylko dlatego, że etap 02 utworzył jakiś model. Przed rozpoczęciem sprawdź:

1. czy sparse model obejmuje całą oczekiwaną sesję;
2. czy kamery mają logiczną geometrię;
3. czy nie ma krytycznych luk wokół twarzy, uszu, dłoni lub stóp;
4. czy osoba nie zmieniła istotnie pozy pomiędzy zdjęciami;
5. czy używasz dokładnie tej samej serii zdjęć, która utworzyła wybrany sparse model.

## Wykonanie w Avatar Studio

### Krok 1. Rozpocznij etap

Po zaliczeniu etapu 02 wybierz **03 Reconstruction** i kliknij **Start stage**.

### Krok 2. Wybierz zdjęcia

Kliknij **Run supported operation** i wskaż katalog oryginalnych zdjęć. Nie używaj kopii przeskalowanych po wykonaniu sparse reconstruction.

### Krok 3. Wybierz sparse model

Wskaż katalog konkretnego modelu, np.:

```text
<workspace>/work/colmap/sparse/0
```

Katalog powinien zawierać `cameras.bin`, `images.bin` i `points3D.bin` albo odpowiadające im pliki tekstowe.

Jeżeli etap 02 utworzył kilka modeli, nie wybieraj automatycznie `0`. Najpierw ustal, który model ma właściwe pokrycie.

### Krok 4. Wybierz metodę meshingu

GUI oferuje:

- `poisson` – zalecany pierwszy wariant dla skanu człowieka; tworzy zwykle ciągłą powierzchnię z gęstej chmury;
- `delaunay` – alternatywa przydatna do porównania, szczególnie gdy Poisson tworzy niepożądane powierzchnie zamykające luki.

W obu przypadkach mesh musi zostać później oceniony wizualnie i oczyszczony.

### Krok 5. Obliczenia

Avatar Studio uruchamia cztery operacje poza głównym wątkiem GUI. W czasie obliczeń można użyć **Cancel operation**.

Domyślny limit rozdzielczości wejściowej dla undistortion wynosi `3200 px` dla dłuższego boku. Jest to kompromis pomiędzy szczegółowością a kosztem pamięci i czasu. Przy bardzo drobnych detalach twarzy warto eksperymentalnie zwiększyć wartość dopiero po uzyskaniu poprawnej rekonstrukcji bazowej.

## Co wykonują poszczególne kroki

### Image undistortion

COLMAP przelicza fotografie do postaci zgodnej z oszacowanym modelem kamery i przygotowuje workspace do Multi-View Stereo. Jeżeli model kamery z etapu 02 jest błędny, problemy pojawią się również tutaj.

### PatchMatch stereo

Dla wielu widoków obliczane są mapy głębi i normalnych. W Avatar Studio włączona jest zgodność geometryczna (`geom_consistency`), która odrzuca część obserwacji niespójnych pomiędzy kamerami.

### Stereo fusion

Mapy głębi są łączone w gęstą chmurę punktów `fused.ply`.

To pierwszy wynik, który warto sprawdzić przed oceną meshu. Jeżeli `fused.ply` ma duże braki, meshing nie odtworzy prawidłowo brakującej geometrii.

### Meshing

Mesher tworzy ciągłą powierzchnię z chmury punktów. Powierzchnia może zawierać:

- tło;
- platformę lub podłogę;
- cienkie błędne mosty;
- zamknięcia otworów;
- samoprzecięcia;
- nadmiarową geometrię przy włosach i palcach.

Są to typowe artefakty skanu, a nie sygnał, że mesh można od razu riggować.

## Oczekiwane pliki

Typowy workspace:

```text
work/colmap/dense/
├── images/
├── sparse/
├── stereo/
├── fused.ply
└── meshed-poisson.ply
```

Dla meshera Delaunay nazwa wyniku jest analogiczna.

Avatar Studio rejestruje wynikowy mesh jako artefakt etapu i zapisuje raport operacji w `reports/`.

## Kontrola jakości gęstej chmury

Najpierw otwórz `fused.ply` w narzędziu umożliwiającym obrót i zbliżenie modelu. Sprawdź kolejno:

1. twarz z przodu;
2. profile twarzy;
3. uszy;
4. spód brody i szyję;
5. tył głowy;
6. barki i pachy;
7. dłonie z obu stron;
8. przestrzenie między palcami;
9. nogi, stopy i przestrzeń pomiędzy nimi.

Brak punktów w danym regionie oznacza brak danych rekonstrukcyjnych. Mesh może później sztucznie zamknąć taki obszar, ale nie odzyska prawdziwej anatomii.

## Kontrola meshu

Mesh powinien być oceniany pod kątem:

- kompletności anatomii;
- lokalnej zgodności z fotografiami;
- błędnych połączeń pomiędzy oddzielnymi częściami ciała;
- geometrii włosów i zarostu;
- powierzchni pod okularami;
- artefaktów od refleksów;
- tła przyklejonego do sylwetki.

Nie wykonuj na tym etapie agresywnego smoothingu. Smoothing może ukryć problem kosztem podobieństwa twarzy.

## Skala

Fotogrametria bez dodatkowego odniesienia nie gwarantuje bezwzględnej skali metrycznej. Po imporcie do Blendera ustaw skalę na podstawie zmierzonego wymiaru antropometrycznego, np. wysokości ciała lub innego wiarygodnego odcinka.

Procedura:

1. wybierz wymiar zmierzony fizycznie;
2. zmierz odpowiadający odcinek w modelu;
3. oblicz współczynnik skali;
4. zastosuj skalę globalnie bez deformowania proporcji;
5. zapisz wartość i źródło pomiaru w raporcie.

## Typowe błędy i procedury naprawcze

### PatchMatch kończy się brakiem pamięci

1. zmniejsz maksymalny rozmiar obrazu;
2. zamknij inne procesy wykorzystujące GPU;
3. nie redukuj od razu liczby zdjęć, jeśli pokrycie jest poprawne;
4. dopiero później dobieraj bardziej agresywne parametry wydajnościowe.

### `fused.ply` jest prawie pusty

Sprawdź sparse model i zgodność katalogu zdjęć. Częstym błędem jest użycie innego zestawu zdjęć niż ten, dla którego obliczono sparse reconstruction.

### Twarz jest zaszumiona

Przyczyny mogą obejmować ruch mimiczny, refleksy skóry, okulary, zarost i zbyt małą liczbę bliskich widoków. Nie naprawiaj takiego problemu wyłącznie filtrem wygładzającym. Porównaj z materiałem referencyjnym i rozważ ponowne wykonanie zdjęć twarzy.

### Palce są zlane

Najczęściej brakuje widoków pomiędzy palcami albo dłoń poruszyła się podczas sesji. Jeżeli indywidualna anatomia dłoni jest istotna, wykonaj osobny capture dłoni zgodnie z dokumentacją.

### Poisson tworzy błędne „błony”

Porównaj gęstą chmurę i wariant Delaunay. Jeżeli dane źródłowe są poprawne, błędne zamknięcia mogą zostać usunięte w cleanupie. Jeżeli w chmurze brakuje geometrii, problem należy rozwiązać wcześniej.

## Import do Blendera

Po zaakceptowaniu wyniku:

1. zaimportuj mesh `.ply` do Blendera;
2. zachowaj oryginalny mesh jako niezmienny snapshot;
3. ustaw jednostki sceny;
4. ustaw skalę antropometryczną;
5. zapisz nową scenę roboczą zamiast nadpisywać wynik COLMAP;
6. zarejestruj scenę lub mesh w Avatar Studio.

Nie dokonuj cleanupu na jedynej kopii skanu.

## Validation

Minimalna walidacja automatyczna w GUI sprawdza, czy meshing utworzył niepusty plik. Jest to warunek konieczny, ale zdecydowanie niewystarczający.

Walidacja człowieka musi dodatkowo potwierdzić:

- kompletność kluczowych regionów;
- zgodność skali;
- brak krytycznych błędnych połączeń;
- zachowanie charakterystycznych cech twarzy;
- wystarczającą jakość do cleanupu.

## DoD

Etap jest zakończony, gdy wynikowa geometria ma znane pochodzenie, poprawną skalę lub zapisaną procedurę jej ustalenia, wystarczającą kompletność do cleanupu, zarejestrowany artefakt oraz raport operacji. Duże luki lub zniekształcenia twarzy wymagają powrotu do etapu zdjęć albo fotogrametrii, a nie maskowania ich w dalszym pipeline.

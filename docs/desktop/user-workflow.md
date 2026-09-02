# Avatar Studio: instrukcja GUI

Ten rozdział opisuje **aktualnie zaimplementowany** interfejs Avatar Studio. Jeżeli funkcja nie jest opisana jako dostępna poniżej, nie należy zakładać, że GUI ją wykonuje automatycznie.

## 1. Utworzenie lub otwarcie projektu

1. Uruchom `Avatar Studio.exe` albo polecenie `avatar-studio` w aktywnym środowisku Python.
2. Przy pierwszym uruchomieniu pojawi się okno wyboru katalogu.
3. Wskaż istniejący katalog projektu albo utwórz nowy katalog.
4. Avatar Studio utworzy prywatny katalog `.avatar-studio/` z bazą `project.sqlite3` oraz katalog `reports/`.
5. Projekt można później zmienić przez **Project → Open / create workspace…**.

Zdjęcia, nagrania głosu i inne dane biometryczne powinny pozostawać w prywatnym workspace, a nie w publicznym repozytorium.

## 2. Konfiguracja narzędzi

Otwórz **Tools → External tool settings…**. Dostępne są pola dla Blender, COLMAP, FFmpeg i Piper. Jeżeli program znajduje się w `PATH`, pole można pozostawić puste. Po zapisaniu ustawień wybierz **Tools → Probe local tools**. Status `MISSING` oznacza, że operacja wymagająca danego narzędzia nie może zostać uruchomiona.

## 3. Nawigacja po pipeline

Lewa kolumna zawiera 21 etapów procesu. Statusy:

- `pending` – zależności nie zostały jeszcze spełnione;
- `ready` – etap może zostać rozpoczęty;
- `in_progress` – etap jest wykonywany;
- `passed` – etap przeszedł bramkę Definition of Done;
- `failed` – operacja lub walidacja zakończyła się błędem;
- `blocked` – etap został jawnie zablokowany.

Górny pasek pokazuje procent zaliczonych etapów całego projektu. Osobny pasek w środkowym panelu pokazuje postęp aktualnie wykonywanej operacji.

## 4. Etap 01: manifest capture i kontrola zdjęć

Przed COLMAP należy zweryfikować serię referencyjną.

1. Otwórz etap **01 Reference acquisition** i kliknij **Start stage**.
2. Kliknij **Run supported operation**.
3. Wskaż katalog zawierający serię zdjęć.
4. Podaj minimalną liczbę fotografii dla przyjętego profilu. Domyślna wartość to `60`.
5. Podaj minimalny dłuższy wymiar zdjęcia. Domyślna wartość to `3000 px`.
6. Avatar Studio przejdzie przez wszystkie wspierane obrazy, obliczy SHA-256, odczyta rozdzielczość oraz wykryje identyczne pliki.
7. Wynik zostanie zapisany jako `capture/capture_manifest.json` i automatycznie zarejestrowany jako artefakt etapu.

Bramka jakości ma status `failed`, gdy zdjęć jest mniej niż wymagane albo wykryto duplikaty binarne. Zbyt mała rozdzielczość jest obecnie ostrzeżeniem, ponieważ nie zawsze dyskwalifikuje cały zestaw. Manifest nie zastępuje kontroli ostrości, ekspozycji, pokrycia kątowego i ruchu osoby opisanych w dokumentacji capture.

## 5. Etap 02: COLMAP sparse reconstruction

1. Otwórz etap **02 Photogrammetry** i kliknij **Start stage**.
2. Kliknij **Run supported operation**.
3. Wskaż katalog zawierający zdjęcia jednej spójnej sesji.
4. Wybierz strategię dopasowania:
   - `exhaustive` – domyślna dla kilkudziesięciu lub kilkuset zdjęć człowieka wykonanych dookoła obiektu;
   - `sequential` – dla uporządkowanej sekwencji klatek;
   - `spatial` – gdy istnieją użyteczne dane pozycji.
5. GUI uruchomi kolejno feature extraction, matching i mapper.
6. Pasek operacji pokazuje aktualną fazę oraz deterministyczny procent ukończenia faz pipeline'u.
7. Po zakończeniu raport JSON zostanie zapisany w `reports/` i zarejestrowany jako artefakt etapu.
8. Brak jakiegokolwiek sparse modelu powoduje wynik walidacji `failed`.

Procent oznacza ukończenie kolejnych faz, a nie estymację czasu pozostałego do zakończenia wewnętrznego algorytmu COLMAP.

## 6. Etap 03: dense reconstruction i mesh

1. Po zaliczeniu etapu 02 otwórz **03 Reconstruction** i rozpocznij etap.
2. Kliknij **Run supported operation**.
3. Wskaż ten sam katalog zdjęć.
4. Wskaż katalog konkretnego modelu sparse, zwykle `work/colmap/sparse/0`.
5. Wybierz `poisson` albo `delaunay`.
6. Avatar Studio wykonuje `image_undistorter → patch_match_stereo → stereo_fusion → meshing`.
7. Pasek postępu pokazuje aktualnie wykonywaną fazę.
8. Wynikowa siatka `.ply` zostaje zarejestrowana jako artefakt wraz z raportem operacji.

## 7. Anulowanie operacji

Podczas pracy narzędzia aktywny jest **Cancel operation**. Żądanie zakończenia jest przekazywane do aktywnego procesu zewnętrznego. W razie braku poprawnego zakończenia proces jest terminowany, a etap otrzymuje wynik `failed`.

## 8. Operacje Blendera

Dla etapów 04–18 GUI nie wykonuje jeszcze automatycznego modelowania, retopologii, UV, rigu ani animacji. Te czynności są wykonywane w Blenderze zgodnie z dokumentacją etapu.

Avatar Studio może natomiast uruchomić inspekcję sceny `.blend` i zapisać raport obejmujący m.in. liczbę siatek, vertices, polygons, UV, materiałów, armatures, bones, shape keys, actions i ustawienia jednostek.

## 9. Piper i FFmpeg

W etapie **19 Piper integration** przycisk **Run supported operation** udostępnia Piper synthesis i FFmpeg normalize WAV. Wyniki oraz provenance są rejestrowane w projekcie. Pełna treść wypowiedzi nie jest zapisywana w raporcie operacji; adapter zapisuje jej hash.

## 10. Rejestrowanie i podgląd artefaktów

Jeżeli etap został wykonany ręcznie, kliknij **Register and inspect artefact**. Avatar Studio zapisuje ścieżkę, rozmiar, SHA-256, typ i dostępne metadane.

Po zaznaczeniu artefaktu w prawej tabeli dostępny jest podgląd:

- obrazy są wyświetlane bezpośrednio w GUI;
- `.obj`, `.ply`, `.stl`, `.glb` i `.gltf` mają lekki interaktywny podgląd wireframe;
- przeciągnięcie lewym przyciskiem myszy obraca model;
- kółko myszy zmienia zoom;
- dla nieobsługiwanego typu pozostają metadane techniczne.

Podgląd jest narzędziem diagnostycznym. Nie zastępuje finalnego renderu materiałów, włosów, SSS ani pełnej oceny deformacji w Blenderze lub silniku czasu rzeczywistego.

## 11. Definition of Done

**Evaluate DoD and pass** wymaga zarejestrowanego artefaktu. Krytyczny wynik `failed` blokuje etap do czasu usunięcia przyczyny albo utworzenia kontrolowanego waivera. Waiver wymaga uzasadnienia ryzyka i sposobu późniejszej weryfikacji. Nie zastępuje artefaktu wynikowego.

Ponowne zarejestrowanie zmienionego artefaktu w zatwierdzonym etapie unieważnia zależne etapy downstream.

## 12. Raport końcowy projektu

Wybierz **Project → Generate final report**. Program tworzy dwa pliki w `reports/`:

- `project-report.md` – raport czytelny dla człowieka;
- `project-report.json` – kanoniczny snapshot maszynowy.

Raport zawiera stan 21 etapów, artefakty wraz z SHA-256, wyniki walidacji, waivery, historię `tool_runs`, konfigurację narzędzi oraz podsumowanie postępu. JSON powinien być traktowany jako źródło do późniejszej automatycznej analizy i audytu provenance.

## 13. Diagnostyka błędu

Jeżeli operacja zakończy się błędem:

1. przeczytaj komunikat w dolnym panelu logu;
2. sprawdź **Probe local tools**;
3. sprawdź ścieżki wejściowe i uprawnienia workspace;
4. otwórz dokumentację etapu;
5. usuń przyczynę i ponownie uruchom operację.

Nie należy ręcznie modyfikować `.avatar-studio/project.sqlite3`.

## 14. Aktualne granice automatyzacji

Avatar Studio automatyzuje obecnie manifest i podstawową kontrolę serii zdjęć, sparse/dense COLMAP, techniczną inspekcję scen Blender oraz podstawowe operacje FFmpeg/Piper. GUI posiada podgląd obrazów i lekkich siatek 3D oraz generuje raport końcowy projektu. Cleanup, retopologia, UV, materiały, włosy, ubrania, rig, skinning i animacja nadal wymagają pracy w DCC. Nie ma jeszcze kolejki wielu operacji ani pełnego automatycznego workflow modelarskiego.

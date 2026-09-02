# Avatar Studio: instrukcja GUI

Ten rozdział opisuje **aktualnie zaimplementowany** interfejs Avatar Studio. Jeżeli funkcja nie jest opisana jako dostępna poniżej, nie należy zakładać, że GUI ją wykonuje automatycznie.

## 1. Utworzenie lub otwarcie projektu

1. Uruchom `Avatar Studio.exe` albo polecenie `avatar-studio` w aktywnym środowisku Python.
2. Przy pierwszym uruchomieniu pojawi się okno wyboru katalogu.
3. Wskaż istniejący katalog projektu albo utwórz nowy katalog, np. `D:\Avatar3D\projects\self-avatar` w Windows albo `~/Avatar3D/projects/self-avatar` w Linux.
4. Avatar Studio utworzy w nim prywatny katalog `.avatar-studio/` z bazą `project.sqlite3` oraz katalog `reports/` na raporty operacji.
5. Projekt można później zmienić przez **Project → Open / create workspace…**.

Zdjęcia, nagrania głosu i inne dane biometryczne powinny pozostawać w prywatnym workspace, a nie w publicznym repozytorium.

## 2. Konfiguracja narzędzi

Otwórz **Tools → External tool settings…**.

Dostępne są pola dla:

- Blender,
- COLMAP,
- FFmpeg,
- Piper.

Jeżeli program znajduje się w systemowym `PATH`, pole można pozostawić puste. Jeżeli nie, użyj **Browse…** i wskaż plik wykonywalny. Ścieżki są zapisywane wyłącznie w bieżącym workspace.

Po zapisaniu ustawień wybierz **Tools → Probe local tools**. W dolnym panelu logu każdy program powinien mieć status `OK`. Status `MISSING` oznacza, że dana operacja nie będzie mogła zostać uruchomiona.

## 3. Nawigacja po pipeline

Lewa kolumna zawiera 21 etapów procesu. Statusy oznaczają:

- `pending` – zależności nie zostały jeszcze spełnione;
- `ready` – etap może zostać rozpoczęty;
- `in_progress` – etap jest wykonywany;
- `passed` – etap przeszedł bramkę Definition of Done;
- `failed` – operacja lub walidacja zakończyła się błędem;
- `blocked` – etap został jawnie zablokowany.

Środkowy panel pokazuje cel etapu, zależności, oczekiwane artefakty, liczbę wyników walidacji i link **Open full documentation**.

## 4. Uruchamianie operacji bez CLI

Przycisk **Run supported operation** jest aktywny tylko tam, gdzie Avatar Studio posiada obecnie operację wykonawczą.

### Etap 02: COLMAP sparse reconstruction

1. Otwórz etap **02 Photogrammetry** i kliknij **Start stage**.
2. Kliknij **Run supported operation**.
3. Wskaż katalog zawierający zdjęcia jednej spójnej sesji.
4. Wybierz strategię dopasowania:
   - `exhaustive` – domyślna dla kilkudziesięciu lub kilkuset zdjęć człowieka wykonanych dookoła obiektu;
   - `sequential` – dla uporządkowanej sekwencji klatek;
   - `spatial` – gdy istnieją użyteczne dane pozycji.
5. GUI uruchomi kolejno feature extraction, matching i mapper.
6. Po zakończeniu raport JSON zostanie zapisany w `reports/` i zarejestrowany jako artefakt etapu.
7. Brak jakiegokolwiek sparse modelu powoduje wynik walidacji `failed`.

### Etap 03: dense reconstruction i mesh

1. Po zaliczeniu etapu 02 otwórz **03 Reconstruction** i rozpocznij etap.
2. Kliknij **Run supported operation**.
3. Wskaż ten sam katalog zdjęć, który był użyty do sparse reconstruction.
4. Wskaż katalog konkretnego modelu sparse, zwykle `work/colmap/sparse/0`.
5. Wybierz mesher:
   - `poisson` – zalecany punkt startowy dla skanu człowieka;
   - `delaunay` – wariant alternatywny, który należy ocenić wizualnie.
6. Avatar Studio wykonuje `image_undistorter → patch_match_stereo → stereo_fusion → meshing`.
7. Wynikowa siatka `.ply` zostaje automatycznie zarejestrowana jako artefakt etapu wraz z raportem operacji.

Operacje COLMAP mogą trwać długo i intensywnie wykorzystywać CPU/GPU. Są wykonywane poza głównym wątkiem GUI.

## 5. Anulowanie operacji

Podczas pracy narzędzia aktywny jest przycisk **Cancel operation**. Jego użycie wysyła żądanie zakończenia do uruchomionego procesu zewnętrznego. Jeżeli proces nie zakończy się poprawnie, etap otrzyma wynik walidacji `failed` i status `failed`.

Nie zamykaj aplikacji przez Menedżer zadań tylko dlatego, że COLMAP długo pracuje. Najpierw użyj **Cancel operation**, aby baza projektu zachowała spójny stan.

## 6. Operacje Blendera

Dla etapów 04–18 GUI nie wykonuje jeszcze automatycznego modelowania, retopologii, UV, rigu ani animacji. Te czynności są wykonywane w Blenderze zgodnie z dokumentacją etapu.

Avatar Studio potrafi jednak uruchomić **głęboką inspekcję sceny `.blend`**. W odpowiednim etapie wybierz **Run supported operation**, wskaż scenę i poczekaj na raport. Inspekcja odczytuje m.in. liczbę siatek, vertices, polygons, UV, materiałów, armatures, bones, shape keys, animacji oraz ustawienia jednostek.

Raport inspekcji nie zastępuje pracy artystycznej ani oceny podobieństwa. Jest technicznym artefaktem walidacyjnym.

## 7. Piper i FFmpeg

W etapie **19 Piper integration** przycisk **Run supported operation** udostępnia dwie operacje.

### Piper synthesis

1. Wybierz `Piper synthesis`.
2. Wpisz tekst wypowiedzi.
3. Wskaż model `.onnx` własnego głosu.
4. Wskaż docelowy plik WAV.
5. Avatar Studio uruchomi Piper i zapisze raport pochodzenia modelu oraz wynikowego audio.

Pełna treść wypowiedzi nie jest kopiowana do raportu operacji. Raport używa bezpiecznego opisu długości tekstu, natomiast adapter Piper zapisuje jego SHA-256.

### FFmpeg normalize WAV

1. Wybierz `FFmpeg normalize WAV`.
2. Wskaż nagranie wejściowe.
3. Wskaż wynikowy WAV.
4. Program wykona normalizację do profilu audio używanego w pipeline mowy.

## 8. Rejestrowanie artefaktów

Jeżeli etap został wykonany ręcznie w programie zewnętrznym, kliknij **Register and inspect artefact** i wskaż wynikowy plik.

Avatar Studio zapisuje:

- pełną ścieżkę,
- wielkość,
- SHA-256,
- rodzaj pliku,
- dostępne metadane techniczne,
- ostrzeżenia inspektora.

Ponowne zarejestrowanie zmienionego artefaktu w **zatwierdzonym** etapie automatycznie unieważnia statusy wszystkich etapów zależnych. Historyczne pliki nie są usuwane z dysku.

## 9. Definition of Done

Przycisk **Evaluate DoD and pass** nie jest zwykłym ręcznym przełącznikiem statusu.

Etap nie może zostać zaliczony bez zarejestrowanego artefaktu. Jeżeli istnieje krytyczny wynik walidacji `failed`, konieczne jest usunięcie przyczyny albo utworzenie kontrolowanego wyjątku (waiver).

Wyjątek wymaga tekstowego uzasadnienia opisującego:

1. dlaczego przejście dalej jest uzasadnione;
2. jakie ryzyko pozostaje;
3. kiedy i jak problem zostanie ponownie zweryfikowany.

Waiver nie zastępuje artefaktu wynikowego.

## 10. Diagnostyka błędu

Jeżeli operacja zakończy się błędem:

1. przeczytaj komunikat w dolnym panelu logu;
2. sprawdź, czy narzędzie ma status `OK` w **Probe local tools**;
3. sprawdź ścieżki wejściowe i uprawnienia zapisu do workspace;
4. otwórz dokumentację danego etapu z linku w środkowym panelu;
5. po poprawieniu przyczyny ponownie rozpocznij etap i uruchom operację.

Raporty udanych operacji znajdują się w `reports/`. Nie należy ręcznie modyfikować bazy `.avatar-studio/project.sqlite3`.

## 11. Aktualne granice automatyzacji

Avatar Studio automatyzuje obecnie rekonstrukcję COLMAP, inspekcję scen Blender oraz podstawowe operacje FFmpeg/Piper. Cleanup, retopologia, UV, tworzenie materiałów, włosów, ubrań, rigu, skinningu i animacji nadal wymagają pracy w DCC. GUI prowadzi przez te etapy, przechowuje artefakty i uruchamia inspekcję, ale nie zastępuje jeszcze narzędzi modelarskich.

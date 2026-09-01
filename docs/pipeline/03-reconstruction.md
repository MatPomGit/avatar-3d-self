# 03. Rekonstrukcja geometrii

**Input:** zatwierdzony sparse model.  
**Editable output:** dense workspace i wysokorozdzielcza chmura/mesh.  
**Derived output:** `avatar_scan_vNNN.ply` oraz raport skali i kompletności.

## Windows

1. Uruchom dense stereo/meshing na kopii projektu COLMAP.
2. Wyeksportuj chmurę i mesh bez redukcji detalu.
3. Zaimportuj wynik do Blendera.
4. Ustaw skalę z pomiaru antropometrycznego.
5. Zapisz pierwszy niezmodyfikowany snapshot skanu.

## Linux

1. Uruchom dense reconstruction dla zatwierdzonego sparse modelu.
2. Wyeksportuj chmurę i mesh w formacie zachowującym skalę i geometrię.
3. Otwórz wynik w Blenderze.
4. Ustal skalę na podstawie znanego wymiaru.
5. Zachowaj niezmieniony artefakt wejściowy przed cleanupem.

## Validation

Sprawdź twarz, uszy, nos, spód brody, szyję, palce, pachy i stopy. Odróżniaj rzeczywiste braki od włosów, refleksów i ruchu. Nie wypełniaj dużych luk automatycznie, jeśli można dograć referencje.

## DoD

Geometria ma poprawną skalę, znany układ osi, zapisane źródło i wystarczające pokrycie do rozpoczęcia cleanupu.

# Avatar Studio: workflow użytkownika

## Utworzenie projektu

### Windows

1. Uruchom `Avatar Studio.exe` albo `avatar-studio` w aktywnym środowisku.
2. Wybierz **New project** i katalog poza repozytorium, np. `D:\Avatar3D\projects\self-avatar`.
3. Skonfiguruj ścieżki Blender, COLMAP, FFmpeg i Piper.
4. Uruchom diagnostykę środowiska.

### Linux

1. Uruchom binarium Avatar Studio albo `avatar-studio`.
2. Wybierz **New project** i katalog, np. `/home/<user>/Avatar3D/projects/self-avatar`.
3. Skonfiguruj ścieżki Blender, COLMAP, FFmpeg i Piper.
4. Uruchom diagnostykę środowiska.

## Praca etapowa

Aplikacja pokazuje tylko etap gotowy do pracy oraz jawnie opisuje zależności etapów zablokowanych. Po każdym etapie użytkownik rejestruje artefakt wynikowy, a aplikacja oblicza hash, zapisuje parametry i uruchamia dostępne walidatory.

Przejście dalej wymaga zaliczenia Definition of Done albo jawnego oznaczenia wyjątku z uzasadnieniem. Wyjątki pozostają widoczne w raporcie końcowym.

## Podgląd wyniku

Panel artefaktu ma docelowo pokazywać m.in. rozmiar pliku, format, jednostki, bounding box, vertices, faces, materials, bones, morph targets, tekstury, animacje, hash, wersję narzędzia oraz wyniki kontroli specyficznych dla danego etapu.

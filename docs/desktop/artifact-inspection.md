# Inspekcja artefaktów

Avatar Studio traktuje wynik każdego etapu jako artefakt możliwy do automatycznej analizy. Rejestracja pliku powinna generować metadane, ostrzeżenia i wynik walidacji zależny od typu zasobu.

## Dane wspólne

Dla każdego pliku aplikacja zapisuje ścieżkę, rozmiar, SHA-256, rozszerzenie, czas modyfikacji, etap pochodzenia i metadane inspektora.

## Typy

### Obrazy

Rozdzielczość, format, tryb koloru, megapiksele i podstawowe ostrzeżenia dotyczące zbyt małej rozdzielczości.

### Audio WAV

Sample rate, kanały, długość, szerokość próbki i czas trwania.

### JSON

Typ korzenia, liczba elementów lub kluczy i poprawność parsowania.

### Modele 3D

Dla wspieranych formatów: vertices, faces/triangles, bounding box, extents, liczba komponentów i ostrzeżenia geometrii. Głębsza inspekcja FBX i `.blend` może wymagać uruchomienia adaptera Blender CLI.

## Adaptery głębokiej analizy

Inspektor lekki nie powinien ładować pełnego DCC ani silnika. Gdy etap wymaga danych specyficznych dla Blendera, COLMAP lub Unreal, Avatar Studio powinno uruchomić lokalny adapter jako osobny proces i odebrać ustrukturyzowany raport JSON.

## Wynik

Metadane nie są automatycznie dowodem zaliczenia etapu. Stage validator interpretuje je według kontraktu etapu, np. sprawdza minimalną rozdzielczość zdjęć, brak pustej geometrii, oczekiwaną skalę lub obecność blend shapes.
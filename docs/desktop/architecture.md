# Avatar Studio: architektura

Avatar Studio jest niezależną aplikacją desktopową, która prowadzi użytkownika przez cały pipeline, uczy procedury i inspektuje wyniki. Nie jest częścią strony WWW.

## Decyzja technologiczna

**Python 3.11 + PySide6 + SQLite + PyInstaller.**

Uzasadnienie:

- pipeline i walidatory są w Pythonie;
- łatwa integracja z Blender CLI, COLMAP, FFmpeg i Piper przez procesy lokalne;
- PySide6 zapewnia natywny desktop UI bez serwera;
- SQLite jest lokalny, transakcyjny i nie wymaga usługi;
- PyInstaller pozwala tworzyć `.exe` na Windows i autonomiczny build Linux.

## Warstwy

```text
PySide6 UI
   ↓
Application services
   ↓
Domain model: Stage / Artifact / Validation / ToolRun
   ↓
SQLite project store
   ↓
Artifact inspectors + tool adapters + deterministic validators
   ↓
Blender / COLMAP / Piper / FFmpeg / filesystem
```

UI nie interpretuje plików produkcyjnych bezpośrednio. Inspektor zwraca zunifikowany obiekt zawierający typ artefaktu, metadane i ostrzeżenia. Głębsze kontrole zależne od aplikacji DCC są wykonywane przez adaptery narzędzi.

## Model stanu

Każdy projekt ma lokalny katalog `.avatar-studio/` z bazą `project.sqlite3` i logami. Jawne raporty walidacji mogą być eksportowane do `reports/*.json`.

Podstawowe encje:

- `StageDefinition`: niezmienna definicja etapu;
- `StageRun`: wykonanie etapu i jego status;
- `Artifact`: plik, SHA-256, typ i metadane;
- `ValidationResult`: check, wartość, próg i wynik;
- `ToolRun`: program, argumenty, exit code i log;
- `ProjectSettings`: ścieżki narzędzi i workspace.

Status etapu: `pending`, `ready`, `in_progress`, `blocked`, `passed`, `failed`.

## Inspekcja artefaktów

Pierwsza warstwa inspekcji działa bez uruchamiania ciężkich programów:

| Typ | Parametry |
| --- | --- |
| obraz | rozdzielczość, format, tryb koloru, megapiksele |
| WAV | sample rate, kanały, szerokość próbki, czas |
| JSON | typ korzenia, liczba i nazwy kluczy lub liczba elementów |
| OBJ/PLY/STL/GLB/glTF/FBX | geometrie, vertices, faces/triangles, bounds i extents, jeśli dostępny jest `trimesh` |
| BLEND | podstawowe metadane pliku; pełna inspekcja później przez Blender adapter |

Każdy zarejestrowany artefakt otrzymuje hash SHA-256. Dzięki temu aplikacja może w przyszłości wykrywać zmianę pliku po zatwierdzeniu etapu i unieważniać wyniki zależne.

## Interfejs

Bieżący układ:

- nagłówek: nazwa workspace oraz procent ukończenia pipeline'u;
- lewy panel: pipeline i status wszystkich etapów;
- środek: instrukcja bieżącego etapu, zależności i oczekiwane wyniki;
- prawy panel: artefakty oraz szczegółowe parametry wybranego pliku;
- dół: logi narzędzi, walidacja i komunikaty diagnostyczne.

Aplikacja nie ukrywa kryteriów. Użytkownik ma widzieć, dlaczego etap jest zablokowany albo zaliczony. Próba zaliczenia etapu bez zarejestrowanego artefaktu wymaga jawnego potwierdzenia.

## Kolejny poziom inspekcji

Następne adaptery powinny rozszerzyć analizę:

- Blender: obiekty, topologia, UV, materiały, armature, shape keys, weights;
- COLMAP: liczba kamer, zarejestrowanych zdjęć, reprojection error i coverage;
- Piper/audio: model głosu, długość wypowiedzi, alignment fonemów i pokrycie visemów;
- runtime package: trójkąty, materiały, tekstury, animacje, morph targets i budżet pamięci.

## Bezpieczeństwo

Program nie wysyła prywatnych materiałów do chmury bez jawnej funkcji i zgody. Wszystkie ścieżki prywatnego workspace są lokalne. Logi nie powinny kopiować treści zdjęć ani nagrań.

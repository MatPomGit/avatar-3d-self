# Avatar Studio: architektura

Avatar Studio jest niezależną aplikacją desktopową, która prowadzi użytkownika przez cały pipeline, uczy procedury i inspektuje wyniki. Nie jest częścią strony WWW.

## Decyzja technologiczna

**Python 3.11 + PySide6 + SQLite + PyInstaller.**

Uzasadnienie:

- pipeline i walidatory są już w Pythonie;
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
Tool adapters and deterministic validators
   ↓
Blender / COLMAP / Piper / FFmpeg / filesystem
```

UI nie interpretuje plików 3D bezpośrednio. Inspekcja artefaktu jest realizowana przez adapter lub walidator, który zwraca ustrukturyzowane metadane.

## Model stanu

Każdy projekt ma lokalny katalog `.avatar-studio/` z bazą `project.sqlite3` i logami. Jawne raporty walidacji mogą być eksportowane do `reports/*.json`.

Podstawowe encje:

- `StageDefinition`: niezmienna definicja etapu;
- `StageRun`: wykonanie etapu i jego status;
- `Artifact`: plik, hash, typ i metadane;
- `ValidationResult`: check, wartość, próg i wynik;
- `ToolRun`: program, argumenty, exit code i log;
- `ProjectSettings`: ścieżki narzędzi i workspace.

Status etapu: `pending`, `ready`, `in_progress`, `blocked`, `passed`, `failed`.

## Interfejs

Docelowy układ:

- lewy panel: pipeline i status wszystkich etapów;
- środek: instrukcja bieżącego etapu oraz wymagane działania;
- prawy panel: artefakty, parametry, metryki i preview;
- dół: logi narzędzi, walidacja i komunikaty diagnostyczne.

Aplikacja nie ukrywa kryteriów. Użytkownik ma widzieć, dlaczego etap jest zablokowany albo zaliczony.

## Bezpieczeństwo

Program nie wysyła prywatnych materiałów do chmury bez jawnej funkcji i zgody. Wszystkie ścieżki prywatnego workspace są lokalne. Logi nie powinny kopiować treści zdjęć ani nagrań.

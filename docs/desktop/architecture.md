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

## Maszynowo czytelne wartości bazowe

Wartości bazowe nie powinny być powielane jako niezależne liczby w kodzie aplikacji. Kanonicznym źródłem danych dla parametrów wspólnych dla dokumentacji, walidatorów i środowiska czasu rzeczywistego jest `config/technical_baselines.yaml`.

Plik ma jawny `schema_version`. Oznacza to, że zmiana struktury danych wymaga świadomej migracji zamiast cichej reinterpretacji istniejących wartości. Moduł `avatar_studio.baselines` udostępnia odczyt całego dokumentu oraz odczyt przez ścieżkę kropkową, np. `behaviour.blink.duration_s`.

W praktyce obowiązuje kolejność:

```text
wartość bazowa → profil konkretnego awatara → wartość zatwierdzona dla eksportu/runtime
```

Wartość bazowa jest punktem startowym. Nie może nadpisywać wiarygodnego pomiaru osoby referencyjnej.

## Maszynowo czytelna terminologia

`config/terminology.yaml` przechowuje kanoniczne polskie nazwy, ich angielskie odpowiedniki, skróty oraz formy zabronione. Jest to warstwa pomocnicza dla dokumentacji, nie słownik tłumaczący identyfikatory API.

Przykładowo nazwa **koartykulacja (coarticulation)** jest terminem kanonicznym. Błędne warianty są wykrywane automatycznie przez `scripts/lint_docs_terminology.py`.

Identyfikatory będące kontraktem technicznym, takie jak `jawOpen`, `roughness` czy `schema_version`, pozostają niezmienione. Nie należy ich tłumaczyć w kodzie ani w danych wymiany.

## Adapter narzędzia

Adapter narzędzia (tool adapter) jest cienką warstwą oddzielającą logikę Avatar Studio od szczegółów uruchamiania programu zewnętrznego. Zmiana ścieżki instalacji, nazwy programu wykonywalnego lub sposobu pobierania wersji nie powinna wymagać zmian w UI.

Wspólny kontrakt `ToolAdapter` obejmuje:

- jawnie wskazaną ścieżkę programu albo wykrywanie przez `PATH`;
- sprawdzenie dostępności bez uruchamiania programu;
- kontrolowany limit czasu wykonania (timeout);
- przechwycenie standardowego wyjścia (stdout);
- przechwycenie standardowego wyjścia błędów (stderr);
- kod zakończenia procesu;
- zapis pełnego polecenia jako danych diagnostycznych.

Pierwsze adaptery obejmują:

- `BlenderAdapter`;
- `ColmapAdapter`;
- `FFmpegAdapter`;
- `PiperAdapter`.

Adapter nie powinien implementować logiki biznesowej etapu. Przykładowo `ColmapAdapter` może uruchomić proces rekonstrukcji, ale decyzja, czy wynik spełnia próg błędu reprojekcji, należy do walidatora domenowego.

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
| WAV | częstotliwość próbkowania (sample rate), kanały, szerokość próbki, czas |
| JSON | typ korzenia, liczba i nazwy kluczy lub liczba elementów |
| OBJ/PLY/STL/GLB/glTF/FBX | geometrie, wierzchołki, ściany/trójkąty, obwiednia i rozmiary, jeśli dostępny jest `trimesh` |
| BLEND | podstawowe metadane pliku; pełna inspekcja później przez adapter Blendera |

Każdy zarejestrowany artefakt otrzymuje hash SHA-256. Dzięki temu aplikacja może wykrywać zmianę pliku po zatwierdzeniu etapu i unieważniać wyniki zależne.

## Interfejs

Bieżący układ:

- nagłówek: nazwa workspace oraz procent ukończenia pipeline'u;
- lewy panel: pipeline i status wszystkich etapów;
- środek: instrukcja bieżącego etapu, zależności i oczekiwane wyniki;
- prawy panel: artefakty oraz szczegółowe parametry wybranego pliku;
- dół: logi narzędzi, walidacja i komunikaty diagnostyczne.

Aplikacja nie ukrywa kryteriów. Użytkownik ma widzieć, dlaczego etap jest zablokowany albo zaliczony. Próba zaliczenia etapu bez zarejestrowanego artefaktu wymaga jawnego potwierdzenia.

## Kolejny poziom inspekcji

Adaptery powinny rozszerzać analizę etapami:

- Blender: obiekty, topologia, UV, materiały, szkielet, klucze kształtu i wagi wpływu kości;
- COLMAP: liczba kamer, zarejestrowanych zdjęć, błąd reprojekcji i pokrycie;
- Piper/audio: model głosu, długość wypowiedzi, dopasowanie czasowe fonemów i pokrycie wizemów;
- FFmpeg: parametry kontenera, kodek, częstotliwość próbkowania i deterministyczne przetwarzanie audio/wideo;
- pakiet runtime: trójkąty, materiały, tekstury, animacje, cele morfowania i budżet pamięci.

## Bezpieczeństwo

Program nie wysyła prywatnych materiałów do chmury bez jawnej funkcji i zgody. Wszystkie ścieżki prywatnego workspace są lokalne. Logi nie powinny kopiować treści zdjęć ani nagrań. Argumenty poleceń muszą być przechowywane jako lista argumentów procesu, a nie składany łańcuch wykonywany przez powłokę, co ogranicza ryzyko niezamierzonej interpretacji znaków specjalnych.

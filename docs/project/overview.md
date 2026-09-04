# Przegląd projektu

Avatar Studio rozwija kompletny cyfrowy odpowiednik człowieka, a nie pojedynczy statyczny model. Rezultatem ma być edytowalna postać czasu rzeczywistego ze spójną geometrią, PBR, włosami, ubraniami, pełnym riggingiem, mimiką, animacją i mową generowaną przez Piper.

## Wynik i granice automatyzacji

Końcowym źródłem prawdy jest wersjonowana, edytowalna scena DCC wraz z osobnymi teksturami, rigiem i animacjami. Towarzyszy jej pochodny pakiet runtime, profil eksportu oraz raport walidacji pozwalający odtworzyć pochodzenie plików. Sam eksport FBX, GLB albo USD nie jest ukończonym źródłem projektu.

Avatar Studio rejestruje artefakty i ich SHA-256, pilnuje zależności i bramek jakości oraz automatyzuje tylko opisane operacje lokalne. Nie wykonuje automatycznie decyzji artystycznych, korekty anatomii, retopologii, UV, materiałów, groomingu, riggingu, skinningu ani animacji. Nie zastępuje Blendera, COLMAP, Piper lub silnika docelowego i nie gwarantuje fotorealizmu na podstawie samego uruchomienia pipeline'u.

## Przygotowanie użytkownika

Przed rozpoczęciem zaplanuj:

- **kompetencje:** fotografia i kontrola ekspozycji, anatomia, modelowanie i retopologia, UV/PBR, rigging i deformacje, animacja oraz diagnostyka eksportu w wybranym silniku; jedna osoba nie musi wykonywać wszystkich ról, ale każda musi mieć właściciela;
- **programy:** Python 3.11 i Avatar Studio, Blender, COLMAP, FFmpeg i Git LFS; Piper jest potrzebny dla syntezy mowy, a Unreal Engine, Unity lub inne środowisko — dla właściwego profilu runtime;
- **sprzęt i dysk:** stację roboczą zdolną uruchomić rekonstrukcję i DCC oraz szybki lokalny dysk. Na pierwszą pełną próbę zarezerwuj orientacyjnie `200–500 GB` wolnego miejsca na fotografie, cache COLMAP, sceny kolejnych wersji, tekstury i eksporty, a produkcję zwymiaruj pomiarem własnego zestawu; wysokie rozdzielczości mogą wymagać więcej. Backup przechowuj na osobnym, chronionym nośniku i nie dopuszczaj do zapełnienia woluminu podczas rekonstrukcji;
- **prywatne dane i zgody:** zdjęcia twarzy i ciała, pomiary, skany, ekspresje, głos oraz ewentualny model Piper. Ustal zakres zgody, retencję, kontrolę dostępu, szyfrowany backup i zasady publikacji przed wykonaniem capture.

## Kolejność lektury i pracy

1. [Konfiguracja Windows](../setup/windows.md) albo [konfiguracja Linux](../setup/linux.md).
2. [Prywatność i dane referencyjne](privacy-and-reference-data.md).
3. [Przechwytywanie materiału](../capture/photography-guide.md).
4. [Modelowanie](../modeling/overview.md).
5. [Specyfikacja rigu](../rigging/skeleton-specification.md).
6. [Materiały](../materials/overview.md).
7. [Architektura animacji](../animation/animation-architecture.md).
8. [Eksport i środowisko czasu rzeczywistego](../runtime/overview.md).
9. [Kryteria walidacji](../validation/acceptance-criteria.md).

[Przegląd pipeline'u](../pipeline/overview.md) jest mapą etapów wykonawczych. Otwieraj z niego instrukcję bieżącego etapu, zamiast wykonywać obszary równolegle bez zatwierdzonych wejść.

## Pierwszy lokalny workspace

Workspace musi być katalogiem projektu użytkownika, a nie podkatalogiem klonu Git. Avatar Studio tworzy w nim `.avatar-studio/project.sqlite3` i `reports/`; fotografie i duże artefakty pozostają zwykłymi plikami obok stanu aplikacji.

### Windows

1. Utwórz na lokalnym, chronionym woluminie na przykład `D:\AvatarStudio\projects\first-avatar`.
2. Uruchom `AvatarStudio.exe` albo `avatar-studio` i wskaż ten katalog w oknie wyboru workspace.
3. Sprawdź w PowerShell:

```powershell
Test-Path 'D:\AvatarStudio\projects\first-avatar\.avatar-studio\project.sqlite3'
Test-Path 'D:\AvatarStudio\projects\first-avatar\reports'
Test-Path 'D:\AvatarStudio\projects\first-avatar\.git'
```

Pierwsze dwa polecenia powinny zwrócić `True`, a ostatnie `False`. Upewnij się ponadto, że wybrana ścieżka nie znajduje się wewnątrz katalogu sklonowanego repozytorium.

### Linux

1. Utwórz na lokalnym katalogu z ograniczonym dostępem, na przykład `~/AvatarStudio/projects/first-avatar`, i ustaw uprawnienia:

```bash
mkdir -p ~/AvatarStudio/projects/first-avatar
chmod 700 ~/AvatarStudio/projects/first-avatar
```

2. Uruchom `avatar-studio` i wskaż ten katalog w oknie wyboru workspace.
3. Sprawdź:

```bash
test -f ~/AvatarStudio/projects/first-avatar/.avatar-studio/project.sqlite3
test -d ~/AvatarStudio/projects/first-avatar/reports
test ! -e ~/AvatarStudio/projects/first-avatar/.git
```

Komplet kodów wyjścia `0` potwierdza oczekiwaną strukturę. Sprawdź również, że `realpath` workspace nie rozpoczyna się ścieżką klonu repozytorium. Sam brak `.git` nie zastępuje kontroli lokalizacji ani uprawnień.

## Minimalna próba syntetyczna

Przed użyciem danych biometrycznych wyrenderuj prosty, nieidentyfikujący obiekt lub cyfrowy manekin z wielu nakładających się punktów widzenia. Zapisz serię poza repozytorium, bez sekretów i bez materiałów prawdziwej osoby.

1. Otwórz syntetyczny workspace i wykonaj **Probe local tools**.
2. W etapie 01 zarejestruj serię, wygeneruj `capture_manifest.json` i obejrzyj raport oraz SHA-256.
3. Jeżeli obrazy mają rzeczywiste nakładanie i zmienną perspektywę, uruchom etap 02, a po jego zaliczeniu etap 03. Zestaw złożony z przypadkowych lub płaskich obrazów służy tylko do próby manifestu i nie powinien przejść rekonstrukcji.
4. Zarejestruj wynik, wykonaj bramkę Definition of Done i wygeneruj raport projektu. Nie publikuj workspace tylko dlatego, że dane są syntetyczne — najpierw sprawdź raporty pod kątem ścieżek i metadanych.

Ta próba potwierdza obsługę katalogów, narzędzi, statusów i raportów. Nie potwierdza podobieństwa, anatomii, deformacji ani gotowości produkcyjnej.

## Bramka jakości i powrót

Po każdym etapie zatrzymaj się przed rozpoczęciem pracy zależnej. Kontynuuj dopiero wtedy, gdy raport jest kompletny, wynik Definition of Done ma status `passed`, a oficjalne wejście ma status artefaktu `approved`. Wynik `failed` oznacza zakaz uruchamiania etapów downstream, eksportowania wadliwego wyniku jako kandydata produkcyjnego oraz nadpisywania ostatniego zatwierdzonego źródła. Najpierw użyj [diagnostyki](../desktop/troubleshooting.md), usuń przyczynę i ponów kontrolę. Waiver jest kontrolowaną decyzją o ryzyku, a nie zmianą wyniku testu na poprawny.

Aby wrócić, znajdź w tabeli artefaktów lub ostatnim raporcie wersję `approved` i zweryfikuj jej ścieżkę oraz SHA-256. Otwórz ją jako źródło, zachowaj bez zmian, a dalszą korektę zapisz jako nową wersję `vNNN`. Odrzuć lub pozostaw do diagnostyki wersję `failed`; nie podmieniaj ręcznie wpisów w `.avatar-studio/project.sqlite3`. Jeśli zatwierdzony plik zniknął albo hash jest inny, odtwórz odpowiadającą mu wersję z kontrolowanego backupu i ponownie ją zarejestruj. Zasady statusów opisuje [wersjonowanie artefaktów](asset-versioning.md).

## Granice produktu

Repozytorium ma trzy warstwy:

1. **Production assets and tooling**: skrypty, manifesty i edytowalne artefakty pipeline'u.
2. **Documentation**: statyczny portal MkDocs publikowany przez GitHub Pages.
3. **Avatar Studio**: lokalna aplikacja desktopowa prowadząca użytkownika przez pipeline i przechowująca jego stan.

Strona WWW nie odczytuje prywatnych zdjęć i nie jest panelem stanu projektu. Aplikacja desktopowa nie zastępuje DCC ani silnika, lecz orkiestruje proces, waliduje wyniki i dokumentuje postęp.

## Niezmienniki

- Kanonicznym źródłem modelu jest edytowalna scena DCC, nie FBX/GLB.
- Prywatne fotografie i nagrania nie trafiają do publicznego repozytorium.
- Każdy etap pozostawia jawny artefakt i raport walidacji.
- Zmiana topologii po rozpoczęciu riggingu jest zmianą łamiącą zależności i wymaga jawnej migracji.
- Wydajność runtime jest kryterium projektowym od początku, a nie końcową optymalizacją.

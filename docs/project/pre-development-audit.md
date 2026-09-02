# Audyt gotowości przed dalszym rozwojem

Dokument jest żywą listą kontrolną stabilizacji Avatar Studio. Pierwszy audyt wykazał, że repozytorium miało szeroką dokumentację i poprawne fundamenty architektoniczne, ale GUI nie wykonywało podstawowego pipeline'u. Od tego czasu wdrożono zasadniczą część warstwy M0.5.

## Stan po stabilizacji fundamentu

Avatar Studio nie jest jeszcze kompletnym automatycznym systemem tworzenia fotorealistycznego człowieka. Jest jednak obecnie wykonywalnym narzędziem desktopowym, które potrafi bez ręcznego wpisywania poleceń:

1. utworzyć lub otworzyć prywatny workspace;
2. skonfigurować ścieżki Blender, COLMAP, FFmpeg i Piper;
3. uruchomić sparse reconstruction COLMAP;
4. uruchomić dense reconstruction, fusion i meshing COLMAP;
5. uruchomić głęboką inspekcję sceny Blender;
6. uruchomić podstawowe operacje FFmpeg i Piper;
7. zapisać historię uruchomień i raporty operacji;
8. zarejestrować artefakty z SHA-256 i metadanymi;
9. zapisać wyniki walidacji i kontrolowane wyjątki DoD;
10. automatycznie unieważnić downstream stages po zmianie zatwierdzonego wejścia;
11. anulować aktywny proces zewnętrzny;
12. przejść bezpośrednio z etapu do właściwej dokumentacji.

Pozostałe etapy produkcyjne, szczególnie cleanup, retopologia, UV, materiały, rig, skinning i animacja, nadal wymagają pracy w Blenderze lub innym DCC. Avatar Studio prowadzi przez ich kolejność, rejestruje wyniki i może inspektować sceny, ale jeszcze ich automatycznie nie wykonuje.

## Zrealizowane zadania P0

### Zgodność dokumentacji z implementacją

- [x] Instrukcja GUI opisuje aktualne kontrolki i rzeczywisty zakres automatyzacji.
- [x] Usunięto stwierdzenie, że użytkownik musi ręcznie konfigurować funkcje, których GUI nie posiada.
- [x] Dokumentacja rozróżnia operacje automatyczne od etapów wykonywanych ręcznie w DCC.
- [x] Zerobajtowe testy, walidator i pozorne końcowe artefakty zostały usunięte; sensowne szablony danych mają jawny minimalny format.

### Minimalny wykonywalny pipeline

- [x] Zdefiniowano scenariusz `zdjęcia -> sparse -> dense/fusion/mesh -> Blender inspection -> artefakty i raporty`.
- [x] Adapter COLMAP obsługuje `image_undistorter`, `patch_match_stereo`, `stereo_fusion` oraz Poisson/Delaunay meshing.
- [x] Utworzono `OperationService` jako warstwę orkiestracji zamiast wywoływania adapterów bezpośrednio z logiki projektu.
- [x] Każda operacja wykonywana przez `OperationService` zapisuje rekord `tool_runs` i raport JSON w `reports/`.
- [x] Dodano test kontraktu dense reconstruction z mockowanym COLMAP.
- [ ] Dodać opcjonalny smoke test end-to-end na prawdziwym mini-zestawie zdjęć w środowisku posiadającym COLMAP.

### GUI bez konieczności wpisywania poleceń

- [x] Projekt można utworzyć lub otworzyć przez wybór workspace.
- [x] Dodano ekran konfiguracji ścieżek Blender/COLMAP/FFmpeg/Piper.
- [x] Dodano operacje GUI dla COLMAP sparse i dense reconstruction, Blender inspection, Piper synthesis i normalizacji FFmpeg.
- [x] Operacje są wykonywane w `QThread`, dzięki czemu główne GUI nie jest blokowane.
- [x] Adaptery wykorzystują proces możliwy do anulowania; **Cancel operation** kończy aktywny subprocess.
- [x] GUI pokazuje opis celu operacji i link do dokumentacji etapu.
- [~] Parametry są zbierane formularzami/dialogami, ale wymagają dalszego ujednolicenia do jednego panelu parametrów.
- [~] Log, błąd i anulowanie są obsługiwane; brakuje dokładnego procentowego postępu dla wieloetapowych operacji COLMAP.
- [ ] Po zakończeniu każdej operacji pokazywać jawnie następną zalecaną czynność jako osobny element UI.

### Rzeczywiste bramki jakości

- [x] Zaliczenie etapu wymaga artefaktu.
- [x] Krytyczny wynik walidacji `failed` blokuje zaliczenie bez jawnego waivera.
- [x] Waiver wymaga tekstowego uzasadnienia i jest przechowywany w bazie projektu.
- [x] Waiver nie może zastąpić brakującego artefaktu.
- [x] Zmiana artefaktu w zatwierdzonym etapie resetuje wszystkie zależne statusy i usuwa ich nieaktualne wyniki walidacji.
- [~] Liczba automatycznych kryteriów DoD jest jeszcze mała; kolejne kryteria trzeba dodawać wraz z implementacją etapów.

## Dokumentacja dydaktyczna

- [x] Rozbudowano etap 02 Fotogrametria do procedury obejmującej przygotowanie, wybór matchera, interpretację sparse modelu, reprojection error, diagnostykę i procedury naprawcze.
- [x] Rozbudowano etap 03 Rekonstrukcja do procedury `undistort -> PatchMatch -> fusion -> meshing`, wraz z kontrolą jakości i typowymi awariami.
- [ ] Ujednolicić pozostałe rozdziały pipeline'u według schematu: cel, wejście, przygotowanie, procedura, parametry, kontrola pośrednia, błędy, naprawa, artefakty, DoD.
- [ ] Priorytetowo rozbudować cleanup, retopologię, UV, rig, skinning, eksport i runtime validation.
- [ ] Dodać ilustracje lub zrzuty GUI tam, gdzie tekst nie wystarcza do jednoznacznego wykonania czynności.

## Inspekcja i podgląd artefaktów

- [x] Dostępna jest głęboka inspekcja `.blend` przez BlenderAdapter uruchamiana z GUI.
- [x] Lekki inspektor obsługuje obrazy, WAV, JSON i popularne formaty mesh.
- [~] Blender report obejmuje geometrię, UV, materiały, armatures, bones, shape keys, actions i jednostki, ale brakuje jeszcze walidacji semantycznej konkretnego szkieletu, materiałów i morph targets.
- [ ] Dodać podgląd obrazów bez opuszczania Avatar Studio.
- [ ] Dodać interaktywny podgląd 3D siatki, rigu i animacji.
- [ ] Powiązać ostrzeżenia inspektora z większą liczbą automatycznych kryteriów etapu.

## Testy i CI

- [x] Główny CI obejmuje `apps/avatar_studio/src`, `scripts` i `tests`.
- [x] Dodano testy bramek DoD, waiverów, unieważniania zależności, konfiguracji narzędzi i dense reconstruction.
- [x] Usunięto puste pliki testów i pusty walidator.
- [x] Dodano headless smoke test GUI; workflow pakowania uruchamia go przed budową aplikacji.
- [ ] Dodać test zgodności deklarowanego statusu funkcji w dokumentacji z rejestrem operacji GUI.
- [ ] Dodać test prawdziwego COLMAP na małym publicznym zestawie demonstracyjnym, uruchamiany opcjonalnie poza szybkim CI.

## Pozostałe zadania przed wersją 1.0

Najważniejsze dalsze prace nie dotyczą już samego uruchomienia podstawowego pipeline'u, lecz zwiększenia jego jakości i zakresu:

1. procentowy postęp i kolejka operacji;
2. podgląd obrazów i 3D;
3. automatyczne kryteria jakości sparse modelu, meshu, UV, rigu i eksportu;
4. głębsza integracja etapów Blender zamiast samej inspekcji;
5. raport końcowy projektu zawierający artefakty, walidacje, waivery i provenance;
6. wersjonowanie/superseding artefaktów zamiast pozostawiania ich wyłącznie jako historii plików;
7. rozbudowa wszystkich instrukcji pipeline'u do poziomu dydaktycznego;
8. pełny demonstrator czasu rzeczywistego.

## Kryterium zakończenia M0.5

M0.5 można uznać za funkcjonalnie osiągnięte dla podstawowego procesu, jeżeli instalacja użytkownika posiada poprawnie skonfigurowany COLMAP i potrafi na realnej serii zdjęć wykonać sekwencję sparse → dense → mesh bez ręcznego CLI. Pełne zamknięcie M0.5 wymaga jeszcze praktycznego smoke testu na rzeczywistym zestawie danych i potwierdzenia workflow CI po zmianach.

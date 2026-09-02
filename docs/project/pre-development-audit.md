# Audyt gotowości przed dalszym rozwojem

Dokument podsumowuje stan projektu Avatar Studio po przeglądzie repozytorium, dokumentacji, kodu aplikacji desktopowej, adapterów narzędzi i roadmapy. Jego celem jest oddzielenie elementów już istniejących od elementów, które są jedynie opisane lub przygotowane architektonicznie.

## Wniosek ogólny

Projekt ma dobrą strukturę architektoniczną, szerokie pokrycie tematyczne dokumentacji i poprawnie rozdzielone warstwy: pipeline, adaptery narzędzi, lokalny stan projektu, inspekcję artefaktów i dokumentację techniczną. Nie jest jednak jeszcze gotowym środowiskiem prowadzącym użytkownika przez podstawowy proces tworzenia awatara bez ręcznego używania narzędzi zewnętrznych.

Największa luka znajduje się pomiędzy warstwą adapterów i dokumentacją a interfejsem użytkownika. GUI potrafi obecnie prowadzić po etapach, przechowywać statusy i rejestrować artefakty, ale nie uruchamia większości operacji produkcyjnych. W wielu miejscach dokumentacja opisuje funkcje docelowe tak, jakby były już dostępne.

## Stan poszczególnych warstw

### Dokumentacja

Mocne strony:

- logiczny podział na 21 etapów pipeline'u;
- osobne sekcje capture, modeling, materials, rigging, animation, speech, runtime i validation;
- dobre rozdzielenie specyfikacji technicznej od procesu produkcyjnego;
- osobne poradniki dotyczące fotografii, samodzielnego wykonywania zdjęć i wariantu osoby obracającej się przed kamerą;
- jawne Definition of Done dla etapów;
- MkDocs i automatyczna kontrola obecności dokumentów w nawigacji.

Braki:

- znaczna część rozdziałów pipeline'u ma charakter checklisty, a nie kompletnej instrukcji dydaktycznej;
- część instrukcji mówi, co zrobić, ale nie pokazuje dokładnie gdzie wykonać operację, jakie parametry ustawić, jak interpretować wynik i co zrobić w przypadku niepowodzenia;
- Windows i Linux często powtarzają niemal tę samą procedurę zamiast rozdzielać część wspólną od różnic systemowych;
- dokumentacja nie wskazuje przy każdym etapie, które czynności wykonuje już GUI, które adapter, a które nadal wymagają ręcznej pracy w Blenderze, COLMAP lub innym programie;
- dokumentacja desktopowa opisuje kilka funkcji, których obecne GUI jeszcze nie posiada.

### Kod podstawowego pipeline'u

Działające fundamenty:

- kanoniczne 21 etapów i zależności;
- lokalny stan projektu w SQLite;
- haszowanie i rejestracja artefaktów;
- lekka inspekcja obrazów, WAV, JSON i wybranych formatów 3D;
- adapter COLMAP do rekonstrukcji rzadkiej;
- adapter Blender do inspekcji sceny;
- adaptery FFmpeg i Piper;
- testy części parserów i kontraktów adapterów.

Braki funkcjonalne:

- brak jednej operacji orkiestrującej minimalny proces od importu zdjęć do rekonstrukcji i przekazania wyniku do dalszej obróbki;
- adapter COLMAP kończy się na sparse reconstruction; podstawowy proces awatara wymaga również jawnej obsługi dense reconstruction / fusion / meshing albo wskazania wspieranego zamiennika;
- brak produkcyjnych operacji GUI dla cleanupu, retopologii, UV, materiałów, rigu i eksportu;
- brak mechanizmu walidacyjnego, który faktycznie blokuje zaliczenie etapu, gdy wymagania nie są spełnione;
- zaliczenie etapu może być wykonane bez artefaktu po prostym potwierdzeniu użytkownika;
- brak automatycznego unieważniania downstream artefacts po zmianie wejścia;
- brak spójnego zapisu uruchomień adapterów do tabeli `tool_runs` z poziomu GUI;
- brak pełnych testów end-to-end minimalnego pipeline'u.

### GUI

Obecnie dostępne:

- wybór katalogu workspace;
- lista 21 etapów i statusów;
- opis etapu, zależności i oczekiwanych wyników;
- odnośnik do pełnej dokumentacji;
- ręczna zmiana statusu etapu;
- rejestracja i inspekcja istniejącego artefaktu;
- diagnostyka obecności lokalnych narzędzi.

Braki blokujące obsługę bez kodu i CLI:

- brak kreatora nowego projektu;
- brak ekranu konfiguracji ścieżek Blender, COLMAP, FFmpeg i Piper;
- brak formularzy parametrów operacji;
- brak przycisków uruchamiających właściwe operacje narzędzi dla etapów;
- brak kolejki zadań i widocznego postępu długich operacji;
- brak obsługi anulowania procesu;
- brak podglądu zdjęć, chmury punktów, siatki 3D, tekstur, rigu lub animacji;
- brak interpretacji wyników walidacji w języku użytkownika;
- brak widoku Definition of Done z automatycznymi i ręcznymi kryteriami;
- brak tworzenia i zarządzania wyjątkami od kryteriów odbioru;
- brak bezpośredniego przycisku pomocy dla konkretnej funkcji lub parametru poza ogólnym linkiem do dokumentu etapu;
- brak raportu końcowego projektu.

## Zadania konieczne przed dalszym rozwojem funkcji wysokiego poziomu

Poniższe zadania powinny zostać potraktowane jako etap stabilizacji obecnego fundamentu.

### P0. Zgodność dokumentacji z implementacją

- [ ] Oznaczyć funkcje jako `implemented`, `partial` lub `planned` w dokumentacji desktopowej i roadmapie.
- [ ] Usunąć lub poprawić stwierdzenia sugerujące, że GUI już uruchamia cały pipeline, waliduje DoD i blokuje błędne etapy.
- [ ] Zaktualizować instrukcję GUI tak, aby odpowiadała faktycznym kontrolkom obecnej wersji.
- [ ] Dodać tabelę `etap -> operacja GUI -> adapter -> narzędzie zewnętrzne -> status implementacji`.
- [ ] Zastąpić pozorne puste artefakty i testy czytelnymi placeholderami albo usunąć je, aby plik 0 B nie sugerował gotowego wyniku.

### P0. Minimalny wykonywalny pipeline

- [ ] Zdefiniować minimalny wspierany scenariusz MVP, np. `zdjęcia -> COLMAP sparse -> dense/mesh -> import/inspekcja Blender -> rejestracja artefaktu`.
- [ ] Dodać obsługę dense reconstruction i meshing albo jawnie zintegrować inne narzędzie realizujące te kroki.
- [ ] Utworzyć warstwę orkiestracji operacji powiązaną z `StageDefinition` zamiast wywoływać adaptery ad hoc.
- [ ] Zapisywać każde uruchomienie narzędzia i raport do `tool_runs` oraz katalogu raportów projektu.
- [ ] Dodać test integracyjny minimalnego pipeline'u z mockowanymi narzędziami oraz osobny test smoke na prawdziwych narzędziach, gdy są dostępne.

### P0. GUI bez konieczności wpisywania poleceń

- [ ] Dodać kreator projektu i ekran ustawień narzędzi.
- [ ] Dodać do etapów panel `Run operation` z formularzem parametrów i wartościami domyślnymi.
- [ ] Połączyć GUI co najmniej z COLMAP, Blender, FFmpeg i Piper adapterami.
- [ ] Uruchamiać ciężkie procesy poza wątkiem UI i raportować progres, log, błąd oraz możliwość anulowania.
- [ ] Dodać przy każdej operacji krótkie wyjaśnienie celu parametrów oraz link `Więcej w dokumentacji` do właściwej sekcji.
- [ ] Pokazywać użytkownikowi następną zalecaną czynność po zakończeniu operacji.

### P0. Rzeczywiste bramki jakości

- [ ] Zamienić ręczne `Mark passed` na mechanizm oceny kryteriów DoD.
- [ ] Rozdzielić kryteria automatyczne i wymagające inspekcji człowieka.
- [ ] Nie pozwalać przejść dalej przy krytycznym błędzie bez jawnie zapisanego wyjątku.
- [ ] Zapisywać uzasadnienie wyjątku i prezentować je w raporcie końcowym.
- [ ] Automatycznie unieważniać downstream stages i artefakty po zmianie zatwierdzonego wejścia.

### P1. Dokumentacja dydaktyczna krok po kroku

- [ ] Ujednolicić każdy rozdział pipeline'u według schematu: cel, wejście, przygotowanie, procedura krok po kroku, parametry, kontrola pośrednia, typowe błędy, procedura naprawcza, artefakty, DoD.
- [ ] Rozbudować szczególnie fotogrametrię, dense reconstruction, cleanup, retopologię, UV, rig, skinning, eksport i walidację runtime.
- [ ] Wprowadzić konkretne przykłady konfiguracji dla minimalnego scenariusza referencyjnego.
- [ ] Wyjaśnić pojęcia techniczne przed użyciem ich jako polecenia wykonawczego.
- [ ] Dodać ilustracje lub zrzuty interfejsu tam, gdzie sam opis tekstowy nie wystarcza.

### P1. Inspekcja i podgląd artefaktów

- [ ] Dodać głęboką inspekcję `.blend` przez BlenderAdapter podczas rejestracji sceny.
- [ ] Dodać inspekcję skeleton, materials, morph targets, UV i animacji dla wspieranych formatów.
- [ ] Dodać podgląd zdjęć i podstawowy interaktywny podgląd 3D.
- [ ] Powiązać ostrzeżenia inspektora z kryteriami etapu.

### P1. Testy i CI

- [ ] Usunąć puste testy lub zaimplementować je.
- [ ] Rozszerzyć główny workflow CI o kod `apps/avatar_studio/src`, ponieważ obecny workflow sprawdza głównie `scripts` i `tests`.
- [ ] Dodać test uruchomienia GUI w trybie headless/smoke.
- [ ] Dodać test zgodności tekstu dokumentacji GUI z funkcjami oznaczonymi jako zaimplementowane.
- [ ] Dodać test, że wszystkie artefakty przykładowe w repozytorium są albo poprawnymi plikami, albo jawnie oznaczonymi placeholderami.

## Roadmapa po audycie

Obecna roadmapa poprawnie rozdziela warstwę bazową od docelowej wersji 1.0, ale zbyt słabo pokazuje stan pośredni. M0 można uznać za w dużej mierze wykonane, natomiast M1-M5 są głównie specyfikacją procesu, a nie działającym workflow programu. M6 zawiera znaczną część zadań, które są w praktyce warunkiem używalności podstawowego produktu i powinny zostać rozpoczęte wcześniej.

Zalecane jest wprowadzenie kamienia milowego **M0.5 / Foundation hardening** obejmującego zadania P0 z tego dokumentu. Dopiero po nim kolejne prace nad zaawansowanymi funkcjami modelowania, rigu i runtime powinny być traktowane jako rozwój funkcjonalny produktu.

## Kryterium zakończenia stabilizacji

Fundament Avatar Studio można uznać za gotowy do dalszego rozwoju, gdy użytkownik bez wpisywania poleceń może:

1. utworzyć projekt;
2. skonfigurować wymagane narzędzia;
3. wskazać serię zdjęć;
4. uruchomić wspierany proces rekonstrukcji;
5. obserwować postęp i błędy;
6. uzyskać zarejestrowany artefakt 3D i raport;
7. zrozumieć wynik walidacji;
8. otworzyć właściwą instrukcję bez szukania jej ręcznie;
9. przejść do następnego etapu tylko po spełnieniu kryteriów albo zapisaniu kontrolowanego wyjątku.

Dopiero ten poziom odpowiada deklaracji, że Avatar Studio pozwala wykonać przynajmniej podstawowy proces tworzenia awatara z poziomu GUI.

# Diagnostyka i rozwiązywanie problemów

Ten rozdział opisuje typowe awarie środowiska Avatar Studio i sposób ich rozpoznawania. Celem diagnostyki nie jest ukrycie błędu, lecz ustalenie, który kontrakt pipeline'u został naruszony.

## Narzędzie nie zostało znalezione

Jeżeli Blender, COLMAP, FFmpeg lub Piper nie znajduje się w `PATH`, Avatar Studio powinien pozwolić wskazać pełną ścieżkę do pliku wykonywalnego.

Sprawdź najpierw wersję programu w terminalu. Na Windows użyj odpowiednio `blender.exe`, `colmap.exe`, `ffmpeg.exe` lub `piper.exe`. Na Linux zwykle wystarczą nazwy bez rozszerzenia.

Nie wpisuj ścieżek instalacyjnych na stałe do kodu projektu. Ścieżka jest konfiguracją stanowiska roboczego.

## Adapter zwraca kod różny od zera

Każde wywołanie narzędzia zapisuje kod zakończenia, standardowe wyjście i standardowy strumień błędów. W pierwszej kolejności sprawdź:

1. pełną komendę;
2. istnienie plików wejściowych;
3. prawa dostępu do katalogu roboczego;
4. zgodność wersji narzędzia;
5. ostatnie linie `stderr`.

Nie oznaczaj etapu jako zaliczony tylko dlatego, że powstał plik wyjściowy. Plik może być niekompletny po częściowo nieudanej operacji.

## Blender nie otwiera sceny

Najczęstsze przyczyny to brak dodatku używanego przez scenę, nowsza wersja pliku `.blend`, brakujące zasoby zewnętrzne lub skrypt wymagający interfejsu graficznego.

Inspekcja automatyczna powinna działać w trybie bez interfejsu. Jeśli scena uruchamia automatyczne skrypty, sprawdź zasady bezpieczeństwa i nie włączaj globalnie wykonywania niezaufanego kodu.

## COLMAP rejestruje mało zdjęć

Niska liczba zarejestrowanych obrazów zwykle wskazuje na niedostateczne nakładanie widoków, poruszenie obiektu, słabe punkty charakterystyczne, odbicia lub błędne maski.

Dla sesji osoby obracającej się przed nieruchomą kamerą szczególnie sprawdź zgodność masek i stabilność pozy. Niski błąd reprojekcji nie kompensuje błędnej geometrii powstałej z niespójnego obiektu.

## FFmpeg tworzy cichy lub zniekształcony WAV

Porównaj źródło z wynikiem odsłuchowo i sprawdź parametry normalizacji. Zbyt agresywne ustawienia mogą podnosić szum lub zmniejszać dynamikę. Sprawdź też liczbę kanałów i częstotliwość próbkowania.

## Piper generuje niepoprawną wymowę

Najpierw oddziel problem modelu głosu od problemu animacji. Sprawdź sam WAV bez awatara. Jeżeli wymowa jest błędna w dźwięku, korekta wizemów nie rozwiąże problemu.

Zweryfikuj model, konfigurację, tekst wejściowy, język oraz parametry `length_scale`, `noise_scale` i `noise_w_scale`. Po każdej zmianie generacji ponownie wykonaj analizę fonemów i koartykulację.

## Dokumentacja nie buduje się

Uruchom:

```bash
python scripts/check_mkdocs_coverage.py
python scripts/lint_docs_terminology.py
mkdocs build --strict
```

Pierwsze polecenie wykrywa dokumenty niewłączone do nawigacji, drugie błędną terminologię, a trzecie błędy struktury MkDocs i lokalnych odwołań wykrywane podczas budowania.

## Baza projektu SQLite

Jeżeli projekt nie otwiera się po awarii programu, nie usuwaj od razu `.avatar-studio/project.sqlite3`. Najpierw wykonaj kopię pliku. Baza jest lokalnym stanem workflow i może zawierać historię artefaktów oraz wyniki walidacji.

## Artefakt zmienił się po zatwierdzeniu

SHA-256 służy do wykrywania takiej sytuacji. Jeśli plik źródłowy ma inny skrót niż zapisany przy walidacji, wyniki zależne powinny zostać uznane za nieaktualne i ponownie przeliczone.

## Minimalny raport błędu

Raport problemu technicznego powinien zawierać:

- wersję Avatar Studio;
- system operacyjny;
- wersję narzędzia zewnętrznego;
- etap pipeline'u;
- pełną komendę bez sekretów;
- kod zakończenia;
- istotny fragment `stderr`;
- oczekiwany i rzeczywisty rezultat.

Nie dołączaj prywatnych zdjęć, nagrań, modelu głosu ani sekretów, jeżeli nie są niezbędne do reprodukcji błędu.

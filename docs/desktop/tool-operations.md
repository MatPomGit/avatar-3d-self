# Operacje narzędzi potoku

Avatar Studio uruchamia ciężkie narzędzia robocze przez adaptery. Adapter jest warstwą oddzielającą logikę projektu od konkretnego programu i jego interfejsu wiersza poleceń (command-line interface, CLI). Dzięki temu UI, testy i walidatory nie muszą znać szczegółów wywołania Blendera, COLMAP, FFmpeg ani Piper.

## Kontrakt wspólny

Każde wywołanie przechowuje:

- pełną listę argumentów bez wykonywania przez powłokę;
- kod zakończenia procesu;
- standardowe wyjście (stdout);
- standardowy strumień błędów (stderr);
- limit czasu wykonania;
- znormalizowany raport JSON właściwy dla operacji.

Raport można zapisać przez `ToolAdapter.write_report()`. Pliki raportów powinny trafiać do `reports/` w prywatnym obszarze roboczym projektu, a nie do publicznego repozytorium, jeżeli zawierają ścieżki do materiałów referencyjnych.

## Blender

`BlenderAdapter.inspect_scene()` uruchamia scenę `.blend` w trybie bez interfejsu (background mode). Operacja nie zmienia sceny. Zwraca między innymi:

- liczbę obiektów i siatek;
- liczbę wierzchołków i ścian;
- liczbę warstw UV;
- liczbę materiałów i obrazów;
- liczbę szkieletów i kości;
- liczbę kluczy kształtu (shape keys);
- liczbę akcji animacji;
- jednostki sceny i skalę jednostki;
- częstotliwość klatek animacji.

W praktyce wzrost liczby wierzchołków, materiałów lub kluczy kształtu zwiększa koszt pamięci i przetwarzania. Raport służy więc zarówno do kontroli kompletności wersji wzorcowej, jak i do późniejszego porównania z profilem eksportu.

## COLMAP

`ColmapAdapter.reconstruct_sparse()` wykonuje trzy etapy:

`ekstrakcja cech → dopasowanie cech → rekonstrukcja rzadka`

Dostępne strategie dopasowania to obecnie `exhaustive`, `sequential` i `spatial`. Dla sesji człowieka wykonywanej wokół nieruchomej osoby najbezpieczniejszym punktem startowym jest zwykle `exhaustive`. Dla uporządkowanych długich sekwencji może być użyte `sequential`.

`ColmapAdapter.analyze_sparse_model()` normalizuje wynik `model_analyzer`. Najważniejsze pola to liczba zarejestrowanych obrazów, liczba punktów 3D, średnia długość ścieżki obserwacji i średni błąd reprojekcji (mean reprojection error).

Błąd reprojekcji jest odległością pomiędzy obserwowanym punktem obrazu a rzutem odpowiadającego mu punktu 3D. Niższa wartość jest zwykle lepsza, ale sama nie gwarantuje poprawnej geometrii. Dla statycznej, dobrze kontrolowanej sesji wartości poniżej około `0,5 px` są bardzo dobre, `0,5-1,0 px` zwykle dobre, `1-2 px` wymagają inspekcji, a wartości powyżej `2 px` są sygnałem ostrzegawczym.

Dla wariantu osoby obracającej się przed nieruchomą kamerą należy nadal stosować zasady rekonstrukcji obiektocentrycznej (object-centric reconstruction) i maski pierwszego planu. Sam adapter nie zmienia tego modelu geometrycznego.

## FFmpeg

`FFmpegAdapter.analyze_audio()` odczytuje podstawowe właściwości strumienia audio:

- czas trwania;
- kodek;
- częstotliwość próbkowania (sample rate);
- liczbę kanałów;
- przepływność, jeśli jest raportowana.

`FFmpegAdapter.normalize_wav()` tworzy materiał pośredni do dalszego przetwarzania mowy. Domyślny profil wyjściowy to jednokanałowy WAV z modulacją kodowo-impulsową (Pulse-Code Modulation, PCM) 16 bitów. Częstotliwość próbkowania jest jawna, a nie zakładana przez kod.

Domyślny punkt startowy normalizacji głośności to `-16 LUFS`, maksymalny poziom szczytowy `-1,5 dBTP` i zakres głośności `11 LU`. Są to parametry techniczne przygotowania sygnału, a nie ustawienia ekspresji głosu. Zbyt agresywna normalizacja może spłaszczać dynamikę i nie powinna zastępować kontroli jakości nagrania źródłowego.

## Piper

`PiperAdapter.synthesize()` realizuje:

`tekst → model Piper → WAV → raport pochodzenia`

Raport nie zapisuje pełnej treści wypowiedzi. Zapisuje skrót SHA-256 tekstu oraz jego długość, co pozwala wykryć zmianę wejścia bez kopiowania treści do logów.

Zapisywane są również:

- ścieżka i SHA-256 modelu ONNX;
- ścieżka i SHA-256 konfiguracji, jeżeli istnieje;
- częstotliwość próbkowania modelu;
- `speaker_id`, jeżeli model jest wielomówcowy;
- `length_scale`;
- `noise_scale` i `noise_w_scale`, jeżeli zostały podane;
- SHA-256 wygenerowanego WAV.

`length_scale = 1,0` oznacza tempo bazowe modelu. Wartość `0,9` skraca wypowiedź i ją przyspiesza, a `1,1` wydłuża i spowalnia. Zmiana tego parametru unieważnia wcześniejsze dopasowanie czasowe fonemów, ponieważ zmienia czas trwania dźwięku.

### Diagnostyczne wyrównanie z serwera HTTP

Bieżący serwer HTTP Piper udostępnia w `/info` listę fonemów i czas trwania każdego fonemu dla ostatniej syntezy. `PiperAdapter.fetch_http_alignment()` pobiera te dane, a `normalize_http_info()` zamienia kolejne czasy trwania na jawne przedziały `start_s` i `end_s`.

Przykład:

```text
m: 0.000-0.060 s
a: 0.060-0.200 s
```

Te dane są traktowane jako diagnostyczne źródło czasu. Przed użyciem w animacji należy je przekształcić do kanonicznego formatu projektu z `docs/speech/alignment-format.md`, znormalizować symbole fonetyczne oraz dopiero później zastosować mapowanie na wizemy i koartykulację (coarticulation).

Adapter nie zapisuje jawnej treści ostatniej wypowiedzi zwróconej przez `/info`. Zapisuje jej skrót SHA-256 i długość.

## Artefakty i unieważnianie danych

Każdy etap zależny od audio powinien traktować zmianę któregokolwiek z poniższych elementów jako zmianę artefaktu źródłowego:

- tekstu;
- modelu głosu;
- konfiguracji modelu;
- parametrów syntezy;
- wynikowego pliku WAV.

Po zmianie należy ponownie wykonać wymuszane dopasowanie czasowe (forced alignment), mapowanie fonemów na wizemy oraz koartykulację (coarticulation).

## Definition of Done

Warstwa operacji narzędzi jest gotowa do użycia w danym etapie, gdy:

- operacja sprawdza istnienie wejścia przed uruchomieniem narzędzia;
- ma jawny limit czasu;
- błąd procesu jest propagowany jako błąd etapu;
- wynik ma znormalizowany raport;
- raport zawiera wystarczające dane do odtworzenia konfiguracji;
- prywatne dane nie są niepotrzebnie kopiowane do logów;
- test jednostkowy sprawdza parser lub kontrakt polecenia bez wymagania instalacji ciężkiego narzędzia w CI.

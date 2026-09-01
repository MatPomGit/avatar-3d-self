# Format danych dopasowania czasowego

Dopasowanie czasowe musi być zapisane jako edytowalny i audytowalny artefakt. Nie przechowujemy wyłącznie gotowych krzywych animacji, ponieważ utrudniałoby to ponowne mapowanie fonemów, zmianę koartykulacji i diagnozowanie błędów synchronizacji.

## Jednostka czasu

Czasy przechowujemy w sekundach jako liczby zmiennoprzecinkowe względem początku pliku audio. Wartość `0,250` oznacza 250 ms od początku WAV.

Sekundy są formatem kanonicznym. Liczba próbek audio lub numer klatki mogą być zapisane pomocniczo, ale zależą od częstotliwości próbkowania i liczby klatek na sekundę.

## Minimalny rekord fonemu

```json
{
  "symbol": "p",
  "canonical": "p",
  "start_s": 0.420,
  "end_s": 0.495,
  "confidence": 0.96,
  "viseme": "PP"
}
```

`symbol` zachowuje wartość zwróconą przez narzędzie, a `canonical` jest wartością po normalizacji. Dzięki temu można później zmienić mapowanie bez utraty danych źródłowych.

## Pewność dopasowania

Miara pewności (confidence) opisuje, jak wiarygodne jest przypisanie segmentu do danego zakresu czasu. Jeżeli narzędzie nie zwraca porównywalnej probabilistycznej wartości, pole powinno być `null`, a nie sztucznie ustawione na `1`.

Dla narzędzia zwracającego wartości 0-1 można przyjąć orientacyjnie:

- `>= 0,85`: wysoka pewność;
- `0,60-0,85`: wynik użyteczny, ale warto kontrolować szybkie i nietypowe fragmenty;
- `< 0,60`: fragment do ręcznej inspekcji.

Progi nie są przenoszone automatycznie między różnymi alignerami.

## Pełny dokument

```json
{
  "schema_version": 1,
  "audio": {
    "path": "speech/utterance_001.wav",
    "sha256": "...",
    "sample_rate_hz": 22050,
    "duration_s": 3.842
  },
  "source": {
    "text": "Przykładowe zdanie.",
    "language": "pl-PL",
    "voice_model": "mateusz",
    "voice_model_version": "v001",
    "aligner": "tool-name",
    "aligner_version": "..."
  },
  "phonemes": []
}
```

Suma czasów segmentów nie musi dokładnie wypełniać całego pliku, ponieważ cisza może być reprezentowana osobnymi segmentami albo przerwami.

## Walidacja

Walidator powinien odrzucać:

- `start_s < 0`;
- `end_s <= start_s`;
- segmenty wychodzące poza długość WAV;
- niechronologiczną kolejność segmentów;
- brak wymaganego `schema_version`;
- zmianę pliku audio bez aktualizacji skrótu SHA-256.

Nakładanie fonemów nie jest domyślnie dozwolone w warstwie źródłowej. Nakładanie wizemów powstaje później w wyniku koartykulacji.

## Wersjonowanie

Zmiana granic czasowych tworzy nową wersję artefaktu. Nie nadpisujemy ręcznej korekty bez zapisania informacji o jej pochodzeniu.

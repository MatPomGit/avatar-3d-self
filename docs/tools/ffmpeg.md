# FFmpeg

FFmpeg jest narzędziem roboczym używanym w Avatar Studio do analizy, konwersji i normalizacji materiału audio. Nie odpowiada za syntezę głosu ani za rozpoznawanie fonemów. Jego zadaniem jest przygotowanie przewidywalnego sygnału wejściowego dla kolejnych etapów mowy.

## Rola w pipeline

Typowy przepływ wygląda następująco:

`audio źródłowe → analiza → normalizacja → WAV PCM → Piper/alignment/walidacja`

Najważniejszym celem jest usunięcie niepotrzebnej zmienności technicznej. Dwa nagrania o tej samej treści mogą różnić się kodekiem, liczbą kanałów, częstotliwością próbkowania i poziomem głośności. Bez normalizacji dalsze porównania stają się trudniejsze.

## Częstotliwość próbkowania

Częstotliwość próbkowania (sample rate) określa, ile próbek sygnału zapisuje się w ciągu sekundy. Przykładowe wartości to `16 kHz`, `22.05 kHz`, `24 kHz`, `44.1 kHz` i `48 kHz`.

W Avatar Studio nie należy arbitralnie zmieniać częstotliwości próbkowania modelu Piper. Jeśli model został wytrenowany dla `22050 Hz`, materiał generowany przez model pozostaje w `22050 Hz`, chyba że późniejszy etap wymaga jawnego przeskalowania.

Zbyt niska wartość ogranicza pasmo i może pogarszać czytelność spółgłosek. Zbyt wysoka wartość nie poprawia automatycznie jakości, a zwiększa rozmiar danych i koszt przetwarzania.

## Liczba kanałów

Dla analizy mowy i wymuszanego dopasowania czasowego preferowany jest pojedynczy kanał mono. Stereo ma sens w materiale odsłuchowym lub przestrzennym, ale nie daje przewagi dla podstawowego alignmentu pojedynczego głosu.

## PCM i głębia bitowa

Modulacja kodowo-impulsowa (Pulse-Code Modulation, PCM) zapisuje próbki bez kompresji stratnej. Domyślnym materiałem pośrednim jest WAV PCM 16 bitów. Jest to format interoperacyjny, przewidywalny i szeroko obsługiwany.

Dla materiału wzorcowego lub dalszej obróbki można zachować większą głębię bitową (bit depth), np. 24 bity, jeżeli źródło ją posiada. Nie należy jednak zwiększać głębi bitowej już skompresowanego źródła i traktować tego jako poprawy jakości.

## Normalizacja głośności

Normalizacja głośności (loudness normalization) wyrównuje postrzegany poziom nagrania. Bazowy profil roboczy Avatar Studio to:

- docelowa głośność zintegrowana: około `-16 LUFS`;
- maksymalny poziom szczytowy rzeczywisty: około `-1.5 dBTP`;
- zakres głośności: około `11 LU`.

Są to wartości techniczne, nie parametry emocji ani ekspresji. Zbyt agresywna normalizacja może zmniejszyć naturalną dynamikę głosu i uwidocznić szum tła.

## Adapter Avatar Studio

`FFmpegAdapter.analyze_audio()` odczytuje podstawowe parametry strumienia, a `FFmpegAdapter.normalize_wav()` tworzy znormalizowany WAV. Raport zawiera SHA-256 wejścia i wyjścia, dzięki czemu zmiana pliku może unieważnić wyniki zależne.

## Windows

Po instalacji sprawdź:

```powershell
ffmpeg -version
```

Jeżeli `ffmpeg.exe` nie znajduje się w `PATH`, wskaż jego pełną ścieżkę w ustawieniach Avatar Studio.

## Linux

```bash
ffmpeg -version
which ffmpeg
```

Wersję programu należy zapisywać w raporcie środowiska dla zatwierdzonych artefaktów.

## Definition of Done

Etap przygotowania audio jest zaliczony, gdy:

- wejście zostało przeanalizowane;
- wynikowy WAV ma jawną częstotliwość próbkowania i liczbę kanałów;
- nie występuje clipping;
- materiał nie ma przypadkowej kompresji stratnej pomiędzy etapami;
- raport zawiera SHA-256 wejścia i wyjścia;
- odsłuch nie ujawnia artefaktów wprowadzonych przez normalizację.

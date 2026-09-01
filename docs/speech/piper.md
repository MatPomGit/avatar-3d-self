# Piper TTS

Piper jest lokalnym systemem syntezy mowy (Text-to-Speech, TTS), który w Avatar Studio generuje rzeczywisty sygnał audio głosu awatara. Jest to źródło dźwięku, a nie bezpośredni sterownik mimiki. Ruch ust powstaje później z fonemów, wizemów i koartykulacji.

## Parametry syntezy

### Skala długości

Parametr `length_scale` steruje długością generowanej mowy. Wartość `1,0` oznacza tempo bazowe modelu. Wartość większa wydłuża wypowiedź i zwykle ją spowalnia, a mniejsza skraca.

Przykładowo:

- `0,85-0,95`: szybsza mowa;
- `1,0`: tempo bazowe;
- `1,05-1,20`: wolniejsza, bardziej wyraźna mowa.

Po zmianie `length_scale` trzeba ponownie wyznaczyć czasy fonemów, ponieważ wcześniejsze znaczniki czasu przestają być poprawne.

### Skale zmienności

Piper udostępnia parametry wpływające na zmienność syntezy, m.in. `noise_scale` oraz `noise_w_scale`. Nie należy ich traktować jako uniwersalnych „suwaków emocji”. Ich efekt zależy od modelu głosu.

Dla modelu produkcyjnego zapisujemy zatwierdzony profil zamiast losowo zmieniać parametry między wypowiedziami. Zbyt duża zmienność utrudnia reprodukcję i walidację synchronizacji.

## Częstotliwość próbkowania

Częstotliwość próbkowania (sample rate) określa liczbę próbek audio na sekundę. Typowe modele Piper używają częstotliwości zapisanej w konfiguracji modelu, np. 22 050 Hz. Nie należy wymuszać innej wartości bez jawnego przetwarzania końcowego.

Zmiana częstotliwości próbkowania nie zmienia czasu wypowiedzi, jeśli plik zostanie poprawnie przeliczony, ale błędna interpretacja tej wartości powoduje zmianę wysokości głosu i czasu odtwarzania.

## Kontrakt artefaktów

Wejście:

- tekst UTF-8;
- identyfikator modelu głosu;
- wersja modelu;
- parametry syntezy.

Wyjście:

- WAV PCM;
- metadane modelu i syntezy;
- opcjonalne surowe fonemy/alignmenty diagnostyczne;
- później osobny kanoniczny artefakt czasów fonemów.

Aktualny serwer HTTP projektu `piper1-gpl` udostępnia po syntezie informacje o fonemach i ich dopasowaniu audio w punkcie `/info`. Avatar Studio może wykorzystać je diagnostycznie, ale zapisuje wynik do własnego [formatu dopasowania czasowego](alignment-format.md), aby kontrakt projektu nie zależał od jednego API.

## Windows

Zalecany sposób integracji to lokalne środowisko Pythona lub uruchomiony lokalnie serwer HTTP Piper.

Przykład instalacji wariantu HTTP:

```powershell
python -m pip install "piper-tts[http]"
```

Uruchomienie serwera z modelem:

```powershell
python -m piper.http_server -m pl_PL-mateusz-medium --host 127.0.0.1 --port 5000
```

Model prywatny może wymagać jawnej ścieżki zgodnej z aktualną instalacją. Nie zapisujemy jej na stałe w publicznym repozytorium.

## Linux

```bash
python3 -m pip install 'piper-tts[http]'
python3 -m piper.http_server -m pl_PL-mateusz-medium --host 127.0.0.1 --port 5000
```

Dla usługi systemowej model i katalog danych powinny być przekazywane przez konfigurację hosta, a nie wpisane do kodu Avatar Studio.

## Synteza przez HTTP

Przykładowe żądanie:

```json
{
  "text": "Dzień dobry.",
  "length_scale": 1.0,
  "noise_scale": 0.667,
  "noise_w_scale": 0.8
}
```

Wartości `noise_scale` i `noise_w_scale` są wyłącznie wartościami startowymi. Profil konkretnego głosu musi zostać odsłuchany i zatwierdzony.

## Prywatność

Model głosu, dane treningowe i niepubliczne nagrania są prywatnymi artefaktami. Repozytorium może zawierać wyłącznie konfigurację adaptera, nazwę logiczną modelu i nieidentyfikujące metadane techniczne.

## Definition of Done

Integracja Piper zalicza etap, jeśli:

- ten sam profil syntezy jest reprodukowalny;
- WAV ma poprawny czas i częstotliwość próbkowania;
- wersja modelu jest zapisana;
- zmiana parametrów wymusza ponowne wyliczenie fonemów;
- model głosu nie trafia do publicznego repozytorium;
- wynik może zostać przekształcony do kanonicznego formatu czasów fonemów.

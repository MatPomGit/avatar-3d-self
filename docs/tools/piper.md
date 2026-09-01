# Piper

Piper jest lokalnym silnikiem syntezy mowy (text-to-speech, TTS) używanym w Avatar Studio do generowania dźwięku z indywidualnego modelu głosu. Piper dostarcza audio i informacje diagnostyczne o fonemach, ale nie steruje bezpośrednio twarzą awatara.

## Rola w pipeline

Kanoniczny przepływ jest następujący:

`tekst → Piper → WAV → fonemy i znaczniki czasu → wizemy → koartykulacja → animacja twarzy`

Rozdzielenie tych etapów jest ważne. Zmiana modelu głosu, tekstu albo parametrów syntezy zmienia czas trwania wypowiedzi, dlatego wcześniejsze wyrównanie fonemów i krzywe wizemów stają się nieaktualne.

## Model ONNX i konfiguracja

Model Piper jest zwykle reprezentowany przez plik ONNX oraz odpowiadający mu plik konfiguracyjny JSON. Konfiguracja zawiera między innymi częstotliwość próbkowania, informacje o języku i parametry modelu.

Avatar Studio zapisuje SHA-256 modelu i konfiguracji w raporcie syntezy. Pozwala to jednoznacznie ustalić, która wersja głosu wygenerowała dany plik WAV.

## `length_scale`

`length_scale` steruje czasem trwania generowanej mowy. Wartość `1.0` oznacza tempo bazowe modelu.

Praktyczne punkty odniesienia:

| Wartość | Efekt |
| ---: | --- |
| `0.85-0.95` | szybsza wypowiedź |
| `1.0` | tempo bazowe |
| `1.05-1.20` | wolniejsza wypowiedź |

Zmniejszenie parametru skraca mowę, zwiększenie ją wydłuża. Zbyt niska wartość może prowadzić do nienaturalnie szybkiej artykulacji, a zbyt wysoka do przeciągania samogłosek i utraty naturalnego rytmu.

Każda zmiana `length_scale` unieważnia wcześniejsze znaczniki czasowe fonemów.

## `noise_scale` i `noise_w_scale`

Parametry zmienności modelu, takie jak `noise_scale` i `noise_w_scale`, wpływają na sposób generacji prosodii i czasu trwania. Nie są uniwersalnymi suwakami emocji. Ich bezpieczne wartości powinny być zatwierdzone dla konkretnego modelu głosu.

Jeżeli model został wcześniej oceniony przy określonym profilu parametrów, ten profil należy zapisać i wersjonować zamiast stroić parametry losowo przy każdej wypowiedzi.

## Modele wielomówcowe

Jeśli model obsługuje wielu mówców, identyfikator mówcy (`speaker_id`) jest częścią pochodzenia artefaktu. Zmiana mówcy oznacza zmianę źródła audio i wymaga ponownego wykonania wszystkich etapów zależnych od mowy.

## Adapter Avatar Studio

`PiperAdapter.synthesize()` zapisuje:

- SHA-256 tekstu bez kopiowania jego pełnej treści do raportu;
- SHA-256 modelu ONNX;
- SHA-256 konfiguracji;
- parametry syntezy;
- częstotliwość próbkowania modelu;
- SHA-256 wynikowego WAV.

Dzięki temu raport pozwala odtworzyć warunki syntezy bez ujawniania zbędnej treści wypowiedzi.

## Dane fonemów z serwera HTTP

Serwer HTTP Piper może udostępniać diagnostyczne dane ostatniej syntezy. Avatar Studio normalizuje czas trwania każdego fonemu do jawnego przedziału:

`symbol + start_s + end_s + duration_s`

Taki format jest później mapowany do kanonicznego profilu fonemów języka polskiego, a następnie do wizemów.

Jeżeli narzędzie nie dostarcza wiarygodnej miary pewności, nie należy wpisywać sztucznej wartości `1.0`. Brak informacji zapisujemy jawnie jako brak danych.

## Windows

Przykładowe uruchomienie modelu lokalnego:

```powershell
piper --model pl_PL-mateusz-medium.onnx --output_file speech.wav
```

W rzeczywistym projekcie ścieżka modelu powinna pochodzić z prywatnego workspace, nie z publicznego repozytorium.

## Linux

```bash
piper --model pl_PL-mateusz-medium.onnx --output_file speech.wav
```

Avatar Studio może używać jawnie wskazanego pliku wykonywalnego, dlatego obecność `piper` w `PATH` nie jest wymagana.

## Prywatność

Indywidualny model głosu, dane treningowe, surowe nagrania oraz prywatne teksty nie powinny być publikowane w repozytorium. Publiczne mogą być adaptery, schematy raportów, dokumentacja i nieidentyfikujące profile techniczne.

## Definition of Done

Synteza jest zaakceptowana, gdy:

- model i konfiguracja są jednoznacznie zidentyfikowane;
- parametry syntezy zostały zapisane;
- WAV istnieje i przechodzi inspekcję techniczną;
- SHA-256 wejść i wyniku zapisano w raporcie;
- zmiana tekstu, modelu lub parametrów unieważnia dane fonemów i wizemów;
- odsłuch nie ujawnia oczywistych błędów wymowy, rytmu ani artefaktów syntezy.

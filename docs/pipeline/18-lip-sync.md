# 18. Lip-sync

Lip-sync zamienia zatwierdzony dźwięk i czas fonemów na ciągłe krzywe wizemów,
żuchwy i języka. Fonem opisuje dźwięk, wizem — jego obserwowalny kształt; relacja
nie jest jeden-do-jednego, ponieważ sąsiednie głoski wpływają na siebie.

**Input:** prywatny WAV, transkrypcja, alignment fonemów, zatwierdzony facial rig,
tabela fonem→wizem i profil eksportu.
**Edytowalny wynik:** wersjonowany alignment oraz osobne krzywe phoneme/viseme,
jaw, tongue, emotion i korekt timingowych.
**Eksport pochodny:** klip krzywych/morph targets z audio lub referencją do niego.

## 1. Walidacja WAV i alignment

1. Pracuj na kopii prywatnego nagrania. WAV musi być PCM, mono (albo mieć jawnie
   wybrany kanał), ze stałą częstotliwością próbkowania — preferowane `48 kHz`,
   minimum `16 kHz` dla mowy — i bez clippingu. Zanotuj sample rate, bit depth,
   liczbę próbek i hash.
2. Usuń tylko znany DC offset i kontrolowany szum; nie obcinaj oddechów ani ciszy
   potrzebnej do osi czasu. Peak poniżej `-1 dBFS` jest bezpiecznym punktem
   startowym. Nie normalizuj ponownie po alignmencie.
3. Zweryfikuj transkrypcję z faktyczną wymową, językiem i pauzami. Forced aligner
   uruchom na tym samym pliku WAV, który trafi do eksportu.
4. Alignment przejrzyj na waveform/spektrogramie, szczególnie zwarcia `/p t k/`,
   bilabialne `/p b m/`, szczelinowe i granice pauz. Pewność narzędzia nie
   zastępuje odsłuchu.

## 2. Format timestampów

Kanonicznie zapisuj czas jako całkowite mikrosekundy od początku **niezmienionego
WAV** w półotwartych przedziałach `[start_us, end_us)`, np.:

```json
{"phoneme":"p","start_us":1250000,"end_us":1310000,"confidence":0.94}
```

Wymagaj `0 ≤ start_us < end_us`, porządku rosnącego, braku nakładania na jednej
ścieżce i `end_us ≤ duration_us`. Zachowaj `sample_rate` i opcjonalne indeksy
próbek; klatki są tylko wynikiem eksportu: `frame = time_s × fps`. Nie używaj
float milliseconds jako źródła ani numerów klatek bez jawnego FPS.

## 3. Fonemy, wizemy i artykulatory

Zbuduj wersjonowaną tabelę zależną od języka. Minimalne klasy startowe:

| Fonemy (przykład) | Wizem | Ruch dominujący |
| --- | --- | --- |
| `/p b m/` | `MBP` | pełne zwarcie warg przed uwolnieniem |
| `/f v/` | `FV` | dolna warga do górnych siekaczy |
| `/t d n l/` | `TDNL` | czubek języka za górnymi zębami |
| `/k g/` | `KG` | grzbiet języka ku podniebieniu miękkiemu |
| `/s z/` | `SZ` | wąska szczelina, zęby blisko |
| `/ʃ ʒ tʃ dʒ/` | `SH` | zaokrąglenie/protruzja i szczelina |
| `/i j/` | `I` | szerokie kąciki, małe otwarcie |
| `/e ɛ/` | `E` | średnie otwarcie |
| `/a/` | `A` | duże otwarcie żuchwy i warg |
| `/o ɔ u w/` | `OU` | funnel/pucker zależnie od głoski |
| cisza/pauza | `REST` | kontrolowany powrót, bez nagłego wyzerowania |

Nie rzeźb jednego nieruchomego kształtu na fonem. Wygeneruj zdarzenia wizemów,
a następnie osobne wkłady: lips, `jawOpen`, jaw forward/lateral, tongue tip/mid/
base i policzki. Żuchwa podąża głównie za stopniem otwarcia samogłoski; nie może
być jedynie skutkiem blend shape warg. Język musi czytelnie różnicować `/ta/` od
`/ka/`, nawet jeśli jest tylko częściowo widoczny.

## 4. Koartykulacja i wygładzanie

Koartykulacja wyprzedzająca rozpoczyna przygotowanie następnego wizemu przed jego
fonemem, a podtrzymująca pozwala poprzedniemu wygasać po granicy. Zacznij od
`40–80 ms` wyprzedzenia i `60–120 ms` wygaszenia; skracaj dla zwartych, wydłużaj
dla samogłosek i wolnej mowy. Za mało daje przełączanie shape-by-shape, za dużo
zaciera `/p t k/` i upodabnia sylaby.

Mieszaj sąsiadów ważoną obwiednią, normalizuj antagonistyczne wizemy i ogranicz
wynik do zakresu rigu. Wygładzanie jest filtrem krótkich zmian: okno `20 ms` jest
niskie, `40–60 ms` typowe, `100 ms` wysokie. Małe zachowuje zwarcia, lecz może
jitterować; duże uspokaja samogłoski, lecz opóźnia i usuwa spółgłoski. Stosuj
osobne attack/release i nie filtruj timestampów oraz geometrii drugi raz tym
samym oknem.

Lip seal ma pierwszeństwo przy `/p b m/`, tongue contact przy `/t d n l/`, a
jaw opening przy otwartych samogłoskach. Dodaj corrective shapes rigu po
zmieszaniu podstaw, nie wypalaj ich w krzywe wizemów.

## 5. Miksowanie z emocją

Zachowaj mowę i emocję na osobnych warstwach. Mowa rezerwuje wewnętrzny kontur
warg, zwarcia, żuchwę i język; emocja zachowuje brwi, oczy, policzki i kontrolowany
udział kącików. Przy krytycznym zwarciu chwilowo zmniejsz maskę smile/frown na
wargach, ale nie wyłączaj całej ekspresji. Ogranicz sumę, rozwiąż antagonistów
(`smile`/`frown`, `pucker`/`stretch`) i testuj niski, typowy oraz silny afekt.

## 6. Korekta stałego przesunięcia

Jeżeli wszystkie ruchy wyprzedzają lub opóźniają dźwięk o podobną wartość,
zmierz offset na co najmniej pięciu ostrych zdarzeniach `/p t k/`. Dla każdego
policz `audio_event_us - curve_event_us`, użyj mediany i dodaj ją jako osobną,
niedestrukcyjną wartość `global_offset_us`. Dodatnia wartość opóźnia krzywe w tej
konwencji. Sprawdź początek, środek i koniec. Stały błąd napraw offsetem; błąd
rosnący w czasie oznacza zły sample rate/FPS lub time stretch i wymaga ponownego
alignmentu, nie coraz większego przesunięcia. Offset urządzenia odtwarzającego
zapisuj w profilu runtime, nie w źródłowych timestampach.

## 7. Eksport i testy

Próbkuj dopiero do docelowego FPS, zachowując krzywe źródłowe w czasie. Eksportuj
nazwy kanałów, tangenty/interpolację, zakres, FPS, start time, `global_offset_us`,
wersję tabeli mapowania i referencję/hash WAV. Po imporcie porównaj wartości oraz
czas zdarzeń; nie dołączaj prywatnego audio do publicznego repozytorium.

Obowiązkowe testy:

- **`/pa ta ka/`** w wolnym i normalnym tempie: `/p/` daje pełne zwarcie, `/t/`
  kontakt czubka języka, `/k/` ruch jego grzbietu; każde uwolnienie poprzedza `/a/`.
- **Zdania ciągłe:** co najmniej jedno wolne i jedno szybkie, z bilabialnymi,
  labiodentalnymi, samogłoskami otwartymi i pauzą. Oceniaj z audio, bez audio i
  klatka po klatce, także z emocją oraz blink/gaze.
- **Klip bez dźwięku:** alignment zawiera wyłącznie `REST`, krzywe wracają
  kontrolowanie do neutralu, nie powstają losowe wizemy ani ruch żuchwy. Jeśli
  WAV jest brakujący lub całkowicie niemy, pipeline nie może udawać mowy.
- **Synchronizacja:** minimum pięć zdarzeń na początku/środku/końcu; brak stałego
  offsetu i dryfu po eksporcie.

## Odzyskiwanie

Przy złym wyniku wyłącz kolejno emocję, smoothing, koartykulację, tongue i jaw,
pozostawiając surowe zdarzenia. Najpierw napraw WAV/alignment, potem mapowanie,
obwiednie i dopiero geometrię. Nie przesuwaj pojedynczych kluczy, dopóki nie
wykluczysz globalnego offsetu lub dryfu zegara.

## Checklisty zamknięcia etapu

### Wejście
- [ ] WAV, transkrypcja, język, hash, sample rate i zgoda na dane są zapisane.
- [ ] Facial rig i wersjonowana tabela phoneme→viseme są zatwierdzone.

### Wynik edytowalny
- [ ] Alignment, viseme, jaw, tongue, emotion i `global_offset_us` są osobne.
- [ ] Timestampy pozostają mikrosekundami od oryginalnego WAV, nie klatkami.

### Eksport
- [ ] Nazwy, FPS, start time, tangenty, offset i wersje mapowania są zachowane.
- [ ] Round-trip nie zmienia wartości ani czasów poza zatwierdzoną tolerancją.

### Walidacja
- [ ] `/pa ta ka/`, zdania ciągłe, emocja+mowa i klip niemy przeszły test.
- [ ] Początek, środek i koniec nie wykazują stałego przesunięcia ani dryfu.

### Błędy blokujące
- [ ] Nie ma clippingu audio, złej osi czasu, brakujących zwarć ani losowej mowy w ciszy.
- [ ] Brak skoków, nadmiernego smoothingu, penetracji zębów/języka i konfliktu emocji.

### Definition of Done
- [ ] Od zwalidowanego WAV do eksportu istnieje powtarzalny, wersjonowany i
      edytowalny przepływ; sylaby i zdania są czytelne z dźwiękiem i bez niego,
      cisza pozostaje neutralna, a timing przechodzi round-trip bez blokad.

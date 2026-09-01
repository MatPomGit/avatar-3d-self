# Secondary motion

Ruch wtórny obejmuje włosy, luźne elementy garderoby i wybrane miękkie tkanki. Jest warstwą nakładaną na poprawny primary motion, nie sposobem na maskowanie błędnego skinningu.

## Model bazowy

Domyślnym modelem dla prostych elementów wtórnych jest tłumiony układ drugiego rzędu:

`x'' + 2*zeta*omega_n*x' + omega_n^2*x = omega_n^2*x_target`

gdzie:

- `x` to pozycja/rotacja elementu wtórnego;
- `x_target` to pozycja wynikająca z ruchu ciała;
- `omega_n = 2*pi*f_n`;
- `f_n` to częstotliwość własna;
- `zeta` to współczynnik tłumienia.

Ten model daje przewidywalne zachowanie niezależne od klatek na sekundę, jeśli integrator używa poprawnego `dt`.

## Ogólne baseline

| Element | `f_n` | `zeta` | Maks. opóźnienie fazowe |
| --- | ---: | ---: | ---: |
| krótkie pasma włosów | 4-6 Hz | 0.75-0.95 | 30-60 ms |
| średnie włosy | 2.5-4 Hz | 0.65-0.85 | 50-100 ms |
| długie włosy | 1.2-2.5 Hz | 0.55-0.80 | 80-160 ms |
| luźna tkanina lokalna | 1.5-3 Hz | 0.65-0.90 | 60-130 ms |
| miękkie tkanki | 2-4 Hz | 0.75-1.0 | 40-100 ms |

To wartości startowe dla rig-based dynamics. Silnik fizyczny cloth/hair może używać innych parametrów, ale powinien być kalibrowany do podobnej odpowiedzi czasowej.

## Stabilność

System musi być testowany przy co najmniej:

- 30 FPS;
- 60 FPS;
- 120 FPS;
- jednorazowym hitch 50 ms.

Zmiana FPS nie może znacząco zmieniać amplitudy lub częstotliwości oscylacji.

## Długie włosy

Długie włosy wymagają łańcuchów kości, groom dynamics lub hybrydy.

### Podział

Dla jednej sekcji włosów baseline to:

- 3-6 segmentów dynamicznych;
- pierwszy segment stabilniejszy;
- rosnąca swoboda ku końcówce;
- końcowy segment o najwyższej amplitudzie.

Przykładowy profil udziału dynamiki dla 5 segmentów:

`0.15, 0.30, 0.50, 0.75, 1.00`.

Root nie powinien wykonywać widocznego ruchu względem skóry głowy.

### Limity

Baseline dla długich włosów:

- maksymalna rotacja segmentu względem parent: 15-30°;
- maksymalny stretch: 1.5% długości;
- collision margin: 2-4 mm;
- self-collision tylko, jeśli target i budżet na to pozwalają.

## Broda

Krótka broda zwykle nie wymaga dynamics. Dłuższa broda może otrzymać bardzo subtelny secondary motion.

Baseline:

- `f_n = 4 Hz`;
- `zeta = 0.9`;
- amplituda translacyjna końcówki zwykle <3 mm podczas normalnego ruchu głowy.

Ruch brody nie może wyglądać jak niezależna miękka tkanina.

## Ubrania

Dla dopasowanej odzieży podstawą jest skinning. Dynamics dodajemy tylko do elementów, które rzeczywiście powinny reagować wtórnie, np. luźny dół koszuli, kaptur, pasek, sznurki.

Nie należy stosować symulacji do całego ubrania tylko dlatego, że jest dostępna.

## Miękkie tkanki

Miękkie tkanki wymagają szczególnie małej amplitudy i dobrego tłumienia.

### Model kobiecy: piersi

Jeżeli anatomia modelu i zakres animacji tego wymagają, stosujemy niezależną dynamikę lewej i prawej piersi powiązaną z klatką piersiową.

Baseline dla codziennego ruchu:

- `f_n = 2.2 Hz`;
- `zeta = 0.85`;
- maksymalna dodatkowa translacja pionowa: 6-12 mm;
- maksymalna translacja przód/tył: 4-8 mm;
- maksymalna rotacja lokalna: 3-6°.

Dla biegu parametry mogą być skalowane przez przyspieszenie ciała, ale amplituda pozostaje ograniczona profilem anatomicznym i ubraniem.

Ruch lewej i prawej strony nie powinien być idealnie zsynchronizowany. Dopuszczalna różnica fazy: 10-30 ms i amplitudy 3-8%, o ile nie powoduje widocznej asymetrii w spoczynku.

Ubranie może dodatkowo redukować amplitudę przez `support_factor`:

`A_effective = A_free * (1 - support_factor)`

z `support_factor` w zakresie 0-1. Baseline dla dopasowanej odzieży: `0.6`.

### Inne miękkie tkanki

Subtelny ruch można stosować także do:

- brzucha;
- pośladków;
- luźniejszej tkanki ramion;
- policzków przy gwałtownych ruchach.

Nie tworzymy osobnych systemów, jeśli efekt jest niewidoczny w docelowych ujęciach.

## Sterowanie przez przyspieszenie

Secondary motion powinien reagować na zmianę prędkości parenta, nie na samą pozycję.

Dla prostego sterowania można używać:

`drive = clamp(k_a * a_local + k_w * alpha_local, -drive_max, drive_max)`

gdzie `a_local` to lokalne przyspieszenie liniowe, a `alpha_local` przyspieszenie kątowe.

Sygnał drive należy filtrować dolnoprzepustowo z cutoff 8-12 Hz, aby nie przenosić jitteru trackingu.

## Kolizje

Dla wydajności używamy uproszczonych colliderów:

- głowa;
- szyja;
- barki;
- klatka;
- plecy;
- biodra;
- przedramiona, jeśli długie włosy często z nimi kolidują.

Collider nie może wystawać na tyle, aby odsuwać włosy lub ubranie w spoczynku.

## Wind i środowisko

Wiatr jest osobną warstwą od inercji ruchu ciała.

Baseline idle wind indoors: `0`.

Drobny proceduralny ruch włosów w bezwietrznym pomieszczeniu jest zabroniony, jeśli nie wynika z oddechu lub ruchu głowy.

## Blend z animacją

Waga secondary motion jest znormalizowana 0-1.

- cutscene/close-up: 1.0;
- standard gameplay: 0.7-1.0;
- daleki LOD: 0-0.4;
- teleport/snap: dynamics resetowane, nie pozostawiają długiego oscylowania.

Po dużym skoku pozycji większym niż 0.5 m w jednej klatce system powinien wykonać `reset_to_target`.

## Walidacja

Testy:

1. start i zatrzymanie chodu;
2. obrót tułowia 90°;
3. szybki ruch głowy lewo-prawo;
4. przysiad;
5. bieg lub ruch o dużym przyspieszeniu;
6. nagłe zatrzymanie;
7. 60 s idle.

Fail, jeśli:

- oscylacja nie wygasa;
- element przechodzi przez ciało;
- amplituda rośnie przy spadku FPS;
- występuje jitter w spoczynku;
- ruch jest idealnie sinusoidalny przez długi czas;
- secondary motion dominuje nad primary motion.

## Definition of Done

Secondary motion jest zaliczony, jeśli:

- wszystkie aktywne elementy mają zapisane `f_n`, `zeta` i limity;
- zachowanie jest stabilne przy 30-120 FPS;
- brak penetracji w standardowych ruchach;
- długie włosy zachowują sylwetkę fryzury;
- ruch miękkich tkanek jest subtelny i tłumiony;
- LOD może ograniczać lub wyłączać dynamikę bez popu pozycji.

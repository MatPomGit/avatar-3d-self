# Techniczne wartości bazowe

Ten dokument definiuje domyślne parametry Avatar Studio dla zachowania, animacji, materiałów, układu sterowania postacią (rig) i walidacji. Są to wartości startowe dla zdrowej dorosłej postaci w neutralnym stanie, a nie niezmienne prawa fizjologiczne. Parametry należy zastępować danymi osoby referencyjnej, gdy dostępne są wiarygodne pomiary.

Nazewnictwo jest zgodne ze [słownikiem terminologicznym](terminology.md).

## Zasada strojenia

Każdy parametr ma trzy poziomy:

1. **wartość bazowa (baseline)**: domyślna wartość używana bez danych indywidualnych;
2. **zakres dopuszczalny (range)**: zakres naturalnej lub produkcyjnej zmienności;
3. **profil awatara (profile)**: wartość zmierzona lub ręcznie zatwierdzona dla konkretnej osoby.

Środowisko czasu rzeczywistego (runtime environment) używa profilu awatara (profile), jeśli istnieje, w przeciwnym razie wartości bazowej (baseline).

## Oczy i mruganie

| Parametr | Wartość bazowa (baseline) | Zakres roboczy |
| --- | ---: | ---: |
| spontaniczne mruganie (spontaneous blink rate) | 12/min | 6-20/min |
| minimalny odstęp między mrugnięciami (minimum inter-blink interval) | 1.2 s | 0.8-2.0 s |
| całkowity czas mrugnięcia (blink duration) | 170 ms | 140-240 ms |
| zamknięcie powieki (closing phase) | 55 ms | 40-80 ms |
| faza domknięcia (closed hold) | 20 ms | 0-40 ms |
| otwarcie powieki (opening phase) | 95 ms | 70-140 ms |
| asymetria lewa/prawa (left-right asymmetry) | 8 ms | 0-20 ms |

Dla częstości mrugania `BR` wyrażonej w mrugnięciach na minutę średni odstęp wynosi:

`T_mean = 60 / BR`.

Dla `BR = 12/min` otrzymujemy `T_mean = 5 s`. Mrugnięć nie generujemy jednak okresowo. Interwał losujemy z przesuniętego rozkładu gamma (shifted gamma distribution):

`T = T_min + Gamma(k=2, theta=(T_mean-T_min)/2)`

z końcowym ograniczeniem do 1.2-12 s. Podwójne mrugnięcie (double blink) jest dozwolone sporadycznie, z odstępem 180-350 ms, ale nie częściej niż około 3% zdarzeń w neutralnej animacji bezczynności (idle animation).

Modyfikatory kontekstu: czytanie i intensywna obserwacja `0.55-0.8 × BR`, swobodna rozmowa `0.9-1.25 × BR`, zmęczenie `1.15-1.5 × BR`.

## Sakkady i fiksacje wzroku

Dla sakkady (saccade) o amplitudzie `A` w stopniach przyjmujemy dla typowych ruchów do 20°:

`T_saccade_ms = clamp(25 + 2.5*A, 30, 90)`.

Jest to praktyczna aproksymacja zależności amplitudy, czasu trwania i prędkości sakkady (saccadic main sequence). Ruch powinien używać profilu minimalizującego szarpnięcie (minimum-jerk trajectory) albo równoważnej krzywej o pojedynczym maksimum prędkości, a nie interpolacji liniowej.

| Parametr | Wartość bazowa (baseline) |
| --- | ---: |
| typowa sakkada dialogowa (conversational saccade) | 2-12° |
| duża sakkada oka (large eye saccade) | 12-20° |
| mikrosakkada (microsaccade) | 0.1-0.6° |
| częstość widocznych mikrosakkad (visible microsaccade rate) | 0.4-1.2 Hz |
| fiksacja na obiekcie (object fixation) | 220-650 ms |
| fiksacja na twarzy rozmówcy (face fixation) | 0.7-2.5 s |
| krótkie odwrócenie wzroku (gaze aversion) | 0.2-1.1 s |

Powyżej około 25-30° preferowany jest współruch głowy (head contribution). Oczy nie powinny długo utrzymywać skrajnego wychylenia.

## Powieki i spojrzenie

Powieka górna powinna podążać za pionowym ruchem oka. Jako wartość bazową przyjmujemy współczynnik śledzenia powieki za ruchem oka (eyelid follow) `0.35`. Dla spojrzenia w dół można zwiększyć go do `0.45`.

## Oddychanie i animacja bezczynności

| Parametr | Wartość bazowa (baseline) | Zakres |
| --- | ---: | ---: |
| częstość oddechu (breathing rate) | 14/min | 10-20/min |
| częstotliwość oddechu (breathing frequency) | 0.233 Hz | 0.17-0.33 Hz |
| ruch klatki piersiowej (chest excursion) | 4 mm | 2-8 mm |
| ruch barków od oddechu (shoulder breathing motion) | 0.35° | 0.1-0.8° |
| wolne kołysanie posturalne (postural sway) | 0.18 Hz | 0.08-0.35 Hz |
| translacja kołysania (sway translation) | 4 mm | 1-10 mm |
| rotacja tułowia (torso sway rotation) | 0.25° | 0.1-0.7° |

Oddychanie nie może być idealną sinusoidą. Zalecany jest lekko asymetryczny cykl: wdech około 42%, wydech około 58% okresu, z modulacją amplitudy ±10% i okresu ±8%.

## Mikroruchy głowy

Podczas słuchania i mowy dodajemy niewielkie korekty orientacji. Typowy pojedynczy ruch to 0.3-2.0° z czasem 250-900 ms. W neutralnej animacji bezczynności (idle animation) nie powinno być więcej niż 2-5 czytelnych korekt na 10 s. Proceduralne drżenie (procedural jitter) poniżej 0.1° należy filtrować, ponieważ wygląda jak błąd śledzenia (tracking error).

## Emocje

Wagi ekspresji są znormalizowane do 0-1. Domyślna ekspresja konwersacyjna zwykle pozostaje w zakresie 0.1-0.55. Wartości 0.8-1.0 są zarezerwowane dla wyraźnej fazy maksymalnego nasilenia (apex).

| Faza | Czas bazowy |
| --- | ---: |
| czas narastania (onset time) | 250 ms |
| utrzymanie maksimum (apex hold) | 700 ms |
| czas wygaszania (offset time) | 450 ms |

Asymetria lewej i prawej strony: losowe 5-12% amplitudy dla naturalnej ekspresji. Nie stosujemy asymetrii do każdego klucza kształtu (shape key) osobno, lecz do semantycznych grup mięśniowych.

## Synchronizacja ruchu ust z mową

Wartość bazowa wizualnego wyprzedzenia artykulacji względem dźwięku (visual speech lead) wynosi 60 ms. Dozwolony zakres to 40-100 ms zależnie od fonemu.

Dla każdego wizemu (viseme) tworzymy krzywą z:

- wyprzedzającym narastaniem (anticipatory attack): 50-80 ms;
- pełnym celem w pobliżu środka fonemu;
- wygaszaniem (release): 80-120 ms;
- nakładaniem z sąsiednim wizemem (viseme overlap).

Jeżeli suma wag konkurujących wizemów przekracza 1.0, stosujemy normalizację grupy. Kanał anatomiczny `jawOpen` pozostaje rozpatrywany osobno. Spółgłoski `/p b m/` muszą uzyskać rzeczywiste domknięcie warg (lip closure), a `/f v/` kontakt dolnej wargi z górnymi zębami.

## Renderowanie oparte na fizyce i skóra

Skóra jest dielektrykiem:

| Parametr | Wartość bazowa (baseline) | Zakres strojenia |
| --- | ---: | ---: |
| metaliczność (metallic) | 0 | 0 |
| współczynnik załamania światła skóry (Index of Refraction, IOR) | 1.40 | 1.38-1.45 |
| współczynnik odbicia Fresnela dla padania prostopadłego (normal-incidence Fresnel reflectance, F0) | 0.028 | wynik z IOR |
| chropowatość czoła (roughness) | 0.38 | 0.30-0.48 |
| chropowatość strefy T (roughness) | 0.34 | 0.26-0.44 |
| chropowatość policzków (roughness) | 0.48 | 0.38-0.60 |
| chropowatość okolic oczu (roughness) | 0.52 | 0.42-0.64 |

Dla fizycznie skalowanego rozpraszania podpowierzchniowego (Subsurface Scattering, SSS) przyjmujemy początkowy efektywny promień rozpraszania RGB (effective scattering radius):

`[1.2, 0.55, 0.25] mm`.

Wartości służą wyłącznie jako punkt startowy. Ostateczne parametry wynikają z porównania z referencją w świetle przednim (front light), bocznym (side light) i tylnym (backlight).

## Oko

| Parametr | Wartość bazowa (baseline) | Zakres |
| --- | ---: | ---: |
| średnica gałki ocznej | 24.0 mm | 23-25 mm |
| średnica tęczówki | 11.8 mm | 11-12.5 mm |
| źrenica neutralna | 3.5 mm | 2-5 mm |
| dynamiczny zakres źrenicy | 2-8 mm | profil osoby/światła |
| współczynnik załamania światła rogówki (Index of Refraction, IOR) | 1.376 | 1.37-1.38 |
| współczynnik załamania światła łez (Index of Refraction, IOR) | 1.336 | 1.33-1.34 |
| chropowatość rogówki (roughness) | 0.02 | 0.01-0.04 |

Stała czasowa zwężania źrenicy (pupil constriction time constant) wynosi bazowo `0.6 s`, a rozszerzania (pupil dilation) `1.2 s`. Bez danych o luminancji źrenica pozostaje stabilna.

## System włosów

Wartości bazowe dla systemu włosów (groom):

| Parametr | Wartość bazowa (baseline) | Zakres |
| --- | ---: | ---: |
| średnica włosa | 70 µm | 50-100 µm |
| prowadnice włosów LOD0 (guide strands) | 800-1500 | zależnie od fryzury |
| włosy renderowane LOD0 (render strands) | 60k-120k | zależnie od środowiska docelowego |
| pojedyncze odstające włosy (flyaway hairs) | 0.5-2% | 0-3% |
| margines kolizji (collision margin) | 3 mm | 2-4 mm |

Redukcja systemu włosów dla kolejnych poziomów szczegółowości (LOD) wynosi orientacyjnie 100%, 60%, 30% i 10-15% lub przejście na płaszczyzny z teksturą włosów (hair cards).

## Szkielet

Kanoniczną pozą spoczynkową (rest pose) jest A-pose. Wartość bazowa odwiedzenia ramion: 35-45°.

Dla profilu fotorealistycznego kości skrętne (twist bones) są domyślnie zalecane dla ramion, przedramion i ud. Rozciąganie w kinematyce odwrotnej (IK stretch) pozostaje wyłączone.

Zakresy testowe:

- zgięcie barku (shoulder flexion): 160°;
- odwiedzenie barku (shoulder abduction): 150°;
- zgięcie łokcia (elbow flexion): 145°;
- pronacja i supinacja przedramienia (forearm pronation/supination): około ±80°;
- zgięcie biodra (hip flexion): 120°;
- zgięcie kolana (knee flexion): 135°.

## Układ sterowania twarzą

Interfejs ARKit używa zakresu 0-1. Wartość `1` oznacza zatwierdzone maksimum danego kanału.

Wartości bazowe dla żuchwy (jaw/mandible):

- pełne otwarcie: 30-35 mm;
- rotacja: około 25-30°;
- przesunięcie boczne (lateral translation): 5-8 mm;
- wysunięcie do przodu (forward translation): 4-7 mm.

Domknięcie warg (lip seal): pełna siła do `jawOpen=0.08`, wygaszenie do zera przy `jawOpen≈0.22`.

Śledzenie powieki za ruchem oka (eyelid follow):

- spojrzenie w górę (look up): 0.30-0.35;
- spojrzenie w dół (look down): 0.40-0.45.

Kształt korekcyjny (corrective shape) dla pary kanałów może używać:

`w_corrective = smoothstep(0.15, 0.55, w_A * w_B)`.

## Ruch wtórny

Kanoniczny model ruchu wtórnego (secondary motion) opisujemy równaniem drugiego rzędu:

`x'' + 2*zeta*omega_n*x' + omega_n^2*x = omega_n^2*x_target`

z `omega_n = 2*pi*f_n`.

| Element | częstotliwość własna `f_n` (natural frequency) | współczynnik tłumienia `zeta` (damping ratio) |
| --- | ---: | ---: |
| krótkie włosy | 4-6 Hz | 0.75-0.95 |
| średnie włosy | 2.5-4 Hz | 0.65-0.85 |
| długie włosy | 1.2-2.5 Hz | 0.55-0.80 |
| luźna tkanina | 1.5-3 Hz | 0.65-0.90 |
| miękkie tkanki | 2-4 Hz | 0.75-1.0 |

Dla modelu kobiecego, jeśli wymagana jest niezależna dynamika wtórna piersi (breast secondary motion), wartość bazowa wynosi `f_n=2.2 Hz`, `zeta=0.85`, z ograniczoną amplitudą wynikającą z anatomii i podparcia przez ubranie.

## Samodzielna sesja z obracającą się osobą

Wariant osoby obracającej się przed kamerą (rotating-subject capture) jest wspieranym procesem dla samodzielnego fotografowania sylwetki.

Wartości bazowe:

- krok kątowy (angular step): 10°;
- 36 pozycji na 360°;
- czas stabilizacji po obrocie (settling time): 2 s;
- minimum dwa poziomy aparatu, preferowane trzy;
- obowiązkowa segmentacja pierwszego planu (foreground segmentation);
- pełny obrót wykonywany całym ciałem razem ze stopami;
- skala nadawana z co najmniej trzech rzeczywistych pomiarów.

## Budżet środowiska czasu rzeczywistego

Pierwszy profil komputerowy zakłada 60 kl./s (frames per second, FPS) i budżet `16.67 ms` na klatkę (frame).

- obliczenia animacji i twarzy na CPU (CPU animation and facial evaluation): `<= 2.0 ms`;
- renderowanie całej postaci na GPU (character rendering): `<= 8.0 ms` w scenie testowej;
- silnik, pozostała scena i margines: `>= 6.67 ms`;
- 99. percentyl czasu klatki (p99 frame time): `<= 33.3 ms` podczas testu 60 s.

Budżety są mierzone na zadeklarowanym sprzęcie referencyjnym i nie są przenoszone bezpośrednio między silnikami.

## Wersjonowanie

Zmiana wartości bazowej (baseline), która wpływa na wygląd lub zachowanie w środowisku czasu rzeczywistego (runtime environment), wymaga odnotowania w historii zmian i raporcie projektu Avatar Studio.
# Techniczne wartości bazowe

Ten dokument definiuje domyślne parametry Avatar Studio dla zachowania, animacji, materiałów, rigu i walidacji. Są to wartości startowe dla zdrowej dorosłej postaci w neutralnym stanie, a nie niezmienne prawa fizjologiczne. Parametry powinny być nadpisywane danymi osoby referencyjnej, jeśli dostępne są wiarygodne pomiary.

## Zasada strojenia

Każdy parametr ma trzy poziomy:

1. `baseline`: wartość domyślna używana bez danych osobowych;
2. `range`: dopuszczalny zakres naturalnej lub produkcyjnej zmienności;
3. `profile`: wartość zmierzona lub ręcznie zatwierdzona dla konkretnego awatara.

Runtime używa `profile`, jeśli istnieje, w przeciwnym razie `baseline`.

## Oczy i mruganie

| Parametr | Baseline | Zakres roboczy |
| --- | ---: | ---: |
| spontaniczne mruganie | 12/min | 6-20/min |
| minimalny odstęp między blinkami | 1.2 s | 0.8-2.0 s |
| pełny czas blink | 170 ms | 140-240 ms |
| zamknięcie powieki | 55 ms | 40-80 ms |
| faza domknięcia | 20 ms | 0-40 ms |
| otwarcie powieki | 95 ms | 70-140 ms |
| asymetria L/R | 8 ms | 0-20 ms |

Dla częstości `BR` w blinkach na minutę średni odstęp wynosi:

`T_mean = 60 / BR`.

Dla baseline `BR = 12/min`, `T_mean = 5 s`. Nie wolno jednak generować blinków co 5 sekund. Interwał losujemy z przesuniętego rozkładu gamma:

`T = T_min + Gamma(k=2, theta=(T_mean-T_min)/2)`

z końcowym ograniczeniem do 1.2-12 s. Po długim interwale prawdopodobieństwo kolejnego blinku może wzrosnąć. Podwójne mrugnięcie jest dozwolone sporadycznie, z odstępem 180-350 ms, ale nie częściej niż około 3% zdarzeń w neutralnym idle.

Modyfikatory kontekstu: czytanie i intensywna obserwacja `0.55-0.8 × BR`, swobodna rozmowa `0.9-1.25 × BR`, zmęczenie `1.15-1.5 × BR`. Modyfikator nie może powodować regularności.

## Sakkady i fiksacje

Dla sakkady o amplitudzie `A` w stopniach przyjmujemy dla typowych ruchów do 20°:

`T_saccade_ms = clamp(25 + 2.5*A, 30, 90)`.

Jest to praktyczna aproksymacja fizjologicznej main sequence. Ruch powinien używać profilu minimum-jerk albo równoważnej krzywej o pojedynczym maksimum prędkości, nie liniowej interpolacji.

| Parametr | Baseline |
| --- | ---: |
| typowa sakkada dialogowa | 2-12° |
| duża sakkada oka | 12-20° |
| mikrosakkada | 0.1-0.6° |
| widoczna mikrosakkada | 0.4-1.2 Hz |
| fiksacja na obiekcie | 220-650 ms |
| fiksacja na twarzy rozmówcy | 0.7-2.5 s |
| krótkie odwrócenie wzroku | 0.2-1.1 s |

Powyżej około 25-30° preferowany jest współruch głowy. Oczy nie powinny długo utrzymywać skrajnego wychylenia.

## Powieki i spojrzenie

Powieka górna powinna podążać za pionowym ruchem oka. Jako baseline przyjmujemy `eyelid_follow = 0.35`, czyli około 35% znormalizowanego pionowego wychylenia oka jest kompensowane zmianą pozycji powieki. Dla spojrzenia w dół można zwiększyć współczynnik do 0.45.

## Oddychanie i idle

| Parametr | Baseline | Zakres |
| --- | ---: | ---: |
| oddechy | 14/min | 10-20/min |
| częstotliwość oddechu | 0.233 Hz | 0.17-0.33 Hz |
| ruch klatki | 4 mm | 2-8 mm |
| ruch barków od oddechu | 0.35° | 0.1-0.8° |
| wolny postural sway | 0.18 Hz | 0.08-0.35 Hz |
| translacja sway | 4 mm | 1-10 mm |
| rotacja tułowia sway | 0.25° | 0.1-0.7° |

Oddychanie nie może być idealną sinusoidą. Zalecany jest lekko asymetryczny cykl: wdech około 42%, wydech około 58% okresu, z modulacją amplitudy ±10% i okresu ±8%.

## Mikroruchy głowy

Podczas słuchania i mowy dodajemy niewielkie korekty orientacji. Typowy pojedynczy ruch to 0.3-2.0° z czasem 250-900 ms. W neutralnym idle nie powinno być więcej niż 2-5 czytelnych korekt na 10 s. Drobny jitter proceduralny poniżej 0.1° należy filtrować, ponieważ wygląda jak błąd trackingu.

## Emocje

Wagi ekspresji są znormalizowane do 0-1. Domyślna ekspresja konwersacyjna powinna zwykle pozostawać w zakresie 0.1-0.55. Wartości 0.8-1.0 są zarezerwowane dla wyraźnego apexu.

| Faza | Czas baseline |
| --- | ---: |
| onset | 250 ms |
| apex hold | 700 ms |
| offset | 450 ms |

Asymetria lewej i prawej strony: losowe 5-12% amplitudy dla ekspresji naturalnej. Nie stosujemy asymetrii do każdego shape key osobno, lecz do semantycznych grup mięśniowych.

## Lip-sync i koartykulacja

Baseline wizualnego wyprzedzenia artykulacji względem audio: 60 ms. Dozwolony zakres to 40-100 ms zależnie od fonemu.

Dla każdego celu viseme tworzymy krzywą z:

- anticipatory attack 50-80 ms;
- pełnym celem w pobliżu centrum fonemu;
- release 80-120 ms;
- overlap z sąsiednim viseme.

Jeżeli suma wag konkurujących visemów przekracza 1.0, stosujemy normalizację grupy, ale `jawOpen` jest traktowany osobno jako kanał anatomiczny. Spółgłoski zwarte `/p b m/` muszą uzyskać rzeczywiste domknięcie warg, a `/f v/` kontakt dolnej wargi z górnymi zębami.

## PBR i skóra

Skóra jest dielektrykiem:

| Parametr | Baseline | Zakres strojenia |
| --- | ---: | ---: |
| metallic | 0 | 0 |
| IOR skóry | 1.40 | 1.38-1.45 |
| Fresnel F0 dla IOR 1.40 | 0.028 | wynik z IOR |
| roughness czoła | 0.38 | 0.30-0.48 |
| roughness T-zone | 0.34 | 0.26-0.44 |
| roughness policzków | 0.48 | 0.38-0.60 |
| roughness okolic oczu | 0.52 | 0.42-0.64 |

Dla fizycznie skalowanego SSS przyjmujemy początkowy efektywny radius RGB:

`[1.2, 0.55, 0.25] mm`.

Wartości te służą wyłącznie jako start strojenia. Ostateczna wartość ma wynikać z porównania z referencją w świetle frontalnym, bocznym i backlight.

## Oko

| Parametr | Baseline | Zakres |
| --- | ---: | ---: |
| średnica gałki ocznej | 24.0 mm | 23-25 mm |
| średnica tęczówki | 11.8 mm | 11-12.5 mm |
| źrenica neutralna | 3.5 mm | 2-5 mm |
| dynamiczny zakres źrenicy | 2-8 mm | profil osoby/światła |
| IOR rogówki | 1.376 | 1.37-1.38 |
| IOR łez/cieczy | 1.336 | 1.33-1.34 |
| roughness rogówki | 0.02 | 0.01-0.04 |

Pupil constriction ma baseline time constant 0.6 s, a dilation 1.2 s. W braku danych o luminancji źrenica pozostaje stabilna.

## Groom

Baseline dla włosów głowy:

| Parametr | Baseline | Zakres |
| --- | ---: | ---: |
| średnica włosa | 70 µm | 50-100 µm |
| guides LOD0 | 800-1500 | zależnie od fryzury |
| render strands LOD0 | 60k-120k | zależnie od targetu |
| flyaways | 0.5-2% | 0-3% |
| collision margin | 3 mm | 2-4 mm |

LOD groomu: około 100%, 60%, 30%, 10-15%/cards.

## Skeleton

Kanoniczny rest pose to A-pose. Baseline odwiedzenia ramion: 35-45°.

Dla profilu fotorealistycznego twist bones są domyślnie zalecane dla ramion, przedramion i ud. Stretch IK jest wyłączony.

Testowe zakresy:

- shoulder flexion 160°;
- shoulder abduction 150°;
- elbow flexion 145°;
- forearm pronation/supination około ±80°;
- hip flexion 120°;
- knee flexion 135°.

## Facial rig

ARKit interface używa zakresu 0-1. `1` oznacza zatwierdzone maksimum danego kanału.

Baseline jaw:

- pełne otwarcie: 30-35 mm;
- rotacja około 25-30°;
- lateral translation 5-8 mm;
- forward 4-7 mm.

Lip seal: pełna siła do `jawOpen=0.08`, wygaszenie do zera przy `jawOpen≈0.22`.

Eyelid follow:

- look up: 0.30-0.35;
- look down: 0.40-0.45.

Corrective dla pary kanałów może używać:

`w_corrective = smoothstep(0.15, 0.55, w_A * w_B)`.

## Secondary motion

Kanoniczny model:

`x'' + 2*zeta*omega_n*x' + omega_n^2*x = omega_n^2*x_target`

z `omega_n = 2*pi*f_n`.

Baseline:

| Element | `f_n` | `zeta` |
| --- | ---: | ---: |
| krótkie włosy | 4-6 Hz | 0.75-0.95 |
| średnie włosy | 2.5-4 Hz | 0.65-0.85 |
| długie włosy | 1.2-2.5 Hz | 0.55-0.80 |
| luźna tkanina | 1.5-3 Hz | 0.65-0.90 |
| miękkie tkanki | 2-4 Hz | 0.75-1.0 |

Dla modelu kobiecego, jeśli wymagany jest niezależny secondary motion piersi, baseline to `f_n=2.2 Hz`, `zeta=0.85`, z ograniczoną amplitudą wynikającą z anatomii i podparcia ubraniem.

## Self-capture z obracającą się osobą

Wariant `rotating_subject` jest wspieranym workflow dla samodzielnego capture sylwetki.

Baseline:

- krok 10°;
- 36 pozycji na 360°;
- opóźnienie po obrocie 2 s;
- minimum dwa poziomy aparatu, preferowane trzy;
- obowiązkowa segmentacja foreground;
- pełny obrót wykonywany całym ciałem razem ze stopami;
- skala nadawana z co najmniej trzech rzeczywistych pomiarów.

## Runtime baseline

Pierwszy profil desktopowy zakłada 60 FPS i budżet 16.67 ms/frame. Docelowo:

- CPU animation + facial evaluation: <= 2.0 ms;
- rendering całej postaci na GPU: <= 8.0 ms w scenie testowej;
- reszta klatki, silnik i margines: >= 6.67 ms;
- brak pojedynczych skoków powyżej 33.3 ms w 99. percentylu podczas testu 60 s.

Budżety są mierzone na zadeklarowanym sprzęcie referencyjnym i nie są przenoszone bezpośrednio między silnikami.

## Wersjonowanie

Zmiana baseline, która wpływa na wygląd lub zachowanie runtime, wymaga odnotowania w changelogu dokumentacji i w raporcie projektu Avatar Studio.

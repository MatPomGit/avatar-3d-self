# Techniczne wartości bazowe

Ten dokument definiuje domyślne parametry Avatar Studio dla zachowania, animacji i walidacji. Są to wartości startowe dla zdrowej dorosłej postaci w neutralnym stanie, a nie niezmienne prawa fizjologiczne. Parametry powinny być nadpisywane danymi osoby referencyjnej, jeśli dostępne są wiarygodne pomiary.

## Zasada strojenia

Każdy parametr ma trzy poziomy:

1. `baseline`: wartość domyślna używana bez danych osobowych;
2. `range`: dopuszczalny zakres naturalnej zmienności;
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

## Runtime baseline

Pierwszy profil desktopowy zakłada 60 FPS i budżet 16.67 ms/frame. Docelowo:

- CPU animation + facial evaluation: <= 2.0 ms;
- rendering całej postaci na GPU: <= 8.0 ms w scenie testowej;
- reszta klatki, silnik i margines: >= 6.67 ms;
- brak pojedynczych skoków powyżej 33.3 ms w 99. percentylu podczas testu 60 s.

Budżety są mierzone na zadeklarowanym sprzęcie referencyjnym i nie są przenoszone bezpośrednio między silnikami.

## Wersjonowanie

Zmiana baseline, która wpływa na wygląd lub zachowanie runtime, wymaga odnotowania w changelogu dokumentacji i w raporcie projektu Avatar Studio.
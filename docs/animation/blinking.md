# Mruganie

Mruganie jest osobną warstwą proceduralną, ale pozostaje zależne od spojrzenia, mowy, emocji i stanu uwagi. Nie używamy periodycznego timera.

## Generator

Neutralny baseline wynosi 12 blinków/min. Średni interwał `T_mean = 60/BR`, ale rzeczywisty interwał jest losowany z przesuniętego rozkładu gamma opisanego w [technicznych wartościach bazowych](../project/technical-baselines.md).

Dla `BR=12/min` średnia wynosi 5 s, przy minimalnym odstępie 1.2 s. Wartości są ograniczane do 12 s, chyba że stan postaci jawnie wymaga dłuższej stabilizacji wzroku.

## Profil pojedynczego blinku

Domyślny czas całkowity: 170 ms:

1. closing: 55 ms;
2. closed/near-closed: 20 ms;
3. opening: 95 ms.

Otwarcie jest wolniejsze od zamknięcia. Używamy krzywych ease-in/ease-out bez odbicia. Lewa i prawa powieka mogą różnić się początkiem o 0-20 ms i amplitudą o 0-5%.

## Typy

- normal blink: pełne zamknięcie 0.95-1.0;
- soft blink: 0.75-0.9, około 15% spontanicznych zdarzeń;
- double blink: drugi blink po 180-350 ms, maksymalnie około 3% neutralnych zdarzeń;
- deliberate blink: animacja sterowana stanem, nie generatorem spontanicznym.

## Zależności

Generator zmniejsza częstość podczas intensywnej obserwacji i zwiększa ją przy zmęczeniu. Blink można zsynchronizować z zakończeniem sakkady, zmianą tury dialogowej lub krótkim odwróceniem głowy. Nie wolno jednak synchronizować każdego blinku z tym samym typem zdarzenia.

Podczas blinku rogówka i gałka oczna nie znikają, a powieka ma ślizgać się po geometrii oka. Rzęsy podążają za powieką.

## Walidacja

Klip 60 s w neutralnym idle powinien zawierać statystycznie nieregularne odstępy, brak mechanicznej periodyczności, brak clippingu i brak identycznych podwójnych blinków. Testujemy również 30 s mowy i 30 s intensywnego gaze target.
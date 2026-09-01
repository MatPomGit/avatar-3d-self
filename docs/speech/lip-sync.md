# Synchronizacja ruchu ust z mową (lip-sync)

**Synchronizacja ruchu ust z mową (lip-sync)** polega na takim sterowaniu ustami, żuchwą i językiem, aby widoczna artykulacja odpowiadała fonemom w nagraniu. Avatar Studio generuje ten ruch z czasów fonemów, a nie wyłącznie z amplitudy sygnału dźwiękowego. Głośność może modulować energię ruchu, ale sama nie określa prawidłowego kształtu ust.

Najważniejszym parametrem czasowym jest przesunięcie widocznej artykulacji względem dźwięku. Jeśli usta reagują zbyt późno, widz odbiera mowę jako opóźnioną. Jeśli ruch wyprzedza dźwięk zbyt mocno, awatar wygląda tak, jakby „zgadywał” słowo przed jego wypowiedzeniem.

Typowe wartości wyprzedzenia:

- 0-20 ms: praktycznie brak wyprzedzenia, często zbyt mało dla naturalnej artykulacji;
- 40-70 ms: typowy zakres dla neutralnej mowy;
- 70-100 ms: przydatny dla spółgłosek wymagających przygotowania warg, np. `/p b m/`;
- ponad 120 ms: zwykle zbyt duże wyprzedzenie i ryzyko widocznego rozjazdu z dźwiękiem.

## Oś czasu

Dla fonemu `p_i` znamy czas początku `t_start`, czas końca `t_end` oraz poziom pewności dopasowania (confidence). Centrum fonemu wyznaczamy jako:

`t_center = (t_start + t_end) / 2`.

Domyślny cel wizualny jest przesuwany o 60 ms przed dźwięk:

`t_visual = t_center - 0.060 s`.

Wartość bazowa 60 ms jest kompromisem między czytelnością ruchu a naturalnością. Dopuszczalny zakres wynosi 40-100 ms. Dla spółgłosek dwuwargowych `/p b m/` preferujemy 70-90 ms wyprzedzenia, ponieważ pełne domknięcie warg musi pojawić się jeszcze przed akustycznym uwolnieniem spółgłoski.

## Krzywa narastania i wygaszania

Każdy wizem otrzymuje **czas narastania (attack time)** i **czas wygaszania (release time)**. Parametry te określają, jak szybko twarz dochodzi do docelowego kształtu i jak szybko z niego wychodzi.

Przykładowo:

- narastanie 20-30 ms daje bardzo gwałtowny ruch, odpowiedni tylko dla części szybkich zwarć;
- 50-80 ms daje naturalne przejście w neutralnej mowie;
- ponad 100 ms daje ruch miękki, ale może zacierać różnice między szybkimi fonemami;
- wygaszanie 50-70 ms daje szybkie przejście do kolejnego kształtu;
- 80-120 ms jest zakresem bazowym;
- ponad 150 ms może powodować „ciągnięcie się” poprzedniego wizemu.

Zamiast trójkąta liniowego używamy krzywej ciągłej klasy C1 (C1-continuous), np. sześciennej funkcji płynnego przejścia (cubic smoothstep). Dzięki temu prędkość ruchu nie zmienia się skokowo.

Jeżeli dwa cele nachodzą na siebie, wagi są mieszane w ramach koartykulacji. Grupy wzajemnie wykluczające się, jak `mouthPucker` i silny `mouthStretch`, są normalizowane.

## Żuchwa

Kanał `jawOpen` opisuje otwarcie żuchwy. Jego wartość wynika przede wszystkim z otwartości fonemu i samogłoski, a nie z poziomu głośności.

W praktyce:

- `jawOpen ≈ 0.0-0.1`: usta niemal zamknięte, typowe dla `/m/`, `/p/` przed uwolnieniem lub neutralnej pozy;
- `0.2-0.4`: małe lub umiarkowane otwarcie, np. część spółgłosek i samogłosek przednich;
- `0.45-0.7`: wyraźne otwarcie typowe dla wielu samogłosek;
- `0.7-1.0`: duże otwarcie, stosowane dla silnie akcentowanych otwartych samogłosek lub ekspresyjnej mowy.

Pełny zakres `0-1` jest znormalizowany i nie oznacza konkretnej odległości w milimetrach bez profilu konkretnej postaci. Żuchwa ma bezwładność: maksymalna zmiana z 0 do 1 nie może zachodzić w jednej klatce, nawet przy błędnym dopasowaniu czasowym.

## Artykulacje kontaktowe

Niektóre fonemy wymagają rzeczywistego kontaktu geometrycznego. Są one ważniejsze niż samo wygładzenie krzywej.

- `PP`: usta muszą osiągnąć pełne domknięcie;
- `FF`: dolna warga powinna zetknąć się lub bardzo zbliżyć do górnych siekaczy;
- `SS`: szczelina między zębami i ustami pozostaje wąska.

Jeśli wygładzanie uniemożliwia spełnienie tych warunków, należy zmniejszyć nakładanie koartykulacyjne albo lokalnie zwiększyć amplitudę wizemu.

## Pewność dopasowania czasowego (alignment confidence)

**Pewność dopasowania czasowego (alignment confidence)** opisuje, jak wiarygodnie narzędzie dopasowało fonem do konkretnego fragmentu nagrania. Niska wartość nie oznacza automatycznie, że fonem jest nieobecny. Może wynikać z hałasu, szybkiej mowy, nietypowej wymowy lub błędu modelu.

Przykładowa interpretacja znormalizowanego wyniku 0-1, jeśli użyty aligner taki zakres udostępnia:

- `0.8-1.0`: wysokie zaufanie, można stosować zwykłe czasy i amplitudy;
- `0.5-0.8`: wynik użyteczny, ale warto zwiększyć wygładzanie;
- `0.3-0.5`: fragment wymaga ostrożności i większego wykorzystania kontekstu sąsiednich fonemów;
- `<0.3`: kandydat do ręcznej kontroli w Avatar Studio.

Dokładne progi zależą od alignera i nie mogą być bezpośrednio przenoszone między różnymi modelami bez kalibracji.

## Test synchronizacji

Akceptowalny pipeline powinien utrzymywać poprawne wyprzedzenie wizualne bez systematycznego opóźnienia. Testujemy wolną, neutralną i szybką mowę, liczby, nazwy własne oraz sekwencje `/pa-ta-ka/`.

Wynik oceniamy:

1. z dźwiękiem, aby sprawdzić subiektywną synchronizację;
2. bez dźwięku, aby sprawdzić czy artykulacja pozostaje czytelna wizualnie;
3. w zwolnionym tempie, aby wykryć pominięte domknięcia, skoki i nadmierne nakładanie koartykulacyjne.
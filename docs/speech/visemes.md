# Wizemy

Avatar Studio używa niewielkiego zestawu wizualnych klas artykulacyjnych, a nie osobnego klucza kształtu (shape key) dla każdego fonemu. **Fonem (phoneme)** jest jednostką dźwiękową mowy, natomiast **wizem (viseme)** opisuje widoczny układ ust, żuchwy i częściowo języka odpowiadający jednej lub kilku głoskom.

Zmiana wizemu wpływa bezpośrednio na to, jaki kształt przyjmują usta podczas mówienia. Zbyt mała amplituda daje efekt niewyraźnej, „zamkniętej” mowy. Zbyt duża powoduje przerysowane ruchy ust i efekt animacji kreskówkowej. Dlatego wartości wizemów są skalowane przez czas trwania fonemu, akcent i kontekst sąsiednich dźwięków.

## Kanoniczny zestaw

| Wizem | Przykładowe fonemy | Dominujący ruch |
| --- | --- | --- |
| SIL | cisza | neutralne usta |
| PP | p, b, m | pełne domknięcie warg |
| FF | f, v | dolna warga do górnych zębów |
| TH | th | język między lub blisko zębów, opcjonalne dla EN |
| DD | t, d, n, l | przedni język, lekko otwarte usta |
| KK | k, g, h | tylna artykulacja, pośredni kształt ust |
| CH | ch, j, sh, zh | zwężenie i lekkie wysunięcie |
| SS | s, z | wąska szczelina, zęby blisko |
| RR | r | zależne od języka, zwykle otwarcie średnie |
| AA | a | szerokie otwarcie żuchwy |
| E | e | usta szerzej, umiarkowane otwarcie |
| I | i, y | szerokie kąciki, małe otwarcie |
| O | o | zaokrąglenie |
| U | u | silniejsze wysunięcie i zaokrąglenie warg |

Polski profil pomija `TH` w zwykłych wypowiedziach, ale zachowuje klasę dla mowy angielskiej.

## Reprezentacja

Wizem jest wektorem kanałów, np. `jawOpen`, `mouthFunnel`, `mouthPucker`, `mouthClose`, `mouthStretchLeft/Right`, `mouthPress` i `tongue`. Nie należy tworzyć jednego monolitycznego celu morfowania (morph target), jeśli może on konfliktować z emocją.

## Koartykulacja

**Koartykulacja (coarticulation)** oznacza, że układ ust potrzebny dla jednego fonemu zaczyna powstawać jeszcze przed jego pełnym wybrzmieniem i jednocześnie jest modyfikowany przez fonemy sąsiednie. W naturalnej mowie człowiek nie ustawia ust kolejno w całkowicie niezależnych pozycjach. Ruchy zachodzą na siebie.

W praktyce koartykulacja decyduje o płynności synchronizacji ruchu ust z mową. Jeśli nakładanie jest zbyt małe, każdy wizem pojawia się osobno i twarz wygląda jak mechanicznie przełączana między kolejnymi pozami. Jeśli nakładanie jest zbyt duże, charakterystyczne zwarcia i kształty fonemów zaczynają się rozmywać, a wymowa staje się wizualnie nieczytelna.

Dwa główne parametry to:

- **czas wyprzedzenia artykulacji (anticipatory attack)**, czyli jak wcześnie przed centrum fonemu zaczyna narastać ruch;
- **czas wygaszania artykulacji (release time)**, czyli jak długo ślad ruchu pozostaje po fonemie.

Przykładowe wartości czasu wyprzedzenia:

- 30-40 ms: małe nakładanie, użyteczne przy bardzo szybkiej i zwartej artykulacji, ale łatwo daje efekt mechaniczny;
- 50-80 ms: typowy zakres dla neutralnej mowy i wartość bazowa projektu;
- 90-120 ms: silne wyprzedzenie, przydatne dla części spółgłosek wymagających przygotowania ust, ale może rozmywać sąsiednie fonemy.

Przykładowe wartości czasu wygaszania:

- 50-70 ms: szybki powrót, przydatny przy szybkich sekwencjach spółgłoskowych;
- 80-120 ms: typowy zakres dla naturalnej mowy;
- 130-160 ms: miękkie, wolne przejścia, odpowiednie raczej dla wolniejszej lub ekspresyjnej wypowiedzi niż szybkiego dialogu.

Jako wartość bazową przyjmujemy narastanie 50-80 ms przed centrum fonemu i wygaszanie 80-120 ms po nim. Sąsiednie wizemy nakładają się. Konfliktujące kanały normalizujemy grupami, natomiast żuchwa pozostaje kanałem anatomicznym i nie jest zwykłą sumą wizemów.

Przykład: w sekwencji `/pa/` wargi powinny zacząć się domykać jeszcze przed akustycznym `/p/`, osiągnąć pełny kontakt dla zwarcia, a następnie szybko przejść do otwarcia potrzebnego dla `/a/`. Brak koartykulacji daje widoczne opóźnienie. Nadmierna koartykulacja może z kolei uniemożliwić pełne domknięcie warg.

## Redukcja krótkich fonemów

Jeżeli fonem trwa mniej niż 45 ms, nie wymuszamy pełnej fazy maksymalnego nasilenia (apex). Maksymalna amplituda skaluje się w dół, aby uniknąć trzepotania ust. Dla `PP` zachowujemy jednak warunek domknięcia, jeśli fonem jest akcentowany i akustycznie czytelny.

## Walidacja

Minimalny zestaw testowy: `/pa ba ma fa va ta da ka ga sa za ra/`, sekwencje samogłosek oraz trzy pełne zdania polskie o różnym tempie. Koartykulację oceniamy dodatkowo na wolnym, neutralnym i szybkim tempie mowy, ponieważ jeden zestaw czasów nie musi być optymalny dla wszystkich trzech przypadków.
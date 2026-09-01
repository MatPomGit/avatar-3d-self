# Visemy

Avatar Studio używa niewielkiego zestawu wizualnych klas artykulacyjnych, a nie osobnego shape key dla każdego fonemu. Fonem pozostaje jednostką czasową, viseme jest celem geometrycznym.

## Kanoniczny zestaw

| Viseme | Przykładowe fonemy | Dominujący ruch |
| --- | --- | --- |
| SIL | cisza | neutralne usta |
| PP | p, b, m | pełne domknięcie warg |
| FF | f, v | dolna warga do górnych zębów |
| TH | th | język między/blisko zębów, opcjonalne dla EN |
| DD | t, d, n, l | przedni język, lekko otwarte usta |
| KK | k, g, h | tylna artykulacja, pośredni kształt ust |
| CH | ch, j, sh, zh | zwężenie i lekkie wysunięcie |
| SS | s, z | wąska szczelina, zęby blisko |
| RR | r | zależne od języka, zwykle otwarcie średnie |
| AA | a | szerokie otwarcie żuchwy |
| E | e | usta szerzej, umiarkowane otwarcie |
| I | i, y | szerokie kąciki, małe otwarcie |
| O | o | zaokrąglenie |
| U | u | silniejsze pucker/funnel |

Polski profil pomija `TH` w zwykłych wypowiedziach, ale zachowuje klasę dla mowy angielskiej.

## Reprezentacja

Viseme jest wektorem kanałów, np. `jawOpen`, `mouthFunnel`, `mouthPucker`, `mouthClose`, `mouthStretchLeft/Right`, `mouthPress`, `tongue`. Nie należy tworzyć jednego monolitycznego morphu, jeśli może on konfliktować z emocją.

## Koartykulacja

Cel zaczyna narastać 50-80 ms przed centrum fonemu i wygasa 80-120 ms po nim. Sąsiednie visemy nakładają się. Konfliktujące kanały normalizujemy grupami, ale jaw pozostaje kanałem anatomicznym i nie jest zwykłą sumą visemów.

## Redukcja krótkich fonemów

Jeżeli fonem trwa <45 ms, nie wymuszamy pełnego apexu. Maksymalna amplituda skaluje się w dół, aby uniknąć trzepotania ust. Dla `PP` zachowujemy jednak warunek domknięcia, jeśli fonem jest akcentowany i akustycznie czytelny.

## Walidacja

Minimalny zestaw testowy: `/pa ba ma fa va ta da ka ga sa za ra/`, sekwencje samogłosek oraz trzy pełne zdania polskie o różnym tempie.
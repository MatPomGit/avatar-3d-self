# Walidacja animacji twarzy

Walidacja obejmuje geometrię, timing i wiarygodność behawioralną. Sam fakt, że shape keys działają, nie oznacza zaliczenia.

## Testy deterministyczne

- blink L/R i bilateralny;
- eye look w osiach ±15°;
- jaw open 0-1;
- smile/frown lewy, prawy i bilateralny;
- brow inner/outer up/down;
- cheek puff/squint;
- nose sneer;
- sekwencja viseme testowa.

Każdy test rejestruje clipping, self-intersection, odwrócone normalne i utratę objętości.

## Timing

Blink: 140-240 ms. Neutralny baseline 170 ms. Sakkada 5° powinna trwać około 38 ms, 10° około 50 ms, 20° około 75 ms zgodnie z profilem projektu. Emocje nie mogą skakać z 0 do 1 w jednej klatce.

## Test 60 s

Nagrywamy close-up neutralnego idle. Automatycznie raportujemy liczbę blinków, średni i minimalny interwał, liczbę sakkad i zakres amplitud. Manualnie oceniamy periodyczność, spojrzenie i asymetrię.

## Test mowy

Minimum trzy zdania oraz `/pa-ta-ka/`. Sprawdzamy anticipację warg, domknięcie `/p b m/`, relację `/f v/`, pracę żuchwy i brak zamrożenia policzków/oczu podczas mowy.

## Pass/fail

Automatyczne progi są warunkiem koniecznym. Ostateczny pass wymaga również oceny wizualnej, ponieważ uncanny valley nie daje się zredukować do jednej metryki.
# Locomotion

Lokomocja jest bazową warstwą ruchu całego ciała. Powinna być możliwa do retargetingu i niezależna od warstw twarzy, spojrzenia i mowy.

## Minimalny zestaw

Idle, walk, fast walk, run, turn in place, start, stop i podstawowe przejścia. Dla każdego klipu kontroluj kontakt stóp, wysokość środka masy, ruch miednicy i przeciwfazę ramion.

## Foot sliding

Ślizganie stóp jest błędem krytycznym. Kontaktowa stopa powinna mieć stabilną pozycję względem podłoża, a root motion lub in-place motion muszą być jawnie wybrane dla targetu.

## Integracja

Lokomocja nie powinna wyłączać mikroruchów głowy, spojrzenia ani gestów górnej części ciała. Łączenie realizuj przez maski, additive layers lub równoważny mechanizm silnika.
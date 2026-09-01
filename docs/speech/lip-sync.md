# Lip-sync

Lip-sync jest generowany z czasów fonemów. Amplituda audio może modulować energię ruchu, ale nie określa kształtu ust.

## Oś czasu

Dla fonemu `p_i` znamy `t_start`, `t_end` i confidence. Centrum fonemu:

`t_center = (t_start + t_end) / 2`.

Domyślny cel wizualny jest przesuwany o 60 ms przed audio:

`t_visual = t_center - 0.060 s`.

Zakres dopuszczalny 40-100 ms. Dla bilabialnych `/p b m/` preferujemy 70-90 ms anticipacji, aby domknięcie warg było widoczne przed wybuchem akustycznym.

## Krzywa

Każdy viseme otrzymuje attack 50-80 ms i release 80-120 ms. Zamiast trójkąta liniowego używamy krzywej C1-continuous, np. cubic smoothstep.

Jeżeli dwa cele nachodzą na siebie, wagi są mieszane. Grupy wzajemnie wykluczające się, jak `mouthPucker` i silny `mouthStretch`, są normalizowane.

## Żuchwa

`jawOpen` wynika przede wszystkim z otwartości fonemu i samogłoski. Nie jest generowany z poziomu głośności. Samogłoski `AA` mają największy zakres, `I` mniejszy. Żuchwa ma bezwładność: maksymalna zmiana z 0 do 1 nie powinna zachodzić w jednej klatce, nawet przy błędnym alignmencie.

## Kontaktowe artykulacje

`PP`: usta muszą osiągnąć kontakt. `FF`: dolna warga ma podejść do górnych siekaczy. `SS`: szczelina ma pozostać wąska. Te ograniczenia geometryczne mają wyższy priorytet niż estetyczne wygładzanie.

## Confidence

Dla niskiego confidence alignera nie wycinamy ruchu. Zwiększamy wygładzanie i korzystamy z kontekstu sąsiednich fonemów. Fragmenty o bardzo niskiej pewności są oznaczane w Avatar Studio do ręcznej inspekcji.

## Test synchronizacji

Akceptowalny pipeline powinien utrzymywać wizualny timing bez systematycznego opóźnienia. Testujemy wolną i szybką mowę, liczby, nazwy własne oraz sekwencje `/pa-ta-ka/`. Wynik jest oceniany z audio i bez audio.
# Kryteria odbiorcze

Testy mają identyfikatory, expected result i wynik. „Wygląda dobrze” może być uwagą ekspercką, ale nie zastępuje protokołu.

| ID | Test | Expected result |
| --- | --- | --- |
| GEO-001 | scale | zgodna ze znanym wymiarem |
| GEO-002 | normals/manifold | brak krytycznych błędów |
| BODY-001 | elbow 0–130° | brak collapse i ostrych fałd |
| BODY-002 | shoulder raise | zachowana objętość barku |
| HAND-001 | full fist | brak self-intersection krytycznego |
| HAND-002 | pinch | thumb/index osiągają kontakt |
| FACE-001 | blink L/R | pełne domknięcie bez penetracji oka |
| FACE-002 | jaw open | jaw, lower teeth i język zachowują relację |
| FACE-003 | smile asymmetric | strony sterowane niezależnie |
| EYE-001 | gaze range | oczy niezależne, eyelid follow poprawny |
| SPEECH-001 | /pa ta ka/ | rozróżnialne closures i timing |
| SPEECH-002 | continuous sentence | brak skokowych viseme transitions |
| HAIR-001 | head turn | brak stałej penetracji włosów |
| CLOTH-001 | squat/walk | brak krytycznych penetracji |
| RUNTIME-001 | target FPS | mieści się w zatwierdzonym budżecie |

## Windows

Raport powinien zawierać platformę, wersje narzędzi i linki/ścieżki do lokalnych klipów kontrolnych.

## Linux

Stosuj te same ID testów. Wynik platformowy jest osobny, ale semantyka testu pozostaje identyczna.

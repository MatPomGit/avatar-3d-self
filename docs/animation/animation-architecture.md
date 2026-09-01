# Warstwowa architektura animacji

Naturalny digital human nie może być jednym klipem z ruszającymi się ustami.

```text
locomotion / base pose
        +
upper-body gesture
        +
head orientation
        +
gaze + micro-saccades
        +
blinking
        +
facial affect
        +
lip-sync / jaw
        +
secondary motion
        ↓
final pose
```

## Priorytety

Locomotion ustala bazę ciała. Gest może nadpisywać wybrane kości upper body. Head orientation jest ograniczana anatomicznie. Gaze ma własny target i nie wymaga obracania głowy 1:1. Blink i micro-saccades są proceduralne z kontrolowanym rozkładem czasu, nie stałym timerem.

Facial affect i lip-sync są mieszane regionowo. Speech może chwilowo ograniczać część ruchów ust wynikających z emocji, ale nie powinien wyłączać policzków, brwi i oczu.

## Windows

Testuj mieszanie warstw w docelowym silniku na zestawie: walk+talk, idle+talk, gesture+talk, gaze shift during speech i emotion transition.

## Linux

Jeżeli target engine wspiera Linux, uruchom ten sam zestaw i porównaj wynik. Offline baking w Blenderze powinien zachować te same priorytety warstw.

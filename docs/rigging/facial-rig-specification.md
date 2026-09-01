# Specyfikacja facial rigu

Projekt używa zestawu zgodnego z ARKit jako interoperacyjnej warstwy sterowania oraz FACS jako warstwy interpretacji ruchów mięśniowych.

## Kanoniczne coefficients

```text
browDownLeft browDownRight browInnerUp browOuterUpLeft browOuterUpRight
cheekPuff cheekSquintLeft cheekSquintRight
eyeBlinkLeft eyeBlinkRight eyeLookDownLeft eyeLookDownRight
eyeLookInLeft eyeLookInRight eyeLookOutLeft eyeLookOutRight
eyeLookUpLeft eyeLookUpRight eyeSquintLeft eyeSquintRight eyeWideLeft eyeWideRight
jawForward jawLeft jawOpen jawRight
mouthClose mouthDimpleLeft mouthDimpleRight mouthFrownLeft mouthFrownRight
mouthFunnel mouthLeft mouthLowerDownLeft mouthLowerDownRight
mouthPressLeft mouthPressRight mouthPucker mouthRight mouthRollLower mouthRollUpper
mouthShrugLower mouthShrugUpper mouthSmileLeft mouthSmileRight
mouthStretchLeft mouthStretchRight mouthUpperUpLeft mouthUpperUpRight
noseSneerLeft noseSneerRight tongueOut
```

## Wymagania dodatkowe

ARKit coefficient nie jest gwarancją poprawnej anatomii. Projekt dopuszcza corrective shapes i kontrolery pomocnicze, np. eyelid follow, lip seal, jaw corrective, cheek compression i nasolabial fold. Te kontrolery nie mogą jednak łamać mapowania warstwy interoperacyjnej.

Jaw jest sterowany anatomicznie przez kość/transform żuchwy. `jawOpen` może współsterować miękką tkanką, ale nie może być wyłącznie morph targetem warg.

## FACS

Każdy istotny shape powinien mieć w dokumentacji relację do Action Units, jeśli istnieje sensowne mapowanie. Nie wymuszaj relacji 1:1, ponieważ ARKit coefficients i FACS opisują różne poziomy sterowania.

## Windows

Eksportuj morph targets z niezmienionymi nazwami. Uruchom walidację kompletności przed FBX/runtime importem.

## Linux

Używaj identycznych nazw i walidatora. Różnice platformy nie mogą zmieniać facial interface.

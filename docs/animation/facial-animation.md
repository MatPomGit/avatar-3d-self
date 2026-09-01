# Facial animation

Facial animation łączy rig wewnętrzny, ARKit/FACS, emocje, mowę i mikroruchy.

## Warstwy

1. neutral/rest pose;
2. emotion/affect;
3. speech articulation;
4. blink i eyelid follow;
5. gaze-related adjustments;
6. micro asymmetry.

Warstwy nie mogą po prostu sumować wartości bez ograniczeń. Potrzebne są maski, priorytety i clampy zapobiegające niefizycznym kombinacjom.

Najważniejsza jest ciągłość ruchu. Nawet poprawny pojedynczy blend shape wygląda sztucznie, jeśli przejście ma nienaturalną dynamikę.
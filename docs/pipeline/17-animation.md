# 17. Animacja

**Input:** zatwierdzony rig i skinning.  
**Editable output:** klipy i warstwowa konfiguracja animacji.  
**Specification:** [Animation architecture](../animation/animation-architecture.md).

## Windows

1. Utwórz bazowe idle, walk i test gesture clips.
2. Oddziel locomotion od upper-body gestures.
3. Dodaj head orientation, gaze, blinking i facial expression jako osobne warstwy.
4. Utrzymuj drobne asymetrie i mikroruchy.
5. Testuj transitions, nie tylko pojedyncze klipy.

## Linux

1. Przygotuj te same warstwy i klipy bazowe.
2. Sprawdź retargeting i root motion zgodnie z target engine.
3. Dodaj procedural gaze/blink i ograniczenia.
4. Wymieszaj gestures z locomotion.
5. Zweryfikuj naturalność w długim idle.

## DoD

Postać nie jest statyczna poza mową, przejścia są płynne, gaze i blink nie są mechanicznie okresowe, a warstwy nie nadpisują się przypadkowo.

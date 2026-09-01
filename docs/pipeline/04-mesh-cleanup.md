# 04. Cleanup high-poly

**Input:** niezmieniony mesh rekonstrukcji.  
**Editable output:** `avatar_body_clean_vNNN.blend`.  
**Derived output:** raport naprawionych regionów.

## Windows

1. Otwórz kopię skanu w Blenderze.
2. Usuń wyłącznie odłączone fragmenty i oczywiste artefakty tła.
3. Napraw małe dziury bez zmiany charakterystycznych rysów.
4. Usuń samoprzecięcia, odwrócone normals i niepotrzebne wnętrza.
5. Zachowaj high-poly jako źródło bake'u, nie jako mesh animacyjny.

## Linux

1. Otwórz kopię skanu w Blenderze.
2. Usuń odłączone artefakty i geometrię tła.
3. Napraw lokalne błędy, zachowując asymetrię i podobieństwo.
4. Sprawdź normals, self-intersections i manifoldness tam, gdzie jest wymagana.
5. Zapisz edytowalny high-poly.

## Failure conditions

Agresywne smoothing, symetryzacja twarzy, usunięcie charakterystycznych cech albo automatyczne „upiększanie” są błędami jakości.

## DoD

High-poly jest czysty technicznie, zachowuje podobieństwo i może być stabilnym źródłem do retopologii i bake'u.

# 21. Walidacja runtime

**Input:** pakiet importowy.  
**Output:** runtime validation report i zatwierdzony demonstrator.

## Windows

1. Zaimportuj model do wybranego silnika.
2. Odtwórz test pose matrix, idle, walk, gesture, gaze, blink, emotions i speech clip.
3. Zmierz frame time, VRAM/RAM, draw calls, triangles, active morphs i koszt animacji.
4. Sprawdź LOD transitions z kilku dystansów.
5. Zapisz wynik wraz ze sprzętem, sterownikiem i wersją silnika.

## Linux

1. Wykonaj analogiczny import, jeżeli target runtime wspiera Linux.
2. Powtórz ten sam zestaw klipów i testów.
3. Zapisz metryki wydajności oraz różnice względem Windows.
4. Zweryfikuj materiały i groom, które mogą mieć inny backend renderera.
5. Zachowaj raport platformowy oddzielnie.

## DoD

Wszystkie testy krytyczne z [Acceptance criteria](../validation/acceptance-criteria.md) mają status passed, a wydajność mieści się w zatwierdzonym budżecie.

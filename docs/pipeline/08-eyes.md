# 08. Oczy

**Input:** retopologizowana głowa i zdjęcia oczu.  
**Editable output:** osobne gałki oczne i materiały.

## Windows

1. Utwórz sclera, iris/pupil i warstwę cornea z poprawnymi pivotami.
2. Dopasuj promień gałki do powiek, nie odwrotnie przez deformowanie oka.
3. Dodaj subtelny limbus i variation sclera bez przesadnego zaczerwienienia.
4. Sprawdź refraction/specular w docelowym rendererze.
5. Zweryfikuj pełny zakres gaze i eyelid follow.

## Linux

1. Zbuduj identyczny układ osobnych elementów oka.
2. Ustaw oś obrotu w geometrycznym środku gałki.
3. Dopasuj powieki i wetline.
4. Przetestuj materiał cornea w renderze PBR.
5. Sprawdź kolizje powiek podczas blink i gaze.

## DoD

Oczy obracają się niezależnie, cornea reaguje na światło, iris zachowuje głębię, a powieki nie przecinają gałki.

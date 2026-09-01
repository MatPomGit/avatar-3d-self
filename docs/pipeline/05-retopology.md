# 05. Retopologia

**Input:** zatwierdzony high-poly.  
**Editable output:** `avatar_body_retopo_vNNN.blend`.  
**Gate:** po akceptacji następuje topology freeze.

## Windows

1. Utwórz nowy quad mesh na powierzchni high-poly.
2. Zbuduj koncentryczny edge flow wokół oczu i ust.
3. Zapewnij pętle dla żuchwy, policzków i nosa.
4. Dodaj kontrolowaną gęstość w barkach, łokciach, nadgarstkach, palcach, biodrach i kolanach.
5. Wykonaj testowe deformacje przed finalnym zatwierdzeniem.

## Linux

1. Retopologizuj high-poly do quadowej siatki deformacyjnej.
2. Zachowaj pętle twarzy wspierające blink, smile, jaw i cheek deformation.
3. Zaprojektuj joint loops zgodnie z kierunkiem zgięcia.
4. Zweryfikuj dłonie i każdy palec osobno.
5. Zamroź topologię dopiero po testowych pozach.

## Validation

Nie oceniaj tylko wireframe'u w A-pose. Testuj jaw open, blink, smile, shoulder raise, elbow 130°, wrist flexion, fist, squat i knee flexion.

## DoD

Topologia jest animacyjna, bez n-gonów w krytycznych regionach, posiada zatwierdzony edge flow i otrzymuje status `approved` jako baza dalszych zależności.

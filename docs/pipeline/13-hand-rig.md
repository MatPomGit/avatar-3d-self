# 13. Rig dłoni

**Input:** body skeleton i zatwierdzone dłonie.  
**Editable output:** niezależny rig palców obu dłoni.

## Windows

1. Dodaj trzy segmenty dla index/middle/ring/pinky oraz poprawną strukturę kciuka.
2. Ustaw osie zgięcia zgodnie ze stawami, nie z globalną osią sceny.
3. Zapewnij niezależny FK każdego palca.
4. Dodaj opcjonalne kontrolery curl/spread jako warstwę wygody.
5. Przetestuj chwyt cylindryczny, pinch, point i fist.

## Linux

1. Zbuduj analogiczną hierarchię każdej dłoni.
2. Skoryguj pivoty według anatomii MCP/PIP/DIP.
3. Dodaj indywidualne sterowanie oraz kontrolery zbiorcze.
4. Zweryfikuj kciuk w opozycji.
5. Sprawdź self-intersections palców.

## DoD

Każdy palec porusza się niezależnie, kciuk osiąga opozycję, a podstawowe chwyty nie powodują krytycznego collapse mesha.

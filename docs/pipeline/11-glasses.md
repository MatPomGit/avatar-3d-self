# 11. Okulary

**Input:** zdjęcia i wymiary rzeczywistych oprawek.  
**Editable output:** osobny model frames + lenses.

## Windows

1. Odtwórz szerokość frontu, mostek, długość zauszników i kształt soczewek z pomiarów.
2. Modeluj oprawki i soczewki oddzielnie.
3. Ustaw mocowanie względem kości głowy, nie do pojedynczego vertexu twarzy.
4. Sprawdź kolizje z brwiami, rzęsami, nosem i uszami podczas mimiki.
5. Skonfiguruj przezroczystość/refraction soczewek dla rendereru docelowego.

## Linux

1. Zbuduj model na podstawie tych samych wymiarów.
2. Ustal pivot i transform względem głowy.
3. Przygotuj osobne materiały frames/lenses.
4. Zweryfikuj ekspresje i head motion.
5. Zapisz wersję bez baked transform errors.

## DoD

Okulary zachowują rzeczywistą geometrię, są stabilne podczas ruchu i nie generują nierealistycznych refleksów ani clippingu.

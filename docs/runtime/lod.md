# Level of Detail

LOD redukuje koszt renderowania i części animacji wraz z odległością od kamery.

## Strategia

LOD0 zachowuje maksymalną jakość twarzy i sylwetki. Kolejne poziomy redukują geometrię, liczbę materiałów, koszt groom i część drobnych blend shapes. Redukcja musi zachować kontur twarzy, dłoni i charakterystyczne elementy wyglądu.

Dla włosów przejście groom → cards może być osobnym poziomem jakości.

Każdy LOD waliduj w ruchu oraz podczas przełączeń, aby uniknąć widocznych popów i zmiany tożsamości twarzy.
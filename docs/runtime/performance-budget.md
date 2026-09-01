# Budżet wydajności

Budżet jest kontraktem pomiarowym. Konkretne limity geometrii zostaną zatwierdzone po wyborze pierwszego target engine i sprzętu, zamiast arbitralnie optymalizować model przed benchmarkiem.

## Wymagane metryki

- target FPS i frame-time budget;
- CPU animation time;
- GPU character rendering time;
- VRAM i RAM;
- triangles per LOD;
- draw calls i material slots;
- liczba skinned meshes;
- liczba bones;
- liczba morph targets oraz maksymalna liczba aktywnych jednocześnie;
- rozdzielczości tekstur i residency;
- koszt groom/hair cards;
- czas ładowania assetu.

## Baseline demonstratora

Pierwszy demonstrator PC powinien celować w stabilne **60 FPS (16,67 ms/frame)** na jawnie wskazanym sprzęcie. Nie jest to gwarancja, że sam awatar może zużyć cały frame budget; raport musi oddzielać koszt postaci od reszty sceny.

## Windows

Benchmark zapisuje wersję Windows, GPU, driver, CPU, engine i ustawienia renderera.

## Linux

Benchmark zapisuje dystrybucję/kernel, GPU, driver, CPU, engine i backend renderera. Wyniki obu platform są oddzielnymi rekordami.

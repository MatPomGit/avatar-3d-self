# Pomiary antropometryczne

Pomiary służą do skali i kontroli proporcji, nie do zastępowania fotografii.

| Pomiar | Zastosowanie |
| --- | --- |
| wzrost | globalna skala |
| vertex głowy → broda | kontrola głowy |
| szerokość barków | proporcje tułowia |
| długość ramienia i przedramienia | joint placement |
| rozpiętość ramion | kontrola kończyn |
| szerokość dłoni, długość palca środkowego | dłonie |
| długość nogi, wysokość kolana | joint placement |
| długość i szerokość stopy | stopy/buty |
| szerokość oprawek, bridge, temple length | okulary |

## Windows

Zapisz pomiary w prywatnym `capture_manifest.json` w milimetrach. Nie używaj separatora przecinkowego w wartościach maszynowych; zapis JSON używa liczby z kropką.

## Linux

Zapisz identyczny zestaw w milimetrach. Skrypty i raporty muszą być niezależne od locale systemu.

Każdy pomiar powinien mieć `value_mm`, metodę, datę i opcjonalną niepewność. Dla pomiarów miękkich tkanek nie udawaj precyzji większej niż rzeczywista.

# 18. Lip-sync

**Input:** audio + phoneme timestamps + facial rig.  
**Editable output:** viseme/jaw curves.  
**Derived output:** zsynchronizowany klip mowy.

## Windows

1. Uzyskaj alignment fonemów do audio.
2. Zamapuj fonemy na mały zestaw viseme targets.
3. Dodaj jaw contribution niezależnie od samych warg.
4. Zastosuj anticipatory i carry-over coarticulation.
5. Wygładź tylko tyle, aby nie zgubić spółgłosek zwartych.

## Linux

1. Wygeneruj te same timestampy fonemów.
2. Użyj wspólnej tabeli phoneme→viseme.
3. Dodaj krzywe jaw, lips i cheeks.
4. Mieszaj sąsiednie visemy zależnie od czasu i kontekstu.
5. Porównaj nagranie z dźwiękiem i bez dźwięku.

## DoD

Bilabials, labiodentals i otwarte samogłoski są rozróżnialne, timing nie wyprzedza/nie opóźnia audio systematycznie, a usta nie przełączają się skokowo shape-by-shape.

# FACS

FACS opisuje ruchy twarzy przez Action Units. W Avatar Studio służy przede wszystkim do semantycznej walidacji ekspresji i projektowania bardziej naturalnych kombinacji niż proste presety emocji.

## Zastosowanie

- dokumentowanie, które regiony twarzy powinny się poruszać;
- budowanie asymetrycznych ekspresji;
- ocena zgodności blend shapes z anatomią;
- tworzenie mapowania między trackingiem ARKit a wewnętrznym facial rig.

Nie należy traktować FACS jako prostego słownika `emocja = jeden blend shape`. Naturalna ekspresja jest kombinacją wielu AU o zmiennym natężeniu i czasie.
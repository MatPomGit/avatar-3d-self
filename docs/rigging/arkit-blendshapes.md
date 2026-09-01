# ARKit blend shapes

ARKit jest interfejsem kompatybilności dla sterowania twarzą, nie gwarancją jakości anatomii. Avatar Studio przyjmuje kanoniczny zestaw 52 współczynników jako warstwę wejściową facial animation.

## Zasady

- zachowuj dokładne, stabilne nazwy mapowania;
- rozdzielaj lewą i prawą stronę tam, gdzie standard to przewiduje;
- jawOpen powinno współpracować z kością żuchwy;
- eyeLook* steruje kierunkiem oczu, nie deformacją całej twarzy;
- pojedynczy współczynnik może mapować się na kilka wewnętrznych kontrolerów.

Wewnętrzny rig może być bogatszy niż ARKit. Warstwa ARKit pozostaje adapterem dla trackingu i wymiany danych.
# Samodzielne wykonywanie zdjęć

Samodzielny capture jest możliwy, ale tradycyjna fotogrametria zakłada statyczny obiekt i zmieniającą pozycję kamery.

## Preferowany wariant

Osoba pozostaje możliwie nieruchoma, a aparat jest kolejno ustawiany wokół niej na statywie. Użyj pilota, timera lub zdalnego wyzwalania. Każda zmiana pozycji aparatu powinna zachować overlap.

## Obracanie osoby

Stała kamera i obracająca się osoba nie są matematycznie równoważne klasycznemu SfM, ponieważ tło pozostaje nieruchome, a obiekt zmienia pozę względem sceny. Taki wariant stosuj tylko w workflow obsługującym turntable/object-centric reconstruction, najlepiej z maskowaniem tła.

Nie mieszaj obu strategii w jednym zestawie bez jawnej kontroli i testowej rekonstrukcji.
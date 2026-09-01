# Samodzielne wykonywanie materiału

Samodzielny capture jest możliwy, ale trzeba rozdzielić fotografię referencyjną od właściwej fotogrametrii. Klasyczna Structure from Motion zakłada statyczną scenę. Obracająca się osoba na tle nieruchomego pokoju łamie to założenie.

## Wariant preferowany: kamera zmienia pozycję

Ustaw aparat na statywie z pilotem lub timerem. Po każdym zdjęciu przestaw statyw o 10-15° wokół zaznaczonego punktu, wróć do identycznej pozy i wykonaj kolejne ujęcie. Jest to wolniejsze, ale zachowuje zgodność geometrii osoby względem tła lepiej niż ciągłe obracanie ciała.

Na podłodze zaznacz pozycje stóp i osi ciała. Użyj znacznika dla kierunku wzroku i wysokości aparatu.

## Wariant turntable: osoba się obraca

Stosuj tylko jako kontrolowany kompromis. Tło powinno być gładkie i możliwe do zamaskowania, a rekonstrukcja powinna używać masek foreground albo workflow wspierającego object-centric/turntable reconstruction. Nie wolno polegać na cechach nieruchomego tła.

Obrót 10-12° na ujęcie. Po każdym kroku zatrzymaj się na 1-2 s przed wyzwoleniem migawki. Zachowaj identyczną A-pose. Włosy, luźna odzież i tkanki miękkie nie mogą swobodnie zmieniać położenia między zdjęciami.

## Automatyzacja

Telefon można sterować zegarkiem, pilotem Bluetooth lub aplikacją timera. Ustaw 3-5 s opóźnienia po zmianie pozy. Parametry ekspozycji i focus powinny być zablokowane.

## Kontrola serii

Co 10-15 zdjęć wykonaj kontrolę pozy na podglądzie. Jeżeli stopy, ręce lub głowa przesunęły się względem markerów, serię od ostatniego poprawnego punktu należy powtórzyć.

## Czego nie robić

Nie obracaj się płynnie podczas burst/video extraction. Nie mieszaj ujęć z innych dni, ogniskowych i oświetlenia w jednym solve. Nie używaj portrait mode.

## Definition of Done

Metoda capture jest zapisana w manifeście jako `moving_camera` albo `turntable_masked`. Dla wariantu turntable maski lub potwierdzenie poprawnego object-centric solve są obowiązkowe przed przejściem dalej.
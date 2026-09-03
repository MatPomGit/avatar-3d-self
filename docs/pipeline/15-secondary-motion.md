# 15. Ruch wtórny

Ruch wtórny (secondary motion) jest opóźnioną reakcją elastycznych części postaci
na ruch podstawowy. Nie może zmieniać intencji pozy ani służyć do ukrywania
błędnego skinningu. Używaj jednostek solvera tylko razem z jego nazwą, wersją,
skalą sceny, krokiem czasu i presetem: wartości znormalizowane poniżej są
punktami startowymi, a nie uniwersalnymi stałymi fizycznymi.

**Input:** zatwierdzony rig i skinning, włosy/ubrania/anatomia, skala, klipy
ruchu oraz profil docelowego solvera.
**Edytowalny wynik:** scena z regionami, guides/secondary bones, proxy kolizji,
ograniczeniami, parametrami i cache.
**Eksport pochodny:** bake kości/wierzchołków albo wersjonowany preset runtime.

## Wybór regionów i collision proxies

1. Obejrzyj referencje przy powolnym przechyle, chodzie, biegu, skręcie i nagłym
   zatrzymaniu. Zaznacz tylko regiony z czytelną bezwładnością: długie pasma
   włosów, luźne ubranie, akcesoria i uzasadnione miękkie tkanki.
2. Oceń znaczenie dla sylwetki, amplitudę i koszt. Nie dynamizuj sztywnych części
   ani regionu, którego ruchu nie potwierdza anatomia/materiał.
3. Podziel region na niezależne grupy zgodne z kierunkiem ruchu. Strony ciała
   zachowaj oddzielnie; długie włosy dziel według guides, nie każdego włosa.
4. Zbuduj proste collision proxies dla głowy, szyi, barków, klatki i potrzebnych
   kończyn: kapsuły/sfery zamiast render mesh. Proxy ma obejmować sylwetkę z małym
   marginesem, podążać za właściwą kością i nie mieć ujemnej skali.
5. Zweryfikuj proxy w całym zakresie animacji. Zbyt małe powoduje penetracje,
   zbyt duże unosi element nad ciałem; nadmierna liczba colliderów obniża
   stabilność i wydajność.

## Parametry i sposób doboru

**Masa (mass)** opisuje bezwładność punktu lub segmentu. Wyższa wartość wolniej
reaguje i mocniej ciągnie łańcuch; niższa szybciej podąża za rodzicem. W
znormalizowanym presecie użyj `0.2` (niska), `0.5` (typowa), `0.8` (wysoka),
często zwiększając masę ku końcówce tylko, gdy wynika to z obiektu. Za mała daje
nerwowe podążanie, za duża nadmierny lag i rozciąganie.

**Sztywność (stiffness)** jest oporem sprężyny na odchylenie lub zgięcie. Jej
zwiększenie utrzymuje kształt bliżej animacji bazowej, zmniejszenie daje większy
łuk. Zacznij od `0.2` dla luźnego pasma, `0.5` dla miękkiej tkanki/ubrania i
`0.8` dla krótkiego, stabilnego elementu. Za niska powoduje wiotkość i kontakt z
ciałem, za wysoka — sztywny ruch lub oscylacje przy dużym kroku solvera.

**Tłumienie (damping)** odbiera energię oscylacji. Wyższe szybciej uspokaja ruch,
niższe pozwala dłużej kołysać się po zatrzymaniu. Punkty startowe to `0.1`
(niskie), `0.45` (typowe), `0.8` (wysokie). Dobieraj je po stiffness: za małe
daje wielokrotne odbicia, za duże sprawia, że region „pływa w miodzie” i nie
reaguje na drobny impuls.

**Ograniczenie (constraint)** wyznacza dozwolony kąt, przesunięcie lub długość.
Zakres np. `5°` jest niski, `15°` typowy, a `30°` wysoki dla pomocniczego łańcucha,
ale zawsze zależy od regionu. Mniejszy chroni sylwetkę; większy pozwala na
swobodę. Za ciasny daje twarde zatrzymanie, za luźny penetracje lub
nieanatomiczne rozciągnięcie. Używaj miękkiego limitu przed twardym i wizualizuj
stożki ograniczeń.

**Margines kolizji (collision margin)** jest odległością bezpieczeństwa od
proxy. Dla skali człowieka zacznij od `2 mm` (niski), `5 mm` (typowy), `10 mm`
(wysoki; grube ubranie). Za mały sprzyja tunelowaniu, za duży tworzy widoczną
szczelinę. **Tarcie (friction)** ogranicza ślizg po colliderze: `0.1`, `0.4` i
`0.8` to niska, typowa i wysoka wartość znormalizowana. Za małe ślizga, za duże
przykleja i może gromadzić energię.

**Liczba podkroków (substeps)** dzieli klatkę na mniejsze kroki obliczeń, a
**iteracje solvera** powtarzają rozwiązanie ograniczeń w każdym kroku. Więcej
zwiększa stabilność i koszt. Zacznij od `2` podkroków/`4` iteracji, użyj
`4/8` dla szybkiego ruchu i tylko diagnostycznie `8/16`. Za mało daje tunelowanie
i rozciąganie; bardzo dużo maskuje zły model lub uniemożliwia budżet runtime.

## Strojenie od ruchu wolnego do gwałtownego

1. Wyłącz kolizje i grawitację, animuj powolny przechył. Ustaw mass/stiffness tak,
   aby kształt zachowywał zamierzoną sylwetkę.
2. Dodaj zatrzymanie i dobierz damping do liczby pożądanych oscylacji. Zmieniaj
   jeden parametr naraz i zapisuj wartość oraz klip.
3. Włącz grawitację, potem constraints. Sprawdź neutral i skrajne pozy przed
   dodaniem kolizji.
4. Włącz kolejno collider głowy, tułowia i kończyn; ustaw margin/friction. Tak
   można wskazać proxy wprowadzające drżenie.
5. Uruchom chód, bieg, obrót 180°, skok/lądowanie i gwałtowny stop. Dopiero przy
   utracie stabilności zwiększ substeps/iterations; nie usztywniaj całego regionu.
6. Testuj różne FPS i co najmniej 30 s pętli. Porównaj sylwetkę, energię po
   zatrzymaniu i koszt z zatwierdzoną referencją.

## Stabilizacja, bake i deterministyczność

Stosuj stały krok czasu, rzeczywistą skalę, ograniczony maksymalny impuls i
Continuous Collision Detection, jeśli solver je wspiera. Rozpoczynaj z
bezkolizyjnej pozy i wykonaj preroll `1–2 s`; teleport, zmiana skali lub start w
penetracji muszą resetować stan. Unikaj łańcuchów z ekstremalnie różnymi masami.

Dla ujęcia finalnego wykonaj bake po zatwierdzeniu FPS, zakresu z uchwytami,
wersji solvera i losowego seed. Zapisz wejściowy klip, preset, collision proxies,
cache oraz hash/wersję. Deterministyczność potwierdź dwoma przebiegami od tej
samej klatki: trajektorie muszą być identyczne w przyjętej tolerancji. Jeśli
runtime nie jest deterministyczny, eksportuj bake; nie deklaruj zgodności tylko
na podstawie podobnego wyglądu.

## Odzyskiwanie po „eksplozji” symulacji

1. Zatrzymaj obliczenia i zachowaj pierwszy błędny numer klatki/log; nie zapisuj
   uszkodzonego cache jako źródła.
2. Wyczyść cache, wróć przed błąd i sprawdź skalę, NaN/Inf, ujemne transformacje,
   teleporty, startowe penetracje oraz collider o zerowym rozmiarze.
3. Odtwórz z jednym regionem, bez kolizji; dodawaj constraints i colliders po
   jednym. Jeśli błąd znika, ostatni składnik jest kandydatem.
4. Zmniejsz krok czasu/zwiększ substeps, ogranicz prędkość/impuls i usuń skrajny
   stosunek mas. Napraw przyczynę, potem wróć do budżetu docelowego.
5. Uruchom od czystego preroll dwa razy, wykonaj bake od nowa i ponownie sprawdź
   gwałtowny klip. Nigdy nie interpoluj ręcznie przez eksplodowane klatki.

## Checklisty zamknięcia etapu

### Wejście
- [ ] Rig, skinning, skala, regiony i klipy wolny/chód/bieg/stop są zatwierdzone.
- [ ] Zapisano solver, wersję, FPS, platformę i budżet wykonania.

### Wynik edytowalny
- [ ] Regiony, guides/bones, proxies, constraints i wszystkie parametry są edytowalne.
- [ ] Preset zawiera jednostki, seed, krok czasu, substeps i iterations.

### Eksport
- [ ] Wybrano jawnie bake albo preset runtime i zachowano pliki źródłowe/cache.
- [ ] Eksport obejmuje właściwy zakres z preroll/uchwytami i poprawną skalę.

### Walidacja
- [ ] Powolny ruch, chód, bieg, obrót, lądowanie i gwałtowny stop są stabilne.
- [ ] Dwa czyste przebiegi są deterministyczne albo wynik został wypieczony.

### Błędy blokujące
- [ ] Nie ma eksplozji, NaN, tunelowania, trwałej penetracji ani nieograniczonego stretch.
- [ ] Ruch nie zmienia anatomii/intencji i mieści się w budżecie runtime.

### Definition of Done
- [ ] Subtelny ruch wtórny ma zatwierdzoną referencję, stabilne kolizje i
      odzyskiwalny preset; wynik jest deterministyczny lub wypieczony oraz
      przechodzi pełną sekwencję od wolnego ruchu do gwałtownego bez blokad.

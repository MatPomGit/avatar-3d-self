# 13. Rig dłoni

Rig dłoni przenosi ruch z kontrolek animatora na anatomiczny łańcuch kości i
siatkę. Położenie stawu wyznacza się z geometrii i referencji, a nie przez równy
podział długości palca. MCP jest stawem u nasady palca, PIP — pierwszym stawem
międzypaliczkowym, a DIP — stawem najbliższym paznokcia. Kciuk ma CMC, MCP i IP;
nie należy nazywać jego segmentów jak trzech stawów pozostałych palców.

**Input:** zatwierdzone dłonie w neutralnej pozie, body skeleton, referencje
otwartej dłoni i chwytów oraz rzeczywista skala sceny.
**Edytowalny wynik (editable output):** wersjonowana scena z kośćmi deformującymi,
kontrolkami, ograniczeniami, wagami i pozami testowymi.
**Eksport pochodny (derived output):** skeleton, skin weights i animacje testowe
dla docelowego środowiska wykonawczego.

## Wyznaczanie pivotów i osi

1. Na widoku dłoniowym, grzbietowym i bocznym zaznacz środek każdej głowy
   stawowej. Dla MCP użyj środka kłykci kości śródręcza; dla PIP/DIP środka
   walca dopasowanego do fałdu zgięciowego i szerokości stawu. Fałd skóry jest
   wskazówką, nie samodzielną definicją pivotu.
2. Przeprowadź przez sąsiednie środki linię podłużną paliczka. Rzutuj pivot do
   wnętrza kości; pivot pozostawiony na powierzchni powoduje zataczanie łuku.
3. Obróć segment testowo o `±10°`. Łuk paznokcia ma podążać za stawem bez
   translacyjnego „wyskoku”. Skoryguj pivot przed skinningiem.
4. Ustal jedną semantykę osi dla obu dłoni: lokalna oś podłużna biegnie od
   rodzica ku dziecku, oś zgięcia jest prostopadła do płaszczyzny naturalnego
   zgięcia, a trzecia wynika z prawoskrętnego układu. Odbicie nazw nie może
   odwrócić znaczenia dodatniego `curl`.
5. Wyznacz płaszczyznę zgięcia osobno dla każdego palca z punktów MCP–PIP–DIP.
   Nie wyrównuj jej do globalnej osi ani do palca środkowego. Zapisz orientację
   neutralną i wartości roll; zastosuj skalę przed wiązaniem.
6. Kciuk orientuj z jego własnej płaszczyzny opozycji. Oś CMC umożliwia zarówno
   odwodzenie, jak i rotację potrzebną do zetknięcia opuszki z pozostałymi.

## Hierarchia i kontrolki

Buduj łańcuch `hand → finger_MCP → finger_PIP → finger_DIP → finger_tip`; kość
końcówki jest markerem, jeśli nie deformuje siatki. Łańcuch kciuka to
`hand → thumb_CMC → thumb_MCP → thumb_IP → thumb_tip`. Kości deformujące nie są
dziećmi kontrolek innego palca. Zachowaj odrębne hierarchie lewej i prawej dłoni,
kanoniczne nazwy projektu i jawne powiązanie z kością dłoni.

1. Dodaj kontrolkę **FK** dla każdego stawu. Ma sterować lokalną rotacją bez
   niejawnej translacji lub skali i pozwalać na niezależne pozowanie.
2. Dodaj wysokopoziomowy `curl` na palec i całą dłoń. Rozdziel wejście krzywymi,
   np. MCP/PIP/DIP `0.35/0.40/0.25`, a potem dopasuj do anatomii. Kontrolka jest
   wygodnym sterownikiem, nie zastępuje FK.
3. Dodaj `spread` głównie do MCP. Rozkład wachlarzowy ma być największy dla
   index/pinky, mniejszy dla ring i bliski zeru dla middle; wygaszaj go podczas
   pełnego fist, aby nie rozrywać przestrzeni między palcami.
4. Dla kciuka rozdziel `opposition`, `curl` i `spread`. Opozycja musi łączyć
   obrót CMC z niewielką kompensacją MCP, zamiast obracać cały kciuk w jednej osi.
5. Ustaw limity jako zabezpieczenie, lecz pozwól wyłączyć je podczas diagnostyki.
   Sprawdź identyczne znaczenie sterowników po odbiciu i eksporcie.

## Dozwolone zakresy ruchu

Zakresy są konserwatywnymi punktami startowymi dla dorosłej dłoni, mierzonymi od
neutralnej pozycji. Referencja konkretnej osoby i brak penetracji mają
pierwszeństwo; przeprost ustaw na `0°`, jeśli nie jest potwierdzony materiałem.

| Staw / ruch | Minimum | Maksimum | Uwagi walidacyjne |
| --- | ---: | ---: | --- |
| index–pinky MCP flexion/extension | `-20°` | `90°` | przeprost tylko z referencji; przy fist kostki tworzą naturalny łuk |
| index–pinky MCP spread | `-15°` | `15°` | zakres maleje przy pełnym zgięciu; middle jest osią wachlarza |
| index–pinky PIP flexion | `0°` | `110°` | bez bocznego załamania i utraty objętości |
| index–pinky DIP flexion | `0°` | `80°` | powinien współpracować z PIP, ale zachować niezależne FK |
| thumb CMC opposition | `0°` | `45°` | opuszka ma dosięgać index i pinky bez zapadania nasady |
| thumb CMC spread | `-15°` | `45°` | sprawdź prześwit pierwszej przestrzeni międzypalcowej |
| thumb MCP flexion | `0°` | `60°` | bez ścinania objętości stawu |
| thumb IP flexion | `0°` | `80°` | paznokieć nie może skręcać względem opuszki |

## Skinning

1. Zwiąż siatkę z kośćmi deformującymi w neutralnej pozie. Najpierw przypisz
   sztywne obszary trzonów paliczków, potem zbuduj zachodzące na siebie gradienty
   wokół stawów.
2. Utrzymuj dominujący wpływ stawu po jego stronie fałdu; nie rozlewaj wag PIP na
   MCP sąsiedniego palca. Normalizuj wagi i przestrzegaj limitu wpływów eksportera.
3. Testuj kolejno `25%`, `50%`, `75%` i maksimum zakresu. Koryguj objętość po
   stronie kostki oraz kompresję od strony dłoni; nie maskuj złego pivotu wagami.
4. Dopiero po poprawnych pivotach dodaj kości pomocnicze lub corrective shapes
   dla zapadania kostek, błony między palcami i skrajnej opozycji kciuka.
5. Porównaj sylwetkę, normalne i wagi po eksporcie z edytowalną sceną.

## Test chwytów

Zapisz osobne pozy: otwarta dłoń, fist, chwyt cylindryczny, spherical grip,
pinch kciuk–index, pinch kciuk–middle, point, tripod grip, key grip i thumb
opposition do każdego palca. Każdą sprawdź z obu stron dłoni oraz w przejściu
neutral → chwyt → neutral. Wymagane są kontakt opuszek bez penetracji, czytelne
kostki, brak collapse objętości i brak skoku po przełączeniu FK/curl. Dla chwytów
z rekwizytem użyj co najmniej cienkiego walca, grubego walca, kuli i płaskiej
karty. Nie przesuwaj rekwizytu, aby ukryć błędny łuk palca.

## Diagnostyka skręcania palców

| Objaw | Test rozstrzygający | Przyczyna i naprawa |
| --- | --- | --- |
| Paznokieć obraca się spiralnie podczas curl | Wyświetl lokalne osie i animuj tylko jeden staw | Niespójny bone roll; przelicz orientację z płaszczyzny palca, nie obracaj corrective shape przeciw błędnej osi. |
| Palec odchyla się bokiem przy zgięciu | Wyłącz skinning i obserwuj sam łańcuch | Oś zgięcia nie jest prostopadła do płaszczyzny MCP–PIP–DIP; popraw rest axes i ponownie binduj. |
| Szkielet jest poprawny, lecz skóra tworzy spiralę | Odtwórz ruch na prostym mesh proxy | Wagi przechodzą ukośnie lub zawierają wpływ sąsiedniego palca; oczyść i znormalizuj gradient. |
| Tylko odbita dłoń skręca się odwrotnie | Porównaj macierze osi i znak `curl` L/R | Ujemna skala lub mechaniczne mirror osi; zastosuj transformacje i zachowaj semantyczny znak sterownika. |
| Skręt pojawia się dopiero po eksporcie | Porównaj rest pose, kolejność Eulera i quaterniony | Eksporter zmienił pre/post-rotation albo osie; wyeksportuj klip osiowy i napraw profil eksportu. |
| Kciuk trafia bokiem opuszki | Animuj osobno CMC opposition i MCP curl | Opozycję zastąpiono samym zgięciem; przebuduj wieloosiową kontrolkę CMC. |

## Checklisty zamknięcia etapu

### Wejście
- [ ] Topologia, skala, neutralna poza i body skeleton są zatwierdzone i wersjonowane.
- [ ] Dostępne są referencje obu dłoni oraz wszystkich wymaganych chwytów.

### Wynik edytowalny
- [ ] Scena zachowuje kości, osie, limity, kontrolki FK/curl/spread i pełne skin weights.
- [ ] Wszystkie palce i strony można stroić niezależnie; corrective shapes pozostają edytowalne.

### Eksport
- [ ] Nazwy, hierarchia, rest pose, osie i limit wpływów odpowiadają profilowi runtime.
- [ ] Klip testowy osi i zestaw chwytów odtwarzają się tak samo po imporcie.

### Walidacja
- [ ] Wszystkie zakresy pośrednie, opozycja kciuka i komplet chwytów przechodzą dla L/R.
- [ ] Brak penetracji, utraty objętości, skoków kontrolek i skręcania paznokci.

### Błędy blokujące
- [ ] Nie występuje błędny pivot, niespójna oś/roll, ujemna skala ani zerwana hierarchia.
- [ ] Żaden chwyt nie wymaga ukrywania collapse mesha lub przesuwania rekwizytu.

### Definition of Done
- [ ] Edytowalny rig oraz eksport dają zgodne, anatomiczne ruchy obu dłoni; każdy
      palec działa niezależnie, kciuk osiąga opozycję, a cały zestaw chwytów i
      diagnostyczny klip osi przechodzą bez błędów blokujących.

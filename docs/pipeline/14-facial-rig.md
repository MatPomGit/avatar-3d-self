# 14. Rig twarzy

Rig twarzy jest hybrydowym systemem sterowania kośćmi i deformacjami miękkich
tkanek. Warstwa interoperacyjna przyjmuje współczynniki ARKit, a FACS opisuje
obserwowalne działania mięśni. Szczegółowe limity uzupełnia [specyfikacja rigu
twarzy](../rigging/facial-rig-specification.md).

**Input:** zamrożona topologia i vertex order, neutralna twarz, expression
capture, oczy, zęby, język i referencje osoby.
**Edytowalny wynik (editable output):** wersjonowana scena z kośćmi, kontrolkami,
blend shapes, sterownikami, mapowaniem ARKit/FACS i testami.
**Eksport pochodny (derived output):** skeleton, morph targets, tabela mapowania
i klipy walidacyjne.

## Cztery poziomy sterowania

- **Kontrolka wysokopoziomowa** wyraża intencję animatora, np. „uśmiech” albo
  „otwórz usta”. Może sterować wieloma kanałami i nie musi być eksportowana.
- **Kość (bone)** jest transformacją w hierarchii. Dobrze nadaje się do sztywnego
  ruchu żuchwy, oczu, zębów i podstawy języka, lecz sama nie opisuje zmarszczek.
- **Kształt deformacyjny (blend shape)** przechowuje przesunięcia wierzchołków od
  neutralnej siatki o niezmiennym vertex order. Modeluje miękkie tkanki i korekty.
- **Współczynnik ARKit (ARKit coefficient)** jest znormalizowanym sygnałem
  semantycznym, zwykle `0–1`. Nazwa `jawOpen` nie jest ani kością, ani gotową
  geometrią: resolver mapuje ją na kość żuchwy, blend shapes i korekty.

Nie utożsamiaj też ARKit z FACS. Jednostka działania mięśniowego (Action Unit,
AU) służy do opisu/analityki; współczynnik ARKit jest interfejsem urządzenia.
Relacja bywa wiele-do-wielu i wymaga udokumentowanego mapowania.

## Przygotowanie neutralnej twarzy

1. Ustaw głowę w osi, wzrok na wprost i żuchwę w fizjologicznym spoczynku. Usta
   mają stykać się lekko albo zachować naturalną szczelinę osoby, bez zaciskania.
2. Usuń z neutralnej pozy przypadkowe `smile`, brow raise, squint i asymetrię
   capture, ale zachowaj anatomię oraz trwałą asymetrię osoby. Nie kompensuj
   błędnej bazy niezerowymi kanałami.
3. Potwierdź zamknięte oczy tylko przez `eyeBlink=1`, a nie przez neutralną
   geometrię. Ustal, że wszystkie addytywne blend shapes mają w neutralu wagę `0`.
4. Zapisz neutralną siatkę, normals/tangents, pozycję oczu, zgryz, skalę i
   fotografię zatwierdzającą. Powrót wszystkich sterowników do zera musi
   odtworzyć identyczne wierzchołki bez dryfu.

## Żuchwa, zęby i język

Wyznacz pivot żuchwy na osi łączącej lewy i prawy staw skroniowo-żuchwowy, z
referencji bocznej i tomografii/skanu, jeśli są legalnie dostępne. Testuj łuk
siekaczy: samo obracanie jest punktem startowym, a otwarcie może wymagać małej
translacji w dół i do przodu. Zatwierdzone maksimum to zwykle około `25–30°` lub
`30–35 mm` między siekaczami, ale referencja osoby ma pierwszeństwo.

Dolne zęby wiąż sztywno z żuchwą, górne — z czaszką. Nie skinuj ich gradientem do
warg. Język nie jest sztywną częścią żuchwy: jego baza dziedziczy ruch żuchwy,
a środek i czubek zachowują niezależne kontrolki do `/t d n l r k g/`. Sprawdź
jamę ustną przy zamknięciu, maksymalnym otwarciu, protruzji i ruchu bocznym;
zęby, dziąsła i język nie mogą się przecinać.

## Budowa blend shapes i nazwy ARKit

Każdy shape rzeźb z zatwierdzonego neutralu, przy stałym vertex order. Najpierw
wykonaj pojedyncze ruchy w wartościach `0, 0.25, 0.5, 0.75, 1`, następnie strony
i kombinacje. Zachowuj objętość czerwieni warg, policzków i łuku powieki. Kanały
lewy/prawy muszą działać bez kopiowania niezamierzonego wpływu przez płaszczyznę
symetrii.

Wymagany kontrakt zawiera dokładnie 52 kanoniczne identyfikatory ARKit:

| Region | Wymagane nazwy |
| --- | --- |
| Brwi | `browDownLeft`, `browDownRight`, `browInnerUp`, `browOuterUpLeft`, `browOuterUpRight` |
| Policzki i nos | `cheekPuff`, `cheekSquintLeft`, `cheekSquintRight`, `noseSneerLeft`, `noseSneerRight` |
| Oczy | `eyeBlinkLeft`, `eyeBlinkRight`, `eyeLookDownLeft`, `eyeLookDownRight`, `eyeLookInLeft`, `eyeLookInRight`, `eyeLookOutLeft`, `eyeLookOutRight`, `eyeLookUpLeft`, `eyeLookUpRight`, `eyeSquintLeft`, `eyeSquintRight`, `eyeWideLeft`, `eyeWideRight` |
| Żuchwa | `jawForward`, `jawLeft`, `jawOpen`, `jawRight` |
| Usta | `mouthClose`, `mouthDimpleLeft`, `mouthDimpleRight`, `mouthFrownLeft`, `mouthFrownRight`, `mouthFunnel`, `mouthLeft`, `mouthLowerDownLeft`, `mouthLowerDownRight`, `mouthPressLeft`, `mouthPressRight`, `mouthPucker`, `mouthRight`, `mouthRollLower`, `mouthRollUpper`, `mouthShrugLower`, `mouthShrugUpper`, `mouthSmileLeft`, `mouthSmileRight`, `mouthStretchLeft`, `mouthStretchRight`, `mouthUpperUpLeft`, `mouthUpperUpRight` |
| Język | `tongueOut` |

Nie zmieniaj wielkości liter. Jeżeli runtime wymaga innych morph target names,
zachowaj osobną, wersjonowaną tabelę aliasów zamiast przemianować źródło.

## Mapowanie do FACS, strony i korekty

Zapisuj mapowanie jako jawne przybliżenie z wersją, np. `browInnerUp → AU1`,
`browOuterUp → AU2`, `browDown → AU4`, `cheekSquint → AU6`, `eyeBlink → AU45`,
`noseSneer → AU9`, `mouthUpperUp → AU10`, `mouthSmile → AU12`,
`mouthDimple → AU14`, `mouthFrown → AU15`, `mouthLowerDown → AU16`,
`mouthPucker → AU18`, `mouthStretch → AU20`, `mouthPress → AU24`,
`jawOpen → AU26`. Kanały kierunkowe oczu/żuchwy oraz część ruchów warg nie ma
prostego odpowiednika AU; oznacz je jako ruch, nie wymuszaj fałszywego AU.

Kanały `Left` i `Right` uruchamiaj osobno przy `0.25`, `0.5` i `1.0`, obserwując
nieruchomą stronę oraz szew środkowy. Kontrolka obustronna może zasilać oba
kanały, ale nie wolno wypalać ich w jeden shape.

Corrective shape jest dodatkową deformacją naprawiającą wynik kombinacji, a nie
zamiennikiem źle wykonanego shape. Uruchamiaj go ciągłym driverem, np.
`smoothstep(0.15, 0.55, w_A × w_B)`, i testuj wejście/wyjście bez skoku. Minimum:
`jawOpen × mouthSmile`, `jawOpen × mouthPucker`, `jawOpen × mouthFunnel`,
`eyeBlink × eyeLookUp/Down`, `cheekSquint × eyeBlink`, `browDown × eyeSquint`
oraz `mouthSmile × cheekSquint`.

## Macierz testowanych kombinacji

| Zestaw | Wartości | Kryterium |
| --- | --- | --- |
| każdy pojedynczy kanał | `0/.25/.5/.75/1` | ciągłość, objętość, poprawne normals, powrót do neutralu |
| każda para L/R | L=`1`, R=`0`; L=`0`, R=`1`; oba=`.5/1` | niezależność stron i brak szwu |
| `jawOpen` + smile/funnel/pucker/close | `.25/.5/1 × .5/1` | czytelna intencja, brak collapse i penetracji zębów |
| blink + look up/down | blink `.5/1`, look `.5/1` | szczelne powieki, zachowany łuk, brak rogówki na zewnątrz |
| cheekSquint + blink/smile | `.5/1 × .5/1` | objętość policzka i naturalny kącik oka |
| browDown + eyeSquint | `.5/1 × .5/1` | brak załamania glabelli/powieki |
| asymetryczny smile + jaw | jedna strona `.5/1`, jaw `.5/1` | brak przeciągania strony przeciwnej |
| mowa + emocja + blink + gaze | niski/typowy/szczytowy poziom | priorytety nie niszczą zwarć, spojrzenia ani ekspresji |
| wszystkie kanały impulsowo | `0→1→0` po kolei | nazwy i routing bez cross-talku |

## Checklisty zamknięcia etapu

### Wejście
- [ ] Neutral, topologia/vertex order, skala, oczy, zęby, język i referencje są zatwierdzone.
- [ ] Materiały biometryczne pozostają prywatne i mają zgodę na użycie.

### Wynik edytowalny
- [ ] Scena zachowuje kontrolki, kości, 52 shapes, drivery, korekty i mapowanie FACS.
- [ ] Neutral oraz strony są niezależne i odtwarzalne.

### Eksport
- [ ] Skeleton, morph targets, normals i kanoniczne nazwy przechodzą round-trip.
- [ ] Dołączono wersjonowaną tabelę aliasów/mapowania i klipy testowe.

### Walidacja
- [ ] Każdy kanał i cała macierz kombinacji przeszły w wartościach pośrednich.
- [ ] Żuchwa, zęby, język, oczy i powieki zachowują anatomię bez penetracji.

### Błędy blokujące
- [ ] Nie ma dryfu neutralu, zmiany vertex order, brakującego kanału ani cross-talku L/R.
- [ ] Nie występują skoki corrective shapes, collapse objętości lub błędny pivot żuchwy.

### Definition of Done
- [ ] Edytowalny rig i eksport udostępniają 52 zgodne kanały, jawny FACS mapping,
      anatomiczną jamę ustną i wszystkie kombinacje bez błędów blokujących; rig
      nadaje się do face trackingu, animacji emocji i lip-sync.

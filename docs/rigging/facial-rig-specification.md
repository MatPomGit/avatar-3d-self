# Specyfikacja facial rigu

Projekt używa zestawu zgodnego z ARKit jako interoperacyjnej warstwy sterowania oraz FACS jako warstwy interpretacji ruchów mięśniowych. Warstwa runtime może używać corrective shapes, kości lub hybrydy, ale interfejs sterowania musi pozostać stabilny.

## Kanoniczne coefficients

```text
browDownLeft browDownRight browInnerUp browOuterUpLeft browOuterUpRight
cheekPuff cheekSquintLeft cheekSquintRight
eyeBlinkLeft eyeBlinkRight eyeLookDownLeft eyeLookDownRight
eyeLookInLeft eyeLookInRight eyeLookOutLeft eyeLookOutRight
eyeLookUpLeft eyeLookUpRight eyeSquintLeft eyeSquintRight eyeWideLeft eyeWideRight
jawForward jawLeft jawOpen jawRight
mouthClose mouthDimpleLeft mouthDimpleRight mouthFrownLeft mouthFrownRight
mouthFunnel mouthLeft mouthLowerDownLeft mouthLowerDownRight
mouthPressLeft mouthPressRight mouthPucker mouthRight mouthRollLower mouthRollUpper
mouthShrugLower mouthShrugUpper mouthSmileLeft mouthSmileRight
mouthStretchLeft mouthStretchRight mouthUpperUpLeft mouthUpperUpRight
noseSneerLeft noseSneerRight tongueOut
```

## Normalizacja

Wszystkie współczynniki interoperacyjne używają zakresu `0..1`.

Zasady:

- `0` oznacza neutralny shape;
- `1` oznacza zatwierdzone maksimum konkretnego kanału;
- wartości pośrednie nie muszą być liniowe geometrycznie, ale muszą zmieniać ekspresję monotonicznie;
- overshoot powyżej 1 jest zabroniony w standardowym runtime;
- corrective shapes nie są wystawiane jako dodatkowe wejścia użytkownika, jeśli wynikają automatycznie z kombinacji kanałów.

## Neutral pose

Neutralna twarz jest osobnym stanem kalibracyjnym.

Wymagania:

- zamknięte usta bez zaciskania;
- żuchwa w pozycji spoczynkowej;
- oczy otwarte naturalnie, bez `eyeWide`;
- brwi w pozycji referencyjnej;
- brak napięcia policzków;
- brak kompensacyjnego uśmiechu.

Neutral nie może być tworzony przez ręczne wyzerowanie błędnie zbudowanych shape keys. To geometria bazowa musi być neutralna.

## Jaw

Żuchwa jest sterowana anatomicznie przez transform/kość.

Baseline:

- `jawOpen = 1.0` odpowiada około 30-35 mm rozwarcia między siekaczami dla przeciętnej osoby dorosłej;
- maksymalny runtime angle: około 25-30°;
- `jawLeft` i `jawRight`: do około 5-8 mm translacji bocznej;
- `jawForward`: około 4-7 mm.

Wartości geometryczne należy dopasować do referencji i skali konkretnej głowy.

`jawOpen` może sterować miękką tkanką i corrective shapes, ale nie może być wyłącznie morph targetem warg.

## Lip seal

Domknięcie warg jest osobnym zachowaniem od zamknięcia żuchwy.

Dodaj pomocniczy mechanizm `lip_seal`, który:

- utrzymuje kontakt czerwieni warg przy małym `jawOpen`;
- wygasa płynnie wraz z otwieraniem ust;
- nie powoduje zasysania warg do wnętrza;
- współpracuje z `mouthClose`, `mouthPress`, `mouthPucker` i fonemami `/p b m/`.

Baseline wygaszania lip seal: pełna siła do `jawOpen=0.08`, przejście do zera przy `jawOpen≈0.22`.

## Powieki

Blink nie jest prostą interpolacją pojedynczego shape key.

Wymagania:

- górna powieka wykonuje większość ruchu;
- dolna powieka wykonuje mniejszy ruch współtowarzyszący;
- shape zamknięcia musi dopasowywać się do rogówki;
- `eyeBlinkLeft/Right=1` daje pełne zamknięcie bez penetracji;
- `eyeSquint` nie może być tym samym kształtem co częściowy blink.

Baseline udziału ruchu:

- górna powieka: około 85%;
- dolna: około 15%.

## Eyelid follow

Powieki podążają za pionowym ruchem oka.

Baseline:

- spojrzenie w górę: follow 0.30-0.35;
- spojrzenie w dół: follow 0.40-0.45.

Follow jest additive względem blink i squint.

## Oczy

Gaze jest sterowany transformami gałek ocznych. ARKit `eyeLook*` pełni rolę interoperacyjnego wejścia, ale target może mapować je na rotację kości/obiektu.

Maksymalny komfortowy zakres bez ruchu głowy:

- horyzontalnie: około ±25°;
- pionowo: około +20° / -25°.

Przy większym wymaganym kącie system gaze powinien uruchamiać współruch głowy.

## Wargi

Wargi wymagają poprawnego volume preservation.

Minimalne correctives:

- smile + jaw open;
- pucker + jaw open;
- funnel + jaw open;
- mouth close + jaw open;
- lip corner compression;
- upper/lower lip roll;
- asymetryczne smile/frown.

Nie wolno dopuścić do zmniejszenia objętości warg przy pełnym uśmiechu tylko dlatego, że wierzchołki zostały rozciągnięte liniowo.

## Policzki i nos

`cheekSquint` powinien wpływać na dolną powiekę i okolice zewnętrznego kącika oka. `noseSneer` wymaga lokalnego uniesienia skrzydełka nosa i fałdu nosowo-wargowego.

Silny uśmiech powinien automatycznie aktywować corrective nasolabial fold nawet wtedy, gdy warstwa wejściowa nie wystawia osobnego kanału.

## Corrective shapes

Corrective shape jest wymagany, jeśli kombinacja dwóch poprawnych shape keys daje anatomicznie błędny wynik.

Priorytetowe pary:

- jawOpen × mouthSmile;
- jawOpen × mouthPucker;
- jawOpen × mouthFunnel;
- eyeBlink × eyeLookUp/Down;
- cheekSquint × eyeBlink;
- browDown × eyeSquint;
- mouthSmile × cheekSquint.

Corrective może być wyzwalany np. iloczynem wag:

`w_corrective = smoothstep(t0, t1, w_A * w_B)`

Baseline `t0=0.15`, `t1=0.55`, jeśli test kombinacji nie wskazuje innego zakresu.

## FACS

Każdy istotny shape powinien mieć relację do Action Units, jeśli istnieje sensowne mapowanie. Nie wymuszamy relacji 1:1, ponieważ ARKit coefficients i FACS opisują inne poziomy abstrakcji.

Przykładowo:

- `browInnerUp` wspiera AU1;
- `browOuterUp` wspiera AU2;
- `browDown` wiąże się głównie z AU4;
- `cheekSquint` z AU6;
- `mouthSmile` z AU12;
- `mouthFrown` z AU15;
- `mouthPucker` z AU18.

## Język

`tongueOut` jest minimum interoperacyjnym. W rig master zalecane jest dodatkowe sterowanie językiem:

- root;
- mid;
- tip;
- lateral curl opcjonalnie.

Język musi podążać za żuchwą, ale zachowywać własne deformacje dla mowy.

## Zęby

- górne zęby są związane z czaszką;
- dolne zęby z żuchwą;
- zęby nie mogą być deformowane przez skin weights;
- przy pełnym `jawOpen` nie mogą przecinać warg ani języka.

## Jakość shape keys

Każdy kanał powinien przejść test w wagach:

`0.0, 0.25, 0.5, 0.75, 1.0`.

Fail, jeśli występuje:

- nagły skok geometrii;
- utrata objętości;
- załamanie normalnych;
- samoprzecięcie;
- niespójność L/R większa niż zamierzona asymetria.

## Windows

Eksportuj morph targets z niezmienionymi nazwami. Uruchom walidację kompletności przed FBX/runtime importem.

## Linux

Używaj identycznych nazw i walidatora. Różnice platformy nie mogą zmieniać facial interface.

## Definition of Done

Facial rig jest zaliczony, jeśli:

- wszystkie 52 kanały interoperacyjne są obecne;
- jaw jest anatomicznym transformem;
- blink zamyka oko bez penetracji;
- gaze działa niezależnie od head rig;
- lip seal zachowuje kontakt warg;
- correctives usuwają błędy najważniejszych kombinacji;
- FACS mapping jest udokumentowany;
- testy pojedynczych shape keys i kombinacji przechodzą bez artefaktów;
- rig umożliwia późniejsze sterowanie face trackingiem i lip-sync.

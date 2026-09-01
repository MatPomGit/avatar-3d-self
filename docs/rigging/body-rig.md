# Układ sterowania ciałem

Układ sterowania postacią (rig) jest warstwą, która zamienia polecenia animatora lub systemu czasu rzeczywistego na ruch szkieletu. Sam szkielet definiuje hierarchię kości, natomiast rig dodaje kontrolery, ograniczenia, kinematykę odwrotną i prostą oraz mechanizmy korekcyjne.

## Podział na warstwy

Avatar Studio rozdziela:

- szkielet deformujący, który wpływa na geometrię;
- układ sterowania, którego używa animator;
- warstwę pomocniczą, np. kości skrętne, mechanizmy rozpraszania rotacji i automatyczne korekcje.

Takie rozdzielenie ułatwia eksport, diagnostykę i przenoszenie animacji między szkieletami.

## Kinematyka prosta i odwrotna

**Kinematyka prosta (Forward Kinematics, FK)** wyznacza położenie końca łańcucha przez kolejne obroty kości od rodzica do dziecka. Jest naturalna dla łukowych ruchów ramion i gestykulacji.

**Kinematyka odwrotna (Inverse Kinematics, IK)** pozwala ustawić cel kończyny, np. dłoń na stole, a system oblicza orientację barku i łokcia. IK jest szczególnie przydatne przy kontakcie stóp z podłożem i dłoni z obiektem.

Przełączanie IK/FK musi zachowywać położenie kończyny. Skok większy niż około 1-2 mm w przestrzeni świata lub widoczna zmiana rotacji przy przełączeniu jest błędem.

## Obręcz barkowa

Bark jest jednym z najtrudniejszych obszarów deformacji. Ruch ramienia nie zachodzi wyłącznie w stawie ramiennym. Współpracują z nim obojczyk i łopatka.

Dla unoszenia ramienia system powinien stopniowo angażować obojczyk. Jako punkt startowy można przyjąć, że do około 30° ruchu ramienia udział obojczyka jest niewielki, a powyżej 60-90° powinien wyraźnie rosnąć. Przy 150° uniesienia brak ruchu obręczy barkowej niemal zawsze prowadzi do zapadnięcia pachy lub sztucznego wydłużenia barku.

Testuj co najmniej:

| Ruch | Wartości testowe |
| --- | --- |
| zgięcie ramienia | 0°, 45°, 90°, 120°, 150° |
| odwiedzenie ramienia | 0°, 45°, 90°, 120°, 150° |
| rotacja wewnętrzna/zewnętrzna | 0°, ±30°, ±60° |

## Kości skrętne

Kość skrętna (twist bone) rozkłada obrót wzdłuż kończyny na kilka segmentów zamiast kumulować całą rotację przy jednym stawie. Zmniejsza efekt „skręconego rękawa” i zapadania objętości przedramienia lub ramienia.

Dla przedramienia dobrym punktem startowym są 1-2 kości skrętne. Przy pronacji lub supinacji około ±80° pierwsza może przejmować około 50-70% rotacji, a pozostała część może zostać rozłożona na sąsiednie segmenty. Dokładny podział należy dobrać na podstawie deformacji geometrii.

## Kręgosłup

Kręgosłup powinien rozpraszać zgięcie i skręt na kilka segmentów. Nie należy koncentrować całej rotacji tułowia w jednej kości lędźwiowej.

Testuj:

- skłon do przodu i do tyłu;
- skłon boczny;
- skręt tułowia około ±30° i ±45°;
- kombinację skrętu z uniesieniem ramion.

## Miednica i kończyny dolne

Miednica jest głównym węzłem przenoszenia masy. Rig musi pozwalać na niezależną kontrolę miednicy i korzenia postaci.

W biodrze testuj zgięcie do około 120°, odwiedzenie do około 45° oraz rotację wewnętrzną i zewnętrzną. W kolanie testuj 45°, 90° i około 130°. Dla stopy wymagane są funkcje podnoszenia pięty, przetoczenia przez śródstopie i palce.

## Definition of Done

Rig ciała jest zatwierdzony, gdy:

- IK/FK przełącza się bez skoku;
- bark zachowuje objętość przy 90-150° uniesienia;
- przedramię nie tworzy spiralnej deformacji przy ±80° pronacji/supinacji;
- kręgosłup rozprasza zgięcie i skręt;
- miednica nie powoduje zapadania pachwin podczas przysiadu;
- wszystkie obowiązkowe pozy przechodzą walidację deformacji.
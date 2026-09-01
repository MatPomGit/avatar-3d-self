# Kanoniczna specyfikacja skeletonu

Nazwy, hierarchy, rest pose i lokalne osie są kontraktem między Blenderem, exporterem, Avatar Studio i target engine. Zmiana skeletonu po rozpoczęciu skinningu wymaga ponownej walidacji wag, retargetingu i animacji.

## Rest pose

Kanoniczną pozycją projektu jest A-pose.

Baseline:

- odwiedzenie ramion: 35-45° od tułowia;
- łokcie prawie wyprostowane, bez przeprostu;
- dłonie w neutralnej pronacji/supinacji, kciuki skierowane lekko do przodu;
- stopy równolegle lub z naturalnym outward angle do 5°;
- głowa w neutralnym ustawieniu względem C-spine.

T-pose jest dopuszczalna wyłącznie jako profil kompatybilności z narzędziem docelowym.

## Rdzeń

```text
root
└── pelvis
    ├── spine_01
    │   └── spine_02
    │       └── spine_03
    │           └── neck_01
    │               └── head
    ├── thigh_l → calf_l → foot_l → ball_l
    └── thigh_r → calf_r → foot_r → ball_r
```

Ramiona od `spine_03`:

```text
clavicle_l → upperarm_l → lowerarm_l → hand_l
clavicle_r → upperarm_r → lowerarm_r → hand_r
```

## Dłonie

Dla każdej strony:

```text
thumb_01 → thumb_02 → thumb_03
index_01 → index_02 → index_03
middle_01 → middle_02 → middle_03
ring_01 → ring_02 → ring_03
pinky_01 → pinky_02 → pinky_03
```

Metacarpals są zalecane dla index/middle/ring/pinky, jeśli target rig obsługuje spread i cupping. Dla kciuka kość bazowa musi odwzorowywać rzeczywisty kierunek CMC, a nie być ustawiona jak kolejny palec.

## Twist bones

Dla profilu fotorealistycznego twist bones są zalecane domyślnie:

- `upperarm_twist_01_l/r`;
- `lowerarm_twist_01_l/r`;
- `thigh_twist_01_l/r`;
- opcjonalnie `calf_twist_01_l/r`.

Jeżeli długość kończyny i topology uzasadniają podział twistu, można zastosować dwa segmenty. Baseline dystrybucji rotacji przedramienia:

- około 65% rotacji na twist chain;
- około 35% w pobliżu kości głównej/łokcia.

Dokładny rozkład stroi się testami deformacji, nie poprzez sztywny podział matematyczny.

## IK/FK

Ramiona i nogi mają oba tryby.

Baseline:

- IK/FK blend ciągły 0-1;
- zachowanie world-space dla kontrolerów IK;
- pole vector stabilny i zapisany w rest pose;
- foot roll jako kontroler pomocniczy, nie deform bone;
- stretch wyłączony domyślnie dla realistycznego człowieka.

## Osie lokalne

W projekcie obowiązuje jedna konwencja osi dla lewej i prawej strony. Lustrzane kończyny mogą mieć przeciwny znak osi pomocniczej, ale primary axis kości musi wskazywać od parent do child.

Walidator powinien wykrywać:

- ujemne skale na deform bones;
- niespójne roll angles;
- zerowe długości kości;
- różne nazwy L/R;
- parentowanie kontrolerów do deform chain w sposób tworzący cykl.

## Umiejscowienie stawów

Pozycja kości wynika z anatomii osoby referencyjnej.

Minimalne zasady:

- hip joint w centrum rotacji głowy kości udowej;
- knee joint w osi kłykci;
- ankle w osi stawu skokowego;
- shoulder joint wewnątrz głowy kości ramiennej, nie na powierzchni barku;
- elbow w osi bloczka/kapitulum;
- wrist w osi między kośćmi przedramienia a śródręczem.

## Zakresy kontrolne

To nie są twarde limity runtime, lecz zakresy testowe skinningu:

| Staw | Test |
| --- | --- |
| shoulder flexion | 0-160° |
| shoulder abduction | 0-150° |
| elbow flexion | 0-145° |
| forearm pronation/supination | około ±80° |
| wrist flexion/extension | około ±70° / ±60° |
| hip flexion | 0-120° |
| knee flexion | 0-135° |
| ankle dorsiflexion/plantarflexion | około 20° / 45° |

## Spine

Trzy kości `spine_01..03` są minimum. Kontrolery mogą stosować spline IK lub rozdzielone FK.

Baseline rozkładu dużego pochylenia tułowia:

- lumbar (`spine_01`): 35%;
- mid spine (`spine_02`): 35%;
- upper thoracic (`spine_03`): 30%.

Nie należy kumulować całej rotacji w jednym segmencie.

## Neck i head

`neck_01` jest minimum deformacyjnym. Dla LOD0 można dodać `neck_02`, jeżeli poprawia deformację szyi.

Head controller ma działać niezależnie od gaze controllerów oczu.

## Male/female morphology

Kanoniczny skeleton pozostaje wspólny dla płci. Różnice anatomiczne są odwzorowywane pozycją stawów, proporcjami i skinningiem, nie osobnymi nazwami kości.

Dodatkowe kości dla piersi w modelu kobiecym należą do secondary-motion layer i nie zmieniają głównego kontraktu skeletonu.

## Deform bones i control rig

Deform skeleton musi być możliwy do eksportu bez control objects.

Do eksportu trafiają tylko:

- root;
- deform bones;
- wymagane twist/secondary bones;
- ewentualne runtime facial bones.

Nie eksportujemy widgetów, constraints helperów ani technicznych kości kontrolnych, jeśli target ich nie potrzebuje.

## Windows

W Blenderze zapisuj skeleton w kanonicznej scenie `.blend`. Eksportuj profil FBX dopiero po przejściu testu hierarchy, axes i rest pose.

## Linux

Stosuj tę samą scenę i nazwy. Blender CLI może automatycznie walidować hierarchy i transforms, ale nie zmienia specyfikacji.

## Definition of Done

Skeleton jest zaliczony, jeśli:

- hierarchy odpowiada specyfikacji;
- nazwy L/R są kompletne;
- rest pose jest zapisana i wersjonowana;
- skala postaci jest 1:1;
- nie ma negative scale na deform bones;
- twist test nie powoduje candy-wrapper deformation;
- IK/FK przełącza się bez skoku większego niż 2 mm w punktach końcowych;
- wszystkie testowe zakresy ruchu można wykonać bez błędu skeletonu.
